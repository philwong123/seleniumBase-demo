#!/usr/bin/env python3

"""
# Filename:    guard-init.py
# Version:     1.8
# Date:        2019/09/05
# Author:      Kan FENG
# Email:       fengkan@sensetime.com
# Description: 1. Initialize user test data;
#              2. Initialize camera (ONVIF, RTSP, DLC) test data;
#              3. Initialize keeper (SenseKeeper, SensePass, SenseID) test data;
#              4. Initialize library test data;
#              5. Support differet versions of databases;
#
# Notes:       Make sure you have modified configurations and set with correct values.
#              python guard-init.py --host=10.5.6.68 -user -camera -keeper -lib
"""

import contextlib
import datetime
import json
import math
import os
import pymysql
import re
import requests
import warnings
import argparse


requests.packages.urllib3.disable_warnings()

with open('./guard/config/init_config.json', encoding='utf-8') as file:
    config = json.load(file)

    FRONTEND_HOST = config['default']['frontend']['host']
    FRONTEND_USERNAME = config['default']['frontend']['username']
    FRONTEND_PASSWORD = config['default']['frontend']['password']

    DATABASE_HOST = config['default']['database']['host']
    DATABASE_PORT = config['default']['database']['port']
    DATABASE_USER = config['default']['database']['user']
    DATABASE_PASSWORD = config['default']['database']['password']
    DATABASE_DATABASE = config['default']['database']['database']

    MAP_PATH = config['default']['map']['path']

    # senseguard-oauth2
    API_LOGIN_PATH = config['api']['senseguard-oauth2']['login']['path']
    API_LOGIN_PAYLOAD = config['api']['senseguard-oauth2']['login']['payload']
    # senseguard-device-management
    API_ADD_DEVICE_GROUP = config['api']['senseguard-device-management']['addDeviceGroup']['path']
    API_ADD_DEVICE_GROUP_PAYLOAD = config['api']['senseguard-device-management']['addDeviceGroup']['payload']
    API_ADD_DEVICE = config['api']['senseguard-device-management']['addDevice']['path']
    API_ADD_DEVICE_PAYLOAD = config['api']['senseguard-device-management']['addDevice']['payload']
    # senseguard-map-management
    API_ADD_MAP_LEVEL = config['api']['senseguard-map-management']['addMapLevel']['path']
    API_ADD_MAP_LEVEL_PAYLOAD = config['api']['senseguard-map-management']['addMapLevel']['payload']
    API_UPLOAD_MAP = config['api']['senseguard-map-management']['uploadMap']['path']
    API_UPLOAD_MAP_PAYLOAD = config['api']['senseguard-map-management']['uploadMap']['payload']
    # senseguard-watchlist-management
    API_ADD_LIBRARY = config['api']['senseguard-watchlist-management']['addLibrary']['path']
    API_ADD_LIBRARY_PAYLOAD = config['api']['senseguard-watchlist-management']['addLibrary']['payload']
    # senseguard-uums
    API_ADD_ORG = config['api']['senseguard-uums']['addOrg']['path']
    API_ADD_ORG_PAYLOAD = config['api']['senseguard-uums']['addOrg']['payload']
    API_ADD_USER = config['api']['senseguard-uums']['addUser']['path']
    API_ADD_USER_PAYLOAD = config['api']['senseguard-uums']['addUser']['payload']
    # senseguard-bulk-tool
    API_ADD_TOTAL_FILE_NAME = config['api']['senseguard-bulk-tool']['addTotalFileName']['path']
    API_ADD_TOTAL_FILE_NAME_PAYLOAD = config['api']['senseguard-bulk-tool']['addTotalFileName']['payload']
    API_BATCH_ADD_TARGET = config['api']['senseguard-bulk-tool']['batchAddTarget']['path']
    API_BATCH_ADD_TARGET_PAYLOAD = config['api']['senseguard-bulk-tool']['addTotalFileName']['payload']

    LIBRARIES = config['libraries']
    USERS = config['users']
    KEEPERS = config['keepers']
    CAMERAS = config['cameras']


def getIpAddress(str):
    return re.findall(r'[0-9]+(?:\.[0-9]+){3}', str)


def login(username=FRONTEND_USERNAME, password=FRONTEND_PASSWORD):
    API_LOGIN_PAYLOAD['username'] = username
    API_LOGIN_PAYLOAD['password'] = password
    LOGIN_URL = "http://%s%s" % (FRONTEND_HOST,
                                 API_LOGIN_PATH)
    response = requests.post(LOGIN_URL, json=API_LOGIN_PAYLOAD, verify=False)
    return response.json().get('accessToken')


@contextlib.contextmanager
def connect_to_database():
    conn = pymysql.connect(host=DATABASE_HOST, port=DATABASE_PORT, user=DATABASE_USER,
                           password=DATABASE_PASSWORD, db=DATABASE_DATABASE)
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    try:
        yield cursor
    finally:
        conn.commit()
        cursor.close()
        conn.close()


def query_by_sql(sql):
    with connect_to_database() as cursor:
        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            cursor.execute(sql)
            data = cursor.fetchall()
    return data


def get_floor_id(floor_name):
    raw_sql = "SELECT floor_id FROM senseguard.info_floor WHERE name='{floor_name}';"
    sql = raw_sql.format(floor_name=pymysql.escape_string(floor_name))
    data = query_by_sql(sql)
    if len(data) == 1:
        return data[0]['floor_id']
    else:
        return None


def send_add_floor_request(floor_name, parent_id=''):
    # accessToken = login()
    headers = {
        "accessToken": accessToken
    }
    API_ADD_MAP_LEVEL_PAYLOAD['name'] = floor_name
    API_ADD_MAP_LEVEL_PAYLOAD['parentId'] = parent_id
    ADD_MAP_LEVEL_URL = "http://%s%s" % (FRONTEND_HOST, API_ADD_MAP_LEVEL)
    response = requests.post(
        ADD_MAP_LEVEL_URL, headers=headers, json=API_ADD_MAP_LEVEL_PAYLOAD, verify=False)
    return response.json().get('floorId')


def add_floor(parent_floor_name, floor_name):
    parent_id = get_floor_id(parent_floor_name)
    if parent_id is None:
        parent_id = send_add_floor_request(parent_floor_name)

    floor_id = get_floor_id(floor_name)
    if floor_id is None:
        floor_id = send_add_floor_request(floor_name, parent_id)

    return floor_id


def get_upload_image_url(floor_name):
    raw_sql = "SELECT url FROM senseguard.info_floor WHERE name='{floor_name}';"
    sql = raw_sql.format(floor_name=pymysql.escape_string(floor_name))
    data = query_by_sql(sql)
    if len(data) == 1:
        if (data[0]['url'] is None or data[0]['url'] == ''):
            return None
        else:
            return data[0]['url']
    else:
        return None


def send_upload_map_request(floor_id, image_file):
    # accessToken = login()
    headers = {
        "accessToken": accessToken
    }
    API_UPLOAD_MAP_PAYLOAD['file'] = (
        image_file, open("%s%s" % (MAP_PATH, image_file), 'rb'))
    UPLOAD_MAP_URL = "http://%s%s" % (FRONTEND_HOST, API_UPLOAD_MAP)
    requests.post(UPLOAD_MAP_URL.replace('{id}', str(
        floor_id)), headers=headers, files=API_UPLOAD_MAP_PAYLOAD, verify=False)


def get_device_group(device_group_name):
    raw_sql = "SELECT group_id FROM senseguard.info_device_group WHERE name='{device_group_name}';"
    sql = raw_sql.format(
        device_group_name=pymysql.escape_string(device_group_name))
    data = query_by_sql(sql)
    if len(data) == 1:
        return data[0]['group_id']
    else:
        return None


def send_add_device_group_request(device_group_name, parent_id=0):
    # accessToken = login()
    headers = {
        "accessToken": accessToken
    }
    API_ADD_DEVICE_GROUP_PAYLOAD['name'] = device_group_name
    API_ADD_DEVICE_GROUP_PAYLOAD['parentId'] = parent_id
    ADD_DEVICE_GROUP_URL = "http://%s%s" % (
        FRONTEND_HOST, API_ADD_DEVICE_GROUP)
    response = requests.post(
        ADD_DEVICE_GROUP_URL, headers=headers, json=API_ADD_DEVICE_GROUP_PAYLOAD, verify=False)
    return response.json().get('groupId')


def add_device_group(parent_device_group_name, device_group_name):
    parent_id = get_device_group(parent_device_group_name)
    if parent_id is None:
        parent_id = send_add_device_group_request(parent_device_group_name)

    device_group_id = get_device_group(device_group_name)
    if device_group_id is None:
        device_group_id = send_add_device_group_request(
            device_group_name, parent_id)

    return device_group_id


def send_add_rtsp_device_request(device_name,  group_id, floor_id, point, rtsp_address):
    # accessToken = login()
    headers = {
        "accessToken": accessToken
    }
    API_ADD_DEVICE_PAYLOAD['deviceType'] = 1
    API_ADD_DEVICE_PAYLOAD['name'] = device_name
    API_ADD_DEVICE_PAYLOAD['groupId'] = group_id
    API_ADD_DEVICE_PAYLOAD['floorId'] = floor_id
    API_ADD_DEVICE_PAYLOAD['ID'] = rtsp_address
    # API_ADD_DEVICE_PAYLOAD['ID'] = getIpAddress(rtsp_address)[0]
    API_ADD_DEVICE_PAYLOAD['point'] = point
    API_ADD_DEVICE_PAYLOAD['rtspAddress'] = rtsp_address
    API_ADD_DEVICE_PAYLOAD['streamType'] = "RTSP"
    API_ADD_DEVICE_PAYLOAD['codeType'] = 1
    API_ADD_DEVICE_PAYLOAD['protocolType'] = "TCP"
    ADD_DEVICE_URL = "http://%s%s" % (FRONTEND_HOST, API_ADD_DEVICE)
    response = requests.post(
        ADD_DEVICE_URL, headers=headers, json=API_ADD_DEVICE_PAYLOAD, verify=False)
    return response.json().get('deviceId')


def send_add_onvif_device_request(
        device_name,  group_id, floor_id, ip, port, onvif_username, onvif_password, point):
    # accessToken = login()
    headers = {
        "accessToken": accessToken
    }
    API_ADD_DEVICE_PAYLOAD['deviceType'] = 1
    API_ADD_DEVICE_PAYLOAD['name'] = device_name
    API_ADD_DEVICE_PAYLOAD['groupId'] = group_id
    API_ADD_DEVICE_PAYLOAD['floorId'] = floor_id
    API_ADD_DEVICE_PAYLOAD['ID'] = ip
    API_ADD_DEVICE_PAYLOAD['ip'] = ip
    API_ADD_DEVICE_PAYLOAD['port'] = port
    API_ADD_DEVICE_PAYLOAD['username'] = onvif_username
    API_ADD_DEVICE_PAYLOAD['password'] = onvif_password
    API_ADD_DEVICE_PAYLOAD['point'] = point
    API_ADD_DEVICE_PAYLOAD['streamType'] = "ONVIF"
    ADD_DEVICE_URL = "http://%s%s" % (FRONTEND_HOST, API_ADD_DEVICE)
    response = requests.post(
        ADD_DEVICE_URL, headers=headers, json=API_ADD_DEVICE_PAYLOAD, verify=False)
    return response.json().get('deviceId')


def send_add_dlc_device_request(
        device_name,  group_id, floor_id, ip, port, dlc_username, dlc_password, point):
    # accessToken = login()
    headers = {
        "accessToken": accessToken
    }
    API_ADD_DEVICE_PAYLOAD['deviceType'] = 4
    if 'VA-ESCC-AA' in device_name:
        API_ADD_DEVICE_PAYLOAD['firmId'] = 1
    else:
        API_ADD_DEVICE_PAYLOAD['firmId'] = 5
    API_ADD_DEVICE_PAYLOAD['name'] = device_name
    API_ADD_DEVICE_PAYLOAD['groupId'] = group_id
    API_ADD_DEVICE_PAYLOAD['floorId'] = floor_id
    API_ADD_DEVICE_PAYLOAD['ID'] = ip
    API_ADD_DEVICE_PAYLOAD['ip'] = ip
    API_ADD_DEVICE_PAYLOAD['port'] = port
    API_ADD_DEVICE_PAYLOAD['username'] = dlc_username
    API_ADD_DEVICE_PAYLOAD['password'] = dlc_password
    API_ADD_DEVICE_PAYLOAD['point'] = point
    ADD_DEVICE_URL = "http://%s%s" % (FRONTEND_HOST, API_ADD_DEVICE)
    response = requests.post(
        ADD_DEVICE_URL, headers=headers, json=API_ADD_DEVICE_PAYLOAD, verify=False)
    return response.json().get('deviceId')


def add_rtsp_device(parent_device_group_name, device_group_name, device_name, floor_id, point, rtsp_address):
    device_group_id = get_device_group(device_group_name)
    if device_group_id is None:
        device_group_id = add_device_group(
            parent_device_group_name, device_group_name)

    send_add_rtsp_device_request(
        device_name,  device_group_id, floor_id, point, rtsp_address)


def add_onvif_device(parent_device_group_name, device_group_name, device_name, floor_id, ip, port, username, password, point):
    device_group_id = get_device_group(device_group_name)
    if device_group_id is None:
        device_group_id = add_device_group(
            parent_device_group_name, device_group_name)

    send_add_onvif_device_request(
        device_name,  device_group_id, floor_id, ip, port, username, password, point)


def add_dlc_device(parent_device_group_name, device_group_name, device_name, floor_id, ip, port, username, password, point):
    device_group_id = get_device_group(device_group_name)
    if device_group_id is None:
        device_group_id = add_device_group(
            parent_device_group_name, device_group_name)

    send_add_dlc_device_request(
        device_name,  device_group_id, floor_id, ip, port, username, password, point)


def send_add_keeper_device_request(device_name, group_id, floor_id, point=[0.0, 0.0]):
    # accessToken = login()
    headers = {
        "accessToken": accessToken
    }
    API_ADD_DEVICE_PAYLOAD['deviceType'] = 2
    API_ADD_DEVICE_PAYLOAD['name'] = device_name
    API_ADD_DEVICE_PAYLOAD['groupId'] = group_id
    API_ADD_DEVICE_PAYLOAD['floorId'] = floor_id
    API_ADD_DEVICE_PAYLOAD['ID'] = device_name
    API_ADD_DEVICE_PAYLOAD['point'] = point
    ADD_DEVICE_URL = "http://%s%s" % (FRONTEND_HOST, API_ADD_DEVICE)
    response = requests.post(
        ADD_DEVICE_URL, headers=headers, json=API_ADD_DEVICE_PAYLOAD, verify=False)
    return response.json().get('deviceId')


def send_add_senseid_device_request(device_name, group_id, floor_id, point=[0.0, 0.0]):
    # accessToken = login()
    headers = {
        "accessToken": accessToken
    }
    API_ADD_DEVICE_PAYLOAD['deviceType'] = 5
    API_ADD_DEVICE_PAYLOAD['name'] = device_name
    API_ADD_DEVICE_PAYLOAD['groupId'] = group_id
    API_ADD_DEVICE_PAYLOAD['floorId'] = floor_id
    API_ADD_DEVICE_PAYLOAD['ID'] = device_name
    API_ADD_DEVICE_PAYLOAD['point'] = point
    ADD_DEVICE_URL = "http://%s%s" % (FRONTEND_HOST, API_ADD_DEVICE)
    response = requests.post(
        ADD_DEVICE_URL, headers=headers, json=API_ADD_DEVICE_PAYLOAD, verify=False)
    return response.json().get('deviceId')


def add_keeper_device(parent_device_group_name, device_group_name, device_name, floor_id, point):
    device_group_id = get_device_group(device_group_name)
    if device_group_id is None:
        device_group_id = add_device_group(
            parent_device_group_name, device_group_name)

    send_add_keeper_device_request(
        device_name,  device_group_id, floor_id, point)


def add_senseid_device(parent_device_group_name, device_group_name, device_name, floor_id, point):
    device_group_id = get_device_group(device_group_name)
    if device_group_id is None:
        device_group_id = add_device_group(
            parent_device_group_name, device_group_name)

    send_add_senseid_device_request(
        device_name,  device_group_id, floor_id, point)


def init_cameras():
    for camera in CAMERAS:
        floor_id = add_floor(camera['parent_floor'], camera['floor_name'])
        if get_upload_image_url(camera['floor_name']) is None:
            send_upload_map_request(floor_id, camera['floor_name']+'.jpg')
        if camera['type'] == 'onvif':
            add_onvif_device(camera['parent_floor'], camera['floor_name'], camera['device_name'], floor_id,
                             camera['ip'], camera['port'], camera['username'], camera['password'], camera['point'])
        if camera['type'] == 'dlc':
            add_dlc_device(camera['parent_floor'], camera['floor_name'], camera['device_name'], floor_id,
                           camera['ip'], camera['port'], camera['username'], camera['password'], camera['point'])
        if camera['type'] == 'rtsp':
            add_rtsp_device(camera['parent_floor'], camera['floor_name'], camera['device_name'],
                            floor_id, camera['point'], camera['rtsp_address'])
        print('%s has been added.' % camera['device_name'])


def init_keepers():
    for keeper in KEEPERS:
        floor_id = add_floor(keeper['parent_floor'], keeper['floor_name'])
        if get_upload_image_url(keeper['floor_name']) is None:
            send_upload_map_request(floor_id, keeper['floor_name']+'.jpg')
        if keeper['type'] == 'SenseID':
            add_senseid_device(keeper['parent_floor'], keeper['floor_name'], keeper['device_name'],
                               floor_id, keeper['point'])
            print('%s has been added.' % keeper['device_name'])
        else:
            if 'number' in keeper.keys():
                for i in range(1, keeper['number']+1):
                    add_keeper_device(keeper['parent_floor'], keeper['floor_name'], keeper['device_name']+str(i),
                                      floor_id, keeper['point'])
                    print('%s has been added.' %
                          (keeper['device_name']+str(i)))
            else:
                add_keeper_device(keeper['parent_floor'], keeper['floor_name'], keeper['device_name'],
                                  floor_id, keeper['point'])
                print('%s has been added.' % keeper['device_name'])


def get_library_id(library_name):
    raw_sql = "SELECT library_id FROM senseguard.info_library WHERE name='{library_name}';"
    sql = raw_sql.format(library_name=pymysql.escape_string(library_name))
    data = query_by_sql(sql)
    if len(data) == 1:
        return data[0]['library_id']
    else:
        return None


def send_add_library_request(library_name, library_type=1):
    # accessToken = login()
    headers = {
        "accessToken": accessToken
    }
    API_ADD_LIBRARY_PAYLOAD['name'] = library_name
    API_ADD_LIBRARY_PAYLOAD['type'] = library_type
    ADD_LIBRARY_URL = "http://%s%s" % (FRONTEND_HOST, API_ADD_LIBRARY)
    response = requests.post(
        ADD_LIBRARY_URL, headers=headers, json=API_ADD_LIBRARY_PAYLOAD, verify=False)

    return response.json().get('libraryId')


def add_library(library_name, library_type):
    library_id = get_library_id(library_name)
    if library_id is None:
        library_id = send_add_library_request(library_name, library_type)

    return library_id


def send_add_total_file_name_request(library_id, library_type, folder_url, file_name):
    # accessToken = login()
    headers = {
        "accessToken": accessToken
    }
    API_ADD_TOTAL_FILE_NAME_PAYLOAD['libraryId'] = library_id
    API_ADD_TOTAL_FILE_NAME_PAYLOAD['libraryType'] = library_type
    API_ADD_TOTAL_FILE_NAME_PAYLOAD['folderUrl'] = folder_url
    API_ADD_TOTAL_FILE_NAME_PAYLOAD['fileName'] = file_name
    ADD_TOTAL_FILE_NAME_URL = "http://%s%s" % (
        FRONTEND_HOST, API_ADD_TOTAL_FILE_NAME)
    response = requests.post(
        ADD_TOTAL_FILE_NAME_URL, headers=headers, json=API_ADD_TOTAL_FILE_NAME_PAYLOAD, verify=False)
    return response.json().get('taskId')


def send_add_target_bulk_tool(task_id, library_name, library_id, library_type, current_request_num, request_total_num, file_total_num, folder_url, imgs):
    headers = {
        "accessToken": accessToken
    }
    API_BATCH_ADD_TARGET_PAYLOAD['taskId'] = task_id
    API_BATCH_ADD_TARGET_PAYLOAD['groupName'] = library_name
    API_BATCH_ADD_TARGET_PAYLOAD['libraryId'] = library_id
    API_BATCH_ADD_TARGET_PAYLOAD['libraryType'] = library_type
    API_BATCH_ADD_TARGET_PAYLOAD['currentRequestNum'] = current_request_num
    API_BATCH_ADD_TARGET_PAYLOAD['requestTotalNum'] = request_total_num
    API_BATCH_ADD_TARGET_PAYLOAD['fileTotalNumber'] = file_total_num
    files = []
    for img in imgs:
        file_payload = ("img", open("%s%s" % (folder_url, img), "rb"))
        files.append(file_payload)
    BATCH_ADD_TARGET_URL = "http://%s%s" % (
        FRONTEND_HOST, API_BATCH_ADD_TARGET)
    response = requests.post(
        BATCH_ADD_TARGET_URL, headers=headers, files=files, data=API_BATCH_ADD_TARGET_PAYLOAD, verify=False)
    # print(API_BATCH_ADD_TARGET_PAYLOAD)
    # print(response.json())


def get_file_names(file_path):
    for _, _, files in os.walk(file_path):
        return files


def batch_add_facial_images(library_id, library_type, library_name, folder_url, library_start_index=0, library_size=2000):
    file_names = get_file_names(folder_url)
    if file_names is not None:
        if len(file_names) - library_start_index - library_size < 0:
            library_size = len(file_names) - library_start_index
        imgs = file_names[library_start_index:library_start_index+library_size]
        task_id = send_add_total_file_name_request(
            library_id, library_type, folder_url, imgs)
        batch_size = 10
        request_total_num = math.ceil(library_size/batch_size)
        for i in range(request_total_num):
            current_request_num = i+1
            if i == request_total_num-1:
                batch_imgs = imgs[library_start_index +
                                  i*batch_size:]
                send_add_target_bulk_tool(task_id, library_name, library_id, library_type,
                                          current_request_num, request_total_num, library_size, folder_url, batch_imgs)
                break
            batch_imgs = imgs[library_start_index +
                              i*batch_size:library_start_index+i*batch_size+batch_size]
            send_add_target_bulk_tool(task_id, library_name, library_id, library_type,
                                      current_request_num, request_total_num, library_size, folder_url, batch_imgs)


def init_libraries():
    for library in LIBRARIES:
        if 'number' in library.keys():
            for i in range(1, library['number']+1):
                library_id = add_library(
                    library['name'] + str(i), library['type'])
                starttime = datetime.datetime.now()
                # print(library_id, library['type'], library['name'] + str(
                #     i), library['img_path'], (i-1)*library['size'], int(library['size']))
                if int(library['size']) > 0:
                    batch_add_facial_images(
                        library_id, library['type'], library['name'] + str(i), library['img_path'], (i-1)*library['size'], int(library['size']))
                endtime = datetime.datetime.now()
                print('%s has been added with %s seconds' %
                      (library['name'] + str(i), (endtime - starttime).seconds))
        else:
            library_id = add_library(library['name'], library['type'])
            batch_add_facial_images(
                library_id, library['type'], library['name'], library['img_path'])
            print('%s has been added.' % (library['name']))


def is_uums_exists():
    raw_sql = "SELECT * FROM information_schema.schemata WHERE schema_name='uums';"
    data = query_by_sql(raw_sql)
    return (len(data) == 1)


def is_info_user_in_senseguard():
    raw_sql = "SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA='senseguard' AND TABLE_NAME='info_user';"
    data = query_by_sql(raw_sql)
    return (len(data) == 1)


def get_org_id(org_name):
    if is_info_user_in_senseguard():
        raw_sql = "SELECT org_id FROM info_organization WHERE name='{org_name}';"
    else:
        raw_sql = "SELECT org_id FROM uums.info_organization WHERE name='{org_name}';"
    sql = raw_sql.format(
        org_name=pymysql.escape_string(org_name))
    data = query_by_sql(sql)
    if len(data) == 1:
        return data[0]['org_id']
    else:
        return None


def send_add_org_request(org_name, parent_id=0):
    # accessToken = login()
    headers = {
        "accessToken": accessToken
    }
    API_ADD_ORG_PAYLOAD['name'] = org_name
    API_ADD_ORG_PAYLOAD['parentId'] = parent_id
    ADD_ORG_URL = "http://%s%s" % (FRONTEND_HOST, API_ADD_ORG)
    response = requests.post(
        ADD_ORG_URL, headers=headers, json=API_ADD_ORG_PAYLOAD, verify=False)
    return response.json().get('orgId')


def add_org(org_name):
    org_id = get_org_id(org_name)
    if org_id is None:
        org_id = send_add_org_request(org_name)

    return org_id


def send_add_user_request(username, realname, org_id=1):
    # accessToken = login()
    headers = {
        "accessToken": accessToken
    }
    API_ADD_USER_PAYLOAD['username'] = username
    API_ADD_USER_PAYLOAD['realname'] = realname
    API_ADD_USER_PAYLOAD['orgId'] = org_id
    ADD_USER_URL = "http://%s%s" % (FRONTEND_HOST, API_ADD_USER)
    response = requests.post(
        ADD_USER_URL, headers=headers, json=API_ADD_USER_PAYLOAD, verify=False)
    return response.json().get('userId')


def init_users():
    for user in USERS:
        org_id = add_org(user['org_name'])
        if 'number' in user.keys():
            for i in range(1, user['number']+1):
                send_add_user_request(
                    user['username']+str(i), user['realname']+str(i), org_id)
                print('%s has been added.' % (user['username']+str(i)))
        else:
            send_add_user_request(user['username'], user['realname'], org_id)
            print('%s has been added.' % user['realname'])


@contextlib.contextmanager
def connect_to_mysql():
    conn = pymysql.connect(host=DATABASE_HOST, port=DATABASE_PORT, user=DATABASE_USER,
                           password=DATABASE_PASSWORD, db=DATABASE_DATABASE)
    cursor = conn.cursor()
    try:
        yield cursor
    finally:
        conn.commit()
        cursor.close()
        conn.close()


def init_uums():
    with connect_to_mysql() as cursor:
        with warnings.catch_warnings():
            if is_info_user_in_senseguard():
                sql = "UPDATE senseguard.info_user SET first_login=1;"
            else:
                sql = "UPDATE uums.info_user SET first_login=1;"
            print(sql)
            cursor.execute(sql)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Senseguard Tool is a tool to initialize test data on the server.')
    parser.add_argument('--host', action='store', dest='host')
    parser.add_argument('-user', action='store_true',
                        default=False, dest='user_switch')
    parser.add_argument('-camera', action='store_true',
                        default=False, dest='camera_switch')
    parser.add_argument('-keeper', action='store_true',
                        default=False, dest='keeper_switch')
    parser.add_argument('-lib', action='store_true',
                        default=False, dest='library_switch')
    args = parser.parse_args()

    if args.host:
        FRONTEND_HOST = args.host
        DATABASE_HOST = args.host

    accessToken = login()

    if accessToken:
        print('Initialize test data start...')
        if args.user_switch:
            init_users()
            init_uums()
        if args.camera_switch:
            init_cameras()
        if args.keeper_switch:
            init_keepers()
        if args.library_switch:
            init_libraries()
        print('Environment is ready.')
    else:
        print('Please check username and password in the file, config.json.')

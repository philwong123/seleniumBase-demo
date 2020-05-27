#!/usr/bin/env python3

"""
# Filename:    guard-cleaner.py
# Version:     1.0.0
# Date:        2019/11/05
# Author:      Kan FENG
# Email:       fengkan@sensetime.com
# Description: 1. Clean all Access Control tasks, Tailing Detection tasks, Video Process tasks and Image Ingress tasks; 
#              2. Delete all static feature databases;
#              3. Create all buckets if it did not exists;
#              4. Initialize all SenseGuard databases;
#              5. Support specific path of SQL files;
#
# Notes:       Make sure you have modified configurations and set with correct values.
#              python guard-cleaner.py --host=10.5.6.68 -ac -td -vps -iis -fdb --path=/data/Gitlab/design -db
# 
"""


import json
import requests
import datetime
import argparse
import os
import time
import sys

sys.path.append(os.path.abspath('./utils'))
from config import Config
from database import Database
from ssh import SSH

nebula_config = Config(os.path.abspath('./guard/config/nebula_config.yml')).config

# web configurations
HTTP_HOST = nebula_config.get("http").get("host")
HTTP_PORT = nebula_config.get("http").get("port")
HTTP_END_POINT = "http://%s:%s" % (HTTP_HOST, HTTP_PORT)
HTTP_RESOURCE_AC_MANAGER_TASK_LIST = nebula_config.get("http").get(
    "resource").get("AccessControlMasterService").get("acManagerTaskList")
HTTP_RESOURCE_AC_MANAGER_TASK_DELETE = nebula_config.get("http").get(
    "resource").get("AccessControlMasterService").get("acManagerTaskDelete")
HTTP_RESOURCE_TD_MANAGER_TASK_LIST = nebula_config.get("http").get(
    "resource").get("TDComparisonService").get("tdManagerTaskList")
HTTP_RESOURCE_TD_MANAGER_TASK_DELETE = nebula_config.get("http").get(
    "resource").get("TDComparisonService").get("tdManagerTaskDelete")
HTTP_RESOURCE_VIDEO_PROCESS_TASK_LIST = nebula_config.get("http").get(
    "resource").get("VideoProcessService").get("videoProcessTaskList")
HTTP_RESOURCE_VIDEO_PROCESS_TASK_DELETE = nebula_config.get("http").get(
    "resource").get("VideoProcessService").get("videoProcessTaskDelete")
HTTP_RESOURCE_STATIC_DATABASE_LIST = nebula_config.get("http").get(
    "resource").get("StaticFeatureDBProxy").get("staticDBDBList")
HTTP_RESOURCE_STATIC_DATABASE_DELETE = nebula_config.get("http").get(
    "resource").get("StaticFeatureDBProxy").get("staticDBDBDelete")
HTTP_RESOURCE_INFRA_OSG_LIST_BUCKETS = nebula_config.get("http").get(
    "resource").get("ObjectStorageGateway").get("infraOSGListBuckets")
HTTP_RESOURCE_INFRA_OSG_CREATE_BUCKET = nebula_config.get("http").get(
    "resource").get("ObjectStorageGateway").get("infraOSGCreateBucket")
HTTP_RESOURCE_IMAGE_INGRESS_TASK_LIST = nebula_config.get("http").get(
    "resource").get("ImageIngressService").get("imageIngressTaskList")
HTTP_RESOURCE_IMAGE_INGRESS_TASK_DELETE = nebula_config.get("http").get(
    "resource").get("ImageIngressService").get("imageIngressTaskDelete")

# ssh configurations
ssh_config = Config('./guard/config/ssh_config.yml').config.get("ssh")

# database configurations
db_config = Config('./guard/config/db_config.yml').config.get("database")


# all basic buckets
buckets = nebula_config.get("buckets")

# all SQL files for initialization
db_init_config = Config('./guard/config/db_config.yml').config.get("init")
PATH_OF_INIT_SQL_FILES = db_init_config.get("path")
INIT_SQL_FILES = db_init_config.get("sql_files")


def logger(func):
    def warpper(*args, **kwargs):
        strat_time = datetime.datetime.now()
        print("[%s]Run %s" % (strat_time, func.__name__))
        return func(*args, **kwargs)
    return warpper


def get_response_in_json_format(resource):
    response = requests.request("GET", HTTP_END_POINT+resource, verify=False)
    return json.loads(str(response.content, "utf-8"))


def send_request_to_delete_tasks(resource_task_list, resource_delete_task):
    json_response = get_response_in_json_format(resource_task_list)
    for i in range(len(json_response["tasks"])):
        if HTTP_RESOURCE_IMAGE_INGRESS_TASK_LIST == resource_task_list:
            task_id = json_response["tasks"][i]["task"]["task_id"]
        else:
            task_id = json_response["tasks"][i]["info"]["task_id"]
        requests.request("DELETE", HTTP_END_POINT +
                         resource_delete_task.replace("{task_id}", task_id))
        print("Task: %s has been deleted!" % task_id)


@logger
def delete_all_ac_tasks():
    send_request_to_delete_tasks(HTTP_RESOURCE_AC_MANAGER_TASK_LIST,
                                 HTTP_RESOURCE_AC_MANAGER_TASK_DELETE)


@logger
def delete_all_td_tasks():
    send_request_to_delete_tasks(HTTP_RESOURCE_TD_MANAGER_TASK_LIST,
                                 HTTP_RESOURCE_TD_MANAGER_TASK_DELETE)


@logger
def delete_all_vps_tasks():
    send_request_to_delete_tasks(HTTP_RESOURCE_VIDEO_PROCESS_TASK_LIST,
                                 HTTP_RESOURCE_VIDEO_PROCESS_TASK_DELETE)


@logger
def delete_all_iis_tasks():
    send_request_to_delete_tasks(HTTP_RESOURCE_IMAGE_INGRESS_TASK_LIST,
                                 HTTP_RESOURCE_IMAGE_INGRESS_TASK_DELETE)


@logger
def delete_all_static_feature_databases():
    response = requests.request(
        "GET", HTTP_END_POINT+HTTP_RESOURCE_STATIC_DATABASE_LIST)
    json_response = json.loads(str(response.content, "utf-8"))
    for i in range(len(json_response["db_infos"])):
        db_name = json_response["db_infos"][i]["name"]
        db_id = json_response["db_infos"][i]["db_id"]
        requests.request("DELETE", HTTP_END_POINT +
                         HTTP_RESOURCE_STATIC_DATABASE_DELETE.replace("{db_id}", db_id))
        print("Static Database: %s (%s) has been deleted!" % (db_name, db_id))


@logger
def check_all_buckets():
    for bucket in buckets:
        payload = '{"bucket_info":{"name":"%s"}}' % bucket
        requests.request("PUT", HTTP_END_POINT +
                         HTTP_RESOURCE_INFRA_OSG_CREATE_BUCKET, data=payload)
        print("Bucket %s has been created." % bucket)


@logger
def init_senseguard_database():
    ssh = SSH(**ssh_config)

    for file in INIT_SQL_FILES:
        if os.path.exists(os.path.join(PATH_OF_INIT_SQL_FILES, file)):
            ssh.scp_local_file(file, PATH_OF_INIT_SQL_FILES, '~/')
            ssh.execute_command(
                f"mysql -h{db_config.get('host')} -P{db_config.get('port')} -u{db_config.get('user')} -p{db_config.get('password')} < {file}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Senseguard Cleaner is a tool to clear data on the server.')
    parser.add_argument('--host', action='store',
                        dest='host', help='host of target server')
    parser.add_argument('--path', action='store',
                        dest='path', help='host of target server')
    parser.add_argument('-ac', action='store_true',
                        default=False, dest='ac_switch', help='host of target server')
    parser.add_argument('-td', action='store_true',
                        default=False, dest='td_switch', help='host of target server')
    parser.add_argument('-vps', action='store_true',
                        default=False, dest='vps_switch', help='host of target server')
    parser.add_argument('-iis', action='store_true',
                        default=False, dest='iis_switch', help='host of target server')
    parser.add_argument('-fdb', action='store_true',
                        default=False, dest='fdb_switch', help='host of target server')
    parser.add_argument('-db', action='store_true',
                        default=False, dest='db_switch', help='host of target server')
    parser.add_argument('-bucket', action='store_true',
                        default=False, dest='bucket_switch', help='host of target server')
    args = parser.parse_args()

    if args.host:
        db_config['host'] = args.host
        ssh_config['hostname'] = args.host
        HTTP_HOST = args.host
        HTTP_END_POINT = "http://%s:%s" % (HTTP_HOST, HTTP_PORT)

    if args.path:
        PATH_OF_INIT_SQL_FILES = args.path

    if args.ac_switch:
        delete_all_ac_tasks()
    if args.td_switch:
        delete_all_td_tasks()
    if args.vps_switch:
        delete_all_vps_tasks()
    if args.iis_switch:
        delete_all_iis_tasks()
    if args.fdb_switch:
        delete_all_static_feature_databases()
    if args.db_switch:
        init_senseguard_database()
    if args.bucket_switch:
        check_all_buckets()

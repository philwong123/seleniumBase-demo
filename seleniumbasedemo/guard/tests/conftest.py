#!/usr/bin/env python3
import os
import time

import pytest
import uuid

from seleniumbase import config as sb_config
from guard.pages.device import DevicePage
from guard.pages.map import MapPage
from guard.pages.login import LoginPage
from guard.pages.portrait import PortraitPage
from guard.pages.task import TaskPage
from guard.pages.timezone import TimezonePage
from guard.pages.user import UserPage
from guard.pages.role import RolePage
from guard.pages.components.menubar import MenuBar
from guard.pages.classes.user import User
from guard.pages.classes.device.rtsp import RTSP
from guard.pages.classes.device.frontend import Frontend
from guard.pages.classes.portrait import Portrait
from guard.pages.classes.task.face_access_control_task import FaceAccessControlTask
from guard.pages.classes.task.face_alert_deployment_task import FaceAlertDeploymentTask
from guard.pages.classes.task.pedestrian_crossing_boundary_detection_task import PedestrianCrossingBoundaryDetectionTask
from guard.pages.classes.task.pedestrian_area_entry_detection_task import PedestrianAreaEntryDetectionTask
from guard.pages.classes.task.vehicle_illegally_parking_detection_task import VehicleIllegallyParkingDetectionTask


def pytest_configure(config):
    """Add custom markers."""
    config.addinivalue_line(
        "markers", "positive: mark a test as a positive case.")
    config.addinivalue_line(
        "markers", "negative: mark a test as a negative case.")
    config.addinivalue_line("markers", "smoke: mark a test as a smoke case.")
    config.addinivalue_line("markers", "shin: mark a test by shin.")
    config.addinivalue_line(
        "markers", "yxl: mark test cases created by yxl.")
    config.addinivalue_line(
        "markers", "debug: mark test cases as debug.")
    """ This runs after command line options have been parsed """
    sb_config.host = config.getoption('host')
    sb_config.username = config.getoption('username')
    sb_config.password = config.getoption('password')
    sb_config.ocr = config.getoption('ocr')
    sb_config.redis = config.getoption('redis')
    sb_config.redis_without_password = config.getoption(
        'redis_without_password')


def pytest_runtest_setup(item):
    print("setting up", item)


def pytest_addoption(parser):
    parser.addoption('--host',
                     action='store',
                     dest='host',
                     default=None,
                     help="""Designates the starting host for the web browser
                          when each test begins.
                          Default: None.""")
    parser.addoption('--username',
                     action='store',
                     dest='username',
                     default=None,
                     help="""Designates the starting username for the web browser
                          when each test begins.
                          Default: None.""")
    parser.addoption('--password',
                     action='store',
                     dest='password',
                     default=None,
                     help="""Designates the starting password for the web browser
                          when each test begins.
                          Default: None.""")
    parser.addoption('--ocr',
                     action='store_true',
                     dest='ocr',
                     help="""Designates the starting ocr for the web browser
                          when each test begins.
                          Default: True.""")
    parser.addoption('--redis',
                     action='store_true',
                     dest='redis',
                     help="""Designates the captcha code for the web browser
                              from redis.
                              Default: True.""")
    parser.addoption('--redis-without-password',
                     action='store_true',
                     dest='redis_without_password',
                     help="""Designates no password for redis.
                              Default: False.""")


def generate_uuid():
    uid = str(uuid.uuid4())
    suid = ''.join(uid.split('-'))
    return f'{suid}'


def get_current_time():
    # 获取当前系统时间时间
    return time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))


@pytest.fixture()
def open(sb):
    """ 打开命令行中指定页面 """
    sb.open(f"https://{sb_config.host}")


@pytest.fixture()
def login(sb):
    """ 登录命令行中指定用户 """
    LoginPage.login(sb, sb_config.username, sb_config.password)


@pytest.fixture()
def portrait_type():
    return '白名单'


@pytest.fixture()
def setup_portrait_database_name_and_delete_portrait_database(sb):
    """ 生成人像库名称并清理该人像库 """
    request = {'name': generate_uuid()}
    MenuBar.click_menu_item_by_text(sb, '配置', '人像库管理')
    yield request
    sb.save_teardown_screenshot()
    PortraitPage.delete_portrait_database_by_name(sb, request['name'])


@pytest.fixture()
def setup_portrait_database(sb, portrait_type):
    """ 添加人像库 """
    request = {'name': generate_uuid()}
    MenuBar.click_menu_item_by_text(sb, '配置', '人像库管理')
    PortraitPage.add_portrait_database_by_name(
        sb, request['name'], type=portrait_type)
    yield request
    sb.save_teardown_screenshot()


@pytest.fixture()
def setup_portrait_database_and_delete_portrait_database(sb, portrait_type):
    """ 添加人像库并清理该人像库 """
    request = {'name': generate_uuid()}
    MenuBar.click_menu_item_by_text(sb, '配置', '人像库管理')
    PortraitPage.add_portrait_database_by_name(
        sb, request['name'], type=portrait_type)
    yield request
    sb.save_teardown_screenshot()
    PortraitPage.delete_portrait_database_by_name(sb, request['name'])


@pytest.fixture()
def setup_portrait_database_name(sb):
    """ 生成人像库名称 """
    request = {'name': generate_uuid()}
    MenuBar.click_menu_item_by_text(sb, '配置', '人像库管理')
    yield request
    sb.save_teardown_screenshot()


@pytest.fixture()
def setup_portrait_name(sb):
    """ 生成人像姓名 """
    request = {'name': generate_uuid()}
    MenuBar.click_menu_item_by_text(sb, '配置', '人像库管理')
    yield request
    sb.save_teardown_screenshot()


@pytest.fixture()
def setup_portrait_with_portrait_database_and_delete_portrait_database(sb, setup_portrait_database_and_delete_portrait_database):
    """ 添加人像到人像库并删除人像库 """
    request = {'name': generate_uuid(
    ), 'portrait_database': setup_portrait_database_and_delete_portrait_database['name']}
    MenuBar.click_menu_item_by_text(sb, '配置', '人像库管理')
    portrait = Portrait(name=request['name'], id_number=request['name'],
                        image_path=os.getcwd()+'/guard/data/portrait/001-JPG.jpg',
                        portrait_databases=[request['portrait_database']])
    PortraitPage.add_portrait(sb, portrait)
    yield request
    sb.save_teardown_screenshot()


@pytest.fixture()
def setup_portrait_with_two_portrait_databases_and_delete_portrait_databases(sb, setup_portrait_database_name):
    """ 添加人像到人像库并删除人像库 """
    request = {'name': generate_uuid(), 'portrait_databases': [f'{setup_portrait_database_name["name"]}1',
                                                               f'{setup_portrait_database_name["name"]}2']}
    for portrait_database in request['portrait_databases']:
        PortraitPage.add_portrait_database_by_name(sb, portrait_database)
    MenuBar.click_menu_item_by_text(sb, '配置', '人像库管理')
    portrait = Portrait(name=request['name'], id_number=request['name'],
                        image_path=os.getcwd()+'/guard/data/portrait/001-JPG.jpg',
                        portrait_databases=request['portrait_databases'])
    PortraitPage.add_portrait(sb, portrait)
    yield request
    sb.save_teardown_screenshot()
    for portrait_database in request['portrait_databases']:
        PortraitPage.delete_portrait_database_by_name(sb, portrait_database)


@pytest.fixture()
def setup_department_name_and_delete_department(sb, portrait_type):
    """ 生成部门名称并清理该部门 """
    request = {'name': generate_uuid()}
    MenuBar.click_menu_item_by_text(sb, '配置', '用户管理')
    yield request
    sb.save_teardown_screenshot()
    UserPage.delete_department_by_name(sb, request['name'], type=portrait_type)


@pytest.fixture()
def setup_department(sb):
    """ 添加部门 """
    request = {'name': generate_uuid()}
    MenuBar.click_menu_item_by_text(sb, '配置', '用户管理')
    UserPage.add_department_by_root_department_name(sb, request['name'])
    yield request
    sb.save_teardown_screenshot()


@pytest.fixture()
def setup_department_and_delete_department(sb):
    """ 添加部门并清理该部门 """
    request = {'name': generate_uuid()}
    MenuBar.click_menu_item_by_text(sb, '配置', '用户管理')
    UserPage.add_department_by_root_department_name(sb, request['name'])
    yield request
    sb.save_teardown_screenshot()
    UserPage.delete_department_by_name(sb, request['name'])


@pytest.fixture()
def setup_subdepartment_name_and_delete_subdepartment(sb):
    """ 生成子部门名称并清理该子部门 """
    request = {'name': generate_uuid()}
    MenuBar.click_menu_item_by_text(sb, '配置', '用户管理')
    yield request
    sb.save_teardown_screenshot()
    UserPage.delete_department_by_name(sb, request['name'])


@pytest.fixture()
def setup_subdepartment(sb):
    """ 添加子部门 """
    request = {'name': generate_uuid()}
    MenuBar.click_menu_item_by_text(sb, '配置', '用户管理')
    UserPage.add_department_by_parent_department_name(sb, request['name'])
    yield request
    sb.save_teardown_screenshot()


@pytest.fixture()
def setup_subdepartment_and_delete_subdepartment(sb):
    """ 添加子部门并清理该子部门 """
    request = {'name': generate_uuid()}
    MenuBar.click_menu_item_by_text(sb, '配置', '用户管理')
    UserPage.add_department_by_parent_department_name(sb, request['name'])
    yield request
    sb.save_teardown_screenshot()
    UserPage.delete_department_by_name(sb, request['name'])


@pytest.fixture()
def setup_user_name_and_delete_user(sb):
    """ 生成用户名并清理该用户 """
    request = {'name': generate_uuid()}
    MenuBar.click_menu_item_by_text(sb, '配置', '用户管理')
    yield request
    sb.save_teardown_screenshot()
    UserPage.delete_user_by_name(sb, request['name'])


@pytest.fixture()
def setup_user_reset_password(sb):
    request = {'name': generate_uuid()}
    MenuBar.click_menu_item_by_text(sb, '配置', '用户管理')
    default_password = UserPage.reset_user_password(sb, request['name'])
    yield str(default_password).strip()
    sb.save_teardown_screenshot()
    UserPage.delete_user_by_name(sb, request['name'])


@pytest.fixture()
def setup_user(sb):
    """ 添加用户 """
    request = {'name': generate_uuid()}
    MenuBar.click_menu_item_by_text(sb, '配置', '用户管理')
    user = User(request['name'], request['name'])
    UserPage.add_user_by_department_name(sb, user)
    yield request
    sb.save_teardown_screenshot()


@pytest.fixture()
def setup_user_and_delete_user(sb):
    """ 添加用户并清理该用户 """
    request = {'name': generate_uuid()}
    MenuBar.click_menu_item_by_text(sb, '配置', '用户管理')
    user = User(request['name'], request['name'])
    UserPage.add_user_by_department_name(sb, user)
    yield request
    sb.save_teardown_screenshot()
    MenuBar.click_menu_item_by_text(sb, '配置', '用户管理')
    UserPage.delete_user_by_name(sb, request['name'])


@pytest.fixture()
def setup_peer_floor_name_and_delete_floor(sb):
    """ 生成同级楼层名称并清理该楼层 """
    request = {'name': generate_uuid()}
    MenuBar.click_menu_item_by_text(sb, '配置', '地图管理')
    yield request
    sb.save_teardown_screenshot()
    MapPage.delete_floor_by_name(sb, request['name'])


@pytest.fixture()
def setup_peer_floor(sb):
    """ 添加同级楼层 """
    request = {'name': generate_uuid()}
    MenuBar.click_menu_item_by_text(sb, '配置', '地图管理')
    MapPage.add_floor_by_root_floor_name(sb, request['name'])
    yield request
    sb.save_teardown_screenshot()


@pytest.fixture()
def setup_peer_floor_and_delete_floor(sb):
    """ 添加同级楼层并清理该楼层 """
    request = {'name': generate_uuid()}
    MenuBar.click_menu_item_by_text(sb, '配置', '地图管理')
    MapPage.add_floor_by_root_floor_name(sb, request['name'])
    yield request
    sb.save_teardown_screenshot()
    MapPage.delete_floor_by_name(sb, request['name'])


@pytest.fixture()
def setup_subordinate_floor_name_and_delete_floor(sb):
    """ 生成下一级楼层名称并清理该下一级楼层 """
    request = {'name': generate_uuid()}
    MenuBar.click_menu_item_by_text(sb, '配置', '地图管理')
    yield request
    sb.save_teardown_screenshot()
    MapPage.delete_floor_by_name(sb, request['name'])


@pytest.fixture()
def setup_subordinate_floor(sb):
    """ 添加下一级楼层 """
    request = {'name': generate_uuid()}
    MenuBar.click_menu_item_by_text(sb, '配置', '地图管理')
    MapPage.add_floor_by_parent_name(sb, request['name'], is_peer=False)
    yield request
    sb.save_teardown_screenshot()


@pytest.fixture()
def setup_device_group_name_and_delete_group(sb):
    """ 生成设备分组名并清理该该设备分组 """
    request = {'name': generate_uuid()}
    MenuBar.click_menu_item_by_text(sb, '配置', '设备管理')
    yield request
    sb.save_teardown_screenshot()
    DevicePage.delete_group_by_name(sb, request['name'])


@pytest.fixture()
def setup_device_group(sb):
    """ 添加设备分组 """
    request = {'name': generate_uuid()}
    MenuBar.click_menu_item_by_text(sb, '配置', '设备管理')
    DevicePage.add_group_by_root_group_name(sb, request['name'])
    yield request
    sb.save_teardown_screenshot()


@pytest.fixture()
def setup_device_group_and_delete_group(sb):
    """ 添加设备分组并清理该分组 """
    request = {'name': generate_uuid()}
    MenuBar.click_menu_item_by_text(sb, '配置', '设备管理')
    DevicePage.add_group_by_root_group_name(sb, request['name'])
    yield request
    sb.save_teardown_screenshot()
    DevicePage.delete_group_by_name(sb, request['name'])

# 添加4/9
@pytest.fixture()
def setup_subordinate_device_group(sb):
    request = {'name': generate_uuid()}
    MenuBar.click_menu_item_by_text(sb, '配置', '设备管理')
    yield request
    sb.save_teardown_screenshot()

@pytest.fixture()
def setup_face_access_control_task_name_and_delete_task(sb):
    """ 生成人脸通行任务名称并清理该任务 """
    request = {'name': generate_uuid()}
    MenuBar.click_menu_item_by_text(sb, '配置', '地图管理')
    MapPage.add_floor_by_root_floor_name(sb, request['name'])
    MenuBar.click_menu_item_by_text(sb, '配置', '设备管理')
    DevicePage.add_group_by_root_group_name(sb, request['name'])
    frontend_device = Frontend(request['name'], request['name'], request['name'],
                               request['name'], 'SensePass')
    DevicePage.add_device_by_type(
        sb, frontend_device, '人脸识别机（前）')
    MenuBar.click_menu_item_by_text(sb, '配置', '人像库管理')
    PortraitPage.add_portrait_database_by_name(sb, request['name'])
    MenuBar.click_menu_item_by_text(sb, '配置', '任务管理')
    yield request
    sb.save_teardown_screenshot()
    MenuBar.click_menu_item_by_text(sb, '配置', '任务管理')
    TaskPage.click_task_tab_by_type(sb, type='人脸-通行任务')
    TaskPage.delete_task_by_name(sb, request['name'])
    MenuBar.click_menu_item_by_text(sb, '配置', '人像库管理')
    PortraitPage.delete_portrait_database_by_name(sb, request['name'])
    MenuBar.click_menu_item_by_text(sb, '配置', '设备管理')
    DevicePage.delete_group_by_name(sb, request['name'])
    MenuBar.click_menu_item_by_text(sb, '配置', '地图管理')
    MapPage.delete_floor_by_name(sb, request['name'])

@pytest.fixture()
def setup_face_alert_deployment_task_name_and_delete_task(sb):
    """ 生成监控任务名称并清理该任务 """
    request = {'name': generate_uuid()}
    MenuBar.click_menu_item_by_text(sb, '配置', '地图管理')
    MapPage.add_floor_by_root_floor_name(sb, request['name'])
    MenuBar.click_menu_item_by_text(sb, '配置', '设备管理')
    DevicePage.add_group_by_root_group_name(sb, request['name'])
    rtsp_device = RTSP(request['name'], request['name'], request['name'],
                               request['name'], 'rtsp://confidence.119:6554/SchoolAnniversary.264')
    DevicePage.add_device_by_type(
        sb, rtsp_device, '网络摄像机')
    MenuBar.click_menu_item_by_text(sb, '配置', '人像库管理')
    PortraitPage.add_portrait_database_by_name(sb, request['name'])
    MenuBar.click_menu_item_by_text(sb, '配置', '任务管理')
    yield request
    sb.save_teardown_screenshot()
    MenuBar.click_menu_item_by_text(sb, '配置', '任务管理')
    TaskPage.click_task_tab_by_type(sb, type='人脸-布控任务')
    TaskPage.delete_task_by_name(sb, request['name'])
    MenuBar.click_menu_item_by_text(sb, '配置', '人像库管理')
    PortraitPage.delete_portrait_database_by_name(sb, request['name'])
    MenuBar.click_menu_item_by_text(sb, '配置', '设备管理')
    DevicePage.delete_group_by_name(sb, request['name'])
    MenuBar.click_menu_item_by_text(sb, '配置', '地图管理')
    MapPage.delete_floor_by_name(sb, request['name'])

@pytest.fixture()
def setup_face_access_control_task_name_with_mul_portrait_and_delete_task(sb):
    """ 生成人脸通行任务名称并清理该任务 """
    request = {'name': generate_uuid(), 'name2': generate_uuid()}
    MenuBar.click_menu_item_by_text(sb, '配置', '地图管理')
    MapPage.add_floor_by_root_floor_name(sb, request['name'])
    MenuBar.click_menu_item_by_text(sb, '配置', '设备管理')
    DevicePage.add_group_by_root_group_name(sb, request['name'])
    frontend_device = Frontend(request['name'], request['name'], request['name'],
                               request['name'], 'SensePass')
    DevicePage.add_device_by_type(
        sb, frontend_device, '人脸识别机（前）')
    MenuBar.click_menu_item_by_text(sb, '配置', '人像库管理')
    PortraitPage.add_portrait_database_by_name(sb, request['name'])
    PortraitPage.add_portrait_database_by_name(sb, request['name2'])
    MenuBar.click_menu_item_by_text(sb, '配置', '任务管理')
    yield request
    sb.save_teardown_screenshot()
    MenuBar.click_menu_item_by_text(sb, '配置', '任务管理')
    TaskPage.click_task_tab_by_type(sb, type='人脸-通行任务')
    TaskPage.delete_task_by_name(sb, request['name'])
    MenuBar.click_menu_item_by_text(sb, '配置', '人像库管理')
    PortraitPage.delete_portrait_database_by_name(sb, request['name'])
    PortraitPage.delete_portrait_database_by_name(sb, request['name2'])
    MenuBar.click_menu_item_by_text(sb, '配置', '设备管理')
    DevicePage.delete_group_by_name(sb, request['name'])
    MenuBar.click_menu_item_by_text(sb, '配置', '地图管理')
    MapPage.delete_floor_by_name(sb, request['name'])

@pytest.fixture()
def setup_face_alert_deployment_task_name_with_mul_portrait_and_delete_task(sb):
    """ 生成人脸通行任务名称并清理该任务 """
    request = {'name': generate_uuid(), 'name2': generate_uuid()}
    MenuBar.click_menu_item_by_text(sb, '配置', '地图管理')
    MapPage.add_floor_by_root_floor_name(sb, request['name'])
    MenuBar.click_menu_item_by_text(sb, '配置', '设备管理')
    DevicePage.add_group_by_root_group_name(sb, request['name'])
    rtsp_device = RTSP(request['name'], request['name'], request['name'],
                       request['name'], 'rtsp://confidence.119:6554/SchoolAnniversary.264')
    DevicePage.add_device_by_type(
        sb, rtsp_device, '网络摄像机')
    MenuBar.click_menu_item_by_text(sb, '配置', '人像库管理')
    PortraitPage.add_portrait_database_by_name(sb, request['name'])
    PortraitPage.add_portrait_database_by_name(sb, request['name2'])
    MenuBar.click_menu_item_by_text(sb, '配置', '任务管理')
    yield request
    sb.save_teardown_screenshot()
    MenuBar.click_menu_item_by_text(sb, '配置', '任务管理')
    TaskPage.click_task_tab_by_type(sb, type='人脸-布控任务')
    TaskPage.delete_task_by_name(sb, request['name'])
    MenuBar.click_menu_item_by_text(sb, '配置', '人像库管理')
    PortraitPage.delete_portrait_database_by_name(sb, request['name'])
    PortraitPage.delete_portrait_database_by_name(sb, request['name2'])
    MenuBar.click_menu_item_by_text(sb, '配置', '设备管理')
    DevicePage.delete_group_by_name(sb, request['name'])
    MenuBar.click_menu_item_by_text(sb, '配置', '地图管理')
    MapPage.delete_floor_by_name(sb, request['name'])

@pytest.fixture()
def setup_pedestrian_crossing_boundary_detection_task_name_and_delete_task(sb):
    """ 生成人体越线检测任务名称并清理该任务 """
    request = {'name': generate_uuid()}
    MenuBar.click_menu_item_by_text(sb, '配置', '地图管理')
    MapPage.add_floor_by_root_floor_name(sb, request['name'])
    MenuBar.click_menu_item_by_text(sb, '配置', '设备管理')
    DevicePage.add_group_by_root_group_name(sb, request['name'])
    rtsp_device = RTSP(request['name'], request['name'], request['name'],
                       request['name'], 'rtsp://confidence.119:6554/test.264')
    DevicePage.add_device_by_type(sb, rtsp_device, '网络摄像机')
    MenuBar.click_menu_item_by_text(sb, '配置', '人像库管理')
    PortraitPage.add_portrait_database_by_name(sb, request['name'])
    MenuBar.click_menu_item_by_text(sb, '配置', '任务管理')
    yield request
    sb.save_teardown_screenshot()
    MenuBar.click_menu_item_by_text(sb, '配置', '任务管理')
    TaskPage.click_task_tab_by_type(sb, type='人体-越线检测任务')
    TaskPage.delete_task_by_name(sb, request['name'])
    MenuBar.click_menu_item_by_text(sb, '配置', '人像库管理')
    PortraitPage.delete_portrait_database_by_name(sb, request['name'])
    MenuBar.click_menu_item_by_text(sb, '配置', '设备管理')
    DevicePage.delete_group_by_name(sb, request['name'])
    MenuBar.click_menu_item_by_text(sb, '配置', '地图管理')
    MapPage.delete_floor_by_name(sb, request['name'])


@pytest.fixture()
def setup_pedestrian_area_entry_detection_task_name_and_delete_task(sb):
    """ 生成人体区域闯入检测任务名称并清理该任务 """
    request = {'name': generate_uuid()}
    MenuBar.click_menu_item_by_text(sb, '配置', '地图管理')
    MapPage.add_floor_by_root_floor_name(sb, request['name'])
    MenuBar.click_menu_item_by_text(sb, '配置', '设备管理')
    DevicePage.add_group_by_root_group_name(sb, request['name'])
    rtsp_device = RTSP(request['name'], request['name'], request['name'],
                       request['name'], 'rtsp://confidence.119:6554/test.264')
    DevicePage.add_device_by_type(sb, rtsp_device, '网络摄像机')
    MenuBar.click_menu_item_by_text(sb, '配置', '人像库管理')
    PortraitPage.add_portrait_database_by_name(sb, request['name'])
    MenuBar.click_menu_item_by_text(sb, '配置', '任务管理')
    yield request
    sb.save_teardown_screenshot()
    MenuBar.click_menu_item_by_text(sb, '配置', '任务管理')
    TaskPage.click_task_tab_by_type(sb, type='人体-区域闯入检测任务')
    TaskPage.delete_task_by_name(sb, request['name'])
    MenuBar.click_menu_item_by_text(sb, '配置', '人像库管理')
    PortraitPage.delete_portrait_database_by_name(sb, request['name'])
    MenuBar.click_menu_item_by_text(sb, '配置', '设备管理')
    DevicePage.delete_group_by_name(sb, request['name'])
    MenuBar.click_menu_item_by_text(sb, '配置', '地图管理')
    MapPage.delete_floor_by_name(sb, request['name'])


@pytest.fixture()
def setup_vehicle_illegally_parking_detection_task_name_and_delete_task(sb):
    """ 生成车辆违停检测任务名称并清理该任务 """
    request = {'name': generate_uuid()}
    MenuBar.click_menu_item_by_text(sb, '配置', '地图管理')
    MapPage.add_floor_by_root_floor_name(sb, request['name'])
    MenuBar.click_menu_item_by_text(sb, '配置', '设备管理')
    DevicePage.add_group_by_root_group_name(sb, request['name'])
    rtsp_device = RTSP(request['name'], request['name'], request['name'],
                       request['name'], 'rtsp://confidence.119:6554/test.264')
    DevicePage.add_device_by_type(sb, rtsp_device, '网络摄像机')
    MenuBar.click_menu_item_by_text(sb, '配置', '人像库管理')
    PortraitPage.add_portrait_database_by_name(sb, request['name'])
    MenuBar.click_menu_item_by_text(sb, '配置', '任务管理')
    yield request
    sb.save_teardown_screenshot()
    MenuBar.click_menu_item_by_text(sb, '配置', '任务管理')
    TaskPage.click_task_tab_by_type(sb, type='车辆-违停检测任务')
    TaskPage.delete_task_by_name(sb, request['name'])
    MenuBar.click_menu_item_by_text(sb, '配置', '人像库管理')
    PortraitPage.delete_portrait_database_by_name(sb, request['name'])
    MenuBar.click_menu_item_by_text(sb, '配置', '设备管理')
    DevicePage.delete_group_by_name(sb, request['name'])
    MenuBar.click_menu_item_by_text(sb, '配置', '地图管理')
    MapPage.delete_floor_by_name(sb, request['name'])


@pytest.fixture()
def setup_role_name_and_delete_role(sb):
    """ 生成角色名称并删除该角色 """
    request = {'name': generate_uuid()}
    MenuBar.click_menu_item_by_text(sb, '配置', '角色管理')
    yield request
    sb.save_teardown_screenshot()
    MenuBar.click_menu_item_by_text(sb, '配置', '角色管理')
    RolePage.delete_role_by_name(sb, request['name'])


@pytest.fixture
def timezone(sb, login):
    request = {'name': f'Timezone-{get_current_time()}'}
    MenuBar.click_menu_item_by_text(sb, '配置', '时间条件')
    yield request
    TimezonePage.delete_or_rename_timezone_name(sb, request["name"])


@pytest.fixture
def timezone_section(sb, login):
    request = {'name': f'Timezone-{get_current_time()}'}
    MenuBar.click_menu_item_by_text(sb, '配置', '时间条件')
    TimezonePage.add_timezone_name(sb, request["name"])
    yield request
    TimezonePage.delete_or_rename_timezone_name(sb, request["name"])


@pytest.fixture
def holidays(sb, login):
    request = {'name': f'H-{get_current_time()}'}
    MenuBar.click_menu_item_by_text(sb, '配置', '时间条件')
    yield request


@pytest.fixture
def workday(sb, login):
    request = {'name': f'W-{get_current_time()}'}
    MenuBar.click_menu_item_by_text(sb, '配置', '时间条件')
    yield request


@pytest.fixture
def negative_te(sb, login):
    request = {'name': f'ABD-{generate_uuid()}'}
    MenuBar.click_menu_item_by_text(sb, '配置', '时间条件')
    yield request

@pytest.fixture
def setup_log(sb):
    MenuBar.click_menu_item_by_text(sb, '配置', '日志管理')
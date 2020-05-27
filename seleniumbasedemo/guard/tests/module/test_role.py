#!/usr/bin/env python3
import pytest
import logging
import uuid
from guard.pages.components.menubar import MenuBar
from guard.pages.classes.user import User
from guard.pages.user import UserPage
from guard.pages.role import RolePage
from guard.pages.login import LoginPage
from guard.pages.personInfo import PersonInfoPage
from guard.pages.systemInfo import SystemInfoPage
from guard.pages.base import BasePage
from guard.pages.message import MessagePage
from selenium.webdriver.common.by import By

roles = list()
'''
测试数据：
格式：[
        {'用户': '用户名1', '角色': '角色名1', '角色权限': '角色权限1'}, 
        {'用户': '用户名2', '角色': '角色名2', '角色权限': '角色权限2'},
        ...
       ]
'''
device_test_data = [
    {'user': 'user_device_view_privilege', 'role': 'role_device_view_privilege', 'permissions': {'设备管理': ['查看']}},
    {'user': 'user_device_add_privilege', 'role': 'role_device_add_privilege', 'permissions': {'设备管理': ['查看', '添加']}},
    {'user': 'user_device_edit_privilege', 'role': 'role_device_edit_privilege', 'permissions': {'设备管理': ['查看', '修改']}},
    {'user': 'user_device_delete_privilege', 'role': 'role_device_delete_privilege',
     'permissions': {'设备管理': ['查看', '删除']}},
    {'user': 'user_device_export_privilege', 'role': 'role_device_export_privilege',
     'permissions': {'设备管理': ['查看', '导出']}},
    {'user': 'user_device_all_privilege', 'role': 'role_device_all_privilege',
     'permissions': {'设备管理': ['查看', '添加', '修改', '删除', '导出']}},
    ]

log_test_data = [
    {'user': 'user_log_view_privilege', 'role': 'role_log_view_privilege', 'permissions': {'日志管理': ['查看']}},
    {'user': 'user_log_export_privilege', 'role': 'role_log_export_privilege', 'permissions': {'日志管理': ['查看', '导出']}},
    ]

role_test_data = [
    {'user': 'user_role_view_privilege', 'role': 'role_role_view_privilege', 'permissions': {'角色管理': ['查看']}},
    {'user': 'user_role_add_privilege', 'role': 'role_role_add_privilege', 'permissions': {'角色管理': ['查看', '添加']}},
    {'user': 'user_role_edit_privilege', 'role': 'role_role_edit_privilege', 'permissions': {'角色管理': ['查看', '修改']}},
    {'user': 'user_role_delete_privilege', 'role': 'role_role_delete_privilege', 'permissions': {'角色管理': ['查看', '删除']}},
    {'user': 'user_role_export_privilege', 'role': 'role_role_export_privilege', 'permissions': {'角色管理': ['查看', '导出']}},
    {'user': 'user_role_all_privilege', 'role': 'role_role_all_privilege',
     'permissions': {'角色管理': ['查看', '添加', '修改', '删除', '导出']}},
    ]

attendance_test_data = [
    {'user': 'user_attendance_view_privilege', 'role': 'role_attendance_view_privilege', 'permissions': {'考勤': ['查看']}},
    {'user': 'user_attendance_edit_privilege', 'role': 'role_attendance_edit_privilege',
     'permissions': {'考勤': ['查看', '修改']}},
    {'user': 'user_attendance_export_privilege', 'role': 'role_attendance_export_privilege',
     'permissions': {'考勤': ['查看', '导出']}},
    ]

user_test_data = [
    {'user': 'user_user_view_privilege', 'role': 'role_user_view_privilege', 'permissions': {'用户管理': ['查看']}},
    {'user': 'user_user_add_privilege', 'role': 'role_user_add_privilege', 'permissions': {'用户管理': ['查看', '添加']}},
    {'user': 'user_user_edit_privilege', 'role': 'role_user_edit_privilege', 'permissions': {'用户管理': ['查看', '修改']}},
    {'user': 'user_user_delete_privilege', 'role': 'role_user_delete_privilege', 'permissions': {'用户管理': ['查看', '删除']}},
    {'user': 'user_user_export_privilege', 'role': 'role_user_export_privilege', 'permissions': {'用户管理': ['查看', '导出']}},
    {'user': 'user_user_all_privilege', 'role': 'role_user_all_privilege',
     'permissions': {'用户管理': ['查看', '添加', '修改', '删除', '导出']}},
    ]

portrait_database_test_data = [
    {'user': 'user_portrait_database_view_privilege', 'role': 'role_portrait_database_view_privilege',
     'permissions': {'人像库管理': ['查看']}},
    {'user': 'user_portrait_database_add_privilege', 'role': 'role_portrait_database_add_privilege',
     'permissions': {'人像库管理': ['查看', '添加']}},
    {'user': 'user_portrait_database_edit_privilege', 'role': 'role_portrait_database_edit_privilege',
     'permissions': {'人像库管理': ['查看', '修改']}},
    {'user': 'user_portrait_database_delete_privilege', 'role': 'role_portrait_database_delete_privilege',
     'permissions': {'人像库管理': ['查看', '删除']}},
    {'user': 'user_portrait_database_export_privilege', 'role': 'role_portrait_database_export_privilege',
     'permissions': {'人像库管理': ['查看', '导出']}},
    {'user': 'user_portrait_database_all_privilege', 'role': 'role_portrait_database_all_privilege',
     'permissions': {'人像库管理': ['查看', '添加', '修改', '删除', '导出']}},
    ]

task_test_data = [
    {'user': 'user_task_view_privilege', 'role': 'role_task_view_privilege', 'permissions': {'任务管理': ['查看']}},
    {'user': 'user_task_add_privilege', 'role': 'role_task_add_privilege', 'permissions': {'任务管理': ['查看', '添加']}},
    {'user': 'user_task_edit_privilege', 'role': 'role_task_edit_privilege', 'permissions': {'任务管理': ['查看', '修改']}},
    {'user': 'user_task_delete_privilege', 'role': 'role_task_delete_privilege', 'permissions': {'任务管理': ['查看', '删除']}},
    {'user': 'user_task_all_privilege', 'role': 'role_task_all_privilege',
     'permissions': {'任务管理': ['查看', '添加', '修改', '删除']}},
    ]
dashboard_test_data = [
    {'user': 'user_dashborad_view_privilege', 'role': 'role_dashborad_view_privilege', 'permissions': {'看板': ['查看']}}]

system_info_test_data = [{'user': 'user_system_info_view_privilege', 'role': 'role_system_info_view_privilege',
                          'permissions': {'系统信息': ['查看']}},
                         {'user': 'user_system_info_edit_privilege', 'role': 'role_system_info_edit_privilege',
                          'permissions': {'系统信息': ['查看', '修改']}},
                         ]

map_management_test_data = [
    {'user': 'user_map_view_privilege', 'role': 'role_map_view_privilege', 'permissions': {'地图管理': ['查看']}},
    {'user': 'user_map_add_privilege', 'role': 'role_map_add_privilege', 'permissions': {'地图管理': ['查看', '添加']}},
    {'user': 'user_map_edit_privilege', 'role': 'role_map_edit_privilege', 'permissions': {'地图管理': ['查看', '修改']}},
    {'user': 'user_map_delete_privilege', 'role': 'role_map_delete_privilege', 'permissions': {'地图管理': ['查看', '删除']}},
    {'user': 'user_map_all_privilege', 'role': 'role_map_all_privilege',
     'permissions': {'地图管理': ['查看', '添加', '修改', '删除']}},
    ]

default_privilege_test_data = [
    {'user': 'user_default_privilege', 'role': 'role_default_privilege', 'permissions': {'': []}}]

tool_privilege_test_data = [
    {'user': 'user_tool_view_privilege', 'role': 'role_tool_view_privilege', 'permissions': {'工具': ['查看']}}]

reception_privilege_test_data = [
    {'user': 'user_reception_view_privilege', 'role': 'role_reception_view_privilege', 'permissions': {'迎宾': ['查看']}}]

live_privilege_test_data = [
    {'user': 'user_live_view_privilege', 'role': 'role_live_view_privilege', 'permissions': {'实况': ['查看']}}]

visitor_test_data = [
    {'user': 'user_visitor_view_privilege', 'role': 'role_visitor_view_privilege', 'permissions': {'访客': ['查看']}},
    {'user': 'user_visitor_add_privilege', 'role': 'role_visitor_add_privilege', 'permissions': {'访客': ['查看', '添加']}},
    {'user': 'user_visitor_edit_privilege', 'role': 'role_visitor_edit_privilege', 'permissions': {'访客': ['查看', '修改']}},
    {'user': 'user_visitor_delete_privilege', 'role': 'role_visitor_delete_privilege',
     'permissions': {'访客': ['查看', '删除']}},
    {'user': 'user_visitor_export_privilege', 'role': 'role_visitor_export_privilege',
     'permissions': {'访客': ['查看', '导出']}},
    {'user': 'user_visitor_all_privilege', 'role': 'role_visitor_all_privilege',
     'permissions': {'访客': ['查看', '添加', '修改', '删除', '导出']}},
    ]

record_test_data = [
    {'user': 'user_record_view_privilege', 'role': 'role_record_view_privilege', 'permissions': {'记录': ['查看']}},
    # {'user': 'user_record_edit_privilege', 'role': 'role_record_edit_privilege', 'permissions': {'记录': ['查看', '修改']}},
    {'user': 'user_record_export_privilege', 'role': 'role_record_export_privilege',
     'permissions': {'记录': ['查看', '导出']}},
    # {'user': 'user_record_all_privilege', 'role': 'role_record_all_privilege',
    #  'permissions': {'记录': ['查看', '修改', '导出']}},
    ]

time_condition_test_data = [{'user': 'user_time_condition_view_privilege', 'role': 'role_time_condition_view_privilege',
                             'permissions': {'时间条件': ['查看']}},
                            {'user': 'user_time_condition_add_privilege', 'role': 'role_time_condition_add_privilege',
                             'permissions': {'时间条件': ['查看', '添加']}},
                            {'user': 'user_time_condition_edit_privilege', 'role': 'role_time_condition_edit_privilege',
                             'permissions': {'时间条件': ['查看', '修改']}},
                            {'user': 'user_time_condition_delete_privilege',
                             'role': 'role_time_condition_delete_privilege', 'permissions': {'时间条件': ['查看', '删除']}},
                            ]

delete_role_data = [('enable', 'assign', '该角色已分配用户，无法删除'), ('enable', 'not assign', '删除角色成功'), ('disable', 'assign', '该角色已分配用户，无法删除'), ('disable', 'not assign', '删除角色成功')]

APPLICATION_CENTER_DICT = {
    "设备管理": '//i[contains(@class, "iconfont icon-device1")]/..',
    "日志管理": '//i[contains(@class, "iconfont icon-diary")]/..',
    "角色管理": '//i[contains(@class, "iconfont icon-character")]/..',
    "人像库管理": '//i[contains(@class, "iconfont icon-renxiangku")]/..',
    "任务管理": '//i[contains(@class, "iconfont icon-task")]/..',
    "用户管理": '//i[contains(@class, "iconfont icon-zu1")]/..',
    "地图管理": '//i[contains(@class, "iconfont icon-map1")]/..',
    "时间条件": '//i[contains(@class, "iconfont icon-timer")]/..',
    "看板": '//i[contains(@class, "iconfont icon-kanban1")]/..',
    "实况": '//i[contains(@class, "iconfont icon-shikuang")]/..',
    "访客": '//i[contains(@class, "iconfont icon-visitor")]/..',
    "考勤": '//i[contains(@class, "iconfont icon-kaoqin")]/..',
    "迎宾": '//i[contains(@class, "iconfont icon-welcome")]/..',
    "记录": '//i[contains(@class, "iconfont icon-record1")]/..',
    "工具:质量分数检测": '//i[contains(@class, "iconfont icon-zu")]/..',
    "工具:1:1人脸验证": '//i[contains(@class, "iconfont icon-facetest")]/..',
    "工具:人脸属性检测": '//i[contains(@class, "iconfont icon-facevalue")]/..'
}

MODULE_OPERATION_PRIVILEGE_ALL = {
    '设备管理': ['查看', '添加', '修改', '删除', '导出'],
    '角色管理': ['查看', '添加', '修改', '删除', '导出'],
    '用户管理': ['查看', '添加', '修改', '删除', '导出'],
    '人像库管理': ['查看', '添加', '修改', '删除', '导出'],
    '访客': ['查看', '添加', '修改', '删除', '导出'],
    '时间条件': ['查看', '添加', '修改', '删除'],
    '日志管理': ['查看', '导出'],
    '考勤': ['查看', '修改', '导出'],
    '记录': ['查看', '修改', '导出'],
    '任务管理': ['查看', '添加', '修改', '删除'],
    '看板': ['查看'],
    '系统信息': ['查看', '修改'],
    '地图管理': ['查看', '添加', '修改', '删除'],
    '工具': ['查看'],
    '迎宾': ['查看'],
    '实况': ['查看'],
}


@pytest.fixture()
def setup_role_user_with_specified_operation(sb, request):
    """ 创建用户使用指定的角色 """
    user_name = request.param['user']
    role_name = request.param['role']
    permissions = request.param['permissions']
    module = str(tuple(permissions.keys())[0])
    sb.sleep(5)
    MenuBar.click_menu_item_by_text(sb, '配置', '角色管理')
    RolePage.add_role_by_name(sb, role_name, permissions)
    RolePage.enable_role_by_name(sb, role_name)
    sb.sleep(2)
    MenuBar.click_menu_item_by_text(sb, '配置', '用户管理')
    user = User(username=user_name, name=user_name, role=role_name)
    UserPage.add_user_by_department_name(sb, user)
    # 新用户第一次登录，修改密码
    first_login_reset_password(sb, user_name)
    #应用中心权限检查
    check_application_center_privilege(sb, permissions)
    # 模块入口
    sb.sleep(2)
    check_module_operation_privilege(sb, permissions, module)
    yield request
    # 测试完成后清理环境：删除用户和角色
    MenuBar.click_personal_info_menu_item(sb, '退出系统')
    sb.sleep(2)
    LoginPage.login(sb, 'shin', '888888')
    MENU_BUTTON = '//div/i[contains(@class, "iconfont icon-config-manage")]'
    sb.wait_for_element_visible(MENU_BUTTON)
    clear_environment(sb, user_name, role_name)
    sb.save_teardown_screenshot()


@pytest.fixture()
def setup_role(sb):
    """ 生成角色"""
    request = {'name': generate_uuid()}
    MenuBar.click_menu_item_by_text(sb, '配置', '角色管理')
    return request


@pytest.fixture()
def setup_multiple_roles(sb):
    MenuBar.click_menu_item_by_text(sb, '配置', '角色管理')
    global roles
    for i in range(20):
        role = generate_uuid()
        roles.append(role)
        RolePage.add_role_by_name(sb, role)
        sb.sleep(1)
    yield roles


@pytest.fixture()
def delete_multiple_roles(sb):
    yield
    MenuBar.click_menu_item_by_text(sb, '配置', '角色管理')
    sb.sleep(2)
    for role in roles:
        RolePage.delete_role_by_name(sb, role)


def generate_uuid():
    uid = str(uuid.uuid4())
    suid = ''.join(uid.split('-'))
    return f'{suid}'


def first_login_reset_password(sb, user_name):
    # 登陆系统创建新用户，并退出当前用户
    MenuBar.click_personal_info_menu_item(sb, '退出系统')
    # 登陆新用户，并修改密码
    LoginPage.login(sb, user_name, '888888')
    PersonInfoPage.reset_password(sb, '888888', 'Guard123', 'Guard123')
    sb.sleep(5)
    # 重新登陆系统，验证密码修改成功
    LoginPage.login(sb, user_name, 'Guard123')
    sb.assert_element_visible('.avatar-name')


def check_application_center_privilege(sb, apps):
    """
        应用中心检查
        参数:
            module: 模块('设备管理','用户管理','角色管理','工具'等)

    """
    APPLICATION_CENTER_BUTTON = '//div/i[contains(@class, "iconfont icon-lujing")]'
    APPLICATION_CENTER_CLOSE_BUTTON = '//div/span[contains(text(), "应用中心")]/../button/i[contains(@class, "el-icon-close")]'
    APPLICATION_CENTER_APPS = ["设备管理", "日志管理", "角色管理", "人像库管理", "任务管理", "用户管理", "地图管理",
                               "时间条件", "工具:1:1人脸验证", "工具:质量分数检测", "工具:人脸属性检测", "看板",
                               "实况", "访客", "考勤", "迎宾", "记录"]
    sb.click(APPLICATION_CENTER_BUTTON, delay=1)
    sb.sleep(2)
    if tuple(apps.keys())[0] not in APPLICATION_CENTER_APPS:
        sb.click(APPLICATION_CENTER_CLOSE_BUTTON, delay=1)
        return
    for app in APPLICATION_CENTER_APPS:
        flag = get_application_center_operation_flag(sb, app)
        assert flag[app] is True if app.split(':')[0] in apps.keys() else flag[app] is False
    sb.click(APPLICATION_CENTER_CLOSE_BUTTON, delay=1)


def clear_environment(sb, user_name, role_name):
    """ 测试结束清理环境：删除指定的角色、用户 """
    sb.sleep(2)
    MenuBar.click_menu_item_by_text(sb, '配置', '用户管理')
    UserPage.delete_user_by_name(sb, user_name)
    MenuBar.click_menu_item_by_text(sb, '配置', '角色管理')
    RolePage.delete_role_by_name(sb, role_name)


def get_device_operation_flag(sb, operation):
    flags = dict()
    if operation == '查看':
        DEVICE_VIEW_PRIVILEGE_BUTTON = '//div/span/i[contains(@class, "icon-view")]'
        sb.sleep(2)
        flags['查看'] = sb.is_element_present(DEVICE_VIEW_PRIVILEGE_BUTTON)
    elif operation == '添加':
        DEVICE_ADD_PRIVILEGE_BUTTON = '//button/span[contains(text(),"添加设备")]'
        sb.sleep(2)
        flags['添加'] = sb.is_element_present(DEVICE_ADD_PRIVILEGE_BUTTON)
    elif operation == '修改':
        DEVICE_EDIT_PRIVILEGE_BUTTON = '//div/span/i[contains(@class, "icon-edit")]'
        flags['修改'] = sb.is_element_present(DEVICE_EDIT_PRIVILEGE_BUTTON)
    elif operation == '删除':
        DEVICE_DELETE_PRIVILEGE_BUTTON = '//div/span/i[contains(@class, "icon-delete")]'
        flags['删除'] = sb.is_element_present(DEVICE_DELETE_PRIVILEGE_BUTTON)
    elif operation == '导出':
        DEVICE_EXPORT_PRIVILEGE_BUTTON = '//button/span[contains(text(),"导出")]'
        flags['导出'] = sb.is_element_present(DEVICE_EXPORT_PRIVILEGE_BUTTON)
    return flags


def get_log_operation_flag(sb, operation):
    flags = dict()
    if operation == '查看':
        LOG_VIEW_PRIVILEGE_BUTTON = '//div[contains(@class, "page el-pagination")]'
        sb.sleep(2)
        flags['查看'] = sb.is_element_present(LOG_VIEW_PRIVILEGE_BUTTON)
    elif operation == '导出':
        LOG_EXPORT_PRIVILEGE_BUTTON = '//button/span[contains(text(),"导出")]'
        flags['导出'] = sb.is_element_present(LOG_EXPORT_PRIVILEGE_BUTTON)
    return flags


def get_role_operation_flag(sb, operation):
    flags = dict()
    if operation == '查看':
        ROLE_VIEW_PRIVILEGE_BUTTON = '//div/span/i[contains(@class, "icon-view")]'
        sb.sleep(2)
        flags['查看'] = sb.is_element_present(ROLE_VIEW_PRIVILEGE_BUTTON)
    elif operation == '添加':
        ROLE_ADD_PRIVILEGE_BUTTON = '//button/span[contains(text(),"添加角色")]'
        sb.sleep(2)
        flags['添加'] = sb.is_element_present(ROLE_ADD_PRIVILEGE_BUTTON)
    elif operation == '修改':
        ROLE_EDIT_PRIVILEGE_BUTTON = '//div/span/i[contains(@class, "icon-edit")]'
        flags['修改'] = sb.is_element_present(ROLE_EDIT_PRIVILEGE_BUTTON)
    elif operation == '删除':
        ROLE_DELETE_PRIVILEGE_BUTTON = '//div/span/i[contains(@class, "icon-delete")]'
        flags['删除'] = sb.is_element_present(ROLE_DELETE_PRIVILEGE_BUTTON)
    elif operation == '导出':
        ROLE_EXPORT_PRIVILEGE_BUTTON = '//button/span[contains(text(),"导出")]'
        flags['导出'] = sb.is_element_present(ROLE_EXPORT_PRIVILEGE_BUTTON)
    return flags


def get_user_operation_flag(sb, operation):
    flags = dict()
    if operation == '查看':
        USER_VIEW_PRIVILEGE_BUTTON = '//div/span/i[contains(@class, "icon-view")]'
        sb.sleep(2)
        flags['查看'] = sb.is_element_present(USER_VIEW_PRIVILEGE_BUTTON)
    elif operation == '添加':
        USER_ADD_PRIVILEGE_BUTTON = '//button/span[contains(text(),"添加用户")]'
        sb.sleep(2)
        flags['添加'] = sb.is_element_present(USER_ADD_PRIVILEGE_BUTTON)
    elif operation == '修改':
        USER_UPDATE_PRIVILEGE_BUTTON = '//div/span/i[contains(@class, "icon-edit")]'
        flags['修改'] = sb.is_element_present(USER_UPDATE_PRIVILEGE_BUTTON)
    elif operation == '删除':
        USER_DELETE_PRIVILEGE_BUTTON = '//div/span/i[contains(@class, "icon-delete")]'
        flags['删除'] = sb.is_element_present(USER_DELETE_PRIVILEGE_BUTTON)
    elif operation == '导出':
        USER_EXPORT_PRIVILEGE_BUTTON = '//button/span[contains(text(),"导出")]'
        flags['导出'] = sb.is_element_present(USER_EXPORT_PRIVILEGE_BUTTON)
    return flags


def get_task_operation_flag(sb, operation):
    flags = dict()
    if operation == '查看':
        TASK_VIEW_PRIVILEGE_BUTTON = '//div/span/i[contains(@class, "icon-view")]'
        sb.sleep(2)
        flags['查看'] = sb.is_element_present(TASK_VIEW_PRIVILEGE_BUTTON)
    elif operation == '添加':
        TASK_ADD_PRIVILEGE_BUTTON = '//button/span[contains(text(),"添加任务")]'
        TASK_ADD_BATCH_PRIVILEGE_BUTTON = '//button/span[contains(text(),"批量添加任务")]/..'
        flag_add = sb.is_element_present(TASK_ADD_PRIVILEGE_BUTTON)
        flag_batch_add = sb.is_element_visible(TASK_ADD_BATCH_PRIVILEGE_BUTTON)
        flags['添加'] = True if flag_add is True and flag_batch_add is True else False
    elif operation == '修改':
        TASK_UPDATE_PRIVILEGE_BUTTON = '//div/span/i[contains(@class, "icon-edit")]'
        TASK_BATCH_OPERATION_PRIVILEGE_BUTTON = '//button/span[contains(text(),"批量操作")]'
        flag_edit = sb.is_element_present(TASK_UPDATE_PRIVILEGE_BUTTON)
        flag_batch_operation = sb.is_element_present(TASK_BATCH_OPERATION_PRIVILEGE_BUTTON)
        flags['修改'] = True if flag_edit is True and flag_batch_operation is True else False
    elif operation == '删除':
        TASK_DELETE_PRIVILEGE_BUTTON = '//div/span/i[contains(@class, "icon-delete")]'
        TASK_BATCH_OPERATION_PRIVILEGE_BUTTON = '//button/span[contains(text(),"批量操作")]'
        flag_delete = sb.is_element_present(TASK_DELETE_PRIVILEGE_BUTTON)
        flag_batch_operation = sb.is_element_present(TASK_BATCH_OPERATION_PRIVILEGE_BUTTON)
        flags['删除'] = True if flag_delete is True and flag_batch_operation is True else False
    return flags


def get_dashboard_operation_flag(sb, operation):
    flags = dict()
    if operation == '查看':
        DASHBOARD_DEVICE_BUTTON = '//div/h2[contains(text(), "设备")]'
        sb.sleep(2)
        flags['查看'] = sb.is_element_present(DASHBOARD_DEVICE_BUTTON)
    return flags


def get_portrait_database_operation_flag(sb, operation):
    flags = dict()
    if operation == '查看':
        PORTRAIT_DATABASE_VIEW_PRIVILEGE_BUTTON = '//div/span/i[contains(@class, "icon-view")]'
        sb.sleep(5)
        flags['查看'] = sb.is_element_present(PORTRAIT_DATABASE_VIEW_PRIVILEGE_BUTTON)
    elif operation == '添加':
        PORTRAIT_DATABASE_ADD_PRIVILEGE_BUTTON = '//button/span[contains(text(),"添加人像")]'
        PORTRAIT_DATABASE_BATCH_OPERATION_PRIVILEGE_BUTTON = '//button/span[contains(text(),"批量上传")]'
        flag_add = sb.is_element_present(PORTRAIT_DATABASE_ADD_PRIVILEGE_BUTTON)
        flag_batch_operantion = sb.is_element_present(PORTRAIT_DATABASE_BATCH_OPERATION_PRIVILEGE_BUTTON)
        flags['添加'] = True if flag_add is True and flag_batch_operantion is True else False
    elif operation == '修改':
        PORTRAIT_DATABASE_UPDATE_PRIVILEGE_BUTTON = '//div/span/i[contains(@class, "icon-edit")]'
        PORTRAIT_DATABASE_BATCH_OPERATION_PRIVILEGE_BUTTON = '//button/span[contains(text(),"批量操作")]'
        flag_edit = sb.is_element_present(PORTRAIT_DATABASE_UPDATE_PRIVILEGE_BUTTON)
        flag_batch_operation = sb.is_element_present(PORTRAIT_DATABASE_BATCH_OPERATION_PRIVILEGE_BUTTON)
        flags['修改'] = True if flag_edit is True and flag_batch_operation is True else False
    elif operation == '删除':
        PORTRAIT_DATABASE_DELETE_PRIVILEGE_BUTTON = '//div/span/i[contains(@class, "icon-delete")]'
        PORTRAIT_DATABASE_BATCH_OPERATION_PRIVILEGE_BUTTON = '//button/span[contains(text(),"批量操作")]'
        flag_delete = sb.is_element_present(PORTRAIT_DATABASE_DELETE_PRIVILEGE_BUTTON)
        flag_batch_operation = sb.is_element_present(PORTRAIT_DATABASE_BATCH_OPERATION_PRIVILEGE_BUTTON)
        flags['删除'] = True if flag_delete is True and flag_batch_operation is True else False
    elif operation == '导出':
        PORTRAIT_DATABASE_EXPORT_PRIVILEGE_BUTTON = '//button/span[contains(text(),"导出人像")]'
        flags['导出'] = sb.is_element_present(PORTRAIT_DATABASE_EXPORT_PRIVILEGE_BUTTON)
    return flags


def get_attendance_operation_flag(sb, operation):
    flags = dict()
    if operation == '查看':
        ATTENDANCE_VIEW_PRIVILEGE = '//a[contains(text(), "考勤应用")]'
        sb.sleep(2)
        flags['查看'] = sb.is_element_present(ATTENDANCE_VIEW_PRIVILEGE)
    elif operation == '修改':
        ATTENDANCE_BUTTON = '//div/button/span[contains(text(), "考勤配置")]'
        EDIT_ATTENDANCE_BUTTON = '//button/span[contains(text(), "编辑考勤配置")]'
        CLOSE_ATTENDANCE_BUTTON = '//div/span[contains(text(), "考勤配置")]/../button/i[contains(@class, "el-icon-close")]'
        sb.click(ATTENDANCE_BUTTON)
        sb.sleep(2)
        flags['修改'] = sb.driver.find_element_by_xpath(EDIT_ATTENDANCE_BUTTON).is_displayed()
        sb.click(CLOSE_ATTENDANCE_BUTTON)
        sb.sleep(2)
    elif operation == '导出':
        ATTENDANCE_EXPORT_BUTTON = '//button/span[contains(text(),"导出")]/..'
        flags['导出'] = sb.find_element(ATTENDANCE_EXPORT_BUTTON).is_enabled()
    return flags


def get_system_info_operation_flag(sb, operation):
    flags = dict()
    if operation == '查看':
        SYSTEM_INFO_PAGE = '//span[contains(text(), "系统信息")]'
        sb.sleep(2)
        flags['查看'] = sb.is_element_present(SYSTEM_INFO_PAGE)
    elif operation == '修改':
        flag_maintenance = SystemInfoPage.is_operation_maintenance_management_button_visible(sb)
        flag_logo = SystemInfoPage.is_change_logo_button_visible(sb)
        flag_title = SystemInfoPage.is_change_title_button_visible(sb)
        flags['修改'] = True if flag_maintenance is False and flag_logo is True and flag_title is True else False
    return flags


def get_map_operation_flag(sb, operation):
    flags = dict()
    if operation == '查看':
        MAP_VIEW_PRIVILEGE = '//div[contains(@title, "Default")]'
        sb.sleep(2)
        flags['查看'] = sb.is_element_present(MAP_VIEW_PRIVILEGE)
    elif operation == '添加':
        MAP_VIEW_PRIVILEGE_BUTTON = '//button/span/span[contains(text(),"添加区域")]'
        flags['添加'] = sb.is_element_present(MAP_VIEW_PRIVILEGE_BUTTON)
    elif operation == '修改':
        MAP_EDIT_PRIVILEGE_BUTTON = '//button/span[contains(text(),"更换地图")]'
        flags['修改'] = sb.is_element_present(MAP_EDIT_PRIVILEGE_BUTTON)
    elif operation == '删除':
        MAP_DELETE_PRIVILEGE_BUTTON = '//button/span[contains(text(),"删除地图")]'
        flags['删除'] = sb.is_element_present(MAP_DELETE_PRIVILEGE_BUTTON)
    return flags


def get_tool_operation_flag(sb):
    FACE_VERIFICATION_MENU = '//li[contains(text(), "1:1人脸验证")]'
    FACE_IMAGE_QUALITY_EVALUATION_MENU = '//li[contains(text(), "质量分数检测")]'
    FACE_ATTRIBUTE_DETECTION_MENU = '//li[contains(text(), "人脸属性检测")]'
    flag_face_verification = sb.is_element_present(FACE_VERIFICATION_MENU)
    flag_face_image_quality_evaluation = sb.is_element_present(FACE_IMAGE_QUALITY_EVALUATION_MENU)
    flag_face_attribute_detection = sb.is_element_present(FACE_ATTRIBUTE_DETECTION_MENU)
    flags = True if flag_face_verification is True and flag_face_image_quality_evaluation is True and flag_face_attribute_detection is True else False
    return flags


def get_reception_operation_flag(sb, operation):
    flags = dict()
    if operation == '查看':
        RECEPTION_VIEW_PRIVILEGE = '//div/ul[contains(@class, "el-pager")]'
        sb.sleep(2)
        flags['查看'] = sb.is_element_present(RECEPTION_VIEW_PRIVILEGE)
    return flags


def get_live_operation_flag(sb, operation):
    flags = dict()
    if operation == '查看':
        LIVE_PAGE_VIEW_PRIVILEGE = '//div[contains(text(), "设备类型")]'
        sb.sleep(2)
        flags['查看'] = sb.is_element_present(LIVE_PAGE_VIEW_PRIVILEGE)
    return flags


def get_visitor_operation_flag(sb, operation):
    flags = dict()
    if operation == '查看':
        # VISITOR_PAGE_VIEW_PRIVILEGE = '//div/i[contains(@class, "icon-eye")]'
        VISITOR_PAGE_VIEW_PRIVILEGE = '//div/ul[contains(@class, "el-pager")]'
        sb.sleep(2)
        flags['查看'] = sb.is_element_present(VISITOR_PAGE_VIEW_PRIVILEGE)
    elif operation == '添加':
        VISITOR_ADD_PRIVILEGE_BUTTON = '//button/span[contains(text(),"新建预约")]'
        flags['添加'] = sb.is_element_present(VISITOR_ADD_PRIVILEGE_BUTTON)
    elif operation == '修改':
        VISITOR_EDIT_PRIVILEGE_BUTTON = '//div/button[contains(@class, "el-button--mini")]'
        flags['修改'] = sb.is_element_present(VISITOR_EDIT_PRIVILEGE_BUTTON)
    elif operation == '删除':
        VISITOR_BATCH_OPERATION_PRIVILEGE_BUTTON = '//button/span[contains(text(),"批量操作")]'
        flags['删除'] = sb.driver.find_element_by_xpath(VISITOR_BATCH_OPERATION_PRIVILEGE_BUTTON).is_displayed()
    elif operation == '导出':
        VISITOR_EXPORT_PRIVILEGE_BUTTON = '//button/span[contains(text(),"导出")]'
        flags['导出'] = sb.is_element_present(VISITOR_EXPORT_PRIVILEGE_BUTTON)
    return flags


def get_time_condition_operation_flag(sb, operation):
    flags = dict()
    TIME_CONDITION_VIEW = '//div[text()="时间条件设置"]'
    TIME_CONDITION_HOLIDAY_BUTTON = '//button/span[contains(text(),"未定义假期")]/..'
    TIME_CONDITION_WORK_DAY_BUTTON = '//button/span[contains(text(),"未定义工作日")]/..'
    TIME_CONDITION_NAME_ADD_BUTTON = '//span[contains(text(), "时间条件名称")]/i[contains(@class, "el-icon-plus timezone-add-icon")]'
    TIME_CONDITION_TIMEZONE_ADD_BUTTON = '//span[contains(text(), "时间段")]/i[contains(@class, "el-icon-plus timezone-add-icon")]'
    TIME_CONDITION_EDIT_BUTTON = '//div/span/i[contains(@class, "icon-edit")]'
    TIME_CONDITION_DELETE_BUTTON = '//div/span/i[contains(@class, "icon-delete")]'
    sb.sleep(2)
    flag_time_condition_view = sb.find_element(TIME_CONDITION_VIEW).is_displayed()
    flag_time_condition_holiday = sb.find_element(TIME_CONDITION_HOLIDAY_BUTTON).is_enabled()
    flag_time_condition_work_day = sb.find_element(TIME_CONDITION_WORK_DAY_BUTTON).is_enabled()
    flag_time_condition_name_add = sb.is_element_present(TIME_CONDITION_NAME_ADD_BUTTON)
    flag_time_condition_timezone_add = sb.is_element_present(TIME_CONDITION_TIMEZONE_ADD_BUTTON)
    flag_time_condition_edit = sb.is_element_present(TIME_CONDITION_EDIT_BUTTON)
    flag_time_condition_delete_button = sb.is_element_present(TIME_CONDITION_DELETE_BUTTON)
    if operation == '查看':
        flags['查看'] = True if flag_time_condition_view is True else False
    if operation == '添加':
        if flag_time_condition_holiday is True and flag_time_condition_work_day is True and \
                flag_time_condition_name_add is True and flag_time_condition_timezone_add is True \
                and flag_time_condition_edit is False and flag_time_condition_delete_button is False:
            flags['添加'] = True
        else:
            flags['添加'] = False
    if operation == '修改':
        if flag_time_condition_holiday is False and flag_time_condition_work_day is False and \
                flag_time_condition_name_add is False and flag_time_condition_timezone_add is False \
                and flag_time_condition_edit is True and flag_time_condition_delete_button is False:
            flags['修改'] = True
        else:
            flags['修改'] = False
    if operation == '删除':
        if flag_time_condition_holiday is False and flag_time_condition_work_day is False and \
                flag_time_condition_name_add is False and flag_time_condition_timezone_add is False \
                and flag_time_condition_edit is False and flag_time_condition_delete_button is True:
            flags['删除'] = True
        else:
            flags['删除'] = False
    return flags


def get_record_operation_flag(sb, operation):
    flags = dict()
    if operation == '查看':
        RECORD_SEARCH_BUTTON = '//span[contains(text(), "筛选")]'
        RECORD_PICTURE_SEARCH_BUTTON = '//div/i[contains(@class, "icon-PictureSearch")]'
        sb.sleep(2)
        flag_record_search = sb.is_element_present(RECORD_SEARCH_BUTTON)
        flag_record_picture_search = sb.is_element_present(RECORD_PICTURE_SEARCH_BUTTON)
        flags['查看'] = True if flag_record_search is True and flag_record_picture_search is True else False
    #需要在新建用户的时候添加设备（待实现），才能在记录中显示比中/未比中。
    elif operation == '修改':
        RECORD_MATCH_BUTTON = '//div/button/span[contains(text(), "比中")]'
        RECORD_UNMATCH_BUTTON = '//div/button/span[contains(text(), "未比中")]'
        flag_record_match = sb.is_element_present(RECORD_MATCH_BUTTON)
        flag_record_unmatch = sb.is_element_present(RECORD_UNMATCH_BUTTON)
        flags['修改'] = True if flag_record_match is True and flag_record_unmatch is True else False
    elif operation == '导出':
        RECORD_EXPORT_BUTTON = '//button/span[contains(text(),"批量导出")]'
        flag_export = sb.is_element_present(RECORD_EXPORT_BUTTON)
        flags['导出'] = flag_export
    return flags


CALL_FUNCTION_MAP = {
    '设备管理': get_device_operation_flag,
    '角色管理': get_role_operation_flag,
    '用户管理': get_user_operation_flag,
    '日志管理': get_log_operation_flag,
    '考勤': get_attendance_operation_flag,
    '人像库管理': get_portrait_database_operation_flag,
    '任务管理': get_task_operation_flag,
    '看板': get_dashboard_operation_flag,
    '系统信息': get_system_info_operation_flag,
    '地图管理': get_map_operation_flag,
    '时间条件': get_time_condition_operation_flag,
    '工具': get_tool_operation_flag,
    '迎宾': get_reception_operation_flag,
    '实况': get_live_operation_flag,
    '访客': get_visitor_operation_flag,
    '记录': get_record_operation_flag,
}


def check_module_operation_privilege(sb, operations, module):
    if module == '系统信息':
        MenuBar.click_personal_info_menu_item(sb, '系统信息')
        sb.sleep(2)
    elif module == '':
        MenuBar.click_personal_info_menu_item(sb, '个人信息')
        sb.sleep(2)
        RESET_PASSWORD_XBUTTON = '//button/span[contains(text(),"修改密码")]'
        flag = sb.is_element_present(RESET_PASSWORD_XBUTTON)
        assert flag is True
        return
    elif module == '工具':
        flag = CALL_FUNCTION_MAP[module](sb)
        assert flag is True
        return
    else:
        MENU_ITEM_XLINK = f'//em[text()="{module}"]'
        BasePage.hover_on_element_by_xpath(sb, MENU_ITEM_XLINK)
        sb.sleep(2)
        sb.click(MENU_ITEM_XLINK, by=By.XPATH)
    module_operation = MODULE_OPERATION_PRIVILEGE_ALL[module]
    for operation in module_operation:
        flag = CALL_FUNCTION_MAP[module](sb, operation)
        logging.info(flag)
        assert flag[operation] is True if operation in operations[module] else flag[operation] is False


def get_application_center_operation_flag(sb, app):
    flags = dict()
    for key, value in APPLICATION_CENTER_DICT.items():
        if key == app:
            flag = sb.find_element(value).is_enabled()
            logging.info({key: flag})
            flags[key] = flag
    return flags


#8899 【角色管理】【主流程】角色-设备管理权限
@pytest.mark.positive
@pytest.mark.parametrize("setup_role_user_with_specified_operation", device_test_data, indirect=True)
def test_create_role_with_device_management_privilege(sb, login, setup_role_user_with_specified_operation):
    setup_role_user_with_specified_operation


#8904【角色管理】【主流程】角色-日志管理权限
@pytest.mark.positive
@pytest.mark.parametrize("setup_role_user_with_specified_operation", log_test_data, indirect=True)
def test_create_role_with_log_management_privilege(sb, login, setup_role_user_with_specified_operation):
    setup_role_user_with_specified_operation


#8902 【角色管理】【主流程】角色-角色管理权限
@pytest.mark.positive
@pytest.mark.parametrize("setup_role_user_with_specified_operation", role_test_data, indirect=True)
def test_create_role_with_role_management_privilege(sb, login, setup_role_user_with_specified_operation):
    setup_role_user_with_specified_operation


#8906【角色管理】【主流程】角色-考勤应用权限
@pytest.mark.positive
@pytest.mark.parametrize("setup_role_user_with_specified_operation", attendance_test_data, indirect=True)
def test_create_role_with_attendance_privilege(sb, login, setup_role_user_with_specified_operation):
    setup_role_user_with_specified_operation


#8903【角色管理】【主流程】角色-用户权限
@pytest.mark.positive
@pytest.mark.parametrize("setup_role_user_with_specified_operation", user_test_data, indirect=True)
def test_create_role_with_user_management_privilege(sb, login, setup_role_user_with_specified_operation):
    setup_role_user_with_specified_operation


#8900 【角色管理】【主流程】角色-人像库管理权限
@pytest.mark.positive
@pytest.mark.parametrize("setup_role_user_with_specified_operation", portrait_database_test_data, indirect=True)
def test_create_role_with_portrait_database_management_privilege(sb, login, setup_role_user_with_specified_operation):
    setup_role_user_with_specified_operation


#8901 【角色管理】【主流程】角色-规则管理权限
@pytest.mark.positive
@pytest.mark.parametrize("setup_role_user_with_specified_operation", task_test_data, indirect=True)
def test_create_role_with_task_management_privilege(sb, login, setup_role_user_with_specified_operation):
    setup_role_user_with_specified_operation


#8909【角色管理】【主流程】角色-看板应用权限
@pytest.mark.positive
@pytest.mark.parametrize("setup_role_user_with_specified_operation", dashboard_test_data, indirect=True)
def test_create_role_with_dashboard_management_privilege(sb, login, setup_role_user_with_specified_operation):
    setup_role_user_with_specified_operation


#8895【角色管理】【主流程】角色-系统信息权限
@pytest.mark.positive
@pytest.mark.parametrize("setup_role_user_with_specified_operation", system_info_test_data, indirect=True)
def test_create_role_with_system_info_privilege(sb, login, setup_role_user_with_specified_operation):
    setup_role_user_with_specified_operation


#8898【角色管理】【主流程】角色-地图管理权限
@pytest.mark.positive
@pytest.mark.parametrize("setup_role_user_with_specified_operation", map_management_test_data, indirect=True)
def test_create_role_with_map_management_privilege(sb, login, setup_role_user_with_specified_operation):
    setup_role_user_with_specified_operation


#8894 【角色管理】【主流程】角色-默认权限
@pytest.mark.positive
@pytest.mark.parametrize("setup_role_user_with_specified_operation", default_privilege_test_data, indirect=True)
def test_create_role_with_default_privilege(sb, login, setup_role_user_with_specified_operation):
    setup_role_user_with_specified_operation


#3620 【角色管理】【主流程】角色-工具应用权限
@pytest.mark.positive
@pytest.mark.parametrize("setup_role_user_with_specified_operation", tool_privilege_test_data, indirect=True)
def test_create_role_with_tool_privilege(sb, login, setup_role_user_with_specified_operation):
    setup_role_user_with_specified_operation


#8908 【角色管理】【主流程】角色-迎宾应用权限
@pytest.mark.positive
@pytest.mark.parametrize("setup_role_user_with_specified_operation", reception_privilege_test_data, indirect=True)
def test_create_role_with_reception_privilege(sb, login, setup_role_user_with_specified_operation):
    setup_role_user_with_specified_operation


#8896【角色管理】【主流程】角色-实况应用权限
@pytest.mark.positive
@pytest.mark.parametrize("setup_role_user_with_specified_operation", live_privilege_test_data, indirect=True)
def test_create_role_with_live_privilege(sb, login, setup_role_user_with_specified_operation):
    setup_role_user_with_specified_operation


#8905 【角色管理】【主流程】角色-访客应用权限
@pytest.mark.positive
@pytest.mark.parametrize("setup_role_user_with_specified_operation", visitor_test_data, indirect=True)
def test_create_role_with_visitor_privilege(sb, login, setup_role_user_with_specified_operation):
    setup_role_user_with_specified_operation


#8897 【角色管理】【主流程】角色-记录应用权限
@pytest.mark.positive
@pytest.mark.parametrize("setup_role_user_with_specified_operation", record_test_data, indirect=True)
def test_create_role_with_record_privilege(sb, login, setup_role_user_with_specified_operation):
    setup_role_user_with_specified_operation


#8907 【角色管理】【主流程】角色-时间条件权限
@pytest.mark.positive
@pytest.mark.parametrize("setup_role_user_with_specified_operation", time_condition_test_data, indirect=True)
def test_create_role_with_time_condition_privilege(sb, login, setup_role_user_with_specified_operation):
    setup_role_user_with_specified_operation


#4473 【角色管理】【主流程】导出-压缩包包括Excel和html两个文件（文件名校验）
@pytest.mark.positive
def test_role_export_rule_check(sb, login):
    MenuBar.click_menu_item_by_text(sb, '配置', '角色管理')
    sb.sleep(2)
    RolePage.export_role_data(sb, 1, 2)


#4418 【角色管理】【主流程】角色权限 - 添加和查看权限级联关系
@pytest.mark.positive
def test_role_checkbox_relevance(sb, login):
    sb.sleep(2)
    MenuBar.click_menu_item_by_text(sb, '配置', '角色管理')
    sb.sleep(2)
    RolePage.click_add_role_button(sb)
    sb.sleep(2)
    for k, v in MODULE_OPERATION_PRIVILEGE_ALL.items():
        RolePage.checkbox_relevance_check(sb, dict({k: v}))


#4477 【角色管理】【格式】导出-html文件内容标题
@pytest.mark.positive
def test_role_export_file_title(sb, login):
    sb.sleep(2)
    MenuBar.click_menu_item_by_text(sb, '配置', '角色管理')
    sb.sleep(2)
    RolePage.export_role_data(sb, 1, 1)
    message_page = '//div/a/i[contains(@class, "icon-news")]'
    sb.click(message_page, delay=1)
    sb.sleep(2)
    assert MessagePage.check_download_file_format(sb, "角色管理", 1) is True


#4439,3622 【角色管理】【异常】添加角色名必填校验
@pytest.mark.negative
def test_input_role_name_check(sb, login):
    sb.sleep(2)
    MenuBar.click_menu_item_by_text(sb, '配置', '角色管理')
    sb.sleep(2)
    RolePage.add_role_by_name(sb, '', {'设备管理': ['查看', '添加', '修改', '删除', '导出']})
    sb.sleep(1)
    ALERT_MESSAGE = '//div[contains(text(), "请输入角色名称")]'
    assert sb.driver.find_element_by_xpath(ALERT_MESSAGE).is_displayed() is True


#3616&3625【角色管理】【主流程】角色权限-模块结构\查看角色
@pytest.mark.positive
def test_role_view_operation_check(sb, login, setup_role_name_and_delete_role):
    sb.sleep(2)
    RolePage.add_role_by_name(sb, setup_role_name_and_delete_role['name'], {'设备管理': ['查看', '添加']})
    RolePage.enable_role_by_name(sb, setup_role_name_and_delete_role['name'])
    flags = RolePage.enabled_operation_check(sb, setup_role_name_and_delete_role['name'], {'设备管理': ['查看', '添加']})
    for module, flag in flags.items():
        assert flag is True if module in ['查看', '添加', '修改', '删除', '导出'] else flag is False
    sb.driver.refresh()
    sb.sleep(2)


#3624【角色管理】【主流程】角色权限-编辑角色
@pytest.mark.positive
def test_role_edit_operation_check(sb, login, setup_role_name_and_delete_role):
    sb.sleep(2)
    RolePage.add_role_by_name(sb, setup_role_name_and_delete_role['name'], {'设备管理': ['查看']})
    RolePage.enable_role_by_name(sb, setup_role_name_and_delete_role['name'])
    RolePage.edit_role_by_name(sb, setup_role_name_and_delete_role['name'], {'设备管理': ['导出']})
    flags = RolePage.enabled_operation_check(sb, setup_role_name_and_delete_role['name'], {'设备管理': ['查看', '导出']})
    for module, flag in flags.items():
        assert flag is True if module in ['查看', '添加', '修改', '删除', '导出'] else flag is False
    sb.driver.refresh()
    sb.sleep(2)


#4432 【角色管理】【异常】角色导出-数字超过最大数字
@pytest.mark.negative
def test_export_role_exceed_max(sb, login):
    sb.sleep(2)
    MenuBar.click_menu_item_by_text(sb, '配置', '角色管理')
    max_num = RolePage.get_current_role_num(sb)
    assert RolePage.export_role_exceed_max(sb, 1, max_num+1) is True


#4449 【角色管理】【异常】角色导出-负数字
@pytest.mark.negative
def test_export_role_with_negative_num(sb, login):
    sb.sleep(2)
    MenuBar.click_menu_item_by_text(sb, '配置', '角色管理')
    assert RolePage.export_role_data(sb, -1, -2) is not False


#4445 【角色管理】【异常】搜索不存在角色
@pytest.mark.negative
def test_search_not_exist_role(sb, login):
    sb.sleep(2)
    MenuBar.click_menu_item_by_text(sb, '配置', '角色管理')
    sb.sleep(2)
    assert RolePage.search_role_by_name(sb, generate_uuid(), exist=False) is True


#4425,4430 【角色管理】【主流程】禁用已激活角色,【角色管理】【主流程】激活已存在禁用状态的角色
@pytest.mark.positive
def test_disable_active_role(sb, login, setup_role_name_and_delete_role):
    sb.sleep(2)
    RolePage.add_role_by_name(sb, setup_role_name_and_delete_role['name'], {'设备管理': ['查看']})
    RolePage.enable_role_by_name(sb, setup_role_name_and_delete_role['name'])
    flag = RolePage.enable_role_by_name(sb, setup_role_name_and_delete_role['name'], disable=True)
    assert flag is True


#4443 【角色管理】【异常】重命名角色名称为已经存在角色列表内的角色名
@pytest.mark.negative
def test_rename_exist_role(sb, login, setup_role_name_and_delete_role):
    sb.sleep(2)
    RolePage.add_role_by_name(sb, setup_role_name_and_delete_role['name'], {'设备管理': ['查看']})
    sb.sleep(2)
    RolePage.rename_role_name(sb, setup_role_name_and_delete_role['name'], 'Administrator')
    RolePage.assert_alert_message(sb, "该名称已存在")
    sb.driver.refresh()


#4450 【角色管理】【异常】角色导出-开始大于结束
@pytest.mark.negative
def test_export_role_start_larger_than_end(sb, login):
    sb.sleep(2)
    MenuBar.click_menu_item_by_text(sb, '配置', '角色管理')
    error_message = '//div/span[text()="导出结束数量应不小于开始数量"]'
    RolePage.export_role_data(sb, 3, 1)
    assert sb.assert_element_present(error_message) is True


#4447 【角色管理】【主功能】禁用已关联用户的角色
@pytest.mark.positive
def test_disable_active_role(sb, login):
    sb.sleep(2)
    MenuBar.click_menu_item_by_text(sb, '配置', '角色管理')
    RolePage.enable_role_by_name(sb, 'Administrator', disable=True)
    RolePage.assert_alert_message(sb, "禁用用户失败")


#4426 【角色管理】【异常】添加存在角色
@pytest.mark.negative
def test_disable_active_role(sb, login):
    sb.sleep(2)
    MenuBar.click_menu_item_by_text(sb, '配置', '角色管理')
    RolePage.add_role_by_name(sb, 'Administrator', {'设备管理': ['查看']})
    RolePage.assert_alert_message(sb, "该名称已存在")


#4438【角色管理】【异常】添加为空角色
@pytest.mark.negative
def test_input_role_name_with_blank(sb, login):
    sb.sleep(2)
    MenuBar.click_menu_item_by_text(sb, '配置', '角色管理')
    RolePage.add_role_by_name(sb, '', {'设备管理': ['查看']})
    error_message = '//div[contains(text(),"请输入角色名称")]'
    assert sb.assert_element_present(error_message) is True


#4424 【角色管理】【主流程】搜索存在角色
@pytest.mark.positive
def test_disable_active_role(sb, login, setup_role_name_and_delete_role):
    sb.sleep(2)
    RolePage.add_role_by_name(sb, setup_role_name_and_delete_role['name'], {'设备管理': ['查看']})
    assert RolePage.search_role_by_name(sb, setup_role_name_and_delete_role['name']) is True


#4442 【角色管理】【主功能】重命名角色
@pytest.mark.positive
def test_rename_role(sb, login, setup_role_name_and_delete_role):
    sb.sleep(2)
    RolePage.add_role_by_name(sb, setup_role_name_and_delete_role['name'], {'权限': ['全选']})
    RolePage.rename_role_name(sb, setup_role_name_and_delete_role['name'], 'role_rename_1234')
    assert RolePage.search_role_by_name(sb, 'role_rename_1234') is True
    RolePage.rename_role_name(sb, 'role_rename_1234', setup_role_name_and_delete_role['name'])


#3626 【角色管理】【主流程】角色权限-删除角色
@pytest.mark.positive
@pytest.mark.parametrize('role_status, user_status, result', delete_role_data)
def test_delete_role(sb, login, setup_role, role_status, user_status, result):
    role_name = setup_role['name']
    sb.sleep(2)
    RolePage.add_role_by_name(sb, role_name, {'权限': ['全选']})
    if role_status == 'enable':
        RolePage.enable_role_by_name(sb, role_name)
    sb.sleep(2)
    if user_status == 'assign':
        MenuBar.click_menu_item_by_text(sb, '配置', '用户管理')
        user = User(username=role_name, name=role_name, role=role_name)
        UserPage.add_user_by_department_name(sb, user)
        sb.sleep(2)
    MenuBar.click_menu_item_by_text(sb, '配置', '角色管理')
    RolePage.delete_role_by_name(sb, role_name)
    RolePage.assert_alert_message(sb, result)
    sb.driver.refresh()
    if user_status == 'assign':
        clear_environment(sb, role_name, role_name)


#4484 【角色管理】【界面】翻页-前往指定页
@pytest.mark.positive
def test_role_jump_to_specific_page(sb, login, setup_multiple_roles):
    RolePage.jump_to_specific_page(sb, 2)
    assert RolePage.check_current_page(sb, 2) is True


#4483 【角色管理】【界面】翻页-上一页
@pytest.mark.positive
def test_role_jump_to_previous_page(sb, login):
    MenuBar.click_menu_item_by_text(sb, '配置', '角色管理')
    sb.sleep(1)
    RolePage.jump_to_specific_page(sb, 2)
    RolePage.jump_to_previous_page(sb)
    assert RolePage.check_current_page(sb, 1) is True


#4482 【角色管理】【界面】翻页-下一页
@pytest.mark.positive
def test_role_jump_to_next_page(sb, login, delete_multiple_roles):
    MenuBar.click_menu_item_by_text(sb, '配置', '角色管理')
    sb.sleep(1)
    RolePage.jump_to_specific_page(sb, 2)
    RolePage.jump_to_next_page(sb)
    assert RolePage.check_current_page(sb, 3) is True


#4440 【角色管理】【异常】添加40字符以上角色
@pytest.mark.negative
@pytest.mark.parametrize('name', [generate_uuid()*2])
def test_add_role_exceed_max_char(sb, login, name):
    MenuBar.click_menu_item_by_text(sb, '配置', '角色管理')
    sb.sleep(2)
    RolePage.add_role_by_name(sb, name, {'权限': ['全选']})
    RolePage.assert_alert_message(sb, "添加角色成功")
    assert RolePage.search_role_by_name(sb, name[0:40]) is True
    sb.sleep(2)
    RolePage.delete_role_by_name(sb, name[0:40])


#4448 【角色管理】【异常】角色导出-空数字
@pytest.mark.negative
@pytest.mark.parametrize('export_start, export_end', [('', '1'), ('1', ''), ('', '')])
def test_export_role_with_null_input(sb, login, export_start, export_end):
    MenuBar.click_menu_item_by_text(sb, '配置', '角色管理')
    sb.sleep(2)
    assert RolePage.export_role_data(sb, export_start, export_end) is False
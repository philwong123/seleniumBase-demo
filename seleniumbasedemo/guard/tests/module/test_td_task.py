#!/usr/bin/env python3

import pytest

from guard.tests.base_test_case import BaseTestCase
from guard.pages.components.menubar import MenuBar
from guard.pages.device import DevicePage
from guard.pages.map import MapPage
from guard.pages.portrait import PortraitPage
from guard.pages.task import TaskPage
from guard.pages.classes.device.rtsp import RTSP
from guard.pages.classes.device.frontend import Frontend
from guard.pages.classes.task.face_access_control_task import FaceAccessControlTask
from guard.pages.classes.task.face_alert_deployment_task import FaceAlertDeploymentTask
from guard.pages.classes.task.pedestrian_crossing_boundary_detection_task import PedestrianCrossingBoundaryDetectionTask
from guard.pages.classes.task.pedestrian_area_entry_detection_task import PedestrianAreaEntryDetectionTask
from guard.pages.classes.task.vehicle_illegally_parking_detection_task import VehicleIllegallyParkingDetectionTask

@pytest.mark.yxl
def test_add_face_alert_deployment_task(
        sb, login, setup_face_alert_deployment_task_name_and_delete_task):
    """添加基本的监控任务"""
    task = FaceAlertDeploymentTask(setup_face_alert_deployment_task_name_and_delete_task['name'],
                                 setup_face_alert_deployment_task_name_and_delete_task['name'],
                                 portraits=[setup_face_alert_deployment_task_name_and_delete_task['name']])
    TaskPage.add_face_alert_deployment_task(sb, task)

@pytest.mark.yxl
def test_add_face_alert_deployment_task_multi_portraits(
        sb, login, setup_face_alert_deployment_task_name_with_mul_portrait_and_delete_task):
    """添加多个人像库的监控任务"""
    task = FaceAlertDeploymentTask(setup_face_alert_deployment_task_name_with_mul_portrait_and_delete_task['name'],
                                 setup_face_alert_deployment_task_name_with_mul_portrait_and_delete_task['name'],
                                 portraits=[
                                     setup_face_alert_deployment_task_name_with_mul_portrait_and_delete_task['name'],
                                     setup_face_alert_deployment_task_name_with_mul_portrait_and_delete_task['name2']
                                 ])
    TaskPage.add_face_alert_deployment_task(sb, task)

@pytest.mark.yxl
def test_add_face_alert_deployment_task_duplicate_task_name(
        sb, login, setup_face_alert_deployment_task_name_and_delete_task):
    """测试任务名重复"""
    # 先用初始值创建一个任务
    task = FaceAccessControlTask(setup_face_alert_deployment_task_name_and_delete_task['name'],
                                 setup_face_alert_deployment_task_name_and_delete_task['name'],
                                 portraits=[
                                     setup_face_alert_deployment_task_name_and_delete_task['name']
                                 ])
    TaskPage.add_face_alert_deployment_task(sb, task)
    # 再添加一个设备
    MenuBar.click_menu_item_by_text(sb, '配置', '设备管理')
    rtsp_device = RTSP(
        setup_face_alert_deployment_task_name_and_delete_task['name'] + 'dup',
        setup_face_alert_deployment_task_name_and_delete_task['name'] + 'dup',
        setup_face_alert_deployment_task_name_and_delete_task['name'],
        setup_face_alert_deployment_task_name_and_delete_task['name'],
        'rtsp://confidence.119:6554/SchoolAnniversary.264')
    DevicePage.add_device_by_type(
        sb, rtsp_device, '网络摄像机')

    # 用新的设备和原先的任务名称、人像库作为添加规则的准备数据
    task2 = FaceAccessControlTask(setup_face_alert_deployment_task_name_and_delete_task['name'],
                                 setup_face_alert_deployment_task_name_and_delete_task['name'] + 'dup',
                                 portraits=[
                                     setup_face_alert_deployment_task_name_and_delete_task['name']
                                 ])
    # 定位到setup中的任务菜单
    MenuBar.click_menu_item_by_text(sb, '配置', '任务管理')
    # 再次添加规则
    TaskPage.add_face_alert_deployment_task(sb, task2)
    # 校验"任务名已存在"
    TaskPage.assert_alert_message(sb, '任务名已存在')
    # 关闭新增任务窗口
    TaskPage.click_task_cancel_button(sb)

@pytest.mark.yxl
def test_add_face_alert_deployment_task_threshold(sb, login, setup_face_alert_deployment_task_name_and_delete_task):
    """添加指定阈值的监控任务,并校验任务详情中的阈值是否更新"""
    task = FaceAccessControlTask(setup_face_alert_deployment_task_name_and_delete_task['name'],
                                 setup_face_alert_deployment_task_name_and_delete_task['name'],
                                 portraits=[
                                     setup_face_alert_deployment_task_name_and_delete_task['name']
                                 ],
                                 threshold='70.0')
    TaskPage.add_face_alert_deployment_task(sb, task)
    TaskPage.detail_task_by_name(sb, task.task_name)
    TaskPage.assert_element_text(sb,'//label[text()="阈值"]/parent::*//div', '70.0%')
    TaskPage.close_task_detail_popup(sb)
#
# @pytest.mark.parametrize("threshold_input, expected", [('65.0','65.0%'),('70.0','70.0%'),('75.0','75.0%'),('80.0','80.0%'),('85.0','85.0%'),('90.0','90.0%'),('95.0','95.0%')])
# @pytest.mark.yxl
# # ("30.0", '30.0%'), ('35.0', '35.0%'), ('40.0', '40.0%'),('45.0','45.0%'),('50.0','50.0%'),('55.0','55.0%'),('60.0','60.0%'),
# def test_add_face_access_control_task_threshold(sb, login, threshold_input, expected, setup_face_access_control_task_name_and_delete_task):
#     """添加指定阈值的前端设备任务,并校验任务详情中的阈值是否更新"""
#     task = FaceAccessControlTask(setup_face_access_control_task_name_and_delete_task['name'], setup_face_access_control_task_name_and_delete_task['name'], portraits=[
#         setup_face_access_control_task_name_and_delete_task['name']], threshold=threshold_input)
#     TaskPage.add_face_access_control_task(sb, task)
#     TaskPage.detail_task_by_name(sb, task.task_name)
#     TaskPage.assert_element_text(sb,'//label[text()="阈值"]/parent::*//span', expected)
#     TaskPage.close_task_detail_popup(sb)
#
@pytest.mark.yxl
def test_add_face_alert_deployment_task_then_disable(sb, login, setup_face_alert_deployment_task_name_and_delete_task):
    """添加监控任务后禁用"""
    task = FaceAccessControlTask(setup_face_alert_deployment_task_name_and_delete_task['name'],
                                 setup_face_alert_deployment_task_name_and_delete_task['name'],
                                 portraits=[
                                     setup_face_alert_deployment_task_name_and_delete_task['name']
                                 ])
    TaskPage.add_face_alert_deployment_task(sb, task)
    TaskPage.switch_task_status_by_name(sb, task.task_name)
#
@pytest.mark.yxl
def test_add_face_alert_deployment_task_then_disable_then_enable(sb, login, setup_face_alert_deployment_task_name_and_delete_task):
    """添加监控任务后禁用再启用"""
    task = FaceAccessControlTask(setup_face_alert_deployment_task_name_and_delete_task['name'],
                                 setup_face_alert_deployment_task_name_and_delete_task['name'],
                                 portraits=[
                                     setup_face_alert_deployment_task_name_and_delete_task['name']
                                 ])
    TaskPage.add_face_alert_deployment_task(sb, task)
    TaskPage.switch_task_status_by_name(sb, task.task_name)
    TaskPage.switch_task_status_by_name(sb, task.task_name)
#
@pytest.mark.yxl
def test_add_face_alert_deployment_task_then_update_taskName(sb, login, setup_face_alert_deployment_task_name_and_delete_task):
    """更新监控任务的任务名称，
    1. 校验任务列表中名是否更新
    2. 校验任务详情中任务名是否更新
    """
    task = FaceAccessControlTask(setup_face_alert_deployment_task_name_and_delete_task['name'],
                                 setup_face_alert_deployment_task_name_and_delete_task['name'],
                                 portraits=[
                                     setup_face_alert_deployment_task_name_and_delete_task['name']
                                 ])
    TaskPage.add_face_alert_deployment_task(sb, task)
    newName = f"{setup_face_alert_deployment_task_name_and_delete_task['name']}upd"
    TaskPage.edit_task_name(sb, setup_face_alert_deployment_task_name_and_delete_task['name'], newName)
    TaskPage.search_task_by_name(sb, newName)
    TaskPage.assert_element_text(sb,'//*[@id="app"]/div/div[1]/section/div/div[2]/div[2]/div[1]/div[1]/div[3]/table/tbody/tr[1]/td[2]/div',newName)
    TaskPage.detail_task_by_name(sb, newName)
    TaskPage.assert_element_text(sb, '//label[text()="任务名称"]/parent::*//div', newName)
    TaskPage.close_task_detail_popup(sb)

@pytest.mark.parametrize("attribute_input", [['入口'], ['出口'], ['第三方对接']])
@pytest.mark.yxl
def test_add_face_alert_deployment_task_attributes(sb, login, attribute_input, setup_face_alert_deployment_task_name_and_delete_task):
    """添加入口|出口|第三方对接|属性的监控任务"""
    task = FaceAccessControlTask(setup_face_alert_deployment_task_name_and_delete_task['name'],
                                 setup_face_alert_deployment_task_name_and_delete_task['name'],
                                 portraits=[
                                     setup_face_alert_deployment_task_name_and_delete_task['name']
                                 ],
                                 attributes=attribute_input)
    TaskPage.add_face_alert_deployment_task(sb, task)
    TaskPage.detail_task_by_name(sb, setup_face_alert_deployment_task_name_and_delete_task['name'])
    TaskPage.assert_element_text(sb, '//label[text()="特殊属性"]/parent::*//div', attribute_input[0])
    TaskPage.close_task_detail_popup(sb)
import os
import time

import pytest

from seleniumbase import BaseCase
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


class SmokeReceptionTest(BaseCase):
    # Smoke-人像库-白名单名称
    SMOKE_PORTRAIT_DATABASE_WHITELIST_NAME = 'smoke-reception-whitelist'
    # Smoke-地图-父楼层名称
    SMOKE_MAP_PARENT_FLOOR_NAME = 'smoke-reception-parent-floor'
    # Smoke-地图-子楼层名称
    SMOKE_MAP_CHILD_FLOOR_NAME = 'smoke-reception-child-floor'
    # Smoke-设备-分组名称
    SMOKE_DEVICE_GROUP_NAME = 'smoke-reception-devices'
    # Smoke-设备-RTSP设备名称
    SMOKE_DEVICE_RTSP_NAME = 'smoke-reception-rtsp'
    # Smoke-设备-RTSP设备深圳视频地址
    SMOKE_DEVICE_RTSP_ADDRESS = 'rtsp://10.151.3.119:6554/test.264'
    # Smoke-任务-任务名称
    SMOKE_TASK_NAME = 'smoke-reception-task'

    def setUp(self):
        super(SmokeReceptionTest, self).setUp()
        LoginPage.login(self, sb_config.username, sb_config.password)

    def tearDown(self):
        self.save_teardown_screenshot()
        super(SmokeReceptionTest, self).tearDown()

    @pytest.mark.smoke
    @pytest.mark.run(order=0)
    @pytest.mark.dependency(name='portrait')
    def test_portrait(self):
        # 访问人像库管理页面
        MenuBar.click_menu_item_by_text(self, '配置', '人像库管理')
        # 添加白名单库
        PortraitPage.add_portrait_database_by_name(
            self, SmokeReceptionTest.SMOKE_PORTRAIT_DATABASE_WHITELIST_NAME, type='白名单')
        PortraitPage.click_add_portrait_button(self)
        self.sleep(2)
        print('当前路径：', os.getcwd())
        PortraitPage.upload_portrait_image(self, '添加人像', os.getcwd()+'/guard/data/portrait/001-JPG.jpg')
        self.sleep(5)

    @pytest.mark.smoke
    @pytest.mark.run(order=1)
    @pytest.mark.dependency(name='map')
    def test_map(self):
        # 访问地图管理页面
        MenuBar.click_menu_item_by_text(self, '配置', '地图管理')
        # 添加父楼层
        MapPage.add_floor_by_root_floor_name(
            self, SmokeReceptionTest.SMOKE_MAP_PARENT_FLOOR_NAME)
        # 添加子楼层
        MapPage.add_floor_by_parent_name(
            self, SmokeReceptionTest.SMOKE_MAP_CHILD_FLOOR_NAME, parent_name=SmokeReceptionTest.SMOKE_MAP_PARENT_FLOOR_NAME, is_peer=False)
        # MapPage.assert_alert_message(self, '创建下一级分组成功')

    @pytest.mark.smoke
    @pytest.mark.run(order=2)
    @pytest.mark.dependency(name='device', depends=['map'])
    def test_device(self):
        # 访问设备管理页面
        MenuBar.click_menu_item_by_text(self, '配置', '设备管理')
        # 创建设备分组
        DevicePage.add_group_by_root_group_name(
            self, SmokeReceptionTest.SMOKE_DEVICE_GROUP_NAME)
        # 添加RTSP设备
        rtsp_device = RTSP(SmokeReceptionTest.SMOKE_DEVICE_RTSP_NAME, SmokeReceptionTest.SMOKE_DEVICE_RTSP_NAME, SmokeReceptionTest.SMOKE_DEVICE_GROUP_NAME,
                           SmokeReceptionTest.SMOKE_MAP_CHILD_FLOOR_NAME, SmokeReceptionTest.SMOKE_DEVICE_RTSP_ADDRESS)
        DevicePage.add_device_by_type(self, rtsp_device, '网络摄像机')

    @pytest.mark.smoke
    @pytest.mark.run(order=3)
    @pytest.mark.dependency(name='task', depends=['portrait', 'device'])
    def test_add_reception_task(self):
        MenuBar.click_menu_item_by_text(self, '配置', '任务管理')
        task = FaceAlertDeploymentTask(SmokeReceptionTest.SMOKE_TASK_NAME, SmokeReceptionTest.SMOKE_DEVICE_RTSP_NAME, portraits=[SmokeReceptionTest.SMOKE_PORTRAIT_DATABASE_WHITELIST_NAME], attributes=['迎宾'])
        TaskPage.add_face_alert_deployment_task(self, task)
        self.sleep(2)
        TaskPage.switch_task_status_by_name(self, SmokeReceptionTest.SMOKE_TASK_NAME)

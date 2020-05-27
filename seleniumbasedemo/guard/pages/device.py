#!/usr/bin/env python3

from selenium.webdriver.common.by import By
from guard.pages.components.group_tree import GroupTree
from guard.pages.base import BasePage
from guard.pages.classes.device.rtsp import RTSP
from guard.pages.classes.device.onvif import ONVIF


class DevicePage(BasePage):
    """ 设备管理页面操作方法

    add_group_by_root_group_name: 添加指定命名的根节点设备分组
    add_group_by_parent_name: 添加指定命名的子设备分组
    delete_group_by_name: 删除指定命名的设备分组
    click_add_device_button: 点击添加设备按钮
    select_device_type: 选择设备类型
    input_device_name: 输入设备名称
    input_device_id: 输入设备ID
    select_device_group_by_name: 选择指定设备分组
    set_device_location: 设置设备点位
    assign_users: 分配指定用户
    input_device_info_by_type: 输入指定类型设备信息
    input_rtsp_address: 输入RTSP地址
    select_camera_type: 选择网络摄像机类型
    click_no_sense_switch: 点击无感门禁开关
    input_no_sense_settings: 输入无感门禁配置
    select_frontend_type: 选择前端比对类型
    input_ip: 输入设备网络地址
    input_port: 输入设备网络端口
    input_username: 输入设备用户名
    input_password: 输入设备密码
    select_dlc_type: 选择人脸抓拍机类型
    add_device_by_type: 添加指定类型设备
    
    """

    def add_group_by_root_group_name(self, name, is_peer=True,parent_name='Default', confirm=True):
        """ 添加指定命名的根节点设备分组

        参数:
            name: 设备分组名称
            is_peer: 是否同级或下一级，默认为同级
            confirm: 是否确认，默认为确认

        """
        if is_peer:
            GroupTree.click_group_menu_by_name(self, parent_name, '创建同级')
        else:
            GroupTree.click_group_menu_by_name(self, parent_name, '创建下一级')
        GROUP_NAME_INPUT = f'div[aria-label="{self.menu}"] > .el-dialog__body > div > div > .el-form > div > div > div > input'
        CONFIRM_BUTTON = f'div[aria-label="{self.menu}"] > .el-dialog__footer > .dialog-footer > .el-button--primary'
        CANCEL_BUTTON = f'div[aria-label="{self.menu}"] > .el-dialog__footer > .dialog-footer > .el-button--info'
        self.update_text(GROUP_NAME_INPUT, name)
        if confirm:
            self.slow_click(CONFIRM_BUTTON)
            self.sleep(1)
        else:
            self.slow_click(CANCEL_BUTTON)

    def add_group_by_parent_name(self, name, parent_name='Default', is_peer=True, confirm=True):
        """ 添加指定命名的子设备分组

        参数:
            name: 子设备分组名称
            parent_name: 父设备分组名称，默认为Default
            is_peer: 是否同级或下一级，默认为同级
            confirm: 是否确认，默认为确认

        """
        if is_peer:
            GroupTree.click_group_menu_by_name(self, parent_name, '创建同级')
        else:
            GroupTree.click_group_menu_by_name(self, parent_name, '创建下一级')
        GROUP_NAME_INPUT = f'div[aria-label="{self.menu}"] > .el-dialog__body > div > div > .el-form > div > div > div > input'
        CONFIRM_BUTTON = f'div[aria-label="{self.menu}"] > .el-dialog__footer > .dialog-footer > .el-button--primary'
        CANCEL_BUTTON = f'div[aria-label="{self.menu}"] > .el-dialog__footer > .dialog-footer > .el-button--info'
        self.update_text(GROUP_NAME_INPUT, name)
        if confirm:
            self.slow_click(CONFIRM_BUTTON)
        else:
            self.slow_click(CANCEL_BUTTON)

#重命名
    def rename_group_by_root_group_name(self, old_name, new_name, confirm=True):
        GroupTree.click_group_menu_by_name(self, old_name, '重命名')
        self.menu = '编辑'
        GROUP_NAME_INPUT = f'div[aria-label="{self.menu}"] > .el-dialog__body > div > div > .el-form > div > div > div > input '
        CONFIRM_BUTTON = f'div[aria-label="{self.menu}"] > .el-dialog__footer > .dialog-footer > .el-button--primary'
        CONFIRM_BUTTON1 = f'div[aria-label="{self.menu}"]'
        CANCEL_BUTTON = f'div[aria-label="{self.menu}"] > .el-dialog__footer > .dialog-footer > .el-button--info'
        self.update_text(GROUP_NAME_INPUT, new_name)

        if confirm:
            self.slow_click(CONFIRM_BUTTON)
            self.sleep(1)
        else:
            self.slow_click(CANCEL_BUTTON)

    def rename_group_by_parent_name(self, old_name, new_name, parent_name='Default', confirm=True):
        GroupTree.click_group_by_name(self, parent_name)
        GroupTree.click_group_menu_by_name(self, old_name, '重命名')
        self.menu = '编辑'
        GROUP_NAME_INPUT = f'div[aria-label="{self.menu}"] > .el-dialog__body > div > div > .el-form > div > div > div > input '
        CONFIRM_BUTTON = f'div[aria-label="{self.menu}"] > .el-dialog__footer > .dialog-footer > .el-button--primary'
        CANCEL_BUTTON = f'div[aria-label="{self.menu}"] > .el-dialog__footer > .dialog-footer > .el-button--info'
        self.update_text(GROUP_NAME_INPUT, new_name)
        if confirm:
            self.click_visible_elements(CONFIRM_BUTTON)
        else:
            self.slow_click(CANCEL_BUTTON)

    def cancel_rename_group(self):
        self.menu = '编辑'
        RENAME_CANCEL_BUTTON = f'div[aria-label="{self.menu}"] > .el-dialog__footer > .dialog-footer > .el-button--info'
        # CONFIRM_BUTTON = f'div[aria-label="{self.menu}"] > .el-dialog__footer > .dialog-footer > .el-button--primary'
        # self.click(CONFIRM_BUTTON)
        # self.sleep(2)
        self.slow_click(RENAME_CANCEL_BUTTON)

#搜索设备组
    def search_device_group_by_name(self, name):
        SEARCH_DEVICE_GROUP_INPUT = '.search-input > input'
        SEARCH_DEVICE_GROUP_BUTTON = '.el-icon-search'
        self.update_text(SEARCH_DEVICE_GROUP_INPUT, name)
        self.click(SEARCH_DEVICE_GROUP_BUTTON)

#查看设备组
    def assert_view_device_group_by_name(self,name):
        self.menu = '详情'
        CANCEL_VIEW_DEVICE_GROUP  = f'div[aria-label="{self.menu}"] >.el-dialog__footer > span > button.el-button.el-button--primary'
        GroupTree.click_group_menu_by_name(self,name,self.menu)
        DevicePage.assert_element_text(self, '.div-right-detail', name)
        self.click(CANCEL_VIEW_DEVICE_GROUP)
        self.sleep(1)






    def delete_group_by_name(self, name, confirm=True):
        """ 删除指定命名的设备分组

        参数:
            name: 设备分组名称
            confirm: 是否确认，默认为确认

        """
        GroupTree.click_group_menu_by_name(self, name, '删除')
        CANCEL_BUTTON = f'div[aria-label="{self.menu}"] > .el-dialog__footer > .dialog-footer > .el-button--info'
        DELETE_BUTTON = f'div[aria-label="{self.menu}"] > .el-dialog__footer > .dialog-footer > .el-button--danger'

        if confirm:
            self.slow_click(DELETE_BUTTON)
        else:
            self.slow_click(CANCEL_BUTTON)

    def click_add_device_button(self):
        """ 点击添加设备按钮 """
        self.menu = '添加设备'
        ADD_DEVICE_XBUTTON = '//button/span[contains(text(),"添加设备")]'
        self.click(ADD_DEVICE_XBUTTON, delay=2)

    def click_edit_device_button(self,name):
        """ 点击编辑设备按钮 """
        self.menu = '编辑'
        SEARCH_DEVICE_INPUT = '.el-col.el-col-4 > div > input'
        SEARCH_DEVICE_BUTTON = '.el-col.el-col-4 > div > span > span > span > i.el-input__icon.el-icon-search'
        EDIT_DEVICE_BUTTON = '.el-table_1_column_14.is-left > div > span:nth-child(2) > i'
        self.click(SEARCH_DEVICE_INPUT)
        self.update_text(SEARCH_DEVICE_INPUT, name)
        self.sleep(3)
        self.click(SEARCH_DEVICE_BUTTON)
        self.sleep(2)
        self.click(EDIT_DEVICE_BUTTON)


    def select_device_type(self, type='网络摄像机'):
        """ 选择设备类型

        参数:
            type: 设备类型，默认为网络摄像机，可选人脸识别机（后）、人脸抓拍机、身份验证一体机、人脸识别机（前）

        """
        DEVICE_TYPE_XDROPDOWN = '//label[text()="设备类型"]/parent::*//input'
        DEVICE_TYPE_XOPTION = f'//div[@class="el-scrollbar"][1]//span[text()="{type}"]'
        self.click(DEVICE_TYPE_XDROPDOWN)
        self.slow_click(DEVICE_TYPE_XOPTION)

    def input_device_name(self, name):
        """ 输入设备名称

        参数:
            name: 设备名称

        """
        DEVICE_NAME_XINPUT = '//label[text()="名称"]/parent::*//input'
        self.update_text(DEVICE_NAME_XINPUT, name)

    def input_device_id(self, id):
        """ 输入设备ID

        参数:
            name: 设备ID

        """
        DEVICE_ID_XINPUT = '//label[text()="ID"]/parent::*//input'
        self.update_text(DEVICE_ID_XINPUT, id)

    def select_device_group_by_name(self, group_name='Default', confirm=True):
        """ 选择指定设备分组

        参数:
            group_name: 设备分组名称，默认为Default
            confirm: 是否确认，默认为确认

        """
        DEVICE_GROUP_XINPUT = '//label[text()="分组"]/parent::*//div[@class="treeselsect-selected el-popover__reference"]//input'
        DEVICE_GROUP_SEARCH_INPUT = '.auroraUI > div > div.treeselsect-content > div.el-input.el-input--small > input'
        DEVICE_GROUP_RADIO_XINPUT = f'//input[@type="radio" and contains(@value, "{group_name}")]/parent::*/following-sibling::span'
        # DEVICE_GROUP_RADIO_INPUT = 'div[role="treeitem"]:not([class="el-tree-node is-hidden is-focusable"]) > div > div > label > span.el-radio__input'
        DEVICE_GROUP_CONFIRM_INPUT = '.auroraUI > div > div.treeselsect-content > div.treeselsect-btns > .el-button--primary'
        DEVICE_GROUP_CANCEL_INPUT = '.auroraUI > div > div.treeselsect-content > div.treeselsect-btns > .el-button--info'
        self.click(DEVICE_GROUP_XINPUT)
        self.click(DEVICE_GROUP_SEARCH_INPUT, delay=1)
        self.update_text(DEVICE_GROUP_SEARCH_INPUT, group_name)
        self.click(DEVICE_GROUP_RADIO_XINPUT)
        if confirm:
            self.slow_click(DEVICE_GROUP_CONFIRM_INPUT)
        else:
            self.slow_click(DEVICE_GROUP_CANCEL_INPUT)

    def set_device_location(self, floor_name='Default', x_offset=0, y_offset=0, confirm=True):
        """ 设置设备点位

        参数:
            floor_name: 设备所在楼层，默认为Default
            x_offset: 设备地图中心X偏移量，默认为0
            y_offset: 设备地图中心Y偏移量，默认为0
            confirm: 是否确认，默认为确认

        """
        DEVICE_FLOOR_SPAN = '.address-class'
        DEVICE_SEARCH_FLOOR_INPUT = 'input[placeholder="请输入平面图名称"]'
        DEVICE_FLOOR_XDIV = f'//div[@class="el-dialog__body"]//span[text()="{floor_name}"]'
        DEVICE_DRAW_LOCATION_A = '.leaflet-draw-draw-marker'
        DEVICE_MAP_IMAGE = '.leaflet-image-layer.leaflet-zoom-animated'
        DEVICE_MAP_IMAGE_DIV = '.leaflet-control-container'
        DEVICE_MAP_CONFIRM_INPUT = 'div[aria-label="设置设备位置"] > .el-dialog__footer > .dialog-footer > .el-button--primary'
        DEVICE_MAP_CANCEL_INPUT = 'div[aria-label="设置设备位置"] > .el-dialog__footer > .dialog-footer > .el-button--info'
        self.slow_click(DEVICE_FLOOR_SPAN)
        self.sleep(2)
        self.update_text(DEVICE_SEARCH_FLOOR_INPUT, floor_name)
        self.click(DEVICE_FLOOR_XDIV, delay=1)
        self.click(DEVICE_DRAW_LOCATION_A, delay=1)
        BasePage.click_element_on_center_by_offset(
            self, DEVICE_MAP_IMAGE_DIV, x_offset, y_offset)
        if confirm:
            self.slow_click(DEVICE_MAP_CONFIRM_INPUT)
        else:
            self.slow_click(DEVICE_MAP_CANCEL_INPUT)

    def assign_users(self, users):
        """ 分配指定用户 """
        pass

    def input_device_info_by_type(self, device, type='网络摄像机'):
        """ 输入指定类型设备信息

        参数:
            device: 设备实例
            type: 设备类型，默认为网络摄像机，可选人脸识别机（后）、人脸抓拍机、身份验证一体机、人脸识别机（前）

        """
        DevicePage.select_device_type(self, type)
        DevicePage.input_device_name(self, device.name)
        DevicePage.input_device_id(self, device.id)
        DevicePage.select_device_group_by_name(self, device.group_name)
        DevicePage.set_device_location(
            self, device.floor_name, device.x_offset, device.y_offset)

    def input_device_info_by_type_edit(self, device, type='网络摄像机'):
        """编辑设备用"""
        DevicePage.select_device_type(self, type)
        DevicePage.input_device_name(self, device.name)
        DevicePage.input_device_id(self, device.id)
        DevicePage.select_device_group_by_name(self, device.group_name)

    def input_rtsp_address(self, rtsp_address):
        """ 输入RTSP地址 """
        DEVICE_RTSP_ADDRESS_XINPUT = '//label[text()="RTSP地址"]/parent::*//input'
        self.update_text(DEVICE_RTSP_ADDRESS_XINPUT, rtsp_address)

    def select_camera_type(self, type='RTSP'):
        """ 选择网络摄像机类型

        参数:
            type: 网络摄像机类型，默认为RTSP，可选ONVIF

        """
        CAMERA_TYPE_RADIO = f'//input[@value="{type}"]/parent::*/span'
        self.click(CAMERA_TYPE_RADIO)

    def select_rtsp_protocol(self,protocol='TCP'):
        """ 切换TCP/UDP """
        SWITCH_PROTOCOL_UDP = '.el-dialog__body > div > form > div:nth-child(7) > div > label:nth-child(2) > span.el-radio__label'
        if protocol == 'UDP':
            self.click(SWITCH_PROTOCOL_UDP)
        else:
            pass

    def select_rtsp_encoding_type(self,type='Direct'):
        """ 切换直连/转码 """
        SWITCH_TYPE_TRANSCODING = '.el-dialog__body > div > form > div:nth-child(6) > div > label:nth-child(2) > span.el-radio__label'
        if type == 'Transcoding':
            self.click(SWITCH_TYPE_TRANSCODING)
        else:
            pass

    def click_no_sense_switch(self, is_no_sense=False):
        """ 点击无感门禁开关

        参数:
            is_no_sense: 是否打开无感门禁，默认为False

        """
        NO_SENSE_SWITCH_DIV = '.el-switch'
        NO_SENSE_SWITCH_INPUT = '.el-switch > .el-switch__core'
        switch_class = self.get_attribute(NO_SENSE_SWITCH_DIV, 'class')
        if is_no_sense and switch_class == 'el-switch':
            self.slow_click(NO_SENSE_SWITCH_INPUT)
        elif not is_no_sense and switch_class == 'el-switch is-checked':
            self.slow_click(NO_SENSE_SWITCH_INPUT)

    def input_no_sense_settings(self, ip, port):
        """ 输入无感门禁配置

        参数:
            ip: 无感门禁网络地址
            port: 无感门禁网络端口

        """
        NO_SENSE_IP_INPUT = f'div[aria-label="{self.menu}"] > .el-dialog__body > div > form > div:nth-child(9) > div:nth-child(1) > div > div > input'
        NO_SENSE_PORT_INPUT = f'div[aria-label="{self.menu}"] > .el-dialog__body > div > form > div:nth-child(9) > div:nth-child(2) > div > div > input'
        self.update_text(NO_SENSE_IP_INPUT, ip)
        self.update_text(NO_SENSE_PORT_INPUT, port)

    def select_frontend_type(self, type):
        """ 选择前端比对类型

        参数:
            type: 前端比对类型，可选SensePass、SensePass Pro、SenseKeeper、SenseGate

        """
        FRONTEND_DEVICE_TYPE_XINPUT = '//label[text()="前端设备"]/parent::*//input'
        FRONTEND_DEVICE_TYPE_XOPTION = f'//div[@class="el-scrollbar"][1]//span[text()="{type}"]'
        self.click(FRONTEND_DEVICE_TYPE_XINPUT)
        self.slow_click(FRONTEND_DEVICE_TYPE_XOPTION)

    def input_ip(self, ip):
        """ 输入设备网络地址

        参数:
            ip: 设备网络地址

        """
        DEVICE_IP_XINPUT = '//label[text()="IP"]/parent::*//input'
        self.update_text(DEVICE_IP_XINPUT, ip)

    def input_port(self, port):
        """ 输入设备网络端口

        参数:
            port: 设备网络端口

        """
        DEVICE_PORT_XINPUT = '//label[text()="Port"]/parent::*//input'
        self.update_text(DEVICE_PORT_XINPUT, port)

    def input_username(self, username):
        """ 输入设备用户名

        参数:
            username: 设备用户名

        """
        DEVICE_USERNAME_XINPUT = '//label[text()="用户名"]/parent::*//input'
        self.update_text(DEVICE_USERNAME_XINPUT, username)

    def input_password(self, password):
        """ 输入设备密码

        参数:
            password: 设备密码

        """
        DEVICE_PASSWORD_XINPUT = '//label[text()="密码"]/parent::*//input'
        self.update_text(DEVICE_PASSWORD_XINPUT, password)

    def select_dlc_type(self, type):
        """ 选择人脸抓拍机类型

        参数:
            type: 人脸抓拍机类型，可选"商汤 -D/-AA系列"、"商汤-11系列"、"大华"、"海康"

        """
        DLC_DEVICE_TYPE_XINPUT = '//label[text()="厂商"]/parent::*//input'
        DLC_DEVICE_TYPE_XOPTION = f'//div[@class="el-scrollbar"][1]//span[text()="{type}"]'
        self.click(DLC_DEVICE_TYPE_XINPUT)
        self.slow_click(DLC_DEVICE_TYPE_XOPTION)

    def add_device_by_type(self, device, type, protocol='TCP',encoding_type='Direct', confirm=True):
        """ 添加指定类型设备

        参数:
            device: 设备实例
            type: 设备类型，默认为网络摄像机，可选人脸识别机（后）、人脸抓拍机、身份验证一体机、人脸识别机（前）
            confirm: 是否确认，默认为确认 

        """
        DevicePage.click_add_device_button(self)
        DevicePage.input_device_info_by_type(self, device, type)
        if (type == '网络摄像机'):
            is_no_sense = (device.no_sense_ip !=
                           '' or device.no_sense_port != '')
            if isinstance(device, RTSP):
                DevicePage.select_camera_type(self, 'RTSP')
                DevicePage.input_rtsp_address(self, device.rtsp_address)
                DevicePage.select_rtsp_protocol(self,protocol)
                DevicePage.select_rtsp_encoding_type(self,encoding_type)
            if isinstance(device, ONVIF):
                DevicePage.select_camera_type(self, 'ONVIF')
                DevicePage.input_ip(self, device.ip)
                DevicePage.input_port(self, device.port)
                DevicePage.input_username(self, device.username)
                DevicePage.input_password(self, device.password)

            DevicePage.click_no_sense_switch(self, is_no_sense)
            if is_no_sense:
                DevicePage.input_no_sense_settings(
                    self, device.no_sense_ip, device.no_sense_port)
        elif (type == '人脸识别机（前）'):
            DevicePage.select_frontend_type(self, device.type)
        elif (type == '人脸抓拍机'):
            DevicePage.select_dlc_type(self, device.manufacturer)
            DevicePage.input_ip(self, device.ip)
            DevicePage.input_port(self, device.port)
            DevicePage.input_username(self, device.username)
            DevicePage.input_password(self, device.password)

        DEVICE_DIALOG_CONFIRM_INPUT = f'div[aria-label="{self.menu}"] > .el-dialog__footer > .dialog-footer > .el-button--primary'
        DEVICE_DIALOG_CANCEL_INPUT = f'div[aria-label="{self.menu}"] > .el-dialog__footer > .dialog-footer > .el-button--info'
        if confirm:
            self.slow_click(DEVICE_DIALOG_CONFIRM_INPUT)
        else:
            self.slow_click(DEVICE_DIALOG_CANCEL_INPUT)

    #删除设备
    def delete_device_by_name(self,name, confirm=True):
        SEARCH_DEVICE_INPUT = '.el-col.el-col-4 > div > input'
        SEARCH_DEVICE_BUTTON = '.el-col.el-col-4 > div > span > span > span > i.el-input__icon.el-icon-search'
        # DELETE_DEVICE_BUTTON = '.el-table_1_column_14.is-left > div > span:nth-child(3) > i'
        # Upadted by yuanxiaolu on 22nd,Apr update DELETE_DEVICE_BUTTON locator
        DELETE_DEVICE_BUTTON = f'//div[text()="{name}"]/parent::*/parent::*//i[@class="iconfont icon-delete"]'
        DELETE_DEVICE_CONFIRM = '.el-dialog__footer > span > button.el-button.el-button--danger'

        DELETE_DEVICE_CANCEL = '.el-dialog__footer > span > button.el-button.el-button--info'
        self.click(SEARCH_DEVICE_INPUT)
        self.update_text(SEARCH_DEVICE_INPUT,name)
        self.sleep(3)
        self.click(SEARCH_DEVICE_BUTTON)
        self.sleep(2)
        self.click(DELETE_DEVICE_BUTTON)
        if confirm:
            self.slow_click(DELETE_DEVICE_CONFIRM)
        else:
            self.slow_click(DELETE_DEVICE_CANCEL)


    #取消添加设备
    def cancel_add_device(self,menu ='添加设备'):
        self.menu = menu
        ADD_CANCEL_BUTTON = f'div[aria-label="{self.menu}"] > .el-dialog__footer > .dialog-footer > .el-button--info'
        self.slow_click(ADD_CANCEL_BUTTON)

    def queren_add_device(self,menu ='添加设备'):
        self.menu = menu
        ADD_QUEREN_BUTTON = f'div[aria-label="{self.menu}"] > .el-dialog__footer > .dialog-footer > .el-button--primary'
        self.slow_click(ADD_QUEREN_BUTTON)
        self.sleep(1)

    #确认rtsp网络协议
    def assert_rtsp_protocol_by_name(self,name,protocol_set):
        self.menu = '详情'
        SEARCH_DEVICE_INPUT = '.el-col.el-col-4 > div > input'
        SEARCH_DEVICE_BUTTON = '.el-col.el-col-4 > div > span > span > span > i.el-input__icon.el-icon-search'
        VIEW_DEVICE_BUTTON = '.el-table_1_column_14.is-left > div > span:nth-child(1) > i'
        VIEW_DEVICE_CANCEL = f'div[aria-label="{self.menu}"]>.el-dialog__footer > span > button.el-button.el-button--info'
        UDP_VIEW = f'//div[@class="el-form-item__content"][contains(text(),"{protocol_set}")]'
        #TCP_VIEW = '//div[@class="el-form-item__content"][contains(text(),"TCP")]'
        self.click(SEARCH_DEVICE_INPUT)
        self.update_text(SEARCH_DEVICE_INPUT, name)
        self.sleep(3)
        self.click(SEARCH_DEVICE_BUTTON)
        self.sleep(2)
        self.click(VIEW_DEVICE_BUTTON)
        self.sleep(2)
        self.is_element_visible(UDP_VIEW)
        self.sleep(2)
        self.click(VIEW_DEVICE_CANCEL)
        self.sleep(2)

    #确认预览
    def assert_view_video(self,menu):
        self.menu = menu
        VIEW_VIDEO_BUTTON = f'div[aria-label="{self.menu}"]>.el-dialog__body > div > form > div.el-form-item.is-required > div > i'
        LOADING_STYLE = '//div[@style = "display: none;"]'
        DEVICE_DIALOG_CANCEL_INPUT = f'div[aria-label="{self.menu}"] > .el-dialog__footer > .dialog-footer > .el-button--info'
        self.click(VIEW_VIDEO_BUTTON)
        self.sleep(15)
        self.assert_no_js_errors()
        self.sleep(1)
        self.click(DEVICE_DIALOG_CANCEL_INPUT)


    #编辑设备
    def edit_device_by_type(self, device, type, name, protocol='TCP', encoding_type='Direct', confirm=True):
        DevicePage.click_edit_device_button(self,name)
        DevicePage.input_device_info_by_type_edit(self, device, type)
        if (type == '网络摄像机'):
            is_no_sense = (device.no_sense_ip !=
                           '' or device.no_sense_port != '')
            if isinstance(device, RTSP):
                DevicePage.select_camera_type(self, 'RTSP')
                DevicePage.input_rtsp_address(self, device.rtsp_address)
                DevicePage.select_rtsp_protocol(self, protocol)
                DevicePage.select_rtsp_encoding_type(self, encoding_type)
            if isinstance(device, ONVIF):
                DevicePage.select_camera_type(self, 'ONVIF')
                DevicePage.input_ip(self, device.ip)
                DevicePage.input_port(self, device.port)
                DevicePage.input_username(self, device.username)
                DevicePage.input_password(self, device.password)

            DevicePage.click_no_sense_switch(self, is_no_sense)
            if is_no_sense:
                DevicePage.input_no_sense_settings(
                    self, device.no_sense_ip, device.no_sense_port)
        elif (type == '人脸识别机（前）'):
            DevicePage.select_frontend_type(self, device.type)
        elif (type == '人脸抓拍机'):
            DevicePage.select_dlc_type(self, device.manufacturer)
            DevicePage.input_ip(self, device.ip)
            DevicePage.input_port(self, device.port)
            DevicePage.input_username(self, device.username)
            DevicePage.input_password(self, device.password)

        DEVICE_DIALOG_CONFIRM_INPUT = f'div[aria-label="{self.menu}"] > .el-dialog__footer > .dialog-footer > .el-button--primary'
        DEVICE_DIALOG_CANCEL_INPUT = f'div[aria-label="{self.menu}"] > .el-dialog__footer > .dialog-footer > .el-button--info'
        if confirm:
            self.slow_click(DEVICE_DIALOG_CONFIRM_INPUT)
        else:
            self.slow_click(DEVICE_DIALOG_CANCEL_INPUT)

    def edit_device_by_type_view(self, device, type, name, protocol='TCP', encoding_type='Direct',):
        DevicePage.click_edit_device_button(self,name)
        DevicePage.input_device_info_by_type_edit(self, device, type)
        if (type == '网络摄像机'):
            is_no_sense = (device.no_sense_ip !=
                           '' or device.no_sense_port != '')
            if isinstance(device, RTSP):
                DevicePage.select_camera_type(self, 'RTSP')
                DevicePage.input_rtsp_address(self, device.rtsp_address)
                DevicePage.select_rtsp_protocol(self, protocol)
                DevicePage.select_rtsp_encoding_type(self, encoding_type)
            if isinstance(device, ONVIF):
                DevicePage.select_camera_type(self, 'ONVIF')
                DevicePage.input_ip(self, device.ip)
                DevicePage.input_port(self, device.port)
                DevicePage.input_username(self, device.username)
                DevicePage.input_password(self, device.password)

            DevicePage.click_no_sense_switch(self, is_no_sense)
            if is_no_sense:
                DevicePage.input_no_sense_settings(
                    self, device.no_sense_ip, device.no_sense_port)
        elif (type == '人脸识别机（前）'):
            DevicePage.select_frontend_type(self, device.type)
        elif (type == '人脸抓拍机'):
            DevicePage.select_dlc_type(self, device.manufacturer)
            DevicePage.input_ip(self, device.ip)
            DevicePage.input_port(self, device.port)
            DevicePage.input_username(self, device.username)
            DevicePage.input_password(self, device.password)

        DEVICE_DIALOG_CONFIRM_INPUT = f'div[aria-label="{self.menu}"] > .el-dialog__footer > .dialog-footer > .el-button--primary'
        DEVICE_DIALOG_CANCEL_INPUT = f'div[aria-label="{self.menu}"] > .el-dialog__footer > .dialog-footer > .el-button--info'
        VIEW_VIDEO_BUTTON = f'div[aria-label="{self.menu}"]>.el-dialog__body > div > form > div.el-form-item.is-required > div > i'
        self.click(VIEW_VIDEO_BUTTON)
        self.sleep(15)
        self.assert_no_js_errors()
        self.sleep(1)
        self.slow_click(DEVICE_DIALOG_CANCEL_INPUT)



    #设备存在
    def assert_device(self,name):
        SEARCH_DEVICE_INPUT = '.el-col.el-col-4 > div > input'
        SEARCH_DEVICE_BUTTON = '.el-col.el-col-4 > div > span > span > span > i.el-input__icon.el-icon-search'
        CHECK_DEVICE_NAME = f'//td[@class="el-table_1_column_2 is-left "]/div[@class="cell" and contains(text(),"{name}")]'
        self.click(SEARCH_DEVICE_INPUT)
        self.update_text(SEARCH_DEVICE_INPUT, name)
        self.sleep(3)
        self.click(SEARCH_DEVICE_BUTTON)
        self.is_element_visible(CHECK_DEVICE_NAME,by = By.XPATH)

    #设备搜索
    def search_device_by_name(self,name):
        SEARCH_DEVICE_INPUT = '.el-col.el-col-4 > div > input'
        SEARCH_DEVICE_BUTTON = '.el-col.el-col-4 > div > span > span > span > i.el-input__icon.el-icon-search'
        self.click(SEARCH_DEVICE_INPUT)
        self.update_text(SEARCH_DEVICE_INPUT, name)
        self.sleep(3)
        self.click(SEARCH_DEVICE_BUTTON)

    def delete_device_by_name_muti(self):
        """批量删除"""
        MUTI_BUTTON = '.main_head > div:nth-child(1) > button:nth-child(2)'
        MUTI_CLICK_ALL = '.is-leaf > div > label > span > span'
        DELETE_MUTI = '.el-button.el-button--danger.el-button--small'
        DELETE_MUTI_CONFIRM = '.el-dialog__footer > span > button.el-button.el-button--danger'
        self.click(MUTI_BUTTON)
        self.sleep(1)
        self.click(MUTI_CLICK_ALL)
        self.sleep(1)
        self.click(DELETE_MUTI)
        self.sleep(1)
        self.click(DELETE_MUTI_CONFIRM)
        self.sleep(1)

    #批量删除不勾选
    def delete_device_by_name_muti_no_select(self):
        MUTI_BUTTON = '.main_head > div:nth-child(1) > button:nth-child(2)'
        #MUTI_CLICK_ALL = '.is-leaf > div > label > span > span'
        DELETE_MUTI = '.el-button.el-button--danger.el-button--small'
        #DELETE_MUTI_CONFIRM = '.el-dialog__footer > span > button.el-button.el-button--danger'
        self.click(MUTI_BUTTON)
        self.sleep(1)
        #self.click(MUTI_CLICK_ALL)
        #self.sleep(1)
        self.click(DELETE_MUTI)
        self.sleep(1)

    #批量移动不勾选
    def move_device_by_name_muti_no_select(self):
        MUTI_BUTTON = '.main_head > div:nth-child(1) > button:nth-child(2)'
        MOVE_MUTI = '.main_head > div:nth-child(2) > button:nth-child(3)'
        self.click(MUTI_BUTTON)
        self.sleep(1)
        self.click(MOVE_MUTI)
        self.sleep(1)

    def select_device_user_by_name_muti_no_select(self):
        """批量选用户不勾选"""
        MUTI_BUTTON = '.main_head > div:nth-child(1) > button:nth-child(2)'
        SELECT_USER_MUTI = '.main_head > div:nth-child(2) > button:nth-child(2)'
        self.click(MUTI_BUTTON)
        self.sleep(1)
        self.click(SELECT_USER_MUTI)
        self.sleep(1)

    def select_device_user_muti_search(self):
        MUTI_BUTTON = '.main_head > div:nth-child(1) > button:nth-child(2)'
        MUTI_CLICK_ALL = '.is-leaf > div > label > span > span'
        SELECT_USER_MUTI = '.main_head > div:nth-child(2) > button:nth-child(2)'
        SEARCH_USER = '.el-dialog__body > div.el-input.el-input--medium.el-input--suffix > input'
        SEARCH_USER_CLICK = '//span[@class="el-tree-node__label" and contains(text(),"Administrator")]/../label[@class="el-checkbox"]/span[@class="el-checkbox__input"]'
        SELECT_USER_CONFIRM = '.el-dialog__body > div.timezone-timezone-footer > button.el-button.el-button--primary'
        self.click(MUTI_BUTTON)
        self.sleep(1)
        self.click(MUTI_CLICK_ALL)
        self.sleep(1)
        self.click(SELECT_USER_MUTI)
        self.sleep(1)
        self.update_text(SEARCH_USER,'Administrator')
        self.sleep(1)
        self.click(SEARCH_USER_CLICK)
        self.sleep(1)
        self.click(SELECT_USER_CONFIRM)
        self.sleep(2)

    def select_device_user_muti_search_invalid_user(self):
        MUTI_BUTTON = '.main_head > div:nth-child(1) > button:nth-child(2)'
        MUTI_CLICK_ALL = '.is-leaf > div > label > span > span'
        SELECT_USER_MUTI = '.main_head > div:nth-child(2) > button:nth-child(2)'
        SEARCH_USER = '.el-dialog__body > div.el-input.el-input--medium.el-input--suffix > input'
        SEARCH_USER_CLICK = '//span[@class="el-tree-node__label" and contains(text(),"Administrator")]/../label[@class="el-checkbox"]/span[@class="el-checkbox__input"]'
        SELECT_USER_CONFIRM = '.el-dialog__body > div.timezone-timezone-footer > button.el-button.el-button--primary'
        self.click(MUTI_BUTTON)
        self.sleep(1)
        self.click(MUTI_CLICK_ALL)
        self.sleep(1)
        self.click(SELECT_USER_MUTI)
        self.sleep(1)
        self.update_text(SEARCH_USER, '   ')
        self.sleep(1)
        BasePage.assert_element_text(self,'.el-dialog__body > div:nth-child(4) > div > div.el-tree__empty-block > span','暂无数据')
        self.sleep(1)
        self.click(SELECT_USER_CONFIRM)
        self.sleep(1)

    def move_device_by_name_muti_search(self,name):
        MUTI_BUTTON = '.main_head > div:nth-child(1) > button:nth-child(2)'
        MUTI_CLICK_ALL = '.is-leaf > div > label > span > span'
        MOVE_MUTI = '.main_head > div:nth-child(2) > button:nth-child(3)'
        MOVE_SEARCH_MUTI = '.el-dialog__body > div.el-input.el-input--medium.el-input--suffix > input'
        CLICK_MOVE_GROUP = f'//span[@class="el-radio__label" and contains(text(),"{name}")]/../span/span'
        CONFIRM_MOVE_GROUP = '.el-dialog__body > div.timezone-timezone-footer > button.el-button.el-button--primary'
        self.click(MUTI_BUTTON)
        self.sleep(1)
        self.click(MUTI_CLICK_ALL)
        self.sleep(1)
        self.click(MOVE_MUTI)
        self.sleep(1)
        self.update_text(MOVE_SEARCH_MUTI, name)
        self.sleep(1)
        self.click(CLICK_MOVE_GROUP)
        self.sleep(1)
        self.click(CONFIRM_MOVE_GROUP)
        self.sleep(1)

    def move_device_by_name_muti_search_invalid_group(self,name):
        MUTI_BUTTON = '.main_head > div:nth-child(1) > button:nth-child(2)'
        MUTI_CLICK_ALL = '.is-leaf > div > label > span > span'
        MOVE_MUTI = '.main_head > div:nth-child(2) > button:nth-child(3)'
        MOVE_SEARCH_MUTI = '.el-dialog__body > div.el-input.el-input--medium.el-input--suffix > input'
        CONFIRM_MOVE_GROUP = '.el-dialog__body > div.timezone-timezone-footer > button.el-button.el-button--primary'
        self.click(MUTI_BUTTON)
        self.sleep(1)
        self.click(MUTI_CLICK_ALL)
        self.sleep(1)
        self.click(MOVE_MUTI)
        self.sleep(1)
        self.update_text(MOVE_SEARCH_MUTI, name)
        BasePage.assert_element_text(self,
                                     '.el-dialog__body > div:nth-child(4) > div > div.el-tree__empty-block > span',
                                     '暂无数据')
        self.sleep(1)
        self.click(CONFIRM_MOVE_GROUP)
        self.sleep(1)

#编辑搜索不存在用户
    def assert_edit_device_search_user_none(self):
        SELECT_DEVICE_USER = '//label[text()="分配用户"]/parent::*//div[@class="treeselsect-selected el-popover__reference"]/div'
        SEARCH_USER_INPUT = '.auroraUI > div > div.treeselsect-content > div.el-input.el-input--small > input'
        self.sleep(2)
        self.click(SELECT_DEVICE_USER)
        self.sleep(1)
        self.update_text(SEARCH_USER_INPUT,'  ')
        BasePage.assert_element_text(self,
                                     '.el-tree > div.el-tree__empty-block > span',
                                     '暂无数据')
        DevicePage.cancel_add_device(self,'编辑')

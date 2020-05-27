#!/usr/bin/env python3

from selenium.webdriver.common.by import By
from guard.pages.base import BasePage
from guard.pages.components.dialog import Dialog


class TaskPage(BasePage):
    """ 任务管理页面操作方法

    click_create_task_button: 点击添加任务按钮
    click_task_tab_by_type: 点击指定类型任务标签
    select_task_type: 选择指定任务类型
    input_task_name: 输入任务名称
    select_task_device_by_name: 选择指定命名的任务设备
    select_task_threshold: 选择指定任务阈值
    select_task_attributes: 选择指定任务特殊属性
    select_task_portraits: 选择指定任务人像库
    add_face_access_control_task: 添加人脸-通行任务
    select_task_time_condition: 选择指定命名的时间条件
    draw_line: 绘制指定告警线
    select_crossing_direction: 选择越线方向
    add_pedestrian_crossing_boundary_detection_task: 添加人体-越线检测任务
    add_pedestrian_area_entry_detection_task: 添加人体-区域闯入检测任务
    add_vehicle_illegally_parking_detection_task: 添加车辆-违停检测任务
    search_task_by_name: 搜索指定命名任务
    delete_task_by_name: 删除指定命名任务
    switch_task_by_name：更改指定命名任务的状态
    edit_task_name: 编辑指定命名任务的名称
    detail_task_by_name: 查看指定命名任务
    close_task_detail_popup: 关闭任务详情窗口
    add_face_alert_deployment_task：添加布控任务
    
    """

    def click_create_task_button(self):
        """ 点击添加任务按钮 """
        self.menu = '添加任务'
        CREATE_TASK_XBUTTON = '//button/span[contains(text(),"添加任务")]'
        self.click(CREATE_TASK_XBUTTON, delay=2)

    def click_task_tab_by_type(self, type='人脸-布控任务'):
        """ 点击指定类型任务标签

        参数:
            type: 任务类型，默认为人脸-布控任务，可选人脸-通行任务、人体-越线检测任务、人体-区域闯入检测任务、车辆-违停检测任务

        """
        TASK_MENU_XLI = f'//ul[@class="task-menu-list"]/li[contains(text(),"{type}")]'
        self.click(TASK_MENU_XLI, delay=1)

    def select_task_type(self, type='人脸-布控任务'):
        """ 选择指定任务类型

        参数:
            type: 任务类型，默认为人脸-布控任务，可选人脸-通行任务、人体-越线检测任务、人体-区域闯入检测任务、车辆-违停检测任务

        """
        TASK_TYPE_XDROPDOWN = '//label[text()="任务类型"]/parent::*//input'
        TASK_TYPE_XOPTION = f'//div[@class="el-scrollbar"][1]//span[text()="{type}"]'
        self.slow_click(TASK_TYPE_XDROPDOWN)
        self.slow_click(TASK_TYPE_XOPTION)

    def input_task_name(self, name):
        """ 输入任务名称

        参数:
            name: 任务名称
        """
        TASK_NAME_XINPUT = '//label[text()="任务名称"]/parent::*//input'
        self.update_text(TASK_NAME_XINPUT, name)

    def select_task_device_by_name(self, device_name, confirm=True):
        """ 选择指定命名的任务设备

        参数:
            device_name: 设备名称
            confirm: 是否确认，默认为确认

        """
        TASK_DEVICE_XINPUT = '//label[text()="设备"]/parent::*//input[@type="text" and @placeholder="请选择"]'
        TASK_DEVICE_SEARCH_INPUT = '.auroraUI > div > div > div.el-input > input'
        TASK_DEVICE_RADIO_XINPUT = f'//span[@class="el-radio__label"]/span[contains(text(), "{device_name}")]'
        TASK_DEVICE_CONFIRM_INPUT = '.auroraUI > div > div > div.treeselsect-btns > .el-button--primary'
        TASK_DEVICE_CANCEL_INPUT = '.auroraUI > div > div > div.treeselsect-btns > .el-button--info'
        self.click(TASK_DEVICE_XINPUT)
        self.click(TASK_DEVICE_SEARCH_INPUT, delay=1)
        self.update_text(TASK_DEVICE_SEARCH_INPUT, device_name)
        self.click(TASK_DEVICE_RADIO_XINPUT)
        # if confirm:
        #     self.slow_click(TASK_DEVICE_CONFIRM_INPUT)
        # else:
        #     self.slow_click(TASK_DEVICE_CANCEL_INPUT)

    def select_task_threshold(self, threshold=""):
        """ 选择指定任务阈值

        参数:
            threshold: 任务阈值，默认90。0，不可多选
        created by yuan xiaolu on 14th,Apr 2020
        """
        TASK_THRESHOLD_XDROPDOWN = '//label[text()="阈值"]/parent::*//input[@type="text"]'
        self.slow_click(TASK_THRESHOLD_XDROPDOWN)
        # self.execute_script('jQuery, window.scrollTo(0, 600)')  # Scrolling the page
        TASK_THRESHOLD_XOPTION = f'//div[@class="el-scrollbar"]//span[text()="{threshold}"]'
        self.slow_click(TASK_THRESHOLD_XOPTION)
        self.slow_click(TASK_THRESHOLD_XDROPDOWN)

    def select_task_attributes(self, attributes=[]):
        """ 选择指定任务特殊属性

        参数:
            attributes: 任务特殊属性，默认为空，可多选入口、出口、防尾随、第三方对接、迎宾，举例：['入口'，'迎宾']

        """
        TASK_ATTRIBUTE_XDROPDOWN = '//label[text()="特殊属性"]/parent::*//input[@type="text"]'
        self.slow_click(TASK_ATTRIBUTE_XDROPDOWN)
        for attribute in attributes:
            TASK_ATTRIBUTE_XOPTION = f'//div[@class="el-scrollbar"][1]//span[text()="{attribute}"]'
            self.slow_click(TASK_ATTRIBUTE_XOPTION)
        self.sleep(3)
        TASK_ATTRIBUTE_AFTER_XDROPDOWN = '//label[text()="特殊属性"]/parent::*//span[contains(@class, "el-input__suffix-inner")]'
        self.slow_click(TASK_ATTRIBUTE_AFTER_XDROPDOWN)



    def select_task_portraits(self, portrait):
        """ 选择指定任务人像库

        参数:
            portraits: 任务绑定人像库名称列表，举例: ['portrait1', 'portrait2']

        """
        PORTRAIT_XINPUT = '//label[text()="人像库"]/parent::*//input[@type="text"]'
        self.slow_click(PORTRAIT_XINPUT)
        PORTRAIT_SEARCH_INPUT = f'div[aria-label="{self.menu}"] > .el-dialog__body > div:nth-child(2) > form:nth-child(1) > div:nth-child(4) > div > div.selsect-container > div > div.selsect-dropdown__wrap > div > input'
        self.update_text(PORTRAIT_SEARCH_INPUT, portrait)
        TASK_PORTRAIT_CHECKBOX_XINPUT = f'//label[text()="人像库"]/parent::*//div[contains(text(), "{portrait}")]/parent::*/label/span/span'
        self.slow_click(TASK_PORTRAIT_CHECKBOX_XINPUT)

        PORTRAIT_CONFIRM_SPAN = f'div[aria-label="{self.menu}"] >.el-dialog__body > div:nth-child(2) > form:nth-child(1) > div:nth-child(4) > div > div.selsect-container > div > div.selsect-dropdown__wrap > div.selsect-dropdown-footer > button.el-button.el-button--primary > span'
        self.slow_click(PORTRAIT_CONFIRM_SPAN)

    def add_face_access_control_task(self, task, confirm=True):
        """ 添加人脸-通行任务

        参数:
            task: 人脸-通行任务实例
            confirm: 是否确认，默认为确认

        """
        TaskPage.click_task_tab_by_type(self, '人脸-通行任务')
        TaskPage.click_create_task_button(self)
        TaskPage.select_task_type(self, '人脸-通行任务')
        TaskPage.input_task_name(self, task.task_name)
        TaskPage.select_task_device_by_name(self, task.device_name)
        TaskPage.select_task_threshold(self, task.threshold)
        TaskPage.select_task_attributes(
            self, task.attributes)
        for portrait in task.portraits:
            TASK_PORTRAIT_CHECKBOX_XINPUT = f'//div[@role="group"]//span[contains(text(), "{portrait}")]/parent::*/label/span/span'
            self.slow_click(TASK_PORTRAIT_CHECKBOX_XINPUT)

        TASK_DIALOG_CONFIRM_INPUT = f'div[aria-label="{self.menu}"] > .el-dialog__footer > .dialog-footer > .el-button--primary'
        TASK_DIALOG_CANCEL_INPUT = f'div[aria-label="{self.menu}"] > .el-dialog__footer > .dialog-footer > .el-button--info'

        if confirm:
            self.slow_click(TASK_DIALOG_CONFIRM_INPUT)
        else:
            self.slow_click(TASK_DIALOG_CANCEL_INPUT)

    def select_task_time_condition(self, time_condition):
        """ 选择指定命名的时间条件
        
        参数:
            time_condition: 时间条件名称

        """
        TASK_TIME_CONDITION_XDROPDOWN = '//label[text()="时间条件"]/parent::*//input[@type="text"]'
        self.slow_click(TASK_TIME_CONDITION_XDROPDOWN)
        if time_condition:
            TASK_TIME_CONDITION_XOPTION = f'//div[@class="el-scrollbar"][1]//span[text()="{time_condition}"]'
            self.slow_click(TASK_TIME_CONDITION_XOPTION)
        self.slow_click(TASK_TIME_CONDITION_XDROPDOWN)

    def draw_line(self, alarm_line):
        """ 绘制指定告警线

        参数:
            alarm_line: 告警线起点和终点列表，举例为[(-100, -100), (100, 100)]
        """
        TASK_DRAW_ALARM_LINE_I = '.iconfont.icon-edit1'
        self.slow_click(TASK_DRAW_ALARM_LINE_I)
        self.sleep(2)
        TASK_DRAW_ALARM_CANVAS = '.draw-line'
        for point in alarm_line:
            BasePage.click_element_on_center_by_offset(
                self, TASK_DRAW_ALARM_CANVAS, x_offset=point[0], y_offset=point[1])

    def select_crossing_direction(self, crossing_direction):
        """ 选择越线方向

        参数:
            crossing_direction: 越线方向名称，可选AB双向越线、由B到A越线、由A到B越线

        """
        TASK_CROSSING_DIRECTION_XDROPDOWN = '//label[text()="越线方向"]/parent::*//input[@type="text"]'
        self.slow_click(TASK_CROSSING_DIRECTION_XDROPDOWN)
        TASK_CROSSING_DIRECTION_XOPTION = f'//div[@class="el-scrollbar"][1]//span[text()="{crossing_direction}"]'
        self.slow_click(TASK_CROSSING_DIRECTION_XOPTION)

    def add_pedestrian_crossing_boundary_detection_task(self, task, confirm=True):
        """ 添加人体-越线检测任务

        参数:
            task: 人体-越线检测任务实例
            confirm: 是否确认，默认为确认

        """
        TaskPage.click_task_tab_by_type(self, '人体-越线检测任务')
        TaskPage.click_create_task_button(self)
        TaskPage.select_task_type(self, '人体-越线检测任务')
        TaskPage.input_task_name(self, task.task_name)
        TaskPage.select_task_device_by_name(self, task.device_name)
        TaskPage.select_task_attributes(
            self, task.attributes)
        TaskPage.select_task_time_condition(self, task.time_condition)
        TaskPage.draw_line(self, task.alarm_line)
        TaskPage.select_crossing_direction(self, task.crossing_direction)

        TASK_DIALOG_CONFIRM_INPUT = f'div[aria-label="{self.menu}"] > .el-dialog__footer > .dialog-footer > .el-button--primary'
        TASK_DIALOG_CANCEL_INPUT = f'div[aria-label="{self.menu}"] > .el-dialog__footer > .dialog-footer > .el-button--info'

        if confirm:
            self.slow_click(TASK_DIALOG_CONFIRM_INPUT)
        else:
            self.slow_click(TASK_DIALOG_CANCEL_INPUT)

    def add_pedestrian_area_entry_detection_task(self, task, confirm=True):
        """ 添加人体-区域闯入检测任务

        参数:
            task: 人体-区域闯入检测任务实例
            confirm: 是否确认，默认为确认

        """
        TaskPage.click_task_tab_by_type(self, '人体-区域闯入检测任务')
        TaskPage.click_create_task_button(self)
        TaskPage.select_task_type(self, '人体-区域闯入检测任务')
        TaskPage.input_task_name(self, task.task_name)
        TaskPage.select_task_device_by_name(self, task.device_name)
        TaskPage.select_task_attributes(
            self, task.attributes)
        TaskPage.select_task_time_condition(self, task.time_condition)
        TaskPage.draw_line(self, task.area_settings)

        TASK_DIALOG_CONFIRM_INPUT = f'div[aria-label="{self.menu}"] > .el-dialog__footer > .dialog-footer > .el-button--primary'
        TASK_DIALOG_CANCEL_INPUT = f'div[aria-label="{self.menu}"] > .el-dialog__footer > .dialog-footer > .el-button--info'

        if confirm:
            self.slow_click(TASK_DIALOG_CONFIRM_INPUT)
        else:
            self.slow_click(TASK_DIALOG_CANCEL_INPUT)

    def add_vehicle_illegally_parking_detection_task(self, task, confirm=True):
        """ 添加车辆-违停检测任务

        参数:
            task: 车辆-违停检测任务实例
            confirm: 是否确认，默认为确认

        """
        TaskPage.click_task_tab_by_type(self, '车辆-违停检测任务')
        TaskPage.click_create_task_button(self)
        TaskPage.select_task_type(self, '车辆-违停检测任务')
        TaskPage.input_task_name(self, task.task_name)
        TaskPage.select_task_device_by_name(self, task.device_name)
        TaskPage.select_task_attributes(
            self, task.attributes)
        TaskPage.select_task_time_condition(self, task.time_condition)
        TaskPage.draw_line(self, task.area_settings)

        TASK_DIALOG_CONFIRM_INPUT = f'div[aria-label="{self.menu}"] > .el-dialog__footer > .dialog-footer > .el-button--primary'
        TASK_DIALOG_CANCEL_INPUT = f'div[aria-label="{self.menu}"] > .el-dialog__footer > .dialog-footer > .el-button--info'

        if confirm:
            self.slow_click(TASK_DIALOG_CONFIRM_INPUT)
        else:
            self.slow_click(TASK_DIALOG_CANCEL_INPUT)

    def search_task_by_name(self, name):
        """ 搜索指定命名任务

        参数:
            name: 任务名称

        """
        SEARCH_TASK_INPUT = '.task-table-header > div > div > input'
        SEARCH_TASK_BUTTON = '.task-table-header > div > div > span > span > i'
        self.update_text(SEARCH_TASK_INPUT, name)
        self.click(SEARCH_TASK_BUTTON)

    def delete_task_by_name(self, name, confirm=True):
        """ 删除指定命名任务

        参数:
            name: 任务名称
            confirm: 是否确认，默认为确认

        """
        TASK_DELETE_XBUTTON = f'//div[text()="{name}"]/parent::*/following-sibling::td//i[contains(@class, "icon-delete")]'
        TaskPage.search_task_by_name(self, name)
        self.click(TASK_DELETE_XBUTTON, 2)

        DELETE_TASK_DIALOG_CONFIRM_INPUT = 'body > div.el-dialog__wrapper > div > div.el-dialog__footer > span > button.el-button.el-button--danger'
        DELETE_TASK_DIALOG_CANCEL_INPUT = 'body > div.el-dialog__wrapper > div > div.el-dialog__footer > span > button.el-button.el-button--info'

        if confirm:
            self.slow_click(DELETE_TASK_DIALOG_CONFIRM_INPUT)
        else:
            self.slow_click(DELETE_TASK_DIALOG_CANCEL_INPUT)

    def switch_task_status_by_name(self, name, confirm=True):
        """ 启用/禁用指定命名任务
        到底是禁用抑或启用任务取决于调用该方法之前任务的状态

        参数:
            name: 任务名称
            confirm: 是否确认，默认为确认
        created by yuan xiaolu on 15th,Apr 2020
        """
        TASK_SWITCH_XBUTTON = f'//div[text()="{name}"]/parent::*/following-sibling::td//span[contains(@class, "el-switch__core")]'
        TaskPage.search_task_by_name(self, name)
        self.click(TASK_SWITCH_XBUTTON, 2)

        SWITCH_TASK_STATUS_CONFIRM_BUTTON = 'body > div.el-dialog__wrapper > div > div.el-dialog__footer > span > button.el-button.el-button--primary'
        SWITCH_TASK_STATUS_CANCEL_BUTTON = 'body > div.el-dialog__wrapper > div > div.el-dialog__footer > span > button.el-button.el-button--info'

        if confirm:
            self.slow_click(SWITCH_TASK_STATUS_CONFIRM_BUTTON)
        else:
            self.slow_click(SWITCH_TASK_STATUS_CANCEL_BUTTON)

    def edit_task_name(self, name, newName,confirm=True):
        """ 更新指定命名任务名称

                参数:
                    name: 任务名称
                    newName: 新的任务名称
                created by yuan xiaolu on 15th,Apr 2020
                """
        TASK_EDIT_XBUTTON = f'//div[text()="{name}"]/parent::*/following-sibling::td//i[contains(@class, "iconfont icon-edit")]'
        TaskPage.search_task_by_name(self, name)
        self.click(TASK_EDIT_XBUTTON, 3)
        self.sleep(5)
        TaskPage.input_task_name(self, name=newName)
        TASK_EDIT_CONFIRM_BUTTON = Dialog.get_dialog_footer_button_element(self, title="编辑")
        TASK_EDIT_CANCEL_BUTTON = Dialog.get_dialog_footer_button_element(self, title="编辑", confirm=False)
        if confirm:
            self.slow_click(TASK_EDIT_CONFIRM_BUTTON)
            TaskPage.search_task_by_name(self, newName)
        else:
            self.slow_click(TASK_EDIT_CANCEL_BUTTON)

    def detail_task_by_name(self, name):
        """ 查看指定命名任务

        参数:
            name: 任务名称
            created by yuan xiaolu on 17th,Apr 2020

        """
        TaskPage.search_task_by_name(self, name)
        TASK_DETAIL_XBUTTON = f'//div[text()="{name}"]/parent::*/following-sibling::td//i[contains(@class, "iconfont icon-view")]'
        self.click(TASK_DETAIL_XBUTTON, 3)
        self.sleep(3)
        TASK_NAME_XSPAN = '//label[text()="任务名称"]/parent::*//span'
        DEVICE_NAME_XSPAN = '//label[text()="设备"]/parent::*//span'
        ATTRIBUTES_XDIV = '//label[text()="特殊属性"]/parent::*//div'
        THRESHOLD_XSPAN = '//label[text()="阈值"]/parent::*//span'
        PORTRAIT_LIST_XSPAN = '//header[text()="人像库列表"]/parent::*//span[contains(@class, "el-tree-node__label")]'

    def close_task_detail_popup(self):
        """ 关闭任务详情窗口
            created by yuan xiaolu on 17th,Apr 2020
        """
        TASK_DETAIL_CLOSE_XBUTTON = '//div[@aria-label="详情"]/parent::*[not(contains(@style, "display: none;"))]//div[@class="el-dialog__header"]//button'
        self.click(TASK_DETAIL_CLOSE_XBUTTON)

    def add_face_alert_deployment_task(self, task, confirm=True):
        """ 添加人脸-布控任务

        参数:
            task: 布控任务实例
            confirm: 是否确认，默认为确认

        """
        TaskPage.click_task_tab_by_type(self, '人脸-布控任务')
        TaskPage.click_create_task_button(self)
        TaskPage.select_task_type(self, '人脸-布控任务')
        TaskPage.input_task_name(self, task.task_name)
        TaskPage.select_task_device_by_name(self, task.device_name)
        TaskPage.select_task_threshold(self, task.threshold)
        TaskPage.select_task_attributes(
            self, task.attributes)
        for portrait in task.portraits:
            TaskPage.select_task_portraits(self,portrait)
            # TASK_PORTRAIT_CHECKBOX_XINPUT = f'//div[@role="group"]//div[contains(text(), "{portrait}")]/parent::*/label/span/span'
            # self.slow_click(TASK_PORTRAIT_CHECKBOX_XINPUT)

        TASK_DIALOG_CONFIRM_INPUT = f'div[aria-label="{self.menu}"] > .el-dialog__footer > .dialog-footer > .el-button--primary'
        TASK_DIALOG_CANCEL_INPUT = f'div[aria-label="{self.menu}"] > .el-dialog__footer > .dialog-footer > .el-button--info'

        if confirm:
            self.slow_click(TASK_DIALOG_CONFIRM_INPUT)
        else:
            self.slow_click(TASK_DIALOG_CANCEL_INPUT)

    # def click_confirm_or_cancel_button_on_detail_or_edit_task_page(self, title, confirm=True):
    #     """
    #     :param self:
    #     :param title: 编辑，详情
    #     :param confirm: True表示确认，False表示取消
    #     :return: 元素定位器
    #     """
    #     if title in ["编辑", "详情"]:
    #         if confirm:
    #             return f'//div[@aria-label="{title}"]/parent::*[not(contains(@style, "display: none;"))]//div//div[@class="el-dialog__footer"]//button[@class="el-button el-button--primary"]'
    #         else:
    #             return f'//div[@aria-label="{title}"]/parent::*[not(contains(@style, "display: none;"))]//div//div[@class="el-dialog__footer"]//button[@class="el-button el-button--info"]'
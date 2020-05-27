#!/usr/bin/env python3

import os


from selenium.webdriver.common.by import By
from guard.pages.components.date_panel import DatePanel
from guard.pages.components.dialog import Dialog
from guard.pages.components.group_tree import GroupTree
from guard.pages.components.table_list import TableList
from guard.pages.base import BasePage
from guard.pages.classes.portrait import Portrait


class PortraitPage(BasePage):
    """ 人像库管理页面操作方法

    expend_portrait_database_by_type: 展开指定类型人像库
    click_portrait_database_by_name: 点击指定名称人像库
    input_portrait_database_name: 输入分组名称
    add_portrait_database_by_name: 添加指定命名和类型的人像库
    search_portrait_database_by_name: 搜索指定命名的人像库
    delete_portrait_database_by_name: 删除指定命名人像库
    rename_portrait_database_by_name: 重命名指定命名人像库
    view_portrait_database_by_name: 查看指定命名人像库
    click_add_portrait_button: 点击添加人像按钮
    upload_portrait_image: 上传人像图片
    input_portrait_name: 输入人像姓名
    input_portrait_alias: 输入人像别名
    input_portrait_id_number: 输入人像No.
    select_portrait_databases: 选择人像所在人像库
    set_gender_by_name: 设置人像性别
    input_portrait_age: 输入人像年龄
    input_portrait_company: 输入人像公司
    input_portrait_department: 输入人像部门
    input_portrait_contact: 输入人像联系方式
    input_portrait_license_plate: 输入人像车牌号
    input_portrait_address: 输入人像地址
    set_current_time_as_portrait_activation_time: 设置人像激活时间为当前时间
    set_portrait_activation_time: 设置人像激活时间
    set_portrait_expiration_time: 设置人像失效时间
    click_enable_status_switch: 点击人像启用状态开关
    add_portrait: 添加指定人像
    search_portrait_by_keyword: 通过关键字搜索指定人像
    edit_portrait_by_name: 编辑指定人像
    delete_portrait_by_keyword: 删除指定人像
    get_portrait_img_src_by_name: 获取指定人像图片地址

    """

    def expend_portrait_database_by_type(self, type):
        """ 展开指定类型人像库

        参数:
            type: 人像库类型，可选白名单、重点人员

        """
        PORTRIAT_DATABASE = f'//div[@title="{type}"]'
        PORTRIAT_DATABASE_DIV = f'//div[@title="{type}"]/parent::*/parent::*'
        is_expended = self.get_attribute(
            PORTRIAT_DATABASE_DIV, 'class')
        if 'is-expanded' not in is_expended:
            self.slow_click(PORTRIAT_DATABASE)

    def click_portrait_database_by_name(self, name, type='白名单'):
        """ 点击指定名称人像库

        参数:
            name: 人像库名称
            type: 人像库类型，默认为白名单，可选重点人员

        """
        PortraitPage.expend_portrait_database_by_type(self, type)
        GroupTree.click_group_by_name(self, name)

    def input_portrait_database_name(self, name):
        """ 输入分组名称

        参数:
            name: 人像库名称
        """
        GROUP_NAME_INPUT = '#red > div > input'
        self.update_text(GROUP_NAME_INPUT, name)

    def add_portrait_database_by_name(self, name, type='白名单', is_frontend=False, confirm=True):
        """ 添加指定命名和类型的人像库

        参数:
            name: 人像库名称
            type: 人像库类型，默认为白名单，可选重点人员
            is_frontend:
            confirm: 是否确认，默认为确认

        """
        GroupTree.click_group_menu_by_name(self, type, "创建下一级")
        GROUP_TYPE_XDROPDOWN = '//div[@class="el-dialog__body"]//input[@placeholder="请选择"]'
        GROUP_TYPE_XOPTION = f'//div[@class="el-scrollbar"][1]//span[text()="{type}"]'
        GROUP_IS_FRONTEND_XSWITCH = '//div[@class="el-dialog__body"]//div[@class="el-switch"]'

        self.click(GROUP_TYPE_XDROPDOWN)
        self.slow_click(GROUP_TYPE_XOPTION)
        PortraitPage.input_portrait_database_name(self, name)

        if is_frontend:
            self.click(GROUP_IS_FRONTEND_XSWITCH, delay=1)

        if confirm:
            Dialog.click_dialog_footer_button_by_text(self, '创建下一级', '确定')
        else:
            Dialog.click_dialog_footer_button_by_text(self, '创建下一级', '取消')

    def search_portrait_database_by_name(self, name):
        """ 搜索指定命名的人像库

        参数:
            name: 人像库名称

        """
        GroupTree.search_group_by_name(self, name)

    def delete_portrait_database_by_name(self, name, confirm=True):
        """ 删除指定命名人像库

        参数:
            name: 人像库名称
            confirm: 是否确认，默认为确认

        """
        PortraitPage.search_portrait_database_by_name(self, name)
        GroupTree.click_group_menu_by_name(self, name, menu='删除')

        if confirm:
            Dialog.click_dialog_footer_button_by_text(self, '删除', '删除')
        else:
            Dialog.click_dialog_footer_button_by_text(self, '删除', '取消')

    def rename_portrait_database_by_name(self, old_name, new_name, confirm=True):
        """ 重命名指定命名人像库

        参数:
            old_name: 原人像库名称
            new_name: 新人像库名称
            confirm: 是否确认，默认为确认

        """
        PortraitPage.search_portrait_database_by_name(self, old_name)
        GroupTree.click_group_menu_by_name(self, old_name, menu='重命名')
        PortraitPage.input_portrait_database_name(self, new_name)

        if confirm:
            Dialog.click_dialog_footer_button_by_text(self, '编辑', '确定')
        else:
            Dialog.click_dialog_footer_button_by_text(self, '编辑', '取消')

    def view_portrait_database_by_name(self, name, confirm=True):
        """ 查看指定命名人像库

        参数:
            name: 人像库名称
            confirm: 是否确认，默认为确认

        """
        PortraitPage.search_portrait_database_by_name(self, name)
        GroupTree.click_group_menu_by_name(self, name, menu='详情')

        if confirm:
            Dialog.click_dialog_footer_button_by_text(self, '详情', '确定')
        else:
            Dialog.click_dialog_footer_button_by_text(self, '详情', '取消')

    def click_add_portrait_button(self):
        """ 点击添加人像按钮

        @Author: YuanXiaolu

        """
        ADD_TARGET_XBUTTON = '//button[span="添加人像"]'
        self.click(ADD_TARGET_XBUTTON)

    def upload_portrait_image(self, title, path):
        """ 上传人像图片

        @Author: YuanXiaolu

        参数:
            title: 对话框标题,可选添加人像、编辑
            path: 人像图片的路径

        """
        if title == '添加人像':
            IMAGE_UPLOAD_INPUT = '#img-upload-btn'
        elif title == '编辑':
            IMAGE_UPLOAD_INPUT = '#img-upload-btn2'
        PortraitPage.upload_file_by_image_path(self, IMAGE_UPLOAD_INPUT, path)

    def input_portrait_name(self, title, name):
        """ 输入人像姓名

        @Author: YuanXiaolu

        参数:
            title: 对话框标题,可选添加人像、编辑
            name: 人像姓名

        """
        PORTRAIT_NAME_XINPUT = f'//div[@aria-label="{title}"]//label[text()="姓名"]/parent::*//input'
        self.update_text(PORTRAIT_NAME_XINPUT, name)

    def input_portrait_alias(self, title, alias='别名'):
        """ 输入人像别名

        @Author: YuanXiaolu

        参数:
            title: 对话框标题,可选添加人像、编辑
            alias: 人像人像别名，默认为别名

        """
        PORTRAIT_ALIAS_XINPUT = f'//div[@aria-label="{title}"]//label[text()="别名"]/parent::*//input'
        self.update_text(PORTRAIT_ALIAS_XINPUT, alias)

    def input_portrait_id_number(self, title, id_number):
        """ 输入人像No.

        @Author: YuanXiaolu

        参数:
            title: 对话框标题,可选添加人像、编辑
            id_number: 人像No.

        """
        PORTRAIT_ID_NUMBER_XINPUT = f'//div[@aria-label="{title}"]//label[text()="No."]/parent::*//input'
        self.update_text(PORTRAIT_ID_NUMBER_XINPUT, id_number)

    def select_portrait_databases(self, title, portrait_databases=[], confirm=True):
        """ 选择人像所在人像库

        参数:
            title: 对话框标题,可选添加人像、编辑
            portrait_databases: 人像库名称列表，举例: ['portrait_database_1', 'portrait_database_2']
            confirm: 是否确认，默认为确认

        """
        PORTRAIT_DATABASE_XINPUT = f'//div[@aria-label="{title}"]//label[text()="人像库"]/parent::*//div'
        self.slow_click(PORTRAIT_DATABASE_XINPUT)
        for portrait_database in portrait_databases:
            PORTRAIT_DATABASE_SEARCH_INPUT = '//div[@role="tooltip" and @aria-hidden="false"]//input[@type="text"]'
            self.update_text(PORTRAIT_DATABASE_SEARCH_INPUT, portrait_database)
            PORTAIT_DATABASE_IS_CHECKED_XBUTTON = '//div[@role="tooltip" and @aria-hidden="false"]//div[@role="treeitem" and @tabindex=0]'
            is_checked = self.get_attribute(
                PORTAIT_DATABASE_IS_CHECKED_XBUTTON, 'class')
            if not "is-checked" in is_checked:
                PORTRAIT_DATABASE_CHECKBOX_XINPUT = f'//span[@class="el-tree-node__label" and text()="{portrait_database}"]/parent::*//label'
                self.slow_click(PORTRAIT_DATABASE_CHECKBOX_XINPUT)

        if confirm:
            PORTRAIT_DATABASE_CONFIRM_XBUTTON = '//div[@role="tooltip" and @aria-hidden="false"]//span[text()="确定"]'
            self.slow_click(PORTRAIT_DATABASE_CONFIRM_XBUTTON)
        else:
            PORTRAIT_DATABASE_CANCEL_XBUTTON = '//div[@role="tooltip" and @aria-hidden="false"]//span[text()="取消"]'
            self.slow_click(PORTRAIT_DATABASE_CANCEL_XBUTTON)

    def set_gender_by_name(self, title, gender):
        """ 设置人像性别

        参数:
            title: 对话框标题,可选添加人像、编辑
            gender: 人像性别，可选男、女

        """
        PORTRAIT_GENDER_XRADIO = f'//div[@aria-label="{title}"]//span[@class="el-radio__label" and text()="{gender}"]'
        self.click(PORTRAIT_GENDER_XRADIO)

    def input_portrait_age(self, title, age=30):
        """ 输入人像年龄

        @Author: YuanXiaolu

        参数:
            title: 对话框标题,可选添加人像、编辑
            age: 人像年龄,默认为30

        """
        PORTRAIT_AGE_XINPUT = f'//div[@aria-label="{title}"]//label[text()="年龄"]/parent::*//input'
        self.update_text(PORTRAIT_AGE_XINPUT, age)

    def input_portrait_company(self, title, company='SENSETIME'):
        """ 输入人像公司

        @Author: YuanXiaolu

        参数:
            title: 对话框标题,可选添加人像、编辑
            company: 人像公司，默认为SENSETIME

        """
        PORTRAIT_COMPANY_XINPUT = f'//div[@aria-label="{title}"]//label[text()="公司"]/parent::*//input'
        self.update_text(PORTRAIT_COMPANY_XINPUT, company)

    def input_portrait_department(self, title, department='IDEA'):
        """ 输入人像部门

        @Author: YuanXiaolu

        参数:
            title: 对话框标题,可选添加人像、编辑
            department: 人像部门，默认为IDEA

        """
        PORTRAIT_DEPARTMENT_XINPUT = f'//div[@aria-label="{title}"]//label[text()="部门"]/parent::*//input'
        self.update_text(PORTRAIT_DEPARTMENT_XINPUT, department)

    def input_portrait_contact(self, title, contact='021-25201101'):
        """ 输入人像联系方式

        @Author: YuanXiaolu

        参数:
            title: 对话框标题,可选添加人像、编辑
            contact: 人像联系方式，默认为021-25201101

        """
        PORTRAIT_CONTACT_XINPUT = f'//div[@aria-label="{title}"]//label[text()="联系方式"]/parent::*//input'
        self.update_text(PORTRAIT_CONTACT_XINPUT, contact)

    def input_portrait_license_plate(self, title, license_plate='沪AAAAAA'):
        """ 输入人像车牌号

        @Author: YuanXiaolu

        参数:
            title: 对话框标题,可选添加人像、编辑
            license_plate: 人像车牌号，默认为沪AAAAAA

        """
        PORTRAIT_LICENSE_PLATE_XINPUT = f'//div[@aria-label="{title}"]//label[text()="车牌号"]/parent::*//input'
        self.update_text(PORTRAIT_LICENSE_PLATE_XINPUT, license_plate)

    def input_portrait_address(self, title, address='上海市徐汇区虹梅路1001'):
        """ 输入人像地址

        @Author: YuanXiaolu

        参数:
            title: 对话框标题,可选添加人像、编辑
            address: 人像地址，默认为上海市徐汇区虹梅路1001

        """
        PORTRAIT_ADDRESS_XINPUT = f'//div[@aria-label="{title}"]//label[text()="住址"]/parent::*//input'
        self.update_text(PORTRAIT_ADDRESS_XINPUT, address)

    def set_current_time_as_portrait_activation_time(self, title):
        """ 设置人像激活时间为当前时间

        @Author: YuanXiaolu

        参数:
            title: 对话框标题,可选添加人像、编辑

        """
        PORTRAIT_ACTIVATION_TIME_XBUTTON = f'//div[@aria-label="{title}"]//label[text()="激活时间"]/parent::*//input'
        PORTRAIT_CURRENT_TIME_XBUTTON = '//button[@class="el-button el-picker-panel__link-btn el-button--text el-button--mini"]'
        self.click(PORTRAIT_ACTIVATION_TIME_XBUTTON)
        self.slow_click(PORTRAIT_CURRENT_TIME_XBUTTON)

    def set_portrait_activation_time(self, title, time='2020-04-01 00:00:00'):
        """ 设置人像激活时间

        参数:
            title: 对话框标题,可选添加人像、编辑
            time: 人像激活时间，默认为2020-04-01 00:00:00

        """
        PORTRAIT_ACTIVATION_TIME_XBUTTON = f'//div[@aria-label="{title}"]//label[text()="激活时间"]/parent::*//input'
        self.update_text(PORTRAIT_ACTIVATION_TIME_XBUTTON, time)
        self.sleep(1)
        DatePanel.click_panel_footer_button_by_text(self, '确定')

    def set_portrait_expiration_time(self, title, time='2021-04-01 00:00:00'):
        """ 设置人像失效时间

        参数:
            title: 对话框标题,可选添加人像、编辑
            time: 人像失效时间，默认为2021-04-01 00:00:00

        """
        PORTRAIT_EXPIRATION_TIME_XBUTTON = f'//div[@aria-label="{title}"]//label[text()="失效时间"]/parent::*//input'
        self.update_text(PORTRAIT_EXPIRATION_TIME_XBUTTON, time)
        self.sleep(1)
        DatePanel.click_panel_footer_button_by_text(self, '确定')

    def click_enable_status_switch(self, title, is_enabled=True):
        """ 点击人像启用状态开关

        参数:
            title: 对话框标题,可选添加人像、编辑
            is_enabled: 人像启用状态，默认为True（启用），可选False（禁用）

        """
        PORTRAIT_ENABLE_STATUS_SWITCH_XDIV = f'//div[@aria-label="{title}"]//label[text()="启用状态"]/parent::*//div[@role="switch"]'
        PORTRAIT_ENABLE_STATUS_SWITCH_XBUTTON = f'//div[@aria-label="{title}"]//label[text()="启用状态"]/parent::*//span'
        switch_class = self.get_attribute(
            PORTRAIT_ENABLE_STATUS_SWITCH_XDIV, 'class')
        if is_enabled and switch_class == 'el-switch':
            self.slow_click(PORTRAIT_ENABLE_STATUS_SWITCH_XBUTTON)
        elif not is_enabled and switch_class == 'el-switch is-checked':
            self.slow_click(PORTRAIT_ENABLE_STATUS_SWITCH_XBUTTON)

    def add_portrait(self, portrait, confirm=True):
        """ 添加指定人像

        参数:
            portrait: 人像类实例
            confirm: 是否确认，默认为确认

        """
        PortraitPage.click_add_portrait_button(self)
        PortraitPage.upload_portrait_image(self, '添加人像', portrait.image_path)
        PortraitPage.input_portrait_name(self, '添加人像', portrait.name)
        PortraitPage.input_portrait_alias(self, '添加人像', portrait.alias)
        PortraitPage.input_portrait_id_number(self, '添加人像', portrait.id_number)
        PortraitPage.select_portrait_databases(
            self, '添加人像', portrait.portrait_databases)
        PortraitPage.set_gender_by_name(self, '添加人像', portrait.gender)
        PortraitPage.input_portrait_age(self, '添加人像', portrait.age)
        PortraitPage.input_portrait_company(self, '添加人像', portrait.company)
        PortraitPage.input_portrait_department(
            self, '添加人像', portrait.department)
        PortraitPage.input_portrait_contact(self, '添加人像', portrait.contact)
        PortraitPage.input_portrait_license_plate(
            self, '添加人像', portrait.license_plate)
        PortraitPage.input_portrait_address(self, '添加人像', portrait.address)
        PortraitPage.set_portrait_activation_time(
            self, '添加人像', portrait.activation_time)
        PortraitPage.set_portrait_expiration_time(
            self, '添加人像', portrait.expiration_time)
        PortraitPage.click_enable_status_switch(self, '添加人像')

        if confirm:
            Dialog.click_dialog_footer_button_by_text(self, '添加人像', '确定')
        else:
            Dialog.click_dialog_footer_button_by_text(self, '添加人像', '取消')
        self.sleep(3)

    def search_portrait_by_keyword(self, keyword):
        """ 通过关键字搜索指定人像

        @Author: YuanXiaolu

        参数:
            keyword: 关键字（姓名、No.、部门）

        """
        PORTRAIT_SEARCH_INPUT = '.inp-search > input'
        PORTRAIT_SEARCH_BUTTON = '.icon-search'
        self.update_text(PORTRAIT_SEARCH_INPUT, keyword)
        self.click(PORTRAIT_SEARCH_BUTTON)

    def edit_portrait_by_name(self, name, portrait, confirm=True):
        """ 编辑指定人像

        参数:
            name: 人像姓名
            portrait: 人像类实例
            confirm: 是否确认，默认为确认

        """
        PortraitPage.search_portrait_by_keyword(self, name)
        TableList.click_edit_button_by_name(self, name)

        PortraitPage.upload_portrait_image(self, '编辑', portrait.image_path)
        PortraitPage.input_portrait_name(self, '编辑', portrait.name)
        PortraitPage.input_portrait_alias(self, '编辑', portrait.alias)
        PortraitPage.input_portrait_id_number(self, '编辑', portrait.id_number)
        PortraitPage.select_portrait_databases(
            self, '编辑', portrait.portrait_databases)
        PortraitPage.set_gender_by_name(self, '编辑', portrait.gender)
        PortraitPage.input_portrait_age(self, '编辑', portrait.age)
        PortraitPage.input_portrait_company(self, '编辑', portrait.company)
        PortraitPage.input_portrait_department(self, '编辑', portrait.department)
        PortraitPage.input_portrait_contact(self, '编辑', portrait.contact)
        PortraitPage.input_portrait_license_plate(
            self, '编辑', portrait.license_plate)
        PortraitPage.input_portrait_address(self, '编辑', portrait.address)
        PortraitPage.set_portrait_activation_time(
            self, '编辑', portrait.activation_time)
        PortraitPage.set_portrait_expiration_time(
            self, '编辑', portrait.expiration_time)
        PortraitPage.click_enable_status_switch(self, '编辑')

        if confirm:
            Dialog.click_dialog_footer_button_by_text(self, '编辑', '确定')
        else:
            Dialog.click_dialog_footer_button_by_text(self, '编辑', '取消')
        self.sleep(3)

    def delete_portrait_by_name(self, name, from_current_group=False, confirm=True):
        """ 删除指定人像

        参数:
            name: 人像姓名
            from_current_group: 默认从总库中删除，可选True，从当前人像库中删除
            confirm: 是否确认，默认为确认

        """
        TableList.click_delete_button_by_name(self, name)

        if from_current_group and confirm:
            Dialog.click_dialog_footer_button_by_text(self, '删除', '仅从分组删除')
        elif not from_current_group and confirm:
            Dialog.click_dialog_footer_button_by_text(self, '删除', '从人像库删除')
        else:
            Dialog.click_dialog_footer_button_by_text(self, '删除', '取消')

    def get_portrait_img_src_by_name(self, name):
        """ 获取指定人像图片地址

        参数:
            name: 人像姓名

        返回:
            指定人像图片地址

        """
        PortraitPage.search_portrait_by_keyword(self, name)
        PORTRAIT_XIMG = f'//div[text()="{name}"]/parent::*/parent::*//img'
        return self.get_attribute(PORTRAIT_XIMG, 'src')

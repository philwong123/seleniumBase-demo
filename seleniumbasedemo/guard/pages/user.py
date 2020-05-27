#!/usr/bin/env python3

from selenium.webdriver.common.by import By
from guard.pages.components.group_tree import GroupTree
from guard.pages.base import BasePage


class UserPage(BasePage):
    """ 用户管理页面操作方法

    add_department_by_root_department_name: 添加指定命名的根节点部门
    add_department_by_parent_department_name: 添加指定命名的子部门
    search_department_by_name: 搜索指定命名的部门
    delete_department_by_name: 删除指定命名的部门
    click_add_user_button: 点击添加用户按钮
    input_username: 输入用户名
    input_name: 输入用户姓名
    select_role: 选择指定命名的角色
    select_status: 选择启用状态
    select_department: 选择指定命名的部门
    add_user_by_department_name: 添加用户
    search_user_by_name: 搜索指定命名的用户
    delete_user_by_name: 删除指定命名的用户

    """

    def add_department_by_root_department_name(self, name, is_peer=True, confirm=True):
        """ 添加指定命名的根节点部门

        参数:
            name: 部门名称
            is_peer: 是否同级或下一级，默认为同级
            confirm: 是否确认，默认为确认

        """
        if is_peer:
            GroupTree.click_group_menu_by_name(self, 'Default', '创建同级')
        else:
            GroupTree.click_group_menu_by_name(self, 'Default', '创建下一级')
        DEPARTMENT_NAME_INPUT = f'div[aria-label="{self.menu}"] > .el-dialog__body > div > span > div > input'
        CONFIRM_BUTTON = f'div[aria-label="{self.menu}"] > .el-dialog__footer > .dialog-footer > .el-button--primary'
        CANCEL_BUTTON = f'div[aria-label="{self.menu}"] > .el-dialog__footer > .dialog-footer > .el-button--info'
        self.update_text(DEPARTMENT_NAME_INPUT, name)
        if confirm:
            self.slow_click(CONFIRM_BUTTON)
        else:
            self.slow_click(CANCEL_BUTTON)

    def add_department_by_parent_department_name(self, name, parent_name='Default', is_peer=True, confirm=True):
        """ 添加指定命名的子部门

        参数:
            name: 子部门名称
            parent_name: 父部门名称，默认为Default
            is_peer: 是否同级或下一级，默认为同级
            confirm: 是否确认，默认为确认

        """
        if is_peer:
            GroupTree.click_group_menu_by_name(self, parent_name, '创建同级')
        else:
            GroupTree.click_group_menu_by_name(self, parent_name, '创建下一级')
        DEPARTMENT_NAME_INPUT = f'div[aria-label="{self.menu}"] > .el-dialog__body > div > span > div > input'
        CONFIRM_BUTTON = f'div[aria-label="{self.menu}"] > .el-dialog__footer > .dialog-footer > .el-button--primary'
        CANCEL_BUTTON = f'div[aria-label="{self.menu}"] > .el-dialog__footer > .dialog-footer > .el-button--info'
        self.update_text(DEPARTMENT_NAME_INPUT, name)
        if confirm:
            self.slow_click(CONFIRM_BUTTON)
        else:
            self.slow_click(CANCEL_BUTTON)

    def search_department_by_name(self, name):
        """ 搜索指定命名的部门

        参数:
            name: 部门名称

        """
        SEARCH_DEPARTMENT_INPUT = '.search-input > input'
        SEARCH_DEPARTMENT_BUTTON = '.el-icon-search'
        self.update_text(SEARCH_DEPARTMENT_INPUT, name)
        self.click(SEARCH_DEPARTMENT_BUTTON)

    def delete_department_by_name(self, name, confirm=True):
        """ 删除指定命名的部门 

        参数:
            name: 部门名称
            confirm: 是否确认，默认为确认

        """
        UserPage.search_department_by_name(self, name)
        GroupTree.click_group_menu_by_name(self, name, '删除')
        CANCEL_BUTTON = f'div[aria-label="{self.menu}"] > .el-dialog__footer > .dialog-footer > .el-button--info'
        DELETE_BUTTON = f'div[aria-label="{self.menu}"] > .el-dialog__footer > .dialog-footer > .el-button--danger'

        if confirm:
            self.slow_click(DELETE_BUTTON)
        else:
            self.slow_click(CANCEL_BUTTON)

    def click_add_user_button(self):
        """ 点击添加用户按钮 """
        self.menu = '添加用户'
        ADD_USER_XBUTTON = '//button/span[contains(text(),"添加用户")]'
        self.click(ADD_USER_XBUTTON, delay=2)

    def input_username(self, username):
        """ 输入用户名

        参数:
            username: 用户名

        """
        USERNAME_XINPUT = '//label[text()="用户名"]/parent::*//input'
        self.update_text(USERNAME_XINPUT, username)

    def input_name(self, name):
        """ 输入用户姓名

        参数:
            name: 姓名

        """
        NAME_XINPUT = '//label[text()="姓名"]/parent::*//input'
        self.update_text(NAME_XINPUT, name)

    def select_role(self, role='Administrator'):
        """ 选择指定命名的角色

        参数:
            role: 角色名称，默认为Administrator

        """
        ROLE_XDROPDOWN = '//label[text()="角色"]/parent::*//input'
        ROLE_XOPTION = f'//div[@class="el-scrollbar"][1]//span[text()="{role}"]'
        self.click(ROLE_XDROPDOWN)
        self.slow_click(ROLE_XOPTION)

    def select_status(self, status='启用'):
        """ 选择启用状态

        参数:
            status: 启用状态，默认为启用，可选禁用

        """
        STATUS_XDROPDOWN = '//label[text()="启用状态"]/parent::*//input'
        STATUS_XOPTION = f'//div[@class="el-scrollbar"][1]//span[text()="{status}"]'
        self.click(STATUS_XDROPDOWN)
        self.slow_click(STATUS_XOPTION)

    def select_department(self, department, confirm=True):
        """ 选择指定命名的部门

        参数:
            department: 部门名称
            confirm: 是否确认，默认为确认

        """
        DEPARTMENT_XINPUT = '//label[text()="部门"]/parent::*//div[@class="treeselsect-selected el-popover__reference"]//input[@type="text"]'
        DEPARTMENT_SEARCH_INPUT = '.auroraUI > div > div > div.el-input > input'
        DEPARTMENT_RADIO_XINPUT = f'//span[@class="el-radio__label" and contains(text(), "{department}")]'
        DEPARTMENT_CONFIRM_INPUT = '.auroraUI > div > div > div.treeselsect-btns > .el-button--primary'
        DEPARTMENT_CANCEL_INPUT = '.auroraUI > div > div > div.treeselsect-btns > .el-button--info'

        self.slow_click(DEPARTMENT_XINPUT)
        self.click(DEPARTMENT_SEARCH_INPUT, delay=1)
        self.update_text(DEPARTMENT_SEARCH_INPUT, department)
        self.click(DEPARTMENT_RADIO_XINPUT)
        if confirm:
            self.slow_click(DEPARTMENT_CONFIRM_INPUT)
        else:
            self.slow_click(DEPARTMENT_CANCEL_INPUT)

    def add_user_by_department_name(self, user, confirm=True):
        """ 添加用户

        参数:
            user: 用户实例
            confirm: 是否确认，默认为确认

        """
        UserPage.click_add_user_button(self)
        UserPage.input_username(self, user.username)
        UserPage.input_name(self, user.name)
        UserPage.select_role(self, user.role)
        UserPage.select_status(self, user.status)
        UserPage.select_department(self, user.department)

        ADD_USER_DIALOG_CONFIRM_INPUT = f'div[aria-label="{self.menu}"] > .el-dialog__footer > .dialog-footer > .el-button--primary'
        ADD_USER_DIALOG_CANCEL_INPUT = f'div[aria-label="{self.menu}"] > .el-dialog__footer > .dialog-footer > .el-button--info'

        if confirm:
            self.slow_click(ADD_USER_DIALOG_CONFIRM_INPUT)
        else:
            self.slow_click(ADD_USER_DIALOG_CANCEL_INPUT)

    def search_user_by_name(self, name):
        """ 搜索指定命名的用户

        参数:
            name: 用户名

        """
        SEARCH_USER_INPUT = '.userInp > .el-input__inner'
        SEARCH_USER_BUTTON = '.userInp > span > span > span > .el-icon-search'
        self.update_text(SEARCH_USER_INPUT, name)
        self.click(SEARCH_USER_BUTTON)

    def delete_user_by_name(self, name, confirm=True):
        """ 删除指定命名的用户

        参数:
            name: 用户名
            confirm: 是否确认，默认为确认

        """
        USER_DELETE_XBUTTON = f'//div[text()="{name}"]/parent::*/following-sibling::td//i[contains(@class, "icon-delete")]'
        UserPage.search_user_by_name(self, name)
        self.click(USER_DELETE_XBUTTON, 2)

        DELETE_USER_DIALOG_CONFIRM_INPUT = '#app > div > div.main-container > section > section > div:nth-child(8) > div > div > div.el-dialog__footer > span > button.el-button.el-button--danger'
        DELETE_USER_DIALOG_CANCEL_INPUT = '#app > div > div.main-container > section > section > div:nth-child(8) > div > div > div.el-dialog__footer > span > button.el-button.cancel.el-button--info'

        if confirm:
            self.slow_click(DELETE_USER_DIALOG_CONFIRM_INPUT)
        else:
            self.slow_click(DELETE_USER_DIALOG_CANCEL_INPUT)

    def reset_user_password(self, name, confirm=True):
        """ 重置用户密码

        参数:
            name: 用户名
            confirm: 是否确认，默认为确认

        """
        USER_EDIT_BUTTON = f'//div[text()="{name}"]/parent::*/following-sibling::td//i[contains(@class, "iconfont icon-view")]'
        USER_RESET_PASSWORD_BUTTON = '//*[@id="app"]/div/div[1]/section/section/div[7]/div[1]/div/div[3]/span/button[1]/span'
        USER_RESET_PASSWORD_CONFIRM_BUTTON = '#app > div > div.main-container > section > section > div:nth-child(9) > div:nth-child(2) > div > div.el-dialog__footer > span > button.el-button.el-button--primary > span'
        USER_RESET_PASSWORD_CANCEL_BUTTON = '#app > div > div.main-container > section > section > div:nth-child(9) > div:nth-child(2) > div > div.el-dialog__footer > span > button.el-button.cancel.el-button--info > span'
        # USER_RESET_PASSWORD_GET_NEW_PASSWORD = '//span[text()="密码已经成功重置为："]/parent::*/span[2]'
        USER_RESET_PASSWORD_GET_NEW_PASSWORD = 'div[aria-label="提示"] > .el-dialog__body > div > span:nth-child(2)'
        UserPage.search_user_by_name(self, name)
        self.click(USER_EDIT_BUTTON, 2)
        self.click(USER_RESET_PASSWORD_BUTTON, 2)
        if confirm:
            self.slow_click(USER_RESET_PASSWORD_CONFIRM_BUTTON)
            default_password = self.get_text(USER_RESET_PASSWORD_GET_NEW_PASSWORD)
            return default_password.strip()
        else:
            self.slow_click(USER_RESET_PASSWORD_CANCEL_BUTTON)

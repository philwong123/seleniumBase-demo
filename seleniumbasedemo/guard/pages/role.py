#!/usr/bin/env python3
from guard.pages.base import BasePage
import logging
import re
from selenium.webdriver.common.keys import Keys


class RolePage(BasePage):
    """ 角色管理页面操作方法

    click_add_role_button: 点击角色按钮
    input_role_name: 输入角色名称
    add_permissions: 勾选指定权限
    add_role_by_name: 添加指定命名和权限的角色
    delete_role_by_name: 删除指定命名的角色
    export_role_data：导出角色数据

    """
    def click_add_role_button(self):
        """ 点击角色按钮 """
        self.menu = '添加角色'
        ADD_ROLE_XBUTTON = '//span[contains(text(),"添加角色")]'
        self.click(ADD_ROLE_XBUTTON)

    def input_role_name(self, name):
        """输入角色名称

        :param name: 角色名称
        :return:
        """
        ADD_ROLE_NAME_XINPUT = '//label[text()="角色名称"]/parent::*//input'
        self.update_text(ADD_ROLE_NAME_XINPUT, name)

    def add_permissions(self, permissions):
        """勾选指定权限

        :param permissions: {'权限':['全选']}、{'系统信息':['查看']}等
        :return:
        """
        for module, operations in permissions.items():
            for operation in operations:
                PERMISSION_XCHECKBOX = f'//label[contains(text(),"{module}")]/parent::*//span[contains(text(),"{operation}")]/parent::*//span[@class="el-checkbox__input"]'
                self.click(PERMISSION_XCHECKBOX, delay=1)

    def add_role_by_name(self, name, permissions={}, confirm=True):
        """添加指定命名和权限的角色

        :param name: 角色名称
        :param permissions: 角色权限，默认为空，可选{'权限':['全选']}、{'系统信息':['查看']}等
        :param confirm:
        :return: 确认/取消，默认为确认
        """
        RolePage.click_add_role_button(self)
        RolePage.input_role_name(self, name)
        RolePage.add_permissions(self, permissions)
        CONFIRM_BUTTON = f'div[aria-label="{self.menu}"] > .el-dialog__footer > .dialog-footer > .el-button--primary'
        CANCEL_BUTTON = f'div[aria-label="{self.menu}"] > .el-dialog__footer > .dialog-footer > .el-button--info'
        self.slow_click(CONFIRM_BUTTON) if confirm else self.slow_click(CANCEL_BUTTON)

    def delete_role_by_name(self, name, confirm=True):
        """删除指定命名的角色

        :param name: 角色名称
        :param confirm: 确认/取消，默认为确认
        :return:
        """
        self.menu = '删除'
        ROLE_DELETE_XBUTTON = f'//div[text()="{name}"]/parent::*/following-sibling::td//i[contains(@class, "icon-delete")]'
        CANCEL_BUTTON = f'div[aria-label="{self.menu}"] > .el-dialog__footer > .dialog-footer > .el-button--info'
        DELETE_BUTTON = f'div[aria-label="{self.menu}"] > .el-dialog__footer > .dialog-footer > .el-button--danger'
        RolePage.search_role_by_name(self, name)
        self.click(ROLE_DELETE_XBUTTON)
        self.slow_click(DELETE_BUTTON) if confirm else self.slow_click(CANCEL_BUTTON)


    def edit_role_by_name(self, name, permissions, confirm=True):
        """ 编辑指定命名的角色

           :param name 角色名称
           :param permissions: {'权限':['全选']}、{'系统信息':['查看']}等
           :param confirm: 确认/取消，默认为确认
           :return:
        """
        self.menu = '编辑'
        ROLE_EDIT_BUTTON = f'//div[text()="{name}"]/parent::*/following-sibling::td//i[contains(@class, "icon-edit")]'
        CANCEL_BUTTON = f'div[aria-label="{self.menu}"] > .el-dialog__footer > .dialog-footer > .el-button--info'
        CONFIRM_BUTTON = f'div[aria-label="{self.menu}"] > .el-dialog__footer > .dialog-footer > .el-button--primary'
        self.click(ROLE_EDIT_BUTTON)
        for module, operations in permissions.items():
            for operation in operations:
                PERMISSION_XCHECKBOX = f'//label[contains(text(),"{module}")]/parent::*//span[contains(text(),"{operation}")]/parent::*//span[@class="el-checkbox__input"]'
                self.click(PERMISSION_XCHECKBOX, delay=1)
        self.slow_click(CONFIRM_BUTTON) if confirm else self.slow_click(CANCEL_BUTTON)

    def enable_role_by_name(self, name, disable=False, confirm=True):
        """启用/禁用角色

        :param name: 角色名称
        :param disable: 是否禁用，默认为否
        :param confirm: 确认/取消，默认为确认
        :return:
        """
        self.menu = '提示'
        ROLE_ENABLE_BUTTON = f'//div[text()="{name}"]/parent::*/following-sibling::td//div[contains(@class, "el-switch")]'
        ROLE_DISABLE_BUTTON = f'//div[text()="{name}"]/parent::*/following-sibling::td//div[contains(@class, "el-switch is-checked")]'
        CANCEL_BUTTON = f'div[aria-label="{self.menu}"] > .el-dialog__footer > .dialog-footer > .el-button--info'
        CONFIRM_BUTTON = f'div[aria-label="{self.menu}"] > .el-dialog__footer > .dialog-footer > .el-button--primary'
        RolePage.search_role_by_name(self, name)
        self.click(ROLE_ENABLE_BUTTON) if disable is False else self.click(ROLE_DISABLE_BUTTON)
        self.slow_click(CONFIRM_BUTTON) if confirm else self.slow_click(CANCEL_BUTTON)
        return True


    def export_role_data(self, start, end, confirm=True):
        """导出角色数据

        :param start: 导出起始数字
        :param end: 导出终止数字
        :param confirm: 确认按钮
        :return:
        """
        ROLE_EXPORT_BUTTON = '//button/span[contains(text(), "导出")]'
        ROLE_EXPORT_CONFIRM_BUTTON = '//button/span[contains(text(), "确定")]'
        ROLE_EXPORT_CANCEL_BUTTON = '//button/span[contains(text(), "取消")]'
        self.click(ROLE_EXPORT_BUTTON)
        EXPORT_START_INDEX = 'div.outNum > div:nth-child(2) > input'
        EXPORT_END_INDEX = 'div.outNum > div:nth-child(4) > input'
        self.update_text(EXPORT_START_INDEX, start)
        self.update_text(EXPORT_END_INDEX, end)
        if confirm:
            try:
                flag = self.driver.find_element_by_xpath(ROLE_EXPORT_CONFIRM_BUTTON+'/..').is_enabled()
                if not flag:
                    return flag
                self.slow_click(ROLE_EXPORT_CONFIRM_BUTTON)
            except Exception as e:
                logging.error(e)
        else:
            self.slow_click(ROLE_EXPORT_CANCEL_BUTTON)

    def checkbox_relevance_check(self, permissions):
        """检查同一模块下查看与其他权限的级联关系

        :param permissions: 模块对应的操作权限 eg.{'访客': ['查看', '添加', '修改', '删除', '导出']}
        :return:
        """
        for module, operations in permissions.items():
            for operation in operations:
                VIEW_PERMISSION_XCHECKBOX_SELETED = f'//label[contains(text(),"{module}")]/parent::*//span[contains(text(),"查看")]/parent::*//span[contains(@class,"is-checked")]'
                VIEW_PERMISSION_XCHECKBOX_UNSELETED = f'//label[contains(text(),"{module}")]/../div/div/label/span[@class="el-checkbox__input"]'
                PERMISSION_XCHECKBOX = f'//label[contains(text(),"{module}")]/parent::*//span[contains(text(),"{operation}")]/parent::*//span[contains(@class,"el-checkbox__input")]'
                PERMISSION_XCHECKBOX_SELECTED = f'//label[contains(text(),"{module}")]/parent::*//span[contains(text(),"{operation}")]/parent::*//span[contains(@class,"is-checked")]'
                PERMISSION_XCHECKBOX_UNSELECTED = f'//label[contains(text(),"{module}")]/parent::*//span[contains(text(),"{operation}")]/parent::*//span[@class="el-checkbox__input"]'
                if not operation == "查看":
                    self.click(PERMISSION_XCHECKBOX, delay=1)
                    view_is_selected = self.driver.find_element_by_xpath(VIEW_PERMISSION_XCHECKBOX_SELETED).is_displayed()
                    operation_is_selected = self.driver.find_element_by_xpath(PERMISSION_XCHECKBOX_SELECTED).is_displayed()
                    logging.info({f"{module} {operation}_is_selected": operation_is_selected})
                    if operation_is_selected:
                        assert view_is_selected is True
                    self.sleep(1)
                    self.click(VIEW_PERMISSION_XCHECKBOX_SELETED, delay=1)
                    view_is_unselected = self.driver.find_element_by_xpath(VIEW_PERMISSION_XCHECKBOX_UNSELETED).is_displayed()
                    operation_is_unselected = self.driver.find_element_by_xpath(PERMISSION_XCHECKBOX_UNSELECTED).is_displayed()
                    logging.info({f"{module} {operation}_is_unselected": operation_is_unselected})
                    if view_is_unselected:
                        assert operation_is_unselected is True
                    RolePage.clear_checkbox(self)

    def clear_checkbox(self):
        """ 清除全选"""
        ALL_PERMISSION_XCHECKBOX_SELECTED = '//label[contains(text(),"权限")]/../div/label/span[contains(@class,"el-checkbox__input")]'
        ALL_PERMISSION_XCHECKBOX_DESELECTED = '//label[contains(text(),"权限")]/../div/label/span[contains(@class, "is-checked")]'
        self.sleep(1)
        self.click(ALL_PERMISSION_XCHECKBOX_SELECTED, delay=1)
        self.sleep(1)
        self.click(ALL_PERMISSION_XCHECKBOX_DESELECTED, delay=1)

    def enabled_operation_check(self, name, permissions):
        """

        :param name：角色名字
        :param permissions: 模块对应的操作权限
        :return:
        """
        flags = dict()
        ROLE_VIEW_BUTTON = f'//div[text()="{name}"]/parent::*/following-sibling::td//i[contains(@class, "icon-edit")]'
        self.click(ROLE_VIEW_BUTTON)
        self.sleep(2)
        for module, operations in permissions.items():
            for operation in operations:
                PERMISSION_CHECKBOX_SELECTED = f'//label[contains(text(),"{module}")]/parent::*//span[contains(text(),"{operation}")]/parent::*//span[contains(@class, "is-checked")]'
                flag = self.driver.find_element_by_xpath(PERMISSION_CHECKBOX_SELECTED).is_enabled()
                flags[operation] = flag
        return flags

    def get_current_role_num(self):
        """

        :return: 当前页面已创建的角色数量
        """
        ROLE_NUM = '//div/span[contains(text(), "角色数量")]'
        element = self.driver.find_element_by_xpath(ROLE_NUM).text
        num = re.findall("\w+\s+(\d+)", element)
        return int(num[0])

    def export_role_exceed_max(self, start, end):
        """【异常】导出终止数大于最大数目

        :param start: 导出起始数
        :param end: 导出终止数
        :return:
        """
        max_num = RolePage.get_current_role_num(self)
        ROLE_EXPORT_BUTTON = '//button/span[contains(text(), "导出")]'
        ROLE_EXPORT_CONFIRM_BUTTON = '//button/span[contains(text(), "确定")]'
        ALERT_MESSAGE = f'//div/span[contains(text(), "当前可导出的记录总数为{max_num}条，请检查输入")]'
        self.click(ROLE_EXPORT_BUTTON)
        EXPORT_START_INDEX = 'div.outNum > div:nth-child(2) > input'
        EXPORT_END_INDEX = 'div.outNum > div:nth-child(4) > input'
        self.update_text(EXPORT_START_INDEX, start)
        self.update_text(EXPORT_END_INDEX, end)
        self.slow_click(ROLE_EXPORT_CONFIRM_BUTTON)
        flag = self.driver.find_element_by_xpath(ALERT_MESSAGE).is_displayed()
        return flag

    def search_role_by_name(self, name, exist=True):
        """搜索指定命名的角色

        :param name: 角色名
        :param exsit: 角色是否存在，默认存在
        :return:
        """
        SEARCH_ROLE_INPUT = '//div[contains(@class, "search-input-role")]/input'
        SEARCH_ROLE_BUTTON = '//span/i[contains(@class, "el-icon-search")]'
        SEARCH_EMPTY_RESULT = '//span[text()="暂无数据"]'
        self.update_text(SEARCH_ROLE_INPUT, name)
        self.click(SEARCH_ROLE_BUTTON)
        self.sleep(1)
        if exist is False:
            return self.driver.find_element_by_xpath(SEARCH_EMPTY_RESULT).is_displayed()
        return True

    def rename_role_name(self, src_name, target_name, confirm=True):
        """重命名role name

        :param src_name: 原始role名字
        :param target_name: 重命名名字
        :param confirm: 是否确认，默认是
        :return:
        """
        ROLE_EDIT_BUTTON = f'//div[text()="{src_name}"]/parent::*/following-sibling::td//i[contains(@class, "icon-edit")]'
        CANCEL_BUTTON = f'div[aria-label="编辑"] > .el-dialog__footer > .dialog-footer > .el-button--info'
        CONFIRM_BUTTON = f'div[aria-label="编辑"] > .el-dialog__footer > .dialog-footer > .el-button--primary'
        self.click(ROLE_EDIT_BUTTON)
        RolePage.input_role_name(self, target_name)
        self.slow_click(CONFIRM_BUTTON) if confirm else self.slow_click(CANCEL_BUTTON)

    def jump_to_specific_page(self, index=1):
        """跳转指定页面

        :param index: 跳转页面的数字，默认第一页
        :return:
        """
        INDEX_INPUT = '//span[@class="el-pagination__jump"]/div/input'
        self.update_text(INDEX_INPUT, index)
        self.sleep(1)
        self.driver.find_element_by_xpath(INDEX_INPUT).send_keys(Keys.ENTER)

    def jump_to_next_page(self):
        """跳转到下一页

        :return:
        """
        NEXT_PAGE_BUTTON = '//button[@class="btn-next"]/i'
        self.slow_click(NEXT_PAGE_BUTTON)

    def jump_to_previous_page(self):
        """跳转到上一页

        :return:
        """
        PREVIOUS_PAGE_BUTTON = '//button[@class="btn-prev"]/i'
        self.slow_click(PREVIOUS_PAGE_BUTTON)

    def check_current_page(self, index):
        """检查当前页面是否为指定页面

        :param index: 当前页面索引
        :return:
        """
        ACTIVE_PAGE = f'//ul[@class="el-pager"]/li[text()={index}]'
        page_state = self.driver.find_element_by_xpath(ACTIVE_PAGE).get_attribute("class")
        if page_state == 'number active':
            return True
        return False

    def view_role_details(self, name):
        """查看角色详情

        :param name: 角色名
        :return:
        """
        VIEW_BUTTON = f'//div[text()="{name}"]/parent::*/following-sibling::td//i[contains(@class, "icon-view")]'
        self.click(VIEW_BUTTON)


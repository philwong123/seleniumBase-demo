#!/usr/bin/env python3

from selenium.webdriver.common.by import By
from guard.pages.components.group_tree import GroupTree
from guard.pages.base import BasePage


class MapPage(BasePage):
    """ 地图管理操作方法

    add_floor_by_root_floor_name: 添加指定命名的根节点楼层
    add_floor_by_parent_name: 添加指定命名的子楼层
    search_floor_by_name: 搜索指定命名的楼层
    delete_floor_by_name: 删除指定命名的楼层
    click_cancel_in_dialog: 点击对话框取消按钮
    rename_floor_by_root_floor_name: 重命名根节点楼层名称
    rename_floor_by_parent_name: 重命名子楼层名称
    
    """

    def add_floor_by_root_floor_name(self, name, is_peer=True, confirm=True):
        """ 添加指定命名的根节点楼层

        参数:
            name: 楼层名称
            is_peer: 是否同级或下一级，默认为同级
            confirm: 是否确认，默认为确认

        """
        if is_peer:
            GroupTree.click_group_menu_by_name(self, 'Default', '创建同级')
        else:
            GroupTree.click_group_menu_by_name(self, 'Default', '创建下一级')
        GROUP_NAME_INPUT = f'div[aria-label="{self.menu}"] > .el-dialog__body > .el-form > div > div > div > input '
        CONFIRM_BUTTON = f'div[aria-label="{self.menu}"] > .el-dialog__footer > .dialog-footer > .el-button--primary'
        CANCEL_BUTTON = f'div[aria-label="{self.menu}"] > .el-dialog__footer > .dialog-footer > .el-button--info'
        self.update_text(GROUP_NAME_INPUT, name)
        if confirm:
            self.slow_click(CONFIRM_BUTTON)
        else:
            self.slow_click(CANCEL_BUTTON)

    def add_floor_by_parent_name(self, name, parent_name='Default', is_peer=True, confirm=True):
        """ 添加指定命名的子楼层

        参数:
            name: 子楼层名称
            parent_name: 父楼层名称，默认为Default
            is_peer: 是否同级或下一级，默认为同级
            confirm: 是否确认，默认为确认

        """
        if is_peer:
            GroupTree.click_group_menu_by_name(self, parent_name, '创建同级')
        else:
            GroupTree.click_group_menu_by_name(self, parent_name, '创建下一级')
        GROUP_NAME_INPUT = f'div[aria-label="{self.menu}"] > .el-dialog__body > .el-form > div > div > div > input '
        CONFIRM_BUTTON = f'div[aria-label="{self.menu}"] > .el-dialog__footer > .dialog-footer > .el-button--primary'
        CANCEL_BUTTON = f'div[aria-label="{self.menu}"] > .el-dialog__footer > .dialog-footer > .el-button--info'
        self.update_text(GROUP_NAME_INPUT, name)
        if confirm:
            self.slow_click(CONFIRM_BUTTON)
        else:
            self.slow_click(CANCEL_BUTTON)

    def search_floor_by_name(self, name):
        """ 搜索指定命名的楼层
        
        参数:
            name: 楼层名称

        """
        SEARCH_FLOOR_INPUT = '.search-input > input'
        SEARCH_FLOOR_BUTTON = '.el-icon-search'
        self.update_text(SEARCH_FLOOR_INPUT, name)
        self.click(SEARCH_FLOOR_BUTTON)

    def delete_floor_by_name(self, name, confirm=True):
        """ 删除指定命名的楼层

        参数:
            name: 楼层名称
            confirm: 是否确认，默认为确认

        """
        MapPage.search_floor_by_name(self, name)
        GroupTree.click_group_menu_by_name(self, name, '删除')
        CANCEL_BUTTON = f'div[aria-label="{self.menu}"] > .el-message-box > .el-message-box__btns > .el-button--info'
        DELETE_BUTTON = f'div[aria-label="{self.menu}"] > .el-message-box > .el-message-box__btns > .el-button--danger'

        if confirm:
            self.slow_click(DELETE_BUTTON)
        else:
            self.slow_click(CANCEL_BUTTON)

    def click_cancel_in_dialog(self):
        """ 点击对话框取消按钮 """
        CANCEL_BUTTON = f'div[aria-label="{self.menu}"] > .el-dialog__footer > .dialog-footer > .el-button--info'
        self.slow_click(CANCEL_BUTTON)

    def rename_floor_by_root_floor_name(self, old_name, new_name, confirm=True):
        """ 重命名根节点楼层名称

        参数:
            old_name: 原楼层名称
            new_name: 新楼层名称
            confirm: 是否确认，默认为确认

        """
        GroupTree.click_group_menu_by_name(self, old_name, '重命名')
        GROUP_NAME_INPUT = f'div[aria-label="{self.menu}"] > .el-dialog__body > .el-form > div > div > div > input '
        CONFIRM_BUTTON = f'div[aria-label="{self.menu}"] > .el-dialog__footer > .dialog-footer > .el-button--primary'
        CANCEL_BUTTON = f'div[aria-label="{self.menu}"] > .el-dialog__footer > .dialog-footer > .el-button--info'
        self.update_text(GROUP_NAME_INPUT, new_name)
        if confirm:
            self.slow_click(CONFIRM_BUTTON)
        else:
            self.slow_click(CANCEL_BUTTON)

    def rename_floor_by_parent_name(self, old_name, new_name, parent_name='Default', confirm=True):
        """ 重命名子楼层名称

        参数:
            old_name: 原楼层名称
            new_name: 新楼层名称
            parent_name: 父楼层名称，默认为Default
            confirm: 是否确认，默认为确认

        """
        GroupTree.click_group_by_name(self, parent_name)
        GroupTree.click_group_menu_by_name(self, old_name, '重命名')
        GROUP_NAME_INPUT = f'div[aria-label="{self.menu}"] > .el-dialog__body > .el-form > div > div > div > input '
        CONFIRM_BUTTON = f'div[aria-label="{self.menu}"] > .el-dialog__footer > .dialog-footer > .el-button--primary'
        CANCEL_BUTTON = f'div[aria-label="{self.menu}"] > .el-dialog__footer > .dialog-footer > .el-button--info'
        self.update_text(GROUP_NAME_INPUT, new_name)
        if confirm:
            self.slow_click(CONFIRM_BUTTON)
        else:
            self.slow_click(CANCEL_BUTTON)

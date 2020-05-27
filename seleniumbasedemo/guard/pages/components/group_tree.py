#!/usr/bin/env python3

from selenium.webdriver.common.by import By
from guard.pages.base import BasePage


class GroupTree(BasePage):
    """ 分组树型组件基本页面操作方法

    click_more_menu_by_name: 点击指定命名的分组弹出更多操作菜单
    click_group_by_name: 点击指定命名的分组
    click_group_menu_by_name: 点击指定命名的分组并点击对应菜单
    search_group_by_name: 搜索指定命名的分组

    """
    menus = {
        '创建下一级': 'Create a subordinate group',
        '创建同级': 'Create a peer group',
        '详情': 'Detail',
        '重命名': 'Rename',
        '删除': 'Delete'
    }

    def click_more_menu_by_name(self, name='白名单'):
        """ 点击指定命名的分组弹出更多操作菜单

        参数:
            name: 分组名称，默认值为白名单 
        """
        GROUP_POPUP_XLINK = f'//div[@title="{name}"]/parent::*/following-sibling::div'
        BasePage.hover_on_element_by_xpath(self, GROUP_POPUP_XLINK)

    def click_group_by_name(self, name):
        """ 点击指定命名的分组

        参数:
            name: 分组名称        
        """
        GROUP_NAME_XDIV = f'//div[@title="{name}"]'
        self.slow_scroll_to(GROUP_NAME_XDIV)
        self.click(GROUP_NAME_XDIV)

    def click_group_menu_by_name(self, name, menu='创建同级', locale='中文'):
        """ 点击指定命名的分组并点击对应菜单

        参数:
            name: 分组名称
            menu: 更多操作菜单名称，默认值为创建同级
            locale: 语言设置，默认值为中文
        """
        GroupTree.click_group_by_name(self, name)
        if locale == '中文':
            self.menu = menu
        else:
            self.menu = menus[menu]

        GroupTree.click_more_menu_by_name(self, name)
        GROUP_POPUP_XMENU = f'//li[@class="menu" and contains(text(),"{menu}")]'
        self.click(GROUP_POPUP_XMENU, by=By.XPATH, delay=1)

    def search_group_by_name(self, name):
        """ 搜索指定命名的分组

        参数:
            name: 分组名称
        """
        GROUP_SEARCH_TEXT = '.search-input > input'
        GROUP_SEARCH_BUTTON = '.search-input > span > span > span > i.el-icon-search'

        self.sleep(2)
        self.update_text(GROUP_SEARCH_TEXT, name)
        self.slow_click(GROUP_SEARCH_BUTTON)

    def assert_group_is_visible(self, name):
        """ 检查指定命名的分组可见

        参数:
            name: 分组名称
        """
        GROUP_NAME_XDIV = f'//div[@title="{name}"]'
        self.is_element_visible(GROUP_NAME_XDIV)

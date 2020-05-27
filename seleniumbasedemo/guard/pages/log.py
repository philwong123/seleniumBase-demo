#!/usr/bin/env python3


from selenium.webdriver.common.by import By
from guard.pages.components.table_list import TableList
from guard.pages.base import BasePage


class LogPage(BasePage):
    """ 日志页面操作方法

    click_module_filter: 点击过滤模块
    click_operations_filter: 点击过滤操作
    filter_log_by_module_name: 按模块名称过滤日志
    filter_log_by_operations_name: 按操作名称过滤日志

    """

    def click_module_filter(self):
        """ 点击过滤模块 """
        TableList.click_arrow_down_button_by_column_name(self, '模块')

    def click_operations_filter(self):
        """ 点击过滤操作 """
        TableList.click_arrow_down_button_by_column_name(self, '操作')

    def filter_log_by_module_name(self, name):
        """ 按模块名称过滤日志

        参数:
            name: 模块名称

        """
        LogPage.click_module_filter(self)
        TableList.click_table_filter_item_by_name(self, name)

    def filter_log_by_operations_name(self, name):
        """ 按操作名称过滤日志

        参数:
            name: 操作名称

        """
        LogPage.click_operations_filter(self)
        TableList.click_table_filter_item_by_name(self, name)

    


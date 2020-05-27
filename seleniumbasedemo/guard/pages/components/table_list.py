#!/usr/bin/env python3

import re

from selenium.webdriver.common.by import By
from guard.pages.base import BasePage


class TableList(BasePage):
    """ 表格列表基本操作方法

    click_view_button_by_name: 点击表格列表中查看按钮
    click_edit_button_by_name: 点击表格列表中编辑按钮
    click_delete_button_by_name: 点击表格列表中删除按钮
    click_arrow_down_button_by_column_name: 点击表格指定列的下拉箭头
    click_table_filter_item_by_name: 点击指定表过滤项
    get_column_index_by_name: 获取指定列的索引
    get_number_of_rows_in_column_by_containing_text: 获取指定列包含指定文本的行数
    get_number_of_rows_in_column_by_not_containing_text: 获取指定列不包含指定文本的行数

    """

    def click_view_button_by_name(self, name):
        """ 点击表格列表中查看按钮

        参数:
            name: 名称

        """
        TABLE_LIST_VIEW_XBUTTON = f'//div[text()="{name}"]/parent::*/following-sibling::td//i[contains(@class, "icon-view")]'
        self.click(TABLE_LIST_VIEW_XBUTTON)

    def click_edit_button_by_name(self, name):
        """ 点击表格列表中编辑按钮

        参数:
            name: 名称

        """
        TABLE_LIST_EDIT_XBUTTON = f'//div[text()="{name}"]/parent::*/following-sibling::td//i[contains(@class, "icon-edit")]'
        self.click(TABLE_LIST_EDIT_XBUTTON)

    def click_delete_button_by_name(self, name):
        """ 点击表格列表中删除按钮

        参数:
            name: 名称

        """
        TABLE_LIST_DELETE_XBUTTON = f'//div[text()="{name}"]/parent::*/following-sibling::td//i[contains(@class, "icon-delete")]'
        self.click(TABLE_LIST_DELETE_XBUTTON)

    def click_arrow_down_button_by_column_name(self, name):
        """ 点击表格指定列的下拉箭头

        参数:
            name: 列名

        """
        TABLE_COLUMN_ARROW_DOWN_XBUTTON = f'//div[text()="{name}"]//i[@class="el-icon-arrow-down"]'
        self.click(TABLE_COLUMN_ARROW_DOWN_XBUTTON)

    def click_table_filter_item_by_name(self, name):
        """ 点击指定表过滤项

        参数:
            name: 过滤项名称

        """
        TABLE_FILTER_ITEM_XLI = f'//div[@class="el-table-filter" and not(contains(@style, "display: none;"))]//li[text()="{name}"]'
        self.click(TABLE_FILTER_ITEM_XLI)

    def get_column_index_by_name(self, name):
        """ 获取指定列的索引

        参数:
            name: 列名

        返回:
            索引值

        """
        TABLE_HEADER_XTH = f'//table[@class="el-table__header"]//div[text()="{name}"]/parent::th'
        HEADER_CLASS = self.get_attribute(TABLE_HEADER_XTH, 'class')
        result = re.search('column_(\d) ', HEADER_CLASS)
        return result.group(1)

    def get_number_of_rows_in_column_by_containing_text(self, column_name, text):
        """ 获取指定列包含指定文本的行数

        参数:
            column_name: 列名
            text: 指定包含的文本

        返回:
            包含指定文本的行数

        """
        index = TableList.get_column_index_by_name(self, column_name)
        ROW_IN_COLUMN_XDIV = f'//td[contains(@class, "column_{index}")]/div[contains(text(), "{text}")]'
        elements = self.find_elements(ROW_IN_COLUMN_XDIV, by=By.XPATH)
        return len(elements)

    def get_number_of_rows_in_column_by_not_containing_text(self, column_name, text):
        """ 获取指定列不包含指定文本的行数

        参数:
            column_name: 列名
            text: 指定包含的文本

        返回:
            包含指定文本的行数

        """
        index = TableList.get_column_index_by_name(self, column_name)
        ROW_IN_COLUMN_XDIV = f'//td[contains(@class, "column_{index}")]/div[not(contains(text(), "{text}"))]'
        elements = self.find_elements(ROW_IN_COLUMN_XDIV, by=By.XPATH)
        return len(elements)

#!/usr/bin/env python3

from selenium.webdriver.common.by import By
from guard.pages.base import BasePage


class MenuBar(BasePage):
    """ 菜单栏基本页面操作方法

    click_menu_item_by_text: 点击指定命名的菜单
    click_personal_info_menu_item: 点击指定命名的分组

    """

    def click_menu_item_by_text(self, menu_text, sub_menu_text=None):
        """ 点击指定命名的菜单

        参数:
            menu_text: 主菜单
            sub_menu_text: 子菜单，默认为空

        """
        self.sleep(5)
        ALERT_MESSAGE_CLOSE = '.el-message__closeBtn'
        # if self.click_if_visible(ALERT_MESSAGE_CLOSE):
        self.click_if_visible(ALERT_MESSAGE_CLOSE)
        if (menu_text == '工具'):
            MENU_ITEM_XLINK = f'//div[text()="{menu_text}"]'
            SUB_MENU_ITEM_XLINK = f'//li[text()="{sub_menu_text}"]'
        else:
            MENU_ITEM_XLINK = f'//em[text()="{menu_text}"]'
            SUB_MENU_ITEM_XLINK = f'//em[text()="{sub_menu_text}"]'

        if (sub_menu_text is not None):
            BasePage.hover_on_element_by_xpath(self, MENU_ITEM_XLINK)
            self.sleep(2)
            self.click(SUB_MENU_ITEM_XLINK, by=By.XPATH)
        else:
            self.click(MENU_ITEM_XLINK, by=By.XPATH)
        self.sleep(5)

    def click_personal_info_menu_item(self, sub_menu_text=None):

        MENU_ITEM_LINK = '#app > div > header > div.navbar.el-row > div.right_menu.el-col.el-col-4 > div > div.el-dropdown > div > i'
        if (sub_menu_text is not None):
            if (sub_menu_text == '退出系统'):
                SUB_MENU_ITEM_LINK = f'//span[text()="{sub_menu_text}"]'
            else:
                SUB_MENU_ITEM_LINK = f'//li[contains(text(),"{sub_menu_text}")]'
            self.click(MENU_ITEM_LINK)
            self.sleep(1)
            self.click(SUB_MENU_ITEM_LINK, by=By.XPATH)
        else:
            self.click(MENU_ITEM_LINK)

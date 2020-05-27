#!/usr/bin/env python3

from guard.pages.base import BasePage


class DatePanel(BasePage):
    """ 时间面板基本操作方法

    click_panel_footer_button_by_text: 点击面板页脚指定文字按钮

    """

    def click_panel_footer_button_by_text(self, text):
        """ 点击面板页脚指定文字按钮

        参数:
            text: 按钮文字，可选此刻、确定

        """
        DATE_PANEL_XBUTTON = f'//div[contains(@class,"el-date-picker") and not(contains(@style, "display: none;"))]/div[@class="el-picker-panel__footer"]//span[contains(text(),"{text}")]'
        self.click(DATE_PANEL_XBUTTON)

#!/usr/bin/env python3

from guard.pages.base import BasePage


class Dialog(BasePage):
    """ 对话框基本操作方法

    click_dialog_footer_button_by_text: 点击对话框页脚指定文字按钮

    """

    def click_dialog_footer_button_by_text(self, title, text):
        """ 点击对话框页脚指定文字按钮

        参数:
            title: 对话框标题
            text: 按钮文字，可选确定、取消、仅从分组删除、从人像库删除

        """
        DIALOG_FOOTER_XBUTTON = f'//div[@aria-label="{title}"]/parent::div[not(@style="display: none;")]//span[@class="dialog-footer"]//span[text()="{text}"]'
        self.slow_click(DIALOG_FOOTER_XBUTTON)


    def get_dialog_footer_button_element(self, title, confirm=True):
        """ 点击对话框页脚指定文字按钮
        任务详情，编辑任务详情，设备详情，编辑设备详情
        :param self:
        :param title: 编辑，详情
        :param confirm: True表示确认，False表示取消
        :return: 元素定位器
        """
        if title in ["编辑", "详情"]:
            if confirm:
                return f'//div[@aria-label="{title}"]/parent::*[not(contains(@style, "display: none;"))]//div//div[@class="el-dialog__footer"]//button[@class="el-button el-button--primary"]'
            else:
                return f'//div[@aria-label="{title}"]/parent::*[not(contains(@style, "display: none;"))]//div//div[@class="el-dialog__footer"]//button[@class="el-button el-button--info"]'
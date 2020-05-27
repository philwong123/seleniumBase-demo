#!/usr/bin/env python3

from selenium.webdriver.common.by import By
from guard.pages.base import BasePage


class PersonInfoPage(BasePage):
    """ 个人信息页面操作方法

    click_reset_password_button: 点击重置密码按钮
    reset_password: 重置密码
    """

    def click_reset_password_button(self):
        """ 点击重置密码按钮 """
        self.menu = '修改密码'
        RESET_PASSWORD_XBUTTON = '//button/span[contains(text(),"修改密码")]'
        self.slow_click(RESET_PASSWORD_XBUTTON)
    
    def reset_password(self, current_password, new_password, confirm_new_password, confirm=True):
        """ 重置密码

        参数:
            current_password: 旧密码
            new_password: 新密码
            confirm_new_password: 再次确认
            confirm: 是否确认，默认为确认
            
        """
        PersonInfoPage.click_reset_password_button(self)
        CURRENT_PASSWORD_XINPUT = '//label[@for="oldpwd"]/parent::*/div/div/input'
        NEW_PASSWORD_XINPUT = '//label[@for="newpwd"]/parent::*/div/div/input'
        CONFIRM_NEW_PASSWORD_XINPUT = '//label[@for="newpwd2"]/parent::*/div/div/input'
        CONFIRM_XBUTTON = '//span[@class="dialog-footer"]/button[1]/span'
        CANCEL_XBUTTON = '//span[@class="dialog-footer"]/button[2]/span'
        self.update_text(CURRENT_PASSWORD_XINPUT, current_password)
        self.update_text(NEW_PASSWORD_XINPUT, new_password)
        self.update_text(CONFIRM_NEW_PASSWORD_XINPUT, confirm_new_password)
        if confirm:
            self.slow_click(CONFIRM_XBUTTON)
        else:
            self.slow_click(CANCEL_XBUTTON)
        



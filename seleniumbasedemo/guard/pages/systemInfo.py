from guard.pages.base import BasePage


class SystemInfoPage(BasePage):
    """ 系统信息页面操作方法

    click_operation_maintenance_management_button: 点击运维管理按钮
    click_change_logo_button: 点击更改logo按钮
    click_change_title_button: 点击更换标题按钮
    click_change_description_button: 点击更换描述按钮
    click_change_reminder_button: 点击更换提示按钮
    """
    OPERATION_MAINTANCE_MANAGEMENT_BUTTON = '//button/span[contains(text(),"运维管理")]'
    CHANGE_LOGO_BUTTON = '//button/span[contains(text(),"更改logo")]'
    CHANGE_TITLE_BUTTON = '//button/span[contains(text(),"更换标题")]'
    CHANGE_DESCRIPTION_BUTTON = '//button/span[contains(text(),"更换描述")]'
    CHANGE_REMIND_BUTTON = '//button/span[contains(text(),"更换提示")]'

    def is_operation_maintenance_management_button_visible(self):
        """运维管理按钮是否可见"""
        return self.find_element(SystemInfoPage.OPERATION_MAINTANCE_MANAGEMENT_BUTTON + '/..').is_enabled()

    def is_change_logo_button_visible(self):
        """更改logo按钮是否可见"""
        return self.is_element_visible(SystemInfoPage.CHANGE_LOGO_BUTTON)

    def is_change_title_button_visible(self):
        """更换标题按钮是否可见"""
        return self.is_element_visible(SystemInfoPage.CHANGE_TITLE_BUTTON)

    def click_operation_maintenance_management_button(self):
        """ 点击运维管理按钮 """
        self.click(SystemInfoPage.OPERATION_MAINTANCE_MANAGEMENT_BUTTON)

    def click_change_logo_button(self):
        """点击更改logo按钮"""
        self.click(SystemInfoPage.CHANGE_LOGO_BUTTON)

    def click_change_title_button(self):
        """点击更换标题按钮"""
        self.click(SystemInfoPage.CHANGE_TITLE_BUTTON)

    def click_change_description_button(self):
        """点击更换描述按钮"""
        self.click(SystemInfoPage.CHANGE_DESCRIPTION_BUTTON)

    def click_change_reminder_button(self):
        """点击更换提示按钮"""
        self.click(SystemInfoPage.CHANGE_REMIND_BUTTON)

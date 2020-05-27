#!/usr/bin/env python3


from selenium.webdriver.common.by import By
from guard.pages.base import BasePage


class TimezonePage(BasePage):
    """ 时间条件
    add_timezone_name: 添加事件条件
    dialog_info_com: 操作类
    add_timezone_section_by_timezone_name：添加时间段
    create_holidays: 添加假期
    check_time: 设置时间
    create_workday: 添加特殊工作日
    dialog_delete: 删除弹框
    delete_or_rename_timezone_name：删除事件条件
    delete_or_rename_holidays_or_workday： 删除假期或特殊工作日
    assert_timezone_section: 判断添加时间段是否成功
    assert_result_by_name: 通过命名判断是否添加成功
    judge_alert_info: 系统页面提示消息框
    """

    def add_timezone_name(self, timezone_name):
        # param timezone_name: 时间条件的名称
        self.sleep(2)
        # 定位 -添加时间条件- 的按钮icon
        ICON = '//span[contains(text(), "时间条件名称")]/i'
        self.find_element(ICON, By.XPATH)
        self.click(ICON)
        TimezonePage.dialog_info_com(self, "添加时间条件", timezone_name)

    def add_timezone_section_by_timezone_name(self, timezone_name):
        """
        :param timezone_name: 给传入的timezone添加时间段
        """
        # 定位到传入的timezone时间条件
        SELECT_TIMEZONE = f'//div[@role="tablist"]//button/span[contains(text(), "{timezone_name}")]'
        ele = self.find_element(SELECT_TIMEZONE, By.XPATH)
        # 定位到 -时间段- 的按钮icon
        ICON = '//span[contains(text(), "时间段")]/i'
        self.find_element(ICON, By.XPATH)
        if not self.driver.find_element_by_xpath(SELECT_TIMEZONE).is_displayed():
            self.sleep(0.5)
            self.driver.execute_script("arguments[0].scrollIntoView();", ele)
        self.click(SELECT_TIMEZONE)
        self.sleep(0.5)
        self.click(ICON)

    def create_holidays(self, tile_name, holidays, num=0):
        """
        添加假期
        :param tile_name: 动态传入定位表达式的标题名称
        :param holidays: 假期名称
        :param num: 设置动态数值，保证时间选择不同
        """
        SET_HOLIDAY = '//span[contains(text(), "未定义假期")]'
        ele = self.find_element(SET_HOLIDAY, By.XPATH)
        if not self.driver.find_element_by_xpath(SET_HOLIDAY).is_displayed():
            self.sleep(0.5)
            self.driver.execute_script("arguments[0].scrollIntoView();", ele)
        self.click(SET_HOLIDAY)
        TimezonePage.dialog_info_com(self, tile_name, holidays)
        SET_TIME = '//header[contains(text(), "假期定义")]/following-sibling::div//span[contains(text(), "设定日期")]'
        self.find_element(SET_TIME, By.XPATH)
        self.click(SET_TIME)
        TimezonePage.check_time(self, num)

    def create_workday(self, tile_name, val, num=0):
        """
        :param tile_name: 动态传入定位表达式的标题名称
        :param val: 特殊工作日名称
        :param num: 设置动态数值，保证时间选择不同
        """
        SET_WORKDAY = '//span[contains(text(), "未定义工作日")]'
        ele = self.find_element(SET_WORKDAY, By.XPATH)
        if not self.driver.find_element_by_xpath(SET_WORKDAY).is_displayed():
            self.sleep(0.5)
            self.driver.execute_script("arguments[0].scrollIntoView();", ele)
        self.click(SET_WORKDAY)
        TimezonePage.dialog_info_com(self, tile_name, val)
        SET_TIME = '//header[contains(text(), "特殊工作日定义")]/following-sibling::div//span[contains(text(), "设定日期")]'
        self.find_element(SET_TIME, By.XPATH)
        self.click(SET_TIME)
        TimezonePage.check_time(self, num)

    def delete_or_rename_timezone_name(self, timezone_name):
        """ 删除时间条件 """
        SELECT_TIMEZONE = f'//div[@role="tablist"]//button/span[contains(text(), "{timezone_name}")]'
        self.find_element(SELECT_TIMEZONE, By.XPATH)
        self.slow_click(SELECT_TIMEZONE)
        ELE_LOC = '//div[@role="tooltip"  and contains(@style, "position")]//span[contains(text(), "删除")]'
        self.find_element(ELE_LOC, By.XPATH)
        self.slow_click(ELE_LOC)
        TimezonePage.dialog_delete(self)

    def delete_or_rename_holidays_or_workday(self, timezone_name):
        """ 删除假期或特殊工作日 """
        SELECT_TIMEZONE = f'//span[text()="{timezone_name}"]/ancestor::tr'
        self.find_element(SELECT_TIMEZONE, By.XPATH)
        self.slow_click(SELECT_TIMEZONE)
        ELE_LOC = '//div[@class="timezone-left-popper"]//span[contains(text(), "删除")]'
        self.find_element(ELE_LOC, By.XPATH)
        self.slow_click(ELE_LOC)
        TimezonePage.dialog_delete(self)

    def dialog_info_com(self, til_name, val, confirm=True):
        """
        :param til_name: 弹框标题
        :param val: 传入input输入框值
        :param confirm: dialog按钮选项。默认确定
        """

        INPUT_TEXT = f'//div[@class="timezone-rename-dialog-header"]//span[contains(text(), "{til_name}")]/ancestor::div[@class="el-dialog__header"]/following-sibling::div[@class="el-dialog__body"]//input'
        self.find_element(INPUT_TEXT, By.XPATH)
        self.update_text(INPUT_TEXT, val)
        if confirm:
            CONFIRM_BUTTON = f'//div[@class="timezone-rename-dialog-header"]//span[contains(text(), "{til_name}")]/ancestor::div[@class="el-dialog__header"]/following-sibling::div[@class="el-dialog__footer"]//span[contains(text(), "确定")]'
            self.find_element(CONFIRM_BUTTON, By.XPATH)
            self.click(CONFIRM_BUTTON)
        else:
            CANCEL_BUTTON = f'//div[@class="timezone-rename-dialog-header"]//span[contains(text(), "{til_name}")]/ancestor::div[@class="el-dialog__header"]/following-sibling::div[@class="el-dialog__footer"]//span[contains(text(), "取消")]'
            self.find_element(CANCEL_BUTTON, By.XPATH)
            self.click(CANCEL_BUTTON)

    def check_time(self, num=1):
        TIME_TODAY = '//div[contains(@class, "el-date-range-picker") and contains(@style, "position")]//div[contains(@class,"is-left")]//td[contains(@class, "today")]'
        self.find_element(TIME_TODAY, By.XPATH)
        self.slow_click(TIME_TODAY)
        TODAY_TEXT = '//div[contains(@class, "el-date-range-picker") and contains(@style, "position")]//div[contains(@class,"is-left")]//td[contains(@class, "today")]//span'
        self.find_element(TODAY_TEXT, By.XPATH)
        today_text = self.get_text(TODAY_TEXT)
        if int(today_text) >= 28:
            # 结束时间为下月1号
            today_text = "1"
            self.sleep(2)
            TIME_END = f'//div[contains(@class, "el-date-range-picker") and contains(@style, "position")]//div[contains(@class,"is-right")]//td//span[text()={today_text}]'
            self.find_element(TIME_END, By.XPATH)
        else:
            today_text = str(int(today_text) + num)
            self.sleep(2)
            TIME_END = f'//div[contains(@class, "el-date-range-picker") and contains(@style, "position")]//div[contains(@class,"is-left")]//td//span[text()={today_text}]'
            self.find_element(TIME_END, By.XPATH)
        self.slow_click(TIME_END)

    def assert_timezone_section(self):
        CHECK_CON_RESULT = '//div[@class="el-tab-pane" and @style=""]//div[contains(@class, "el-row")]//span[contains(text(), ":")]'
        self.find_element(CHECK_CON_RESULT, By.XPATH)
        return self.get_text(CHECK_CON_RESULT)

    def assert_result_by_name(self, name):
        RESULT = f'//span[contains(text(), "{name}")]'
        self.find_element(RESULT, By.XPATH)
        return self.get_text(RESULT)

    def dialog_delete(self, is_delete=True):
        if is_delete:
            CONFIRM_BTN = '//button//span[contains(text(), "删除")]'
            self.find_element(CONFIRM_BTN, By.XPATH)
            self.click(CONFIRM_BTN)
        else:
            # 点击取消按钮
            CONFIRM_BTN = '//button//span[contains(text(), "取消")]'
            self.find_element(CONFIRM_BTN, By.XPATH)
            self.click(CONFIRM_BTN)

    def judge_alert_info(self):
        INFO_TEXT = '//div[@role="alert"]//p'
        self.find_element(INFO_TEXT, By.XPATH)
        self.click(INFO_TEXT)
        return self.get_text(INFO_TEXT)

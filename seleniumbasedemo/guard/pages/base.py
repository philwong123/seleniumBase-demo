#!/usr/bin/env python3

import uuid
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from seleniumbase.fixtures import page_actions


class BasePage(object):
    """ 页面基本操作

    assert_alert_message: 检查包含指定内容的警告信息和关闭按按钮显示
    hover_on_element_by_xpath: 通过XPath悬停鼠标在指定元素上
    upload_file_by_image_path: 通过指定元素上传指定路径的图片
    click_element_on_center_by_offset: 点击指定元素相对中心偏移量的位置
    assert_element_text: 检查元素文字是否符合预期值
    assert_element_attribute_value: 检查元素属性是否符合预期值

    """

    def assert_alert_message(self, message):
        """ 检查包含指定内容的警告信息和关闭按按钮显示

        参数:
            message: 警告信息中的信息

        """
        ALERT_MESSAGE_P = '.el-message__content'
        ALERT_MESSAGE_CLOSE = '.el-message__closeBtn.el-icon-close'
        actual = self.get_text(ALERT_MESSAGE_P)
        self.assert_true(actual == message)
        self.assert_element_visible(ALERT_MESSAGE_CLOSE)
        self.click(ALERT_MESSAGE_CLOSE)

    def hover_on_element_by_xpath(self, selector):
        """ 通过XPath悬停鼠标在指定元素上

        参数:
            selector: 元素XPath

        """
        page_actions.wait_for_element_visible(
            self.driver, selector, by=By.XPATH)
        element = self.driver.find_element(
            by=By.XPATH, value=selector)
        actions = ActionChains(self.driver).move_to_element(element)
        actions.perform()

    def upload_file_by_image_path(self, selector, path):
        """ 通过指定元素上传指定路径的图片

        参数:
            selector: 上传文件的元素
            path: 上传图片的路径

        """
        self.driver.execute_script(
            f"document.querySelector('{selector}').style='display: grid';")
        self.choose_file(selector, path)
        self.driver.execute_script(
            f"document.querySelector('{selector}').style='display: none;';")

    def click_element_on_center_by_offset(self, selector, x_offset=0, y_offset=0, by=By.CSS_SELECTOR):
        """ 点击指定元素相对中心偏移量的位置

        参数:
            selector: 上传文件的元素
            x_offset: X偏移量，默认值为0
            y_offset: Y偏移量,默认值为0
            by: 元素定位方式，默认为By.CSS_SELECTOR，可选By.XPATH

        """
        page_actions.wait_for_element_visible(
            self.driver, selector, by=by)
        element = self.driver.find_element(
            by=by, value=selector)
        width = element.size.get('width')
        height = element.size.get('height')
        actions = ActionChains(self.driver)
        actions.move_to_element(element)
        actions.perform()
        self.sleep(1)
        actions.move_by_offset(x_offset, y_offset)
        actions.perform()
        self.sleep(1)
        actions.click()
        actions.perform()

    def assert_element_text(self, selector, expect):
        """ 检查元素文字是否符合预期值

        参数:
            selector: 页面元素
            expect: 预期显示文本内容

        """
        actual = self.get_text(selector)
        self.assert_true(actual == expect)

    def click_task_cancel_button(self):
        """ 点击新建任务中的取消按钮 """
        TASK_DIALOG_CANCEL_INPUT = '//*[@id="app"]/div/div[1]/section/div/div[2]/div[3]/div/div[3]/span/button[2]'
        self.slow_click(TASK_DIALOG_CANCEL_INPUT)

    def assert_element_attribute_value(self, selector, attribute, expect):
        """ 检查元素属性是否符合预期值

        参数:
            selector: 页面元素
            attribute: 元素属性
            export: 预期元素属性值

        """
        actual = self.get_attribute(
            selector, attribute)
        self.assert_true(actual == expect)

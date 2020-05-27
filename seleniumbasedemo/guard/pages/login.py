#!/usr/bin/env python3

from selenium.webdriver.common.by import By
from seleniumbase import config as sb_config
from utils.config import Config
from utils.ssh import SSH
import os
# import pytesseract
import cv2
import utils.captcha_recognition
import re
import subprocess
# from PIL import Image
import numpy as np
from utils.redis_database import GetRedisData
from guard.pages.base import BasePage


class LoginPage(BasePage):
    """ 登录页面操作方法

    login: 登录指定用户
    get_captcha_from_k8s_log: 从K8S日志中获取验证码
    get_captcha_from_ocr: 通过OCR获取验证码
    get_captcha_from_redis: 通过Redis获取验证码

    """

    # HTTP_CONFIG = Config('./guard/config/http_config.yml').config
    # SSH_CONFIG = Config('../config/ssh_config.yml').config

    SSH_CONFIG = Config(os.getcwd() + '/guard/config/ssh_config.yml').config

    def login(self, username, password, captcha=None):
        """ 登录指定用户

        参数:
            username: 用户名
            password: 用户密码
            captcha: 验证码，默认为空
        """
        USERNAME_INPUT = 'input[name="username"]'
        PASSWORD_INPUT = 'input[name="password"]'
        CAPTCHA_INPUT = 'input[name="verifyCode"]'
        LOGIN_BUTTON = 'button.el-button.el-button--primary'

        self.open(f"https://{sb_config.host}")
        self.update_text(USERNAME_INPUT, username)
        self.update_text(PASSWORD_INPUT, password)
        if (captcha is None):
            if (sb_config.ocr):
                while self.is_element_visible(CAPTCHA_INPUT) and self.get_text(CAPTCHA_INPUT) == '':
                    self.update_text(
                        CAPTCHA_INPUT, LoginPage.get_captcha_from_ocr(self))
                    self.click(LOGIN_BUTTON)
                    self.sleep(5)
                    if ('/monitor' in self.get_current_url()) or ('/personInfo' in self.get_current_url()):
                        break
                    self.update_text(USERNAME_INPUT, username)
                    self.update_text(PASSWORD_INPUT, password)
            else:
                self.update_text(
                    CAPTCHA_INPUT, LoginPage.get_captcha_from_redis(self))
                self.click(LOGIN_BUTTON)
        else:
            self.update_text(CAPTCHA_INPUT, captcha)
            self.click(LOGIN_BUTTON)

    def get_captcha_from_k8s_log():
        """ 从K8S日志中获取验证码

        返回: 验证码字符串

        """
        ssh_config = LoginPage.SSH_CONFIG.get("ssh")
        ssh_config['hostname'] = sb_config.host
        ssh = SSH(**ssh_config)
        oauth2_pod_name = ssh.execute_command(
            "kubectl get pods | grep oauth2 | awk '{print $1}'")
        captcha = ssh.execute_command(
            f"kubectl logs {oauth2_pod_name.rstrip()} --tail 2 | grep 生成验证码存入redis | awk -F ' ' '{{print $5}}'")
        return captcha.rstrip()

    def get_captcha_from_ocr(self):
        """ 通过OCR获取验证码

        返回: 验证码字符串

        """
        count = 0
        while count < 10:
            CAPTCHA_IMG = 'div.verify-code > div.code-pic > img'
            CAPTCHA_REFRESH_BUTTON = 'div.verify-code > div.refresh > i'
            self.save_element_as_image_file(CAPTCHA_IMG, 'captcha')
            image = cv2.imread('captcha.png')
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            gray = cv2.boxFilter(gray, -1, (3, 3), normalize=True)
            gray = cv2.threshold(
                gray, 252, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
            cv2.imwrite('captcha.png', gray)
            self.sleep(3)

            captcha = utils.captcha_recognition.captcha_read('captcha.png')
            if captcha is not None:
                captcha = ''.join(
                    filter(lambda c: c.isdigit() or c.isalpha(), f'{captcha}'))
                count += 1
                if len(captcha) == 6:
                    return captcha
                else:
                    self.click(CAPTCHA_REFRESH_BUTTON)

    def get_captcha_from_redis(self):
        """ 通过Redis获取验证码

        返回: 验证码字符串

        """
        img_url = self.driver.find_element_by_xpath(
            "//*[@class='code-pic']").get_attribute("innerHTML")
        pattern = ".*timestamp=(\d+)"
        timestamp = re.findall(pattern, img_url)
        redis = GetRedisData(sb_config.host)
        captcha_code = redis.get_result_from_redis(
            "Senseguard:Oauth2:Login:" + timestamp[0])
        print(captcha_code)
        return captcha_code

#!/usr/bin/env python3

import os
import pytest

# from seleniumbase.fixtures import page_actions
# from guard.tests.base_test_case import BaseTestCase
from guard.pages.components.menubar import MenuBar
from guard.pages.personInfo import PersonInfoPage
from guard.pages.login import LoginPage
from guard.pages.user import UserPage
from guard.pages.classes.user import User


@pytest.mark.positive
def test_reset_password(sb, login, setup_user_and_delete_user):
    # 登陆系统创建新用户，并退出当前用户
    MenuBar.click_personal_info_menu_item(sb, '退出系统')
    # 登陆新用户，并修改密码
    LoginPage.login(sb, setup_user_and_delete_user['name'], '888888')
    PersonInfoPage.reset_password(sb, '888888', 'Guard123', 'Guard123')
    sb.sleep(5)
    # 重新登陆系统，验证密码修改成功
    LoginPage.login(sb, setup_user_and_delete_user['name'], 'Guard123')
    sb.assert_element_visible('.avatar-name')
    sb.sleep(5)

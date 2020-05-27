#!/usr/bin/env python3

import pytest
from guard.pages.login import LoginPage
from guard.pages.user import UserPage
from guard.pages.components.menubar import MenuBar
from guard.pages.personInfo import PersonInfoPage
from seleniumbase import config as sb_config


@pytest.mark.positive
def test_login(sb):
    LoginPage.login(sb, sb_config.username, sb_config.password)
    sb.assert_element_visible('.avatar-name')


@pytest.mark.negative
def test_login_with_wrong_captcha(sb):
    LoginPage.login(sb, sb_config.username, sb_config.password, 'captcha')
    LoginPage.assert_alert_message(sb, '验证码错误')


@pytest.mark.negative
def test_login_with_wrong_username(sb):
    LoginPage.login(sb, 'user_not_exist', '888888')
    LoginPage.assert_alert_message(sb, '用户名或密码错误，请重新输入')


@pytest.mark.negative
def test_login_with_wrong_password(sb):
    LoginPage.login(sb, sb_config.username, '123456')
    LoginPage.assert_alert_message(sb, '用户名或密码有误，请重新输入，您还有 4 次机会')


@pytest.mark.positive
def test_first_login_reset_password(sb, login, setup_user):
    # 登陆系统创建新用户，并退出当前用户
    MenuBar.click_personal_info_menu_item(sb, '退出系统')
    # 登陆新用户，并修改密码
    LoginPage.login(sb, setup_user['name'], '888888')
    PersonInfoPage.reset_password(sb, '888888', 'Guard123', 'Guard123')
    sb.sleep(5)
    # 重新登陆系统，验证密码修改成功
    LoginPage.login(sb, setup_user['name'], 'Guard123')
    sb.assert_element_visible('.avatar-name')


@pytest.mark.positive
def test_refresh_captcha(sb, open):
    captcha_1 = LoginPage.get_captcha_from_redis(sb)
    CAPTCHA_REFRESH_BUTTON = 'div.verify-code > div.refresh > i'
    sb.click(CAPTCHA_REFRESH_BUTTON)
    sb.sleep(2)
    captcha_2 = LoginPage.get_captcha_from_redis(sb)
    assert(captcha_2 != '')
    assert(captcha_1 != captcha_2)


@pytest.mark.negative
def test_captcha_with_refresh_page(sb, open):
    captcha_1 = LoginPage.get_captcha_from_redis(sb)
    sb.refresh_page()
    sb.sleep(2)
    captcha_2 = LoginPage.get_captcha_from_redis(sb)
    assert(captcha_2 != '')
    assert(captcha_1 != captcha_2)


@pytest.fixture()
def login_with_wrong_username_password(sb, open, request):
    username = request.param['username']
    password = request.param['password']
    LoginPage.login(sb, username, password)


@pytest.mark.negative
def test_login_with_wrong_password_five_times(sb, login, setup_user):
    ALERT_MESSAGE_LIST = ['用户名或密码有误，请重新输入，您还有 4 次机会', '用户名或密码有误，请重新输入，您还有 3 次机会',
                          '用户名或密码有误，请重新输入，您还有 2 次机会', '用户名或密码有误，请重新输入，您还有 1 次机会',
                          '多次输入密码有误,账户已被锁定，请联系IT部门']
    MenuBar.click_personal_info_menu_item(sb, '退出系统')
    for i in range(5):
        LoginPage.login(sb, setup_user['name'], '123456')
        sb.sleep(1)
        LoginPage.assert_alert_message(sb, ALERT_MESSAGE_LIST[i])
        sb.sleep(2)


@pytest.mark.negative
def test_locked_account_login_in_thirty_minutes(sb, login, setup_user):
    MenuBar.click_personal_info_menu_item(sb, '退出系统')
    for i in range(6):
        LoginPage.login(sb, setup_user['name'], '123456')
        sb.sleep(1)
    LoginPage.assert_alert_message(sb, "多次输入密码有误,账户已被锁定，请联系IT部门")


@pytest.mark.positive
def test_login_with_reset_locked_account(sb, login, setup_user):
    #5次登录错误，账户被锁定
    MenuBar.click_personal_info_menu_item(sb, '退出系统')
    for i in range(5):
        LoginPage.login(sb, setup_user['name'], '123456')
        sb.sleep(1)
    #管理员登录，重置密码
    LoginPage.login(sb, sb_config.username, sb_config.password)
    sb.sleep(2)
    MenuBar.click_menu_item_by_text(sb, '配置', '用户管理')
    default_password = UserPage.reset_user_password(sb, setup_user['name'])
    MenuBar.click_personal_info_menu_item(sb, '退出系统')
    sb.sleep(2)
    # 重新登录，并修改密码
    LoginPage.login(sb, setup_user['name'], str(default_password).strip())
    PersonInfoPage.reset_password(sb, str(default_password).strip(), 'Guard123', 'Guard123')
    sb.sleep(5)
    # 重新登陆系统，验证密码修改成功
    LoginPage.login(sb, setup_user['name'], 'Guard123')
    sb.assert_element_visible('.avatar-name')



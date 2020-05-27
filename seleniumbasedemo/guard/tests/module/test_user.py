#!/usr/bin/env python3

import os
import pytest

from guard.pages.components.menubar import MenuBar
from guard.pages.user import UserPage
from guard.pages.classes.user import User


@pytest.mark.positive
def test_add_department(sb, login, setup_department_name_and_delete_department):
    UserPage.add_department_by_root_department_name(
        sb, setup_department_name_and_delete_department['name'])
    UserPage.assert_alert_message(sb, '创建同级分组成功')


@pytest.mark.positive
def test_delete_existing_department(sb, login, setup_department):
    UserPage.delete_department_by_name(
        sb, setup_department['name'])
    UserPage.assert_alert_message(sb, '删除分组成功')


@pytest.mark.positive
def test_add_sub_department(sb, login, setup_department_and_delete_department, setup_subdepartment_name_and_delete_subdepartment):
    UserPage.add_department_by_parent_department_name(
        sb, setup_subdepartment_name_and_delete_subdepartment['name'], setup_department_and_delete_department['name'], is_peer=False)


@pytest.mark.positive
def test_delete_subdepartment(sb, login, setup_department_and_delete_department, setup_subdepartment):
    UserPage.delete_department_by_name(sb, setup_subdepartment['name'])
    UserPage.assert_alert_message(sb, '删除分组成功')


@pytest.mark.positive
def test_add_user(sb, login, setup_user_name_and_delete_user):
    user = User(
        setup_user_name_and_delete_user['name'], setup_user_name_and_delete_user['name'])
    UserPage.add_user_by_department_name(sb, user)
    UserPage.assert_alert_message(sb, '添加用户成功')


@pytest.mark.positive
def test_delete_existing_user(sb, login, setup_user):
    MenuBar.click_menu_item_by_text(sb, '配置', '用户管理')
    UserPage.delete_user_by_name(sb, setup_user['name'])
    UserPage.assert_alert_message(sb, '删除用户成功')

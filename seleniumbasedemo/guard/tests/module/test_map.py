#!/usr/bin/env python3

import pytest
from parameterized import parameterized

from guard.pages.components.menubar import MenuBar
from guard.pages.map import MapPage


@pytest.mark.positive
def test_add_peer_floor(sb, login, setup_peer_floor_name_and_delete_floor):
    MapPage.add_floor_by_root_floor_name(
        sb, setup_peer_floor_name_and_delete_floor['name'])
    MapPage.assert_alert_message(sb, '创建同级分组成功')


@pytest.mark.positive
def test_add_subordinate_floor(sb, login, setup_peer_floor_and_delete_floor, setup_subordinate_floor_name_and_delete_floor):
    MapPage.add_floor_by_parent_name(
        sb, setup_subordinate_floor_name_and_delete_floor['name'], parent_name=setup_peer_floor_and_delete_floor['name'], is_peer=False)
    MapPage.assert_alert_message(sb, '创建下一级分组成功')


@pytest.mark.parametrize('name', ['', '  '])
@pytest.mark.negative
def test_invalid_peer_floor(sb, login, name):
    MenuBar.click_menu_item_by_text(sb, '配置', '地图管理')
    MapPage.add_floor_by_root_floor_name(sb, name)
    MapPage.assert_element_text(sb, '.el-form-item__error', '请输入分组名称')


@pytest.mark.parametrize('name', ['', '  '])
@pytest.mark.negative
def test_invalid_peer_floor(sb, login, setup_peer_floor_and_delete_floor, name):
    MenuBar.click_menu_item_by_text(sb, '配置', '地图管理')
    MapPage.add_floor_by_parent_name(
        sb, name, parent_name=setup_peer_floor_and_delete_floor['name'], is_peer=False)
    MapPage.assert_element_text(sb, '.el-form-item__error', '请输入分组名称')
    MapPage.click_cancel_in_dialog(sb)


@pytest.mark.negative
def test_add_same_peer_floor(sb, login, setup_peer_floor_and_delete_floor):
    MapPage.add_floor_by_root_floor_name(
        sb, setup_peer_floor_and_delete_floor['name'])
    MapPage.assert_alert_message(sb, '地图名已存在')
    MapPage.click_cancel_in_dialog(sb)


@pytest.mark.negative
def test_add_same_subordinate_floor(sb, login, setup_peer_floor_and_delete_floor, setup_subordinate_floor_name_and_delete_floor):
    MapPage.add_floor_by_parent_name(
        sb, setup_subordinate_floor_name_and_delete_floor['name'], parent_name=setup_peer_floor_and_delete_floor['name'], is_peer=False)
    MapPage.add_floor_by_parent_name(
        sb, setup_subordinate_floor_name_and_delete_floor['name'], parent_name=setup_peer_floor_and_delete_floor['name'], is_peer=False)
    MapPage.assert_alert_message(sb, '地图名已存在')
    MapPage.click_cancel_in_dialog(sb)


@pytest.mark.positive
def test_rename_peer_floor(sb, login, setup_peer_floor):
    new_name = f"{setup_peer_floor['name']}N"
    MapPage.rename_floor_by_root_floor_name(
        sb, setup_peer_floor['name'], new_name)
    MapPage.assert_alert_message(sb, '重命名成功！')
    MapPage.delete_floor_by_name(sb, new_name)


@pytest.mark.positive
def test_rename_subordinate_floor(sb, login, setup_peer_floor_and_delete_floor):
    old_name = f"{setup_peer_floor_and_delete_floor['name']}O"
    new_name = f"{setup_peer_floor_and_delete_floor['name']}N"
    MapPage.add_floor_by_parent_name(
        sb, old_name, parent_name=setup_peer_floor_and_delete_floor['name'], is_peer=False)
    MapPage.rename_floor_by_parent_name(
        sb, old_name, new_name, parent_name=setup_peer_floor_and_delete_floor['name'])
    MapPage.assert_alert_message(sb, '重命名成功！')
    MapPage.delete_floor_by_name(sb, new_name)


@pytest.mark.negative
def test_rename_same_peer_floor(sb, login, setup_peer_floor_and_delete_floor):
    MapPage.rename_floor_by_root_floor_name(
        sb, setup_peer_floor_and_delete_floor['name'], 'Default')
    MapPage.assert_alert_message(sb, '地图名已存在')
    MapPage.click_cancel_in_dialog(sb)


@pytest.mark.negative
def test_rename_same_subordinate_floor(sb, login, setup_peer_floor_and_delete_floor):
    subordinate_name = f"{setup_peer_floor_and_delete_floor['name']}S"
    MapPage.add_floor_by_parent_name(
        sb, subordinate_name, parent_name=setup_peer_floor_and_delete_floor['name'], is_peer=False)
    MapPage.rename_floor_by_parent_name(
        sb, subordinate_name, 'Default', parent_name=setup_peer_floor_and_delete_floor['name'])
    MapPage.assert_alert_message(sb, '地图名已存在')
    MapPage.click_cancel_in_dialog(sb)
    MapPage.delete_floor_by_name(sb, subordinate_name)


@pytest.mark.positive
def test_delete_existing_peer_floor(sb, login, setup_peer_floor):
    MenuBar.click_menu_item_by_text(sb, '配置', '地图管理')
    MapPage.delete_floor_by_name(sb, setup_peer_floor['name'])
    MapPage.assert_alert_message(sb, '删除分组成功！')


@pytest.mark.positive
def test_delete_existing_subordinate_floor(sb, login, setup_peer_floor_and_delete_floor):
    subordinate_name = f"{setup_peer_floor_and_delete_floor['name']}S"
    MapPage.add_floor_by_parent_name(
        sb, subordinate_name, parent_name=setup_peer_floor_and_delete_floor['name'], is_peer=False)
    MenuBar.click_menu_item_by_text(sb, '配置', '地图管理')
    MapPage.delete_floor_by_name(sb, subordinate_name)
    MapPage.assert_alert_message(sb, '删除分组成功！')

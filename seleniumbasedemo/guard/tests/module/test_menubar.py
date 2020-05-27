#!/usr/bin/env python3

import pytest

from guard.pages.components.menubar import MenuBar


@pytest.mark.positive
def test_menubar(sb, login):
    MenuBar.click_menu_item_by_text(sb, '看板')
    MenuBar.click_menu_item_by_text(sb, '实况')
    MenuBar.click_menu_item_by_text(sb, '访客')
    MenuBar.click_menu_item_by_text(sb, '考勤')
    MenuBar.click_menu_item_by_text(sb, '记录')
    MenuBar.click_menu_item_by_text(sb, '迎宾')
    MenuBar.click_menu_item_by_text(sb, '配置', '设备管理')
    MenuBar.click_menu_item_by_text(sb, '工具', '1:1人脸验证')

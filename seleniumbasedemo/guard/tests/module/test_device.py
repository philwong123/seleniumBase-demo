#!/usr/bin/env python3

import pytest

from guard.pages.components.group_tree import GroupTree
from guard.pages.components.menubar import MenuBar
from guard.pages.device import DevicePage
from guard.pages.classes.device.device import Device
from guard.pages.classes.device.rtsp import RTSP
from guard.pages.classes.device.onvif import ONVIF
from guard.pages.classes.device.dlc import DLC
from guard.pages.classes.device.frontend import Frontend

#正常创建分组
@pytest.mark.positive
def test_add_device_group(sb, login, setup_device_group_name_and_delete_group):
    DevicePage.add_group_by_root_group_name(
        sb, setup_device_group_name_and_delete_group['name'])
    DevicePage.assert_alert_message(sb, '创建同级分组成功')

#正常删除分组
@pytest.mark.positive
def test_add_device_group(sb, login, setup_device_group):
    DevicePage.delete_group_by_name(sb, setup_device_group['name'])
    DevicePage.assert_alert_message(sb, '删除分组成功')

#删除有子分组的父分组
@pytest.mark.negative
def test_delete_peer_device_group_with_subordinate(sb, login, setup_device_group,setup_subordinate_device_group):
    DevicePage.add_group_by_root_group_name(
        sb, name = setup_subordinate_device_group['name'],is_peer=False,parent_name = setup_device_group['name'])
    DevicePage.delete_group_by_name(sb, setup_device_group['name'])
    DevicePage.assert_alert_message(sb, '删除分组成功')

#创建空名，空格名父分组
@pytest.mark.parametrize('name', ['', '  '])
@pytest.mark.negative
def test_invalid_peer_device_group(sb,name,login):
    MenuBar.click_menu_item_by_text(sb, '配置', '设备管理')
    DevicePage.add_group_by_root_group_name(
        sb, name)
    DevicePage.assert_element_text(sb, '.el-form-item__error', '请输入分组名称')

#创建空名，空格名子分组
@pytest.mark.parametrize('name', ['', '  '])
@pytest.mark.negative
def test_invalid_device_group(sb,name,login):
    MenuBar.click_menu_item_by_text(sb, '配置', '设备管理')
    DevicePage.add_group_by_root_group_name(
        sb, name,is_peer=False)
    DevicePage.assert_element_text(sb, '.el-form-item__error', '请输入分组名称')

#创建超长字符分组
@pytest.mark.parametrize('name', ['a1234567890123456789012345678901234567890','a123456789012345678901234567890123456789'])
@pytest.mark.negative
def test_longname_peer_device_group(sb,name,login):
    name_cut = name[0:40]
    MenuBar.click_menu_item_by_text(sb, '配置', '设备管理')
    DevicePage.add_group_by_root_group_name(
        sb, name)
    #DevicePage.assert_alert_message(sb, '创建同级分组成功')
    DevicePage.search_device_group_by_name(sb, name_cut)
    GroupTree.assert_group_is_visible(sb,name_cut)
    DevicePage.delete_group_by_name(sb, name_cut)

#创建重名父分组
@pytest.mark.negative
def test_add_same_peer_device_group(sb, login, setup_device_group):
    DevicePage.add_group_by_root_group_name(
        sb, setup_device_group['name'])
    DevicePage.assert_alert_message(sb, '该名称已存在')
    DevicePage.delete_group_by_name(sb, setup_device_group['name'])

#创建重名子分组
@pytest.mark.negative
def test_add_same_device_group(sb, login, setup_device_group,setup_subordinate_device_group):
    DevicePage.add_group_by_root_group_name(
        sb, name = setup_subordinate_device_group['name'],is_peer=False,parent_name = setup_device_group['name'])
    DevicePage.add_group_by_root_group_name(
        sb, name = setup_subordinate_device_group['name'],is_peer=False,parent_name = setup_device_group['name'])
    DevicePage.assert_alert_message(sb, '该名称已存在')
    DevicePage.delete_group_by_name(sb, setup_device_group['name'])

#重命名父分组
@pytest.mark.positive
def test_rename_peer_device_group(sb, login, setup_device_group):
    new_name = f"{setup_device_group['name']}N"
    #new_name = "1111"
    DevicePage.rename_group_by_root_group_name(
        sb, setup_device_group['name'], new_name)
    DevicePage.search_device_group_by_name(sb,new_name)
    GroupTree.assert_group_is_visible(sb,new_name)
    DevicePage.delete_group_by_name(sb,new_name)


#重命名子分组
@pytest.mark.positive
def test_rename_subordinate_device_group(sb, login, setup_device_group,setup_subordinate_device_group):
    new_name = f"{setup_subordinate_device_group['name']}N"
    #new_name = "1111"
    DevicePage.add_group_by_root_group_name(
        sb, name=setup_subordinate_device_group['name'], is_peer=False, parent_name=setup_device_group['name'])
    DevicePage.rename_group_by_parent_name(
        sb, setup_subordinate_device_group['name'], new_name,parent_name=setup_device_group['name'])
    DevicePage.search_device_group_by_name(sb,new_name)
    GroupTree.assert_group_is_visible(sb,new_name)
    DevicePage.delete_group_by_name(sb,setup_device_group['name'])

#重命名重名父分组
@pytest.mark.negative
def test_rename_same_peer_device_group(sb, login, setup_device_group):
    new_name = "Default"
    DevicePage.rename_group_by_root_group_name(
        sb, setup_device_group['name'], new_name)
    DevicePage.assert_alert_message(sb, '该名称已存在')
    DevicePage.delete_group_by_name(sb,setup_device_group['name'])


#重命名重名子分组
@pytest.mark.negative
def test_rename_same_subordinate_device_group(sb, login, setup_device_group,setup_subordinate_device_group):
    new_name = "Default"
    DevicePage.add_group_by_root_group_name(
        sb, name=setup_subordinate_device_group['name'], is_peer=False, parent_name=setup_device_group['name'])
    DevicePage.rename_group_by_parent_name(
        sb, setup_subordinate_device_group['name'], new_name,parent_name=setup_device_group['name'])
    DevicePage.assert_alert_message(sb, '该名称已存在')
    DevicePage.delete_group_by_name(sb,setup_device_group['name'])

#重命名空名，空格名父分组
@pytest.mark.parametrize('name', [' ', '  '])
@pytest.mark.negative
def test_rename_invalid_peer_device_group(sb, login, setup_device_group,name):
    DevicePage.rename_group_by_root_group_name(
        sb, setup_device_group['name'], name)
    DevicePage.assert_element_text(sb, '.el-form-item__error', '请输入分组名称')
    DevicePage.cancel_rename_group(sb)
    DevicePage.delete_group_by_name(sb,setup_device_group['name'])

#重命名空名，空格名子分组
@pytest.mark.parametrize('name', [' ', '  '])
@pytest.mark.negative
def test_rename_invalid_subordinate_device_group(sb, login,setup_subordinate_device_group,name, setup_device_group):
    DevicePage.add_group_by_root_group_name(
        sb, name=setup_subordinate_device_group['name'], is_peer=False, parent_name=setup_device_group['name'])
    DevicePage.rename_group_by_parent_name(
        sb, setup_subordinate_device_group['name'], name,parent_name=setup_device_group['name'])
    DevicePage.assert_element_text(sb, '.el-form-item__error', '请输入分组名称')
    DevicePage.cancel_rename_group(sb)
    DevicePage.delete_group_by_name(sb,setup_device_group['name'])

#重命名超长字符分组
@pytest.mark.parametrize('name', ['a123456789012345678901234567890123456789', 'a1234567890123456789012345678901234567890'])
@pytest.mark.negative
def test_rename_longname_peer_device_group(sb, login, setup_device_group,name):
    name_cut = name[0:40]
    DevicePage.rename_group_by_root_group_name(
        sb, setup_device_group['name'], name_cut)
    DevicePage.search_device_group_by_name(sb, name_cut)
    GroupTree.assert_group_is_visible(sb, name_cut)
    DevicePage.delete_group_by_name(sb, name_cut)

#【设备管理】【异常】搜索不存在设备分组
@pytest.mark.negative
def test_search_inexistence_device_group(sb,login, setup_device_group):
    group_name=f"{setup_device_group['name']}GR"
    DevicePage.search_device_group_by_name(sb, group_name)
    DevicePage.assert_element_text(sb,'.el-tree__empty-text','暂无数据')
    DevicePage.search_device_group_by_name(sb, setup_device_group['name'])
    DevicePage.delete_group_by_name(sb, setup_device_group['name'])

#【设备管理】【界面】删除包含未启动设备且含有子分组的父分组
@pytest.mark.negative
def test_delete_subordinate_device_group_with_device(sb, login, setup_device_group,setup_subordinate_device_group):
    DevicePage.add_group_by_root_group_name(
        sb, name = setup_subordinate_device_group['name'],is_peer=False,parent_name = setup_device_group['name'])
    device_name = f"{setup_device_group['name']}RTSP"
    rtsp_device = RTSP(device_name, device_name, setup_subordinate_device_group['name'],
                       'Default', 'rtsp://1.1.1.1:554/test.264')
    DevicePage.add_device_by_type(sb, rtsp_device, '网络摄像机')
    DevicePage.delete_group_by_name(sb, setup_device_group['name'])
    DevicePage.assert_alert_message(sb, '删除分组成功')

#【设备管理】【界面】删除包含未启动设备的子分组
@pytest.mark.negative
def test_delete_subordinate_device_group_with_device(sb, login, setup_device_group,setup_subordinate_device_group):
    DevicePage.add_group_by_root_group_name(
        sb, name = setup_subordinate_device_group['name'],is_peer=False,parent_name = setup_device_group['name'])
    device_name = f"{setup_device_group['name']}RTSP"
    rtsp_device = RTSP(device_name, device_name, setup_subordinate_device_group['name'],
                       'Default', 'rtsp://1.1.1.1:554/test.264')
    DevicePage.add_device_by_type(sb, rtsp_device, '网络摄像机')
    DevicePage.search_device_group_by_name(sb,setup_subordinate_device_group['name'])
    DevicePage.delete_group_by_name(sb, setup_subordinate_device_group['name'])
    DevicePage.assert_alert_message(sb, '删除分组成功')
    DevicePage.delete_group_by_name(sb, setup_device_group['name'])

#【设备管理】【界面】查看设备分组详情
@pytest.mark.positive
def test_view_device_group(sb, login, setup_device_group_name_and_delete_group,setup_device_group):
    DevicePage.add_group_by_root_group_name(
        sb, setup_device_group_name_and_delete_group['name'])
    DevicePage.assert_alert_message(sb, '创建同级分组成功')
    DevicePage.assert_view_device_group_by_name(sb,setup_device_group_name_and_delete_group['name'])









#####设备
##rtsp设备
#正常添加
@pytest.mark.positive
def test_add_rtsp_device(sb, login, setup_device_group_and_delete_group):
    device_name = f"{setup_device_group_and_delete_group['name']}RTSP"
    # rtsp_device = RTSP('rtsp', 'rtsp', group_name,
    #                    'Default', 'rtsp://confidence.119:6554/test.264')
    rtsp_device = RTSP(device_name, device_name, setup_device_group_and_delete_group['name'],
                       'Default', 'rtsp://1.1.1.1:554/test.264')
    DevicePage.add_device_by_type(sb, rtsp_device, '网络摄像机')
    DevicePage.assert_alert_message(sb, '添加设备成功')
    DevicePage.delete_device_by_name(sb,device_name)
    #DevicePage.delete_group_by_name(sb, setup_device_group_and_delete_group['name'])

#【RTSP】【界面】添加RTSP摄像头地址为空（必填校验）
@pytest.mark.negative
def test_add_rtsp_device_no_url(sb, login, setup_device_group_and_delete_group):
    device_name = f"{setup_device_group_and_delete_group['name']}RTSP"
    rtsp_device = RTSP(device_name, device_name, setup_device_group_and_delete_group['name'],
                       'Default', '')
    DevicePage.add_device_by_type(sb, rtsp_device, '网络摄像机')
    DevicePage.assert_element_text(sb, '.el-form-item__error', '请输入非空内容')
    DevicePage.cancel_add_device(sb)
    #DevicePage.delete_group_by_name(sb, setup_device_group_and_delete_group['name'])

#【RTSP】【异常】添加RTSP摄像头传输协议切换
@pytest.mark.negative
def test_add_rtsp_device_UDP(sb, login, setup_device_group_and_delete_group):
    device_name = f"{setup_device_group_and_delete_group['name']}RTSP"
    # rtsp_device = RTSP('rtsp', 'rtsp', group_name,
    #                    'Default', 'rtsp://confidence.119:6554/test.264')
    rtsp_device = RTSP(device_name, device_name, setup_device_group_and_delete_group['name'],
                       'Default', 'rtsp://1.1.1.1:554/test.264')
    DevicePage.add_device_by_type(sb, rtsp_device, '网络摄像机','UDP')
    DevicePage.assert_rtsp_protocol_by_name(sb,device_name,'UPD')
    DevicePage.delete_device_by_name(sb,device_name)

#【RTSP】【异常】添加RTSP摄像头编码类型切换
@pytest.mark.negative
def test_add_rtsp_device_Transcoding(sb, login, setup_device_group_and_delete_group):
    device_name = f"{setup_device_group_and_delete_group['name']}RTSP"
    # rtsp_device = RTSP('rtsp', 'rtsp', group_name,
    #                    'Default', 'rtsp://confidence.119:6554/test.264')
    rtsp_device = RTSP(device_name, device_name, setup_device_group_and_delete_group['name'],
                       'Default', 'rtsp://1.1.1.1:554/test.264')
    DevicePage.add_device_by_type(sb, rtsp_device, '网络摄像机',encoding_type='Transcoding')
    DevicePage.assert_rtsp_protocol_by_name(sb,device_name,'编码')
    DevicePage.delete_device_by_name(sb,device_name)

#【RTSP】【主功能】添加RTSP摄像头预览正确地址
@pytest.mark.positive1
def test_add_rtsp_device_view_video(sb, login,setup_device_group_and_delete_group):
    menu = '添加设备'
    DevicePage.click_add_device_button(sb)
    DevicePage.input_rtsp_address(sb,'rtsp://confidence.119:6554/test.264')
    DevicePage.assert_view_video(sb,menu)


#【设备管理】【异常】添加设备名称为空（必填校验）RTSP
@pytest.mark.parametrize('name', ['', '  '])
@pytest.mark.negative
def test_add_rtsp_device_no_name(sb,name, login, setup_device_group_and_delete_group):
    D_id= f"{setup_device_group_and_delete_group['name']}RTSP"
    rtsp_device = RTSP(name, D_id, setup_device_group_and_delete_group['name'],
                       'Default', 'rtsp://1.1.1.1:554/test.264')
    DevicePage.add_device_by_type(sb, rtsp_device, '网络摄像机')
    DevicePage.assert_element_text(sb, '.el-form-item__error', '请输入设备名称')
    DevicePage.cancel_add_device(sb)
    #DevicePage.delete_group_by_name(sb, setup_device_group_and_delete_group['name'])

#【设备管理】【异常】编辑设备名称为多个空格 RTSP

@pytest.mark.parametrize('name', [' ', '  '])
@pytest.mark.negative
def test_edit_rtsp_device_no_name(sb,name, login, setup_device_group_and_delete_group):
    D_id= f"{setup_device_group_and_delete_group['name']}RTSP"
    rtsp_device = RTSP(D_id, D_id, setup_device_group_and_delete_group['name'],
                       'Default', 'rtsp://1.1.1.1:554/test.264')
    DevicePage.add_device_by_type(sb, rtsp_device, '网络摄像机')
    rtsp_device = RTSP(name, D_id, setup_device_group_and_delete_group['name'],
                       'Default', 'rtsp://1.1.1.1:554/test.264')
    DevicePage.edit_device_by_type(sb, rtsp_device, '网络摄像机',name = D_id)
    #DevicePage.queren_add_device(sb,menu='编辑')
    DevicePage.assert_element_text(sb, '.el-form-item__error', '请输入设备名称')
    DevicePage.cancel_add_device(sb,menu='编辑')

#【设备管理】【异常】添加设备名称长度超40（长度校验）RTSP
@pytest.mark.parametrize('name', ['a1234567890123456789012345678901234567890','a123456789012345678901234567890123456789'])
@pytest.mark.negative
def test_add_rtsp_device_long_name(sb,name, login, setup_device_group_and_delete_group):
    name_cut = name[0:40]
    D_id= f"{setup_device_group_and_delete_group['name']}RTSP"
    rtsp_device = RTSP(name, D_id, setup_device_group_and_delete_group['name'],
                       'Default', 'rtsp://1.1.1.1:554/test.264')
    DevicePage.add_device_by_type(sb, rtsp_device, '网络摄像机')
    DevicePage.assert_device(sb,name_cut)

#编辑设备名称长度超40（长度校验）RTSP
@pytest.mark.parametrize('name', ['a1234567890123456789012345678901234567890','a123456789012345678901234567890123456789'])
@pytest.mark.negative
def test_edit_rtsp_device_long_name(sb,name, login, setup_device_group_and_delete_group):
    name_cut = name[0:40]
    D_id= f"{setup_device_group_and_delete_group['name']}RTSP"
    rtsp_device = RTSP(D_id, D_id, setup_device_group_and_delete_group['name'],
                       'Default', 'rtsp://1.1.1.1:554/test.264')
    DevicePage.add_device_by_type(sb, rtsp_device, '网络摄像机')
    rtsp_device = RTSP(name, D_id, setup_device_group_and_delete_group['name'],
                       'Default', 'rtsp://1.1.1.1:554/test.264')
    DevicePage.edit_device_by_type(sb, rtsp_device, '网络摄像机',name = D_id)
    DevicePage.assert_device(sb, name_cut)

#【设备管理】【异常】搜索不存在设备 RTSP
@pytest.mark.negative
def test_search_inexistence_device(sb,login, setup_device_group_and_delete_group):
    device_name = f"{setup_device_group_and_delete_group['name']}RTSP"
    DevicePage.search_device_by_name(sb,device_name)
    DevicePage.assert_element_text(sb,'.el-table__empty-text','暂无数据')


#【设备管理】【主流程】批量删除未激活未绑定规则的设备 RTSP
@pytest.mark.positive
def test_delete_device_muti(sb,login, setup_device_group_and_delete_group):
    device_name = f"{setup_device_group_and_delete_group['name']}RTSP"
    rtsp_device = RTSP(device_name, device_name, setup_device_group_and_delete_group['name'],
                       'Default', 'rtsp://1.1.1.1:554/test.264')
    DevicePage.add_device_by_type(sb, rtsp_device, '网络摄像机')
    DevicePage.search_device_by_name(sb,setup_device_group_and_delete_group['name'])
    DevicePage.delete_device_by_name_muti(sb)
    DevicePage.search_device_by_name(sb, device_name)
    DevicePage.assert_element_text(sb, '.el-table__empty-text', '暂无数据')

#【设备管理】【异常】批量删除设备未勾选 RTSP
@pytest.mark.negative
def test_delete_device_muti_no_select(sb,login, setup_device_group_and_delete_group):
    device_name = f"{setup_device_group_and_delete_group['name']}RTSP"
    rtsp_device = RTSP(device_name, device_name, setup_device_group_and_delete_group['name'],
                       'Default', 'rtsp://1.1.1.1:554/test.264')
    DevicePage.add_device_by_type(sb, rtsp_device, '网络摄像机')
    DevicePage.search_device_by_name(sb,setup_device_group_and_delete_group['name'])
    DevicePage.delete_device_by_name_muti_no_select(sb)
    DevicePage.assert_alert_message(sb, '请选择设备')

#【设备管理】【异常】批量添加到分组未勾选 RTSP
@pytest.mark.negative
def test_move_device_muti_no_select(sb,login, setup_device_group_and_delete_group):
    device_name = f"{setup_device_group_and_delete_group['name']}RTSP"
    rtsp_device = RTSP(device_name, device_name, setup_device_group_and_delete_group['name'],
                       'Default', 'rtsp://1.1.1.1:554/test.264')
    DevicePage.add_device_by_type(sb, rtsp_device, '网络摄像机')
    DevicePage.search_device_by_name(sb,setup_device_group_and_delete_group['name'])
    DevicePage.move_device_by_name_muti_no_select(sb)
    DevicePage.assert_alert_message(sb, '请选择设备')

#【设备管理】【异常】批量操作添加到用户未勾选 RTSP
@pytest.mark.negative
def test_select_device_user_muti_no_select(sb,login, setup_device_group_and_delete_group):
    device_name = f"{setup_device_group_and_delete_group['name']}RTSP"
    rtsp_device = RTSP(device_name, device_name, setup_device_group_and_delete_group['name'],
                       'Default', 'rtsp://1.1.1.1:554/test.264')
    DevicePage.add_device_by_type(sb, rtsp_device, '网络摄像机')
    DevicePage.search_device_by_name(sb,setup_device_group_and_delete_group['name'])
    DevicePage.select_device_user_by_name_muti_no_select(sb)
    DevicePage.assert_alert_message(sb, '请选择设备')

#【设备管理】【界面】批量操作添加到用户勾选 RTSP
@pytest.mark.positive
def test_select_device_user_muti(sb,login, setup_device_group_and_delete_group):
    device_name = f"{setup_device_group_and_delete_group['name']}RTSP"
    rtsp_device = RTSP(device_name, device_name, setup_device_group_and_delete_group['name'],
                       'Default', 'rtsp://1.1.1.1:554/test.264')
    DevicePage.add_device_by_type(sb, rtsp_device, '网络摄像机')
    DevicePage.search_device_by_name(sb,setup_device_group_and_delete_group['name'])
    DevicePage.select_device_user_muti_search(sb)
    DevicePage.assert_alert_message(sb,'所选设备分配到用户成功')

#【设备管理】【界面】批量操作添加到用户搜索功能 RTSP
@pytest.mark.negative
def test_select_device_user_muti_search_invalid_user(sb,login, setup_device_group_and_delete_group):
    device_name = f"{setup_device_group_and_delete_group['name']}RTSP"
    rtsp_device = RTSP(device_name, device_name, setup_device_group_and_delete_group['name'],
                       'Default', 'rtsp://1.1.1.1:554/test.264')
    DevicePage.add_device_by_type(sb, rtsp_device, '网络摄像机')
    DevicePage.search_device_by_name(sb,setup_device_group_and_delete_group['name'])
    DevicePage.select_device_user_muti_search_invalid_user(sb)
    DevicePage.assert_alert_message(sb, '请选择用户')

#【设备管理】【界面】批量添加到分组勾选
@pytest.mark.positive
def test_move_device_muti(sb,login, setup_device_group_and_delete_group,setup_device_group):
    device_name = f"{setup_device_group_and_delete_group['name']}RTSP"
    rtsp_device = RTSP(device_name, device_name, setup_device_group_and_delete_group['name'],
                       'Default', 'rtsp://1.1.1.1:554/test.264')
    DevicePage.add_device_by_type(sb, rtsp_device, '网络摄像机')
    DevicePage.search_device_by_name(sb, setup_device_group_and_delete_group['name'])
    DevicePage.move_device_by_name_muti_search(sb,setup_device_group['name'])
    DevicePage.assert_alert_message(sb, '所选设备移动到分组成功')
    DevicePage.assert_rtsp_protocol_by_name(sb, device_name, setup_device_group['name'])
    DevicePage.delete_group_by_name(sb, setup_device_group['name'])

# 设备管理】【界面】批量移动到分组搜索功能（不存在）
@pytest.mark.negative111
def test_move_device_muti_invalid_group(sb,login, setup_device_group_and_delete_group):
    device_name = f"{setup_device_group_and_delete_group['name']}RTSP"
    invalid_group = f"{setup_device_group_and_delete_group['name']}NONE"
    rtsp_device = RTSP(device_name, device_name, setup_device_group_and_delete_group['name'],
                       'Default', 'rtsp://1.1.1.1:554/test.264')
    DevicePage.add_device_by_type(sb, rtsp_device, '网络摄像机')
    DevicePage.search_device_by_name(sb, setup_device_group_and_delete_group['name'])
    DevicePage.move_device_by_name_muti_search_invalid_group(sb,invalid_group)
    DevicePage.assert_alert_message(sb, '请选择分组')

#【RTSP】【异常】编辑RTSP摄像头地址为空（必填校验）

@pytest.mark.parametrize('url', [' ', '  '])
@pytest.mark.negative
def test_edit_rtsp_device_no_url(sb,url, login, setup_device_group_and_delete_group):
    D_id= f"{setup_device_group_and_delete_group['name']}RTSP"
    rtsp_device = RTSP(D_id, D_id, setup_device_group_and_delete_group['name'],
                       'Default', 'rtsp://1.1.1.1:554/test.264')
    DevicePage.add_device_by_type(sb, rtsp_device, '网络摄像机')
    rtsp_device = RTSP(D_id, D_id, setup_device_group_and_delete_group['name'],
                       'Default', url)
    DevicePage.edit_device_by_type(sb, rtsp_device, '网络摄像机',name = D_id)
    #DevicePage.queren_add_device(sb,menu='编辑')
    DevicePage.assert_element_text(sb, '.el-form-item__error', '请输入非空内容')
    DevicePage.cancel_add_device(sb,menu='编辑')

#【RTSP】【主流程】编辑RTSP摄像头传输协议切换
@pytest.mark.negative
def test_edit_rtsp_device_change_protocol(sb, login, setup_device_group_and_delete_group):
    device_name= f"{setup_device_group_and_delete_group['name']}RTSP"
    rtsp_device = RTSP(device_name, device_name, setup_device_group_and_delete_group['name'],
                       'Default', 'rtsp://1.1.1.1:554/test.264')
    DevicePage.add_device_by_type(sb, rtsp_device, '网络摄像机')
    rtsp_device = RTSP(device_name, device_name, setup_device_group_and_delete_group['name'],
                       'Default', 'rtsp://1.1.1.1:554/test.264')
    DevicePage.edit_device_by_type(sb, rtsp_device, '网络摄像机',name = device_name,protocol='UPD')
    DevicePage.assert_rtsp_protocol_by_name(sb,device_name,'UPD')
    DevicePage.delete_device_by_name(sb,device_name)

#【RTSP】【主流程】编辑RTSP摄像头编码类型切换
@pytest.mark.negative
def test_edit_rtsp_device_change_encoding_type(sb, login, setup_device_group_and_delete_group):
    device_name= f"{setup_device_group_and_delete_group['name']}RTSP"
    rtsp_device = RTSP(device_name, device_name, setup_device_group_and_delete_group['name'],
                       'Default', 'rtsp://1.1.1.1:554/test.264')
    DevicePage.add_device_by_type(sb, rtsp_device, '网络摄像机')
    rtsp_device = RTSP(device_name, device_name, setup_device_group_and_delete_group['name'],
                       'Default', 'rtsp://1.1.1.1:554/test.264')
    DevicePage.edit_device_by_type(sb, rtsp_device, '网络摄像机',name = device_name,encoding_type='Transcoding')
    DevicePage.assert_rtsp_protocol_by_name(sb,device_name,'编码')
    DevicePage.delete_device_by_name(sb,device_name)

#【RTSP】【界面】编辑RTSP摄像头预览正确地址
@pytest.mark.negative
def test_edit_rtsp_device_change_url_view(sb, login, setup_device_group_and_delete_group):
    device_name= f"{setup_device_group_and_delete_group['name']}RTSP"
    rtsp_device = RTSP(device_name, device_name, setup_device_group_and_delete_group['name'],
                       'Default', 'rtsp://1.1.1.1:554/test.264')
    DevicePage.add_device_by_type(sb, rtsp_device, '网络摄像机')
    rtsp_device = RTSP(device_name, device_name, setup_device_group_and_delete_group['name'],
                       'Default', 'rtsp://confidence.119:6554/test.264')
    DevicePage.edit_device_by_type_view(sb, rtsp_device, '网络摄像机',name = device_name)
    DevicePage.delete_device_by_name(sb,device_name)

# #【设备管理】【界面】添加摄像头类型切换
# @pytest.mark.negative
# def test_select_device_type(sb,login,setup_device_group_and_delete_group):
#     DevicePage.click_add_device_button(sb)
#     DevicePage.select_device_type(sb,'网络摄像机')
#     DevicePage.assert_element_text(sb, '.el-scrollbar__wrap > ul > li.el-select-dropdown__item.selected.hover>span', '网络摄像机')
#     DevicePage.select_device_type(sb, '人脸识别机（后）')
#     DevicePage.assert_element_text(sb, '.el-scrollbar__wrap > ul > li.el-select-dropdown__item.selected.hover>span',
#                                    '人脸识别机（后）')
#     DevicePage.select_device_type(sb, '人脸抓拍机')
#     DevicePage.assert_element_text(sb, '.el-scrollbar__wrap > ul > li.el-select-dropdown__item.selected.hover>span',
#                                    '人脸抓拍机')
#     DevicePage.select_device_type(sb, '身份验证一体机')
#     DevicePage.assert_element_text(sb, '.el-scrollbar__wrap > ul > li.el-select-dropdown__item.selected.hover>span',
#                                    '身份验证一体机')
#     DevicePage.select_device_type(sb, '人脸识别机（前）')
#     DevicePage.assert_element_text(sb, '.el-scrollbar__wrap > ul > li.el-select-dropdown__item.selected.hover>span',
#                                    '人脸识别机（前）')
#     DevicePage.cancel_add_device(sb)

#设备管理】【界面】编辑摄像头类型切换
@pytest.mark.negative
def test_edit_rtsp_device_change_camera_type(sb, login, setup_device_group_and_delete_group):
    device_name= f"{setup_device_group_and_delete_group['name']}RTSP"
    rtsp_device = RTSP(device_name, device_name, setup_device_group_and_delete_group['name'],
                       'Default', 'rtsp://1.1.1.1:554/test.264')
    DevicePage.add_device_by_type(sb, rtsp_device, '网络摄像机')
    DevicePage.click_edit_device_button(sb, device_name)

    onvif_device = ONVIF(device_name, device_name, setup_device_group_and_delete_group['name'],
                         'Default', '1.1.2.1', '80', 'admin', 'admin12345')
    DevicePage.edit_device_by_type(sb, onvif_device, '网络摄像机',name = device_name)
    DevicePage.assert_rtsp_protocol_by_name(sb,device_name,'ONVIF')
    DevicePage.delete_device_by_name(sb,device_name)

#【设备管理】【界面】查看设备类型
@pytest.mark.positive1
def test_view_device(sb, login, setup_device_group_and_delete_group):
    device_name= f"{setup_device_group_and_delete_group['name']}RTSP"
    rtsp_device = RTSP(device_name, device_name, setup_device_group_and_delete_group['name'],
                       'Default', 'rtsp://1.1.1.1:554/test.264')
    DevicePage.add_device_by_type(sb, rtsp_device, '网络摄像机')
    DevicePage.assert_rtsp_protocol_by_name(sb,device_name,'RTSP')

#编辑设备换组
@pytest.mark.negative
def test_edit_move_device(sb,login, setup_device_group_and_delete_group,setup_device_group):
    device_name= f"{setup_device_group_and_delete_group['name']}RTSP"
    rtsp_device = RTSP(device_name, device_name, setup_device_group_and_delete_group['name'],
                       'Default', 'rtsp://1.1.1.1:554/test.264')
    DevicePage.add_device_by_type(sb, rtsp_device, '网络摄像机')
    rtsp_device = RTSP(device_name, device_name, setup_device_group['name'],
                       'Default', 'rtsp://1.1.1.1:554/test.264')
    DevicePage.edit_device_by_type(sb, rtsp_device, '网络摄像机', name=device_name)
    DevicePage.assert_rtsp_protocol_by_name(sb, device_name,setup_device_group['name'])
    DevicePage.delete_device_by_name(sb, device_name)
    DevicePage.delete_group_by_name(sb, setup_device_group['name'])

#设备管理】【界面】编辑用户检索 不存在
@pytest.mark.negative
def test_edit_device_search_user_none(sb,login, setup_device_group_and_delete_group,):
    device_name= f"{setup_device_group_and_delete_group['name']}RTSP"
    rtsp_device = RTSP(device_name, device_name, setup_device_group_and_delete_group['name'],
                       'Default', 'rtsp://1.1.1.1:554/test.264')
    DevicePage.add_device_by_type(sb, rtsp_device, '网络摄像机')
    DevicePage.click_edit_device_button(sb,device_name)
    DevicePage.assert_edit_device_search_user_none(sb)



@pytest.mark.positive
def test_add_no_sense_rtsp_device(sb, login, setup_device_group_and_delete_group):
    device_name = f"{setup_device_group_and_delete_group['name']}RTSP"
    # no_sense_rtsp_device = RTSP('no_sense_rtsp', 'no_sense_rtsp', group_name,
    #                             'Default', 'rtsp://confidence.119:6554/test.264', 'confidence.119', '22')
    rtsp_device = RTSP(device_name, device_name, setup_device_group_and_delete_group['name'],
                       'Default', 'rtsp://1.1.1.1:554/test.264', 'confidence.119', '22')
    DevicePage.add_device_by_type(sb, rtsp_device, '网络摄像机')
    DevicePage.assert_alert_message(sb, '添加设备成功')


@pytest.mark.positive
def test_add_frontend_sensepass_device(sb, login, setup_device_group_and_delete_group):
    device_name = f"{setup_device_group_and_delete_group['name']}SP"
    frontend_device = Frontend(device_name, device_name, setup_device_group_and_delete_group['name'],
                               'Default', 'SensePass')
    DevicePage.add_device_by_type(
        sb, frontend_device, '人脸识别机（前）')
    DevicePage.assert_alert_message(sb, '添加设备成功')


@pytest.mark.shin
def test_add_frontend_sensepasspro_device(sb, login, setup_device_group_and_delete_group):
    device_name = f"{setup_device_group_and_delete_group['name']}SPP"
    frontend_device = Frontend(device_name, device_name, setup_device_group_and_delete_group['name'],
                               'Default', 'SensePass Pro')
    DevicePage.add_device_by_type(
        sb, frontend_device, '人脸识别机（前）')
    DevicePage.assert_alert_message(sb, '添加设备成功')


@pytest.mark.positive
def test_add_frontend_sensekeeper_device(sb, login, setup_device_group_and_delete_group):
    device_name = f"{setup_device_group_and_delete_group['name']}SK"
    frontend_device = Frontend(device_name, device_name, setup_device_group_and_delete_group['name'],
                               'Default', 'SenseKeeper')
    DevicePage.add_device_by_type(
        sb, frontend_device, '人脸识别机（前）')
    DevicePage.assert_alert_message(sb, '添加设备成功')


@pytest.mark.positive
def test_add_frontend_sensegate_device(sb, login, setup_device_group_and_delete_group):
    device_name = f"{setup_device_group_and_delete_group['name']}SK"
    frontend_device = Frontend(device_name, device_name, setup_device_group_and_delete_group['name'],
                               'Default', 'SenseGate')
    DevicePage.add_device_by_type(
        sb, frontend_device, '人脸识别机（前）')
    DevicePage.assert_alert_message(sb, '添加设备成功')


@pytest.mark.positive
def test_add_backend_device(sb, login, setup_device_group_and_delete_group):
    device_name = f"{setup_device_group_and_delete_group['name']}BE"
    backend_device = Device(device_name, device_name, setup_device_group_and_delete_group['name'],
                            'Default')
    DevicePage.add_device_by_type(sb, backend_device, '人脸识别机（后）')
    DevicePage.assert_alert_message(sb, '添加设备成功')


@pytest.mark.positive
def test_add_senseid_device(sb, login, setup_device_group_and_delete_group):
    device_name = f"{setup_device_group_and_delete_group['name']}SID"
    senseid_device = Device(device_name, device_name, setup_device_group_and_delete_group['name'],
                            'Default')
    DevicePage.add_device_by_type(sb, senseid_device, '身份验证一体机')
    DevicePage.assert_alert_message(sb, '添加设备成功')

###ONVIF设备
@pytest.mark.positive
def test_add_onvif_device(sb, login, setup_device_group_and_delete_group):
    device_name = f"{setup_device_group_and_delete_group['name']}ONVIF"
    # onvif_device = ONVIF('Onvif', 'Onvif', group_name,
    #                      'Default', 'confidence.116.175', '80', 'admin', 'admin12345')
    onvif_device = ONVIF(device_name, device_name, setup_device_group_and_delete_group['name'],
                         'Default', '1.1.2.1', '80', 'admin', 'admin12345')
    DevicePage.add_device_by_type(sb, onvif_device, '网络摄像机')
    DevicePage.assert_alert_message(sb, '添加设备成功')

#【ONVIF】【异常】添加ONVIF摄像头用户名为空（必填校验）

@pytest.mark.parametrize('name', ['', '  '])
@pytest.mark.negative
def test_add_onvif_device_no_username(sb, login,name, setup_device_group_and_delete_group):
    device_name = f"{setup_device_group_and_delete_group['name']}ONVIF"
    onvif_device = ONVIF(device_name, device_name, setup_device_group_and_delete_group['name'],
                         'Default', '1.1.2.1', '80', name, 'admin12345')
    DevicePage.add_device_by_type(sb, onvif_device, '网络摄像机')
    DevicePage.assert_element_text(sb, '.el-form-item__error', '请输入非空内容')
    DevicePage.cancel_add_device(sb)

#【ONVIF】【异常】添加ONVIF摄像头PORT为空（必填校验）
@pytest.mark.parametrize('port', ['', '  '])
@pytest.mark.negative
def test_add_onvif_device_no_port(sb, login,port, setup_device_group_and_delete_group):
    device_name = f"{setup_device_group_and_delete_group['name']}ONVIF"
    onvif_device = ONVIF(device_name, device_name, setup_device_group_and_delete_group['name'],
                         'Default', '1.1.2.1', port, 'admin', 'admin12345')
    DevicePage.add_device_by_type(sb, onvif_device, '网络摄像机')
    DevicePage.assert_element_text(sb, '.el-form-item__error', '请输入非空内容')
    DevicePage.cancel_add_device(sb)

#【ONVIF】【异常】添加ONVIF摄像头IP为空（必填校验）
@pytest.mark.parametrize('ip', [''])
@pytest.mark.negative
def test_add_onvif_device_no_ip(sb, login,ip, setup_device_group_and_delete_group):
    device_name = f"{setup_device_group_and_delete_group['name']}ONVIF"
    onvif_device = ONVIF(device_name, device_name, setup_device_group_and_delete_group['name'],
                         'Default',ip, '80', 'admin', 'admin12345')
    DevicePage.add_device_by_type(sb, onvif_device, '网络摄像机')
    DevicePage.assert_element_text(sb, '.el-form-item__error', '请输入非空内容')
    DevicePage.cancel_add_device(sb)

#【ONVIF】【异常】添加ONVIF摄像头密码为空（必填校验）
@pytest.mark.parametrize('password', ['', '  '])
@pytest.mark.negative
def test_add_onvif_device_no_password(sb, login,password, setup_device_group_and_delete_group):
    device_name = f"{setup_device_group_and_delete_group['name']}ONVIF"
    onvif_device = ONVIF(device_name, device_name, setup_device_group_and_delete_group['name'],
                         'Default','1.1.2.1', '80', 'admin',password)
    DevicePage.add_device_by_type(sb, onvif_device, '网络摄像机')
    DevicePage.assert_element_text(sb, '.el-form-item__error', '请输入非空内容')
    DevicePage.cancel_add_device(sb)

#【ONVIF】【异常】添加ONVIF摄像头IP为非规格（必填校验）
@pytest.mark.parametrize('ip', ['11111'])
@pytest.mark.negative
def test_add_onvif_device_irregularity_ip(sb, login,ip, setup_device_group_and_delete_group):
    device_name = f"{setup_device_group_and_delete_group['name']}ONVIF"
    onvif_device = ONVIF(device_name, device_name, setup_device_group_and_delete_group['name'],
                         'Default',ip, '80', 'admin', 'admin12345')
    DevicePage.add_device_by_type(sb, onvif_device, '网络摄像机')
    DevicePage.assert_element_text(sb, '.el-form-item__error', '请输入正确的ip格式')
    DevicePage.cancel_add_device(sb)

#【ONVIF】【异常】添加ONVIF摄像头PORT为格式不正确（格式校验）
@pytest.mark.parametrize('port', ['wwwww'])
@pytest.mark.negative
def test_add_onvif_device_irregularity_port(sb, login,port, setup_device_group_and_delete_group):
    device_name = f"{setup_device_group_and_delete_group['name']}ONVIF"
    onvif_device = ONVIF(device_name, device_name, setup_device_group_and_delete_group['name'],
                         'Default', '1.1.2.1', port, 'admin', 'admin12345')
    DevicePage.add_device_by_type(sb, onvif_device, '网络摄像机')
    DevicePage.assert_element_text(sb, '.el-form-item__error', '请输入非空内容')
    DevicePage.cancel_add_device(sb)

#【ONVIF】【异常】添加ONVIF摄像头PORT大于65535（长度校验）
@pytest.mark.parametrize('port', ['12312411'])
@pytest.mark.negative
def test_add_onvif_device_long_port(sb, login,port, setup_device_group_and_delete_group):
    device_name = f"{setup_device_group_and_delete_group['name']}ONVIF"
    onvif_device = ONVIF(device_name, device_name, setup_device_group_and_delete_group['name'],
                         'Default', '1.1.2.1', port, 'admin', 'admin12345')
    DevicePage.add_device_by_type(sb, onvif_device, '网络摄像机')
    DevicePage.assert_element_text(sb, '.el-form-item__error', '请输入1-65535范围内的端口')
    DevicePage.cancel_add_device(sb)

#【ONVIF】【异常】添加ONVIF摄像头密码超20位（必填校验）
@pytest.mark.parametrize('password', ['a12345678901234567890'])
@pytest.mark.negative
def test_add_onvif_device_long_password(sb, login,password, setup_device_group_and_delete_group):
    password_cut = password[0:20]
    device_name = f"{setup_device_group_and_delete_group['name']}ONVIF"
    onvif_device = ONVIF(device_name, device_name, setup_device_group_and_delete_group['name'],
                         'Default','1.1.2.1', '80', 'admin',password)
    DevicePage.add_device_by_type(sb, onvif_device, '网络摄像机')
    DevicePage.assert_rtsp_protocol_by_name(sb, device_name, password_cut)

#【ONVIF】【异常】添加ONVIF摄像头用户名超40位（必填校验）
@pytest.mark.parametrize('name', ['a1234567890123456789012345678901234567890'])
@pytest.mark.negative
def test_add_onvif_device_long_username(sb, login,name, setup_device_group_and_delete_group):
    name_cut = name[0:40]
    device_name = f"{setup_device_group_and_delete_group['name']}ONVIF"
    onvif_device = ONVIF(device_name, device_name, setup_device_group_and_delete_group['name'],
                         'Default', '1.1.2.1', '80', name, 'admin12345')
    DevicePage.add_device_by_type(sb, onvif_device, '网络摄像机')
    DevicePage.assert_rtsp_protocol_by_name(sb, device_name, name_cut)


#【ONVIF】【异常】编辑ONVIF摄像头IP为格式不正确（必填校验）
@pytest.mark.parametrize('ip', ['11111'])
@pytest.mark.negative
def test_edit_onvif_device_irregularity_ip(sb, login,ip, setup_device_group_and_delete_group):
    device_name = f"{setup_device_group_and_delete_group['name']}ONVIF"
    onvif_device = ONVIF(device_name, device_name, setup_device_group_and_delete_group['name'],
                         'Default', '1.1.2.1', '80', 'admin', 'admin12345')
    DevicePage.add_device_by_type(sb, onvif_device, '网络摄像机')
    onvif_device = ONVIF(device_name, device_name, setup_device_group_and_delete_group['name'],
                         'Default', ip, '80', 'admin', 'admin12345')
    DevicePage.edit_device_by_type(sb, onvif_device, '网络摄像机',device_name)
    DevicePage.assert_element_text(sb, '.el-form-item__error', '请输入正确的ip格式')
    DevicePage.cancel_add_device(sb,'编辑')

#【ONVIF】【异常】编辑ONVIF摄像头PORT为格式不正确（格式校验）
@pytest.mark.parametrize('port', ['wwwww'])
@pytest.mark.negative
def test_edit_onvif_device_irregularity_port(sb, login,port, setup_device_group_and_delete_group):
    device_name = f"{setup_device_group_and_delete_group['name']}ONVIF"
    onvif_device = ONVIF(device_name, device_name, setup_device_group_and_delete_group['name'],
                         'Default', '1.1.2.1', '80', 'admin', 'admin12345')
    DevicePage.add_device_by_type(sb, onvif_device, '网络摄像机')
    onvif_device = ONVIF(device_name, device_name, setup_device_group_and_delete_group['name'],
                         'Default', '1.1.2.1', port, 'admin', 'admin12345')
    DevicePage.edit_device_by_type(sb, onvif_device, '网络摄像机', device_name)
    DevicePage.assert_element_text(sb, '.el-form-item__error', '请输入非空内容')
    DevicePage.cancel_add_device(sb,'编辑')

#【ONVIF】【异常】编辑ONVIF摄像头PORT大于65535（长度校验）
@pytest.mark.parametrize('port', ['12312411'])
@pytest.mark.negative
def test_edit_onvif_device_long_port(sb, login,port, setup_device_group_and_delete_group):
    device_name = f"{setup_device_group_and_delete_group['name']}ONVIF"
    onvif_device = ONVIF(device_name, device_name, setup_device_group_and_delete_group['name'],
                         'Default', '1.1.2.1', '80', 'admin', 'admin12345')
    DevicePage.add_device_by_type(sb, onvif_device, '网络摄像机')
    onvif_device = ONVIF(device_name, device_name, setup_device_group_and_delete_group['name'],
                         'Default', '1.1.2.1', port, 'admin', 'admin12345')
    DevicePage.edit_device_by_type(sb, onvif_device, '网络摄像机', device_name)
    DevicePage.assert_element_text(sb, '.el-form-item__error', '请输入1-65535范围内的端口')
    DevicePage.cancel_add_device(sb,'编辑')

#【ONVIF】【异常】编辑ONVIF摄像头密码超20位（必填校验）
@pytest.mark.parametrize('password', ['a12345678901234567890'])
@pytest.mark.negative1
def test_edit_onvif_device_long_password(sb, login,password, setup_device_group_and_delete_group):
    password_cut = password[0:20]
    device_name = f"{setup_device_group_and_delete_group['name']}ONVIF"
    onvif_device = ONVIF(device_name, device_name, setup_device_group_and_delete_group['name'],
                         'Default','1.1.2.1', '80', 'admin','admin12345')
    DevicePage.add_device_by_type(sb, onvif_device, '网络摄像机')
    onvif_device = ONVIF(device_name, device_name, setup_device_group_and_delete_group['name'],
                         'Default','1.1.2.1', '80', 'admin',password)
    DevicePage.edit_device_by_type(sb, onvif_device, '网络摄像机', device_name)
    DevicePage.assert_rtsp_protocol_by_name(sb, device_name, password_cut)

#【ONVIF】【异常】编辑ONVIF摄像头用户名超40位（必填校验）
@pytest.mark.parametrize('name', ['a1234567890123456789012345678901234567890'])
@pytest.mark.negative
def test_edit_onvif_device_long_username(sb, login,name, setup_device_group_and_delete_group):
    name_cut = name[0:40]
    device_name = f"{setup_device_group_and_delete_group['name']}ONVIF"
    onvif_device = ONVIF(device_name, device_name, setup_device_group_and_delete_group['name'],
                         'Default', '1.1.2.1', '80', 'admin', 'admin12345')
    DevicePage.add_device_by_type(sb, onvif_device, '网络摄像机')
    onvif_device = ONVIF(device_name, device_name, setup_device_group_and_delete_group['name'],
                         'Default', '1.1.2.1', '80', name, 'admin12345')
    DevicePage.edit_device_by_type(sb, onvif_device, '网络摄像机', device_name)
    DevicePage.assert_rtsp_protocol_by_name(sb, device_name, name_cut)

#【ONVIF】【异常】编辑ONVIF摄像头密码为多个空格
@pytest.mark.parametrize('password', [' ','  '])
@pytest.mark.negative
def test_edit_onvif_device_no_password(sb, login,password, setup_device_group_and_delete_group):
    device_name = f"{setup_device_group_and_delete_group['name']}ONVIF"
    onvif_device = ONVIF(device_name, device_name, setup_device_group_and_delete_group['name'],
                         'Default','1.1.2.1', '80', 'admin','admin12345')
    DevicePage.add_device_by_type(sb, onvif_device, '网络摄像机')
    onvif_device = ONVIF(device_name, device_name, setup_device_group_and_delete_group['name'],
                         'Default','1.1.2.1', '80', 'admin',password)
    DevicePage.edit_device_by_type(sb, onvif_device, '网络摄像机', device_name)
    DevicePage.assert_element_text(sb, '.el-form-item__error', '请输入非空内容')
    DevicePage.cancel_add_device(sb,'编辑')

#【ONVIF】【异常】编辑ONVIF摄像头用户名为多个空格
@pytest.mark.parametrize('name', [' ','  '])
@pytest.mark.negative
def test_edit_onvif_device_no_username(sb, login,name, setup_device_group_and_delete_group):
    device_name = f"{setup_device_group_and_delete_group['name']}ONVIF"
    onvif_device = ONVIF(device_name, device_name, setup_device_group_and_delete_group['name'],
                         'Default','1.1.2.1', '80', 'admin','admin12345')
    DevicePage.add_device_by_type(sb, onvif_device, '网络摄像机')
    onvif_device = ONVIF(device_name, device_name, setup_device_group_and_delete_group['name'],
                         'Default','1.1.2.1', '80', name,'admin12345')
    DevicePage.edit_device_by_type(sb, onvif_device, '网络摄像机', device_name)
    DevicePage.assert_element_text(sb, '.el-form-item__error', '请输入非空内容')
    DevicePage.cancel_add_device(sb,'编辑')

#【ONVIF】【异常】编辑ONVIF摄像头port为多个空格
@pytest.mark.parametrize('port', [' ','  '])
@pytest.mark.negative
def test_edit_onvif_device_no_port(sb, login,port, setup_device_group_and_delete_group):
    device_name = f"{setup_device_group_and_delete_group['name']}ONVIF"
    onvif_device = ONVIF(device_name, device_name, setup_device_group_and_delete_group['name'],
                         'Default','1.1.2.1', '80', 'admin','admin12345')
    DevicePage.add_device_by_type(sb, onvif_device, '网络摄像机')
    onvif_device = ONVIF(device_name, device_name, setup_device_group_and_delete_group['name'],
                         'Default','1.1.2.1', port, 'admin','admin12345')
    DevicePage.edit_device_by_type(sb, onvif_device, '网络摄像机', device_name)
    DevicePage.assert_element_text(sb, '.el-form-item__error', '请输入非空内容')
    DevicePage.cancel_add_device(sb,'编辑')

#【ONVIF】【异常】编辑ONVIF摄像头ip为多个空格
@pytest.mark.parametrize('ip', [' ','  '])
@pytest.mark.negative1
def test_edit_onvif_device_no_ip(sb, login,ip, setup_device_group_and_delete_group):
    device_name = f"{setup_device_group_and_delete_group['name']}ONVIF"
    onvif_device = ONVIF(device_name, device_name, setup_device_group_and_delete_group['name'],
                         'Default','1.1.2.1', '80', 'admin','admin12345')
    DevicePage.add_device_by_type(sb, onvif_device, '网络摄像机')
    onvif_device = ONVIF(device_name, device_name, setup_device_group_and_delete_group['name'],
                         'Default',ip, '80', 'admin','admin12345')
    DevicePage.edit_device_by_type(sb, onvif_device, '网络摄像机', device_name)
    DevicePage.assert_element_text(sb, '.el-form-item__error', '请输入正确的ip格式')
    DevicePage.cancel_add_device(sb,'编辑')











@pytest.mark.positive
def test_add_dlc_d_device(sb, login, setup_device_group_and_delete_group):
    device_name = f"{setup_device_group_and_delete_group['name']}DLCD"
    # dlc_device = DLC('SenseDLC-D', 'SenseDLC-D', group_name,
    #                      'Default', '商汤 -D/-AA系列', 'confidence.116.175', '37777', 'admin', 'admin1234')
    dlc_device = DLC(device_name, device_name, setup_device_group_and_delete_group['name'],
                     'Default', '商汤 -D/-AA系列', '1.1.1.1', '37777', 'admin', 'admin1234')
    DevicePage.add_device_by_type(sb, dlc_device, '人脸抓拍机')
    DevicePage.assert_alert_message(sb, '添加设备成功')


@pytest.mark.positive
def test_add_dlc_11_device(sb, login, setup_device_group_and_delete_group):
    device_name = f"{setup_device_group_and_delete_group['name']}DLC11"
    # dlc_device = DLC('SenseDLC-11', 'SenseDLC-11', group_name,
    #                      'Default', '商汤-11系列', 'confidence.116.180', '36123', 'admin', 'admin1234')
    dlc_device = DLC(device_name, device_name,  setup_device_group_and_delete_group['name'],
                     'Default', '商汤-11系列', '1.1.1.2', '36123', 'admin', 'admin1234')
    DevicePage.add_device_by_type(sb, dlc_device, '人脸抓拍机')
    DevicePage.assert_alert_message(sb, '添加设备成功')


@pytest.mark.positive
def test_add_dlc_dahua_device(sb, login, setup_device_group_and_delete_group):
    device_name = f"{setup_device_group_and_delete_group['name']}DLCDH"
    # dlc_device = DLC('Dahua', 'Dahua', group_name,
    #                      'Default', '大华', 'confidence.116.173', '37777', 'admin', 'admin1234')
    dlc_device = DLC(device_name, device_name, setup_device_group_and_delete_group['name'],
                     'Default', '大华', '1.1.1.3', '37777', 'admin', 'admin1234')
    DevicePage.add_device_by_type(sb, dlc_device, '人脸抓拍机')
    DevicePage.assert_alert_message(sb, '添加设备成功')


@pytest.mark.positive
def test_add_dlc_hikvision_device(sb, login, setup_device_group_and_delete_group):
    device_name = f"{setup_device_group_and_delete_group['name']}DLCHK"
    # dlc_device = DLC('Hikvision', 'Hikvision', group_name,
    #                      'Default', '海康', 'confidence.116.199', '8000', 'admin', 'admin1234')
    dlc_device = DLC(device_name, device_name, setup_device_group_and_delete_group['name'],
                     'Default', '海康', '1.1.1.4', '8000', 'admin', 'admin1234')
    DevicePage.add_device_by_type(sb, dlc_device, '人脸抓拍机')
    DevicePage.assert_alert_message(sb, '添加设备成功')

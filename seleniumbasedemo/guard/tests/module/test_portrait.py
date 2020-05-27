#!/usr/bin/env python3

import os

import pytest
from seleniumbase import config as sb_config
from parameterized import parameterized

from guard.pages.components.dialog import Dialog
from guard.pages.components.menubar import MenuBar
from guard.pages.components.table_list import TableList
from guard.pages.portrait import PortraitPage
from guard.pages.classes.portrait import Portrait


@pytest.mark.parametrize('portrait_type', ['白名单', '重点人员'])
@pytest.mark.positive
def test_add_portrait_database(sb, login, portrait_type, setup_portrait_database_name_and_delete_portrait_database):
    PortraitPage.add_portrait_database_by_name(
        sb, setup_portrait_database_name_and_delete_portrait_database['name'], type=portrait_type)
    PortraitPage.assert_alert_message(sb, '创建下一级分组成功')
    PortraitPage.search_portrait_database_by_name(
        sb, setup_portrait_database_name_and_delete_portrait_database['name'])
    sb.is_element_visible(
        f'//div[@title="{setup_portrait_database_name_and_delete_portrait_database["name"]}"]')


@pytest.mark.parametrize('name', ['', '  '])
@pytest.mark.negative
def test_add_portrait_database_with_invalid_name(sb, login, name):
    MenuBar.click_menu_item_by_text(sb, '配置', '人像库管理')
    PortraitPage.add_portrait_database_by_name(sb, name)
    PortraitPage.assert_element_text(sb, '.tips > span', '请输入分组名称')


@pytest.mark.parametrize('portrait_type', ['白名单', '重点人员'])
@pytest.mark.positive
def test_view_portrait_database(sb, login, portrait_type, setup_portrait_database_and_delete_portrait_database):
    PortraitPage.view_portrait_database_by_name(
        sb, setup_portrait_database_and_delete_portrait_database['name'], confirm=False)
    sb.is_element_visible('//div[@class="left"]/span[text()="分组类型"]')
    sb.is_element_visible('//div[@class="left"]/span[text()="分组名称"]')
    sb.is_element_visible('//div[@class="left"]/span[text()="创建时间"]')
    sb.is_element_visible('//div[@class="left"]/span[text()="创建者"]')
    sb.is_element_visible(
        f'//div[@class="right"]/span[text()="{portrait_type}"]')
    sb.is_element_visible(
        f'//div[@class="right"]/span[text()="{setup_portrait_database_and_delete_portrait_database["name"]}"]')
    sb.is_element_visible(
        f'//div[@class="right"]/span[text()="{sb_config.username}"]')


@pytest.mark.parametrize('portrait_type', ['白名单', "重点人员"])
@pytest.mark.positive
def test_rename_existing_portrait_database(sb, login, setup_portrait_database):
    new_name = f'{setup_portrait_database["name"]}N'
    PortraitPage.rename_portrait_database_by_name(
        sb, setup_portrait_database['name'], new_name)
    PortraitPage.search_portrait_database_by_name(
        sb, setup_portrait_database['name'])
    sb.is_element_visible(
        f'//div[@title="{new_name}"]')
    PortraitPage.delete_portrait_database_by_name(sb, new_name)


@pytest.mark.parametrize('portrait_type', ['白名单', "重点人员"])
@pytest.mark.parametrize('name', ['  '])
@pytest.mark.negative
def test_rename_existing_portrait_database_with_invalid_name(sb, login, name, setup_portrait_database_and_delete_portrait_database):
    PortraitPage.rename_portrait_database_by_name(
        sb, setup_portrait_database_and_delete_portrait_database['name'], name)
    PortraitPage.assert_element_text(sb, '.tips > span', '请输入分组名称')
    Dialog.click_dialog_footer_button_by_text(sb, '编辑', '取消')


@pytest.mark.parametrize('portrait_type', ['白名单', "重点人员"])
@pytest.mark.positive
def test_delete_existing_portrait_database(sb, login, setup_portrait_database):
    PortraitPage.delete_portrait_database_by_name(
        sb, setup_portrait_database['name'])
    PortraitPage.assert_alert_message(sb, '删除分组成功')
    sb.is_element_visible('//span[text()="暂无数据"]')


@pytest.mark.parametrize('portrait_type', ['白名单', "重点人员"])
@pytest.mark.positive
def test_search_existing_portrait_database(sb, login, setup_portrait_database_and_delete_portrait_database):
    PortraitPage.search_portrait_database_by_name(
        sb, setup_portrait_database_and_delete_portrait_database['name'])
    sb.is_element_visible(
        f'//div[@title="{setup_portrait_database_and_delete_portrait_database["name"]}"]')


@pytest.mark.negative
def test_search_not_existing_portrait_database(sb, login, setup_portrait_database_name):
    PortraitPage.search_portrait_database_by_name(
        sb, setup_portrait_database_name['name'])
    sb.is_element_visible('//span[text()="暂无数据"]')


@pytest.mark.parametrize('image_path', ['/guard/data/portrait/001-JPG.jpg', '/guard/data/portrait/002-JPEG.jpeg',
                                        '/guard/data/portrait/003-PNG.png', '/guard/data/portrait/004-BMP.bmp'])
@pytest.mark.positive
def test_add_valid_portrait(sb, login, setup_portrait_database_and_delete_portrait_database, setup_portrait_name, image_path):
    portrait = Portrait(name=setup_portrait_name['name'], id_number=setup_portrait_name['name'],
                        image_path=os.getcwd()+image_path,
                        portrait_databases=[setup_portrait_database_and_delete_portrait_database['name']])
    PortraitPage.add_portrait(sb, portrait)
    PortraitPage.assert_alert_message(sb, '添加人像成功')
    PortraitPage.search_portrait_by_keyword(sb, setup_portrait_name['name'])
    sb.is_element_visible(
        f'//table//div[@class="cell" and contains(text(), "{setup_portrait_name["name"]}")]')


@pytest.mark.parametrize('image_path, alert_message',
                         [('/guard/data/portrait/005-NoFace.jpeg', '检测不到人脸'),
                          ('/guard/data/portrait/006-MultiFace.jpg', '检测到多个人脸'),
                          ('/guard/data/portrait/007-LowQuality.jpeg', '图片质量分数过低'),
                          ('/guard/data/portrait/008-Over16MB.jpeg',
                           '上传图片大小不能超过 16MB!'),
                          ('/guard/data/portrait/009-LessThan32Pixel.jpg',
                           '图片大小不合格，请选择大于32*32像素但不大于16M的图片'),
                          ('/guard/data/portrait/010-GIF.gif', '上传图片只能是 JPG/PNG/JPEG/BMP 格式!')])
@pytest.mark.negative
def test_add_invalid_portrait_image(sb, login, setup_portrait_name, image_path, alert_message):
    PortraitPage.click_add_portrait_button(sb)
    PortraitPage.upload_portrait_image(sb, '添加人像', os.getcwd()+image_path)
    PortraitPage.assert_alert_message(sb, alert_message)


@pytest.mark.negative
def test_required_fields_when_adding_portrait(sb, login, setup_portrait_name):
    PortraitPage.click_add_portrait_button(sb)
    Dialog.click_dialog_footer_button_by_text(sb, '添加人像', '确定')
    sb.is_element_visible(
        '//div[@class="el-form-item__error" and contains(text(), "请上传本地人像照片")]')
    sb.is_element_visible(
        '//div[@class="el-form-item__error" and contains(text(), "请输入姓名")]')
    sb.is_element_visible(
        '//div[@class="el-form-item__error" and contains(text(), "请输入No.")]')
    sb.is_element_visible(
        '//div[@class="el-form-item__error" and contains(text(), "请选择人像库")]')
    sb.is_element_visible(
        '//div[@class="el-form-item__error" and contains(text(), "请选择时间")]')


@pytest.mark.positive
def test_fields_length_when_adding_portrait(sb, login, setup_portrait_name):
    PortraitPage.click_add_portrait_button(sb)
    PortraitPage.assert_element_attribute_value(
        sb, '//div[@aria-label="添加人像"]//label[text()="姓名"]/parent::*//input', 'maxlength', '40')
    PortraitPage.assert_element_attribute_value(
        sb, '//div[@aria-label="添加人像"]//label[text()="别名"]/parent::*//input', 'maxlength', '40')
    PortraitPage.assert_element_attribute_value(
        sb, '//div[@aria-label="添加人像"]//label[text()="No."]/parent::*//input', 'maxlength', '32')
    PortraitPage.assert_element_attribute_value(
        sb, '//div[@aria-label="添加人像"]//label[text()="年龄"]/parent::*//input', 'maxlength', '3')
    PortraitPage.assert_element_attribute_value(
        sb, '//div[@aria-label="添加人像"]//label[text()="公司"]/parent::*//input', 'maxlength', '40')
    PortraitPage.assert_element_attribute_value(
        sb, '//div[@aria-label="添加人像"]//label[text()="部门"]/parent::*//input', 'maxlength', '40')
    PortraitPage.assert_element_attribute_value(
        sb, '//div[@aria-label="添加人像"]//label[text()="联系方式"]/parent::*//input', 'maxlength', '40')
    PortraitPage.assert_element_attribute_value(
        sb, '//div[@aria-label="添加人像"]//label[text()="车牌号"]/parent::*//input', 'maxlength', '40')
    PortraitPage.assert_element_attribute_value(
        sb, '//div[@aria-label="添加人像"]//label[text()="住址"]/parent::*//input', 'maxlength', '30')


@pytest.mark.positive
def test_delete_existing_portrait_in_one_portrait_database_from_global_portrait_database(sb, login, setup_portrait_with_portrait_database_and_delete_portrait_database):
    PortraitPage.search_portrait_by_keyword(
        sb, setup_portrait_with_portrait_database_and_delete_portrait_database['name'])
    PortraitPage.delete_portrait_by_name(
        sb, setup_portrait_with_portrait_database_and_delete_portrait_database['name'])
    PortraitPage.assert_alert_message(sb, '删除人像成功')
    PortraitPage.search_portrait_by_keyword(
        sb, setup_portrait_with_portrait_database_and_delete_portrait_database['name'])
    sb.is_element_visible('//span[text()="暂无数据"]')


@pytest.mark.positive
def test_delete_existing_portrait_in_two_portrait_databases_from_current_portrait_database(sb, login, setup_portrait_with_two_portrait_databases_and_delete_portrait_databases):
    PortraitPage.search_portrait_by_keyword(
        sb, setup_portrait_with_two_portrait_databases_and_delete_portrait_databases['name'])
    PortraitPage.click_portrait_database_by_name(
        sb, setup_portrait_with_two_portrait_databases_and_delete_portrait_databases['portrait_databases'][0])
    PortraitPage.delete_portrait_by_name(
        sb, setup_portrait_with_two_portrait_databases_and_delete_portrait_databases['name'], from_current_group=True)
    PortraitPage.assert_alert_message(sb, '删除人像成功')
    PortraitPage.search_portrait_by_keyword(
        sb, setup_portrait_with_two_portrait_databases_and_delete_portrait_databases['name'])
    sb.is_element_visible(
        f'//div[@title="{setup_portrait_with_two_portrait_databases_and_delete_portrait_databases["portrait_databases"][1]}" and text()="{setup_portrait_with_two_portrait_databases_and_delete_portrait_databases["portrait_databases"][1]} (1)"]')


@pytest.mark.positive
def test_delete_existing_portrait_in_two_portrait_databases_from_global_portrait_database(sb, login, setup_portrait_with_two_portrait_databases_and_delete_portrait_databases):
    PortraitPage.search_portrait_by_keyword(
        sb, setup_portrait_with_two_portrait_databases_and_delete_portrait_databases['name'])
    PortraitPage.click_portrait_database_by_name(
        sb, setup_portrait_with_two_portrait_databases_and_delete_portrait_databases['portrait_databases'][0])
    PortraitPage.delete_portrait_by_name(
        sb, setup_portrait_with_two_portrait_databases_and_delete_portrait_databases['name'])
    PortraitPage.assert_alert_message(sb, '删除人像成功')
    PortraitPage.search_portrait_by_keyword(
        sb, setup_portrait_with_two_portrait_databases_and_delete_portrait_databases['name'])
    sb.is_element_visible('//span[text()="暂无数据"]')


@pytest.mark.positive
def test_search_existing_portrait(sb, login, setup_portrait_with_portrait_database_and_delete_portrait_database):
    PortraitPage.search_portrait_by_keyword(
        sb, setup_portrait_with_portrait_database_and_delete_portrait_database['name'])
    sb.is_element_visible(
        f'//table//div[@class="cell" and contains(text(), "{setup_portrait_with_portrait_database_and_delete_portrait_database["name"]}")]')


@pytest.mark.negative
def test_search_not_existing_portrait(sb, login, setup_portrait_name):
    PortraitPage.search_portrait_by_keyword(
        sb, setup_portrait_name['name'])
    sb.is_element_visible('//span[text()="暂无数据"]')


@pytest.mark.parametrize('image_path', ['/guard/data/portrait/001-JPG.jpg', '/guard/data/portrait/002-JPEG.jpeg',
                                        '/guard/data/portrait/003-PNG.png', '/guard/data/portrait/004-BMP.bmp'])
@pytest.mark.positive
def test_edit_valid_portrait(sb, login, setup_portrait_with_portrait_database_and_delete_portrait_database, image_path):
    old_img_src = PortraitPage.get_portrait_img_src_by_name(
        sb, setup_portrait_with_portrait_database_and_delete_portrait_database['name'])
    portrait = Portrait(name=setup_portrait_with_portrait_database_and_delete_portrait_database['name'],
                        id_number=setup_portrait_with_portrait_database_and_delete_portrait_database[
                            'name'],
                        image_path=os.getcwd()+image_path,
                        portrait_databases=[setup_portrait_with_portrait_database_and_delete_portrait_database['portrait_database']])
    PortraitPage.edit_portrait_by_name(
        sb, setup_portrait_with_portrait_database_and_delete_portrait_database['name'], portrait)
    new_img_src = PortraitPage.get_portrait_img_src_by_name(
        sb, setup_portrait_with_portrait_database_and_delete_portrait_database['name'])
    assert new_img_src != old_img_src


@pytest.mark.parametrize('image_path, alert_message',
                         [('/guard/data/portrait/005-NoFace.jpeg', '检测不到人脸'),
                          ('/guard/data/portrait/006-MultiFace.jpg', '检测到多个人脸'),
                          ('/guard/data/portrait/007-LowQuality.jpeg', '图片质量分数过低'),
                          ('/guard/data/portrait/008-Over16MB.jpeg',
                           '上传图片大小不能超过 16MB!'),
                          ('/guard/data/portrait/009-LessThan32Pixel.jpg',
                           '图片大小不合格，请选择大于32*32像素但不大于16M的图片'),
                          ('/guard/data/portrait/010-GIF.gif', '上传图片只能是 JPG/PNG/JPEG/BMP 格式!')])
@pytest.mark.negative
def test_edit_invalid_portrait_image(sb, login, setup_portrait_with_portrait_database_and_delete_portrait_database, image_path, alert_message):
    TableList.click_edit_button_by_name(
        sb, setup_portrait_with_portrait_database_and_delete_portrait_database['name'])
    PortraitPage.upload_portrait_image(sb, '编辑', os.getcwd()+image_path)
    Dialog.click_dialog_footer_button_by_text(sb, '编辑', '取消')

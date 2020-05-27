#!/usr/bin/env python3

import os
import pytest
import re
from parameterized import parameterized

from guard.pages.components.menubar import MenuBar
from guard.pages.tools import Tools
from guard.data.portrait.face_property.face_property import FacePropertyData as FPData


@pytest.mark.positive
def test_score_detection(sb, login):
    MenuBar.click_menu_item_by_text(sb, '工具', '质量分数检测')
    Tools.evaluate_face_image_quality(
        sb, os.getcwd()+'/guard/data/seleniumbase.jpg')
    assert re.match(r'\d+.\d+%', Tools.get_face_image_quality_result(sb))


@pytest.mark.positive
def test_detect_facial_attribute(sb, login):
    """ 测试1:1人脸验证功能 """
    sb.sleep(2)
    MenuBar.click_menu_item_by_text(sb, '工具', '1:1人脸验证')
    Tools.verify_one_to_one_face(
        sb, os.getcwd()+'/guard/data/portrait/face_img/img1.jpg', os.getcwd()+'/guard/data/portrait/face_img/img2.jpg')
    assert '评分参考' == Tools.get_one_to_one_face_result(sb)


@pytest.mark.positive
def test_check_all_face_property(sb, login):
    """ 测试人脸属性输出的属性字段 """
    MenuBar.click_menu_item_by_text(sb, '工具', '人脸属性检测')
    Tools.detect_facial_attribute(
        sb, os.getcwd()+'/guard/data/portrait/face_property/seleniumbase.jpg')

    sex_data = Tools.get_facial_attribute_by_name(sb, "性别")
    age_data = Tools.get_facial_attribute_by_name(sb, "年龄")
    phiz_data = Tools.get_facial_attribute_by_name(sb, "表情")
    mustache_data = Tools.get_facial_attribute_by_name(sb, "胡子")
    glasse_data = Tools.get_facial_attribute_by_name(sb, "眼镜")
    mask_data = Tools.get_facial_attribute_by_name(sb, "口罩")
    helmet_data = Tools.get_facial_attribute_by_name(sb, "安全帽")
    hat_data = Tools.get_facial_attribute_by_name(sb, "帽子")

    assert '性别:' == sex_data[0] and '年龄:' == age_data[0] and '表情:' == phiz_data[0] and '胡子:' == mustache_data[
        0] and '眼镜:' == glasse_data[0] and '口罩:' == mask_data[0] and '安全帽:' == helmet_data[0] and '帽子:' == hat_data[0]


@pytest.mark.parametrize('data', FPData.face_data)
@pytest.mark.negative
def test_check_face_mustache(sb, login, data):
    """ 上传不同的人脸照片，查看输出的人脸属性 """
    MenuBar.click_menu_item_by_text(sb, '工具', '人脸属性检测')
    Tools.detect_facial_attribute(
        sb, os.getcwd()+f'/guard/data/portrait/face_property/{data["img_path"]}')

    sex_data = Tools.get_facial_attribute_by_name(sb, "性别")
    age_data = Tools.get_facial_attribute_by_name(sb, "年龄")
    phiz_data = Tools.get_facial_attribute_by_name(sb, "表情")
    mustache_data = Tools.get_facial_attribute_by_name(sb, "胡子")
    glasse_data = Tools.get_facial_attribute_by_name(sb, "眼镜")
    mask_data = Tools.get_facial_attribute_by_name(sb, "口罩")
    helmet_data = Tools.get_facial_attribute_by_name(sb, "安全帽")
    hat_data = Tools.get_facial_attribute_by_name(sb, "帽子")

    assert data["sex"] in sex_data[-1] and data["age"] in age_data[-1] and data["phiz"] in phiz_data[-1] and data["mustache"] in mustache_data[-1] and data[
        "glasse"] in glasse_data[-1] and data["mask"] in mask_data[-1] and data["helmet"] in helmet_data[-1] and data["hat"] in hat_data[-1]

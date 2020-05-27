#!/usr/bin/env python3


from selenium.webdriver.common.by import By
from guard.pages.base import BasePage


class Tools(BasePage):
    """ 工具操作方法

    evaluate_face_image_quality: 检测指定图片质量分数
    get_check_content_detection_result: 获取质量分数检测结果
    detect_facial_attribute: 检测指定图片人脸属性
    get_facial_attribute_by_name: 获取人脸属性
    assert_facial_attribute_by_name: 验证指定人脸属性
    verify_one_to_one_face: 1:1人脸验证两张指定路径图片
    get_one_to_one_face_result: 获取1:1人脸验证结果

    """

    def evaluate_face_image_quality(self, path):
        """ 检测指定图片质量分数

        参数:
            path: 检测图片的路径

        """
        IMAGE_UPLOAD_INPUT = 'input[type="file"]'
        BasePage.upload_file_by_image_path(self, IMAGE_UPLOAD_INPUT, path)

        CHECK_CONTENT_DETECTION_BUTTON = '.app-tools-content-detection-detectbtn'
        self.slow_click(CHECK_CONTENT_DETECTION_BUTTON)

    def get_face_image_quality_result(self):
        """ 获取质量分数检测结果 

        返回: 质量分数结果

        """
        # CHECK_CONTENT_DETECTION_BUTTON_RESULT = '.app-tools-content-detection-detectbtn'
        CHECK_CONTENT_DETECTION_RESULT = '.app-tools-content-center'
        self.find_element(CHECK_CONTENT_DETECTION_RESULT)
        return "".join(filter(lambda c: c not in [' '], self.get_text(CHECK_CONTENT_DETECTION_RESULT)))

    def detect_facial_attribute(self, path):
        """ 检测指定图片人脸属性

        参数:
            path: 检测图片的路径

        """
        IMAGE_UPLOAD_INPUT = 'input[type="file"]'
        BasePage.upload_file_by_image_path(self, IMAGE_UPLOAD_INPUT, path)

        CHECK_CONTENT_FACE_BUTTON = '.app-tools-content-face-detectbtn'
        self.slow_click(CHECK_CONTENT_FACE_BUTTON)

    def get_facial_attribute_by_name(self, name):
        """ 获取人脸属性

        参数:
            name: 人脸属性名称，可选性别、年龄、表情、胡子、眼睛、口罩、安全帽、帽子

        返回: 对应人脸属性结果

        """
        CHECK_CONTENT_FACE_RESULT = f'//div[@class="app-tools-content-detection-right"]//li//span[contains(text(), "{name}")]'
        CHECK_CONTENT_SEX = f'//div[@class="app-tools-content-detection-right"]//li//span[contains(text(), "{name}")]/parent::li'
        self.find_element(CHECK_CONTENT_FACE_RESULT, By.XPATH)
        self.find_element(CHECK_CONTENT_SEX, By.XPATH)
        data_text = [self.get_text(
            CHECK_CONTENT_FACE_RESULT), self.get_text(CHECK_CONTENT_SEX)]
        return data_text

    def verify_one_to_one_face(self, path_one, path_two):
        """ 1:1人脸验证两张指定路径图片

        参数:
            path_one: 指定被比较图片路径
            path_two: 指定比较图片路径

        """
        IMAGE_UPLOAD_INPUT_L = '.app-tools-content-pics .imageselsect-container:first-child > input[type="file"]'
        IMAGE_UPLOAD_INPUT_R = '.app-tools-content-pics .imageselsect-container:last-child > input[type="file"]'

        BasePage.upload_file_by_image_path(
            self, IMAGE_UPLOAD_INPUT_L, path_one)
        self.sleep(1)
        BasePage.upload_file_by_image_path(
            self, IMAGE_UPLOAD_INPUT_R, path_two)
        self.sleep(3)
        CHECK_CONTENT_FACE_BUTTON = '.app-tools-content-pics-vsbtn'
        self.slow_click(CHECK_CONTENT_FACE_BUTTON)

    def get_one_to_one_face_result(self):
        """ 获取1:1人脸验证结果 

        返回: 1:1人脸验证结果
        """
        CHECK_CONTENT = '.app-tools-content-pics-vsbtn-popover > strong'
        self.find_element(CHECK_CONTENT)
        return self.get_text(CHECK_CONTENT)

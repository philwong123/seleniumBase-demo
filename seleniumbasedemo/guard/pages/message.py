import os
import re
import logging
import zipfile
from pathlib import Path
from guard.pages.base import BasePage
from seleniumbase import config as sb_config

class MessagePage(BasePage):
    """ 消息页面操作方法



    """
    EXPORT_NAME_MAP_MODULE_DICT = {"设备管理": "设备导出", "考勤": "考勤导出 - 公司", "角色管理": "角色导出", "记录": "检索记录导出", "日志管理": "操作日志导出",
                                   "用户管理": "用户导出", "访客": "访客导出", "人像库管理": "人像入库"}

    def get_export_file_name(self, module, index=0):
        """

        :param module: 导出文件的模块名称，eg："设备管理"
        :param index: 导出文件的索引，默认index=0表示最近的一条
        :return: 导出文件名字
        """
        EXPORT_FILE_XPATH = f'//div/span[contains(text(), "{MessagePage.EXPORT_NAME_MAP_MODULE_DICT[module]}")]/../../../descendant::*//div[contains(text(),"zip")]'
        export_file_name = self.driver.find_elements_by_xpath(EXPORT_FILE_XPATH)[index].text
        return export_file_name

    def download_export_file(self, module, index=0):
        """

        :param module: 导出文件的模块名称，eg："设备管理"
        :param index: 导出文件的索引，默认index=0表示最近的一条
        :return: 导出文件路径
        """
        file_name = MessagePage.get_export_file_name(self, module, index)
        DOWNLOAD_FILE_BUTTON = f'//div[contains(text(), "{file_name}")]/../descendant::div/span[contains(text(),"点击下载")]'
        self.click(DOWNLOAD_FILE_BUTTON)
        self.sleep(2)
        root_path = Path(os.getcwd())
        file_path = root_path / 'downloaded_files' / file_name
        return file_path

    def get_download_file(self, src_file):
        """

        :param src_file: 导出的zip文件路径
        :return: 解压后的文件名
        """
        extract_files = list()
        try:
            if zipfile.is_zipfile(src_file):
                fz = zipfile.ZipFile(src_file, 'r')
                for f in fz.namelist():
                    # fz.extract(f, dst_path, sb_config.username.encode(encoding="utf-8"))
                    extract_files.append(f)
                logging.info(extract_files)
                fz.close()
                return extract_files
        except Exception as e:
            logging.error(e)

    def check_download_file_format(self, module, index=0):
        """

        :param module: 导出文件的模块名称
        :param index: 导出文件的索引, 默认index=0表示最近的一条
        :return:
        """
        file = MessagePage.download_export_file(self, module, index)
        extracted_files = MessagePage.get_download_file(self, file)
        pattern = 'Export_\d{8}_\d{6}'
        for f in extracted_files:
            if re.match(pattern, f) is None:
                return False
        return True

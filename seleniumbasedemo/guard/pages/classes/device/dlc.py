#!/usr/bin/env python3

from guard.pages.classes.device.no_sense_device import NoSenseDevice


class DLC(NoSenseDevice):
    """ 人脸抓拍机类

    属性:
        name: 设备名称
        id: 设备ID
        group_name: 设备分组名称
        floor_name: 楼层名称
        manufacturer: 人脸抓拍机厂商
        ip: 人脸抓拍机网络地址
        port: 人脸抓拍机网络端口
        username: 人脸抓拍机用户名
        password: 人脸抓拍机密码
        rtsp_address: RTSP视频地址
        no_sense_ip: 继电器网络地址
        no_sense_port: 继电器网络端口

    """

    def __init__(self, name, id, group_name, floor_name, manufacturer, ip, port, username, password, no_sense_ip='', no_sense_port=''):
        NoSenseDevice.__init__(self, name, id, group_name,
                               floor_name, no_sense_ip, no_sense_port)
        self.__manufacturer = manufacturer
        self.__ip = ip
        self.__port = port
        self.__username = username
        self.__password = password

    @property
    def manufacturer(self):
        return self.__manufacturer

    @manufacturer.setter
    def manufacturer(self, value):
        self.__manufacturer = value

    @property
    def ip(self):
        return self.__ip

    @ip.setter
    def ip(self, value):
        self.__ip = value

    @property
    def port(self):
        return self.__port

    @port.setter
    def port(self, value):
        self.__port = value

    @property
    def username(self):
        return self.__username

    @username.setter
    def username(self, value):
        self.__username = value

    @property
    def password(self):
        return self.__password

    @password.setter
    def password(self, value):
        self.__password = value

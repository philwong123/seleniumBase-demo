#!/usr/bin/env python3

from guard.pages.classes.device.no_sense_device import NoSenseDevice


class ONVIF(NoSenseDevice):
    """ ONVIF摄像头类

    属性:
        name: 设备名称
        id: 设备ID
        group_name: 设备分组名称
        floor_name: 楼层名称
        ip: ONVIF摄像头网络地址
        port: ONVIF摄像头网络端口
        username: ONVIF摄像头用户名
        password: ONVIF摄像头密码
        no_sense_ip: 继电器网络地址
        no_sense_port: 继电器网络端口

    """

    def __init__(self, name, id, group_name, floor_name, ip, port, username, password, no_sense_ip='', no_sense_port=''):
        NoSenseDevice.__init__(self, name, id, group_name,
                               floor_name, no_sense_ip, no_sense_port)
        self.__ip = ip
        self.__port = port
        self.__username = username
        self.__password = password

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

#!/usr/bin/env python3

from guard.pages.classes.device.device import Device


class NoSenseDevice(Device):
    """ 无感门禁设备类

    属性:
        name: 设备名称
        id: 设备ID
        group_name: 设备分组名称
        floor_name: 楼层名称
        no_sense_ip: 继电器网络地址
        no_sense_port: 继电器网络端口

    """

    def __init__(self, name, id, group_name, floor_name, no_sense_ip='', no_sense_port=''):
        Device.__init__(self, name, id, group_name, floor_name)
        self.__no_sense_ip = no_sense_ip
        self.__no_sense_port = no_sense_port

    @property
    def no_sense_ip(self):
        return self.__no_sense_ip

    @no_sense_ip.setter
    def no_sense_ip(self, value):
        self.__no_sense_ip = value

    @property
    def no_sense_port(self):
        return self.__no_sense_port

    @no_sense_port.setter
    def no_sense_port(self, value):
        self.__no_sense_port = value

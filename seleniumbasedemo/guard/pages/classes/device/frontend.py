#!/usr/bin/env python3

from guard.pages.classes.device.device import Device


class Frontend(Device):
    """ 人脸识别机（前）类

    属性:
        name: 设备名称
        id: 设备ID
        group_name: 设备分组名称
        floor_name: 楼层名称
        type: 人脸识别机（前）类型，默认为SensePass，可选SensePass Pro、SenseKeeper、SenseGate

    """

    def __init__(self, name, id, group_name, floor_name, type='SensePass'):
        Device.__init__(self, name, id, group_name, floor_name)
        self.__type = type

    @property
    def type(self):
        return self.__type

    @type.setter
    def type(self, value):
        self.__type = value

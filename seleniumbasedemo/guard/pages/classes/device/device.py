#!/usr/bin/env python3


class Device(object):
    """ 设备基础类

    属性:
        name: 设备名称
        id: 设备ID
        group_name: 设备分组名称
        floor_name: 楼层名称
        x_offset: X相对位置，默认为0
        y_offset: Y相对位置，默认为0

    """

    def __init__(self, name, id, group_name, floor_name, x_offset=0, y_offset=0):
        self.__name = name
        self.__id = id
        self.__group_name = group_name
        self.__floor_name = floor_name
        self.__x_offset = x_offset
        self.__y_offset = y_offset

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        self.__name = value

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, value):
        self.__id = value

    @property
    def group_name(self):
        return self.__group_name

    @group_name.setter
    def group_name(self, value):
        self.__group_name = value

    @property
    def floor_name(self):
        return self.__floor_name

    @floor_name.setter
    def floor_name(self, value):
        self.__floor_name = value

    @property
    def x_offset(self):
        return self.__x_offset

    @x_offset.setter
    def x_offset(self, value):
        self.__width_offset = value

    @property
    def y_offset(self):
        return self.__y_offset

    @y_offset.setter
    def y_offset(self, value):
        self.__y_offset = value

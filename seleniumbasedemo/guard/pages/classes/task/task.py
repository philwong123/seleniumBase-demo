#!/usr/bin/env python3


class Task(object):
    """ 任务基础类

    属性:
        task_name: 任务名称
        device_name: 设备名称
        attributes: 任务特殊属性，默认为空，可多选入口、出口、防尾随、第三方对接、迎宾，举例：['入口'，'迎宾']

    """

    def __init__(self, task_name, device_name, attributes=[]):
        self.__task_name = task_name
        self.__device_name = device_name
        self.__attributes = attributes

    @property
    def task_name(self):
        return self.__task_name

    @task_name.setter
    def task_name(self, value):
        self.__task_name = value

    @property
    def device_name(self):
        return self.__device_name

    @device_name.setter
    def device_name(self, value):
        self.__device_name = value

    @property
    def attributes(self):
        return self.__attributes

    @attributes.setter
    def attributes(self, value):
        self.__attributes = value

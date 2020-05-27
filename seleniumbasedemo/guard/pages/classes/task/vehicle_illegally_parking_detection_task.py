#!/usr/bin/env python3

from guard.pages.classes.task.task import Task


class VehicleIllegallyParkingDetectionTask(Task):
    """ 车辆违停检测任务类

    属性:
        task_name: 任务名称
        device_name: 设备名称
        illegal_parking_time: 违停时限，默认为1
        area_settings: 区域设置列表，默认为[(-100, -100), (100, -100), (100, 100), (-100, 100), (-100, -100)]
        time_condition: 时间条件名称，默认为空
        attributes: 任务特殊属性，默认为空，可多选入口、出口、防尾随、第三方对接、迎宾，举例：['入口'，'迎宾']

    """

    def __init__(self, task_name, device_name, illegal_parking_time=1, area_settings=[(-100, -100), (100, -100), (100, 100), (-100, 100), (-100, -100)], time_condition=None, attributes=[]):
        Task.__init__(self, task_name, device_name, attributes=[])
        self.__illegal_parking_time = illegal_parking_time
        self.__area_settings = area_settings
        self.__time_condition = time_condition

    @property
    def illegal_parking_time(self):
        return self.__illegal_parking_time

    @illegal_parking_time.setter
    def illegal_parking_time(self, value):
        self.__illegal_parking_time = value

    @property
    def area_settings(self):
        return self.__area_settings

    @area_settings.setter
    def area_settings(self, value):
        self.__area_settings = value

    @property
    def time_condition(self):
        return self.__time_condition

    @time_condition.setter
    def time_condition(self, value):
        self.__time_condition = value
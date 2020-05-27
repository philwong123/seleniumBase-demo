#!/usr/bin/env python3

from guard.pages.classes.task.task import Task


class PedestrianCrossingBoundaryDetectionTask(Task):
    """ 人体越线检测任务类

    属性:
        task_name: 任务名称
        device_name: 设备名称
        alarm_line: 告警线，默认为[(-100, -100), (100, 100)]
        crossing_direction: 越线方向名称，可选AB双向越线、由B到A越线、由A到B越线
        time_condition: 时间条件名称，默认为空
        attributes: 任务特殊属性，默认为空，可多选入口、出口、防尾随、第三方对接、迎宾，举例：['入口'，'迎宾']

    """

    def __init__(self, task_name, device_name, alarm_line=[(-100, -100), (100, 100)], crossing_direction='AB双向越线', time_condition=None, attributes=[]):
        Task.__init__(self, task_name, device_name, attributes=[])
        self.__alarm_line = alarm_line
        self.__crossing_direction = crossing_direction
        self.__time_condition = time_condition

    @property
    def alarm_line(self):
        return self.__alarm_line

    @alarm_line.setter
    def alarm_line(self, value):
        self.__alarm_line = value

    @property
    def crossing_direction(self):
        return self.__crossing_direction

    @crossing_direction.setter
    def crossing_direction(self, value):
        self.__crossing_direction = value

    @property
    def time_condition(self):
        return self.__time_condition

    @time_condition.setter
    def time_condition(self, value):
        self.__time_condition = value

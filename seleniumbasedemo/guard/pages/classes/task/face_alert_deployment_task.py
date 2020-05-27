#!/usr/bin/env python3

from guard.pages.classes.task.task import Task


class FaceAlertDeploymentTask(Task):
    """ 人脸布控任务类

    属性:
        task_name: 任务名称
        device_name: 设备名称
        portraits: 人像库名称列表，举例: ['portrait1', 'portrait2']
        threshold: 任务阈值，默认为90.0
        attributes: 任务特殊属性，默认为空，可多选入口、出口、防尾随、第三方对接、迎宾，举例：['入口'，'迎宾']

    """

    def __init__(self, task_name, device_name, portraits, threshold='90.0', attributes=[]):
        Task.__init__(self, task_name, device_name, attributes=[])
        self.__portraits = portraits
        self.__threshold = threshold

    @property
    def portraits(self):
        return self.__portraits

    @portraits.setter
    def portraits(self, value):
        self.__portraits = value

    @property
    def threshold(self):
        return self.__threshold

    @threshold.setter
    def threshold(self, value):
        self.__threshold = value

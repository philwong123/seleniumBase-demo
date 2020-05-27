#!/usr/bin/env python3

from guard.pages.classes.device.no_sense_device import NoSenseDevice


class RTSP(NoSenseDevice):
    """ RTSP摄像头类

    属性:
        name: 设备名称
        id: 设备ID
        group_name: 设备分组名称
        floor_name: 楼层名称
        rtsp_address: RTSP视频地址
        no_sense_ip: 继电器网络地址
        no_sense_port: 继电器网络端口

    """

    def __init__(self, name, id, group_name, floor_name, rtsp_address, no_sense_ip='', no_sense_port=''):
        NoSenseDevice.__init__(self, name, id, group_name,
                               floor_name, no_sense_ip, no_sense_port)
        self.__rtsp_address = rtsp_address

    @property
    def rtsp_address(self):
        return self.__rtsp_address

    @rtsp_address.setter
    def rtsp_address(self, value):
        self.__rtsp_address = value

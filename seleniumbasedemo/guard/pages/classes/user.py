#!/usr/bin/env python3


class User(object):
    """ 用户类

    属性:
        username: 用户名
        name: 姓名
        department: 部门名称，默认为Default
        role: 角色名称，默认为Administrator
        status: 启用状态，默认为启用，可选禁用

    """

    def __init__(self, username, name, department='Default', role='Administrator', status='启用'):
        self.__username = username
        self.__name = name
        self.__department = department
        self.__role = role
        self.__status = status

    @property
    def username(self):
        return self.__username

    @username.setter
    def username(self, value):
        self.__username = value

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        self.__name = value

    @property
    def department(self):
        return self.__department

    @department.setter
    def department(self, value):
        self.__department = value

    @property
    def role(self):
        return self.__role

    @role.setter
    def role(self, value):
        self.__role = value

    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self, value):
        self.__status = value

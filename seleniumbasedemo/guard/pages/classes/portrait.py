#!/usr/bin/env python3


class Portrait(object):
    """ 人像基础类

    属性:
        name: 人像姓名
        id_number: 人像No.
        image_path: 人像图片地址
        portrait_databases: 人像所在人像库
        gender: 人像性别,默认为男，可选女
        alias: 人像别名，默认为空
        age: 人像年龄，默认为空
        company: 人像公司，默认为空
        department: 人像部门，默认为空
        contact: 人像联系方式，默认为空
        license_plate: 人像车牌，默认为空
        address: 人像住址，默认为空
        activation_time: 人像激活时间，默认为空
        expiration_time: 人像失效时间，默认为空
        enable_status: 人像启用状态，默认为启用，可选False（禁用）

    """

    def __init__(self, name, id_number, image_path, portrait_databases, gender='男',
                 alias='', age='', company='', department='', contact='', license_plate='',
                 address='', activation_time='', expiration_time='', enable_status=True):
        self.__name = name
        self.__id_number = id_number
        self.__image_path = image_path
        self.__portrait_databases = portrait_databases
        self.__gender = gender
        self.__alias = alias
        self.__age = age
        self.__company = company
        self.__department = department
        self.__contact = contact
        self.__license_plate = license_plate
        self.__address = address
        self.__activation_time = activation_time
        self.__expiration_time = expiration_time
        self.__enable_status = enable_status

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        self.__name = value

    @property
    def id_number(self):
        return self.__id_number

    @id_number.setter
    def id_number(self, value):
        self.__id_number = value

    @property
    def image_path(self):
        return self.__image_path

    @image_path.setter
    def image_path(self, value):
        self.__image_path = value

    @property
    def portrait_databases(self):
        return self.__portrait_databases

    @portrait_databases.setter
    def portrait_databases(self, value):
        self.__portrait_databases = value

    @property
    def gender(self):
        return self.__gender

    @gender.setter
    def gender(self, value):
        self.__gender = value

    @property
    def alias(self):
        return self.__alias

    @alias.setter
    def alias(self, value):
        self.__alias = value

    @property
    def age(self):
        return self.__age

    @age.setter
    def age(self, value):
        self.__age = value

    @property
    def company(self):
        return self.__company

    @company.setter
    def company(self, value):
        self.__company = value

    @property
    def department(self):
        return self.__department

    @department.setter
    def department(self, value):
        self.__department = value

    @property
    def contact(self):
        return self.__contact

    @contact.setter
    def contact(self, value):
        self.__contact = value

    @property
    def license_plate(self):
        return self.__license_plate

    @license_plate.setter
    def license_plate(self, value):
        self.__license_plate = value

    @property
    def address(self):
        return self.__address

    @address.setter
    def address(self, value):
        self.__address = value

    @property
    def activation_time(self):
        return self.__activation_time

    @activation_time.setter
    def activation_time(self, value):
        self.__activation_time = value

    @property
    def expiration_time(self):
        return self.__expiration_time

    @expiration_time.setter
    def expiration_time(self, value):
        self.__expiration_time = value

    @property
    def enable_status(self):
        return self.__enable_status

    @enable_status.setter
    def enable_status(self, value):
        self.__enable_status = value

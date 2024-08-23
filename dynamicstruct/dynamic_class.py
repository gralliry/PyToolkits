#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Description:
import importlib


class DynamicClass(object):
    def __new__(cls, name, *args, **kwargs):
        # 从模块中获取类
        module_name, class_name = name.rsplit('.', 1)
        # 动态导入模块
        module = importlib.import_module(module_name)
        ins_class = getattr(module, class_name)
        # 创建实例
        instance = ins_class(*args, **kwargs)
        return instance

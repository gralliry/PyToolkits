#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Description:
import os
from typing import Callable

UnionObj = object()

IDENTIFIER = ""


def set_identifier(name: str):
    global IDENTIFIER
    IDENTIFIER = name


def setenv(key: str, value, ):
    if isinstance(IDENTIFIER, str) and IDENTIFIER != "":
        key = IDENTIFIER + "_" + key
    os.environ[key.upper()] = str(value)


def getenv(key: str, default=UnionObj, require: bool = True, dtype: Callable = str):
    if isinstance(IDENTIFIER, str) and IDENTIFIER != "":
        key = IDENTIFIER + "_" + key
    key = key.upper()
    if key in os.environ and os.environ[key] is not None:
        return dtype(os.getenv(key))
    elif default is not UnionObj:
        return default
    elif require:
        # 如果设置了default就可以不用设置require了
        raise ValueError(f"Required key:{key} are missing")
    else:
        return None

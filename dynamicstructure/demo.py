#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Description:
from .dynamic_dict import DynamicDict

if __name__ == "__main__":
    load = lambda x: x
    d = DynamicDict(load)
    print(d)  # {}
    d["1"] = "a"
    print(d)  # {'1': 'a'}
    print(d[2])  # 2
    print(d)  # {'1': 'a', 2: 2}

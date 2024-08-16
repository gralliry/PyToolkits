#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Description:
class DynamicDict(dict):
    def __init__(self, load_fn, init_dict=None):
        if not isinstance(init_dict, dict):
            init_dict = dict()
        super().__init__(**init_dict)
        self._load_fn = load_fn

    def __getitem__(self, key, default=None):
        if key in self:
            return self[key]
        value = self[key] = self._load_fn(key)
        return value
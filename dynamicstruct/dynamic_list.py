#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Description:
class DynamicList(list):
    def __init__(self, load_fn, length):
        super().__init__()
        self._unique_obj = object()
        self.extend([self._unique_obj for _ in range(length)])
        self._load_fn = load_fn

    def __getitem__(self, index):
        item = self[index]
        if item is self._unique_obj:
            item = self[index] = self._load_fn(index)
        return item

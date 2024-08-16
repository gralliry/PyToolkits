#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Description:
from collections import deque

import numpy as np


class NumpySplitter:
    def __init__(self, ndarray, split_shape):
        split_shape = np.array(split_shape, dtype=np.int32)
        if len(ndarray.shape) != len(split_shape):
            raise ValueError("The dimensions of ndarray do not correspond")
        if not np.all(split_shape > 0):
            raise ValueError("The number of partitions on all dimensions must be greater than 0")
        if not np.all(ndarray.shape >= split_shape):
            raise ValueError("At least one dimension is smaller than the number of partitions "
                             "in the corresponding dimension")
        if not np.all(ndarray.shape % split_shape == 0):
            raise ValueError("Dimensions must be divisible by the corresponding number of partitions")
        # __next__
        self.shape = split_shape
        # 分割ndarray到ndarray中
        self.ndarray = deque(self.__flatten(ndarray))
        self.slarray = deque()
        # True 代表 下一次是读，False 代表 下一次是写
        self.is_set = True

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        return False

    def __iter__(self):
        return self

    def __next__(self) -> np.ndarray:
        # 迭代获取元素
        if self.is_end():
            raise StopIteration
        return self.__get()

    def __get(self):
        # 如果迭代一次中未设置，那么下次读取还会是该元素
        if not self.is_set:
            raise AssertionError("The element given last time you did not write")
        self.is_set = False
        return self.ndarray[0]

    def is_end(self):
        return len(self.ndarray) == 0

    def get(self) -> np.ndarray:
        # 非迭代获取元素
        if self.is_end():
            raise AssertionError("All elements have been processed")
        return self.__get()

    # 设置新元素
    def set(self, value) -> None:
        if self.is_end():
            raise AssertionError("All elements have been processed")
        if self.is_set:
            raise AssertionError("You did not get a new element after the last write")
        # 设置新参数
        self.slarray.append(value)
        self.ndarray.popleft()
        # 设置状态转移
        self.is_set = True

    def mould(self) -> np.ndarray:
        # 如果还有元素未处理
        if not self.is_end():
            raise AssertionError("There are still elements that have not been processed")
        if len(self.slarray) == 0:
            raise AssertionError("The result of the object has been obtained")
        slarray = list(self.slarray)
        self.slarray.clear()
        return self.__mould(slarray)

    def __mould(self, ndarray, depth=0) -> np.ndarray:
        if depth >= len(self.shape):
            return ndarray[0]
        new_ndarray = []
        for sub_ndarray in np.array_split(ndarray, self.shape[depth]):
            new_ndarray.append(self.__mould(sub_ndarray, depth + 1))
        return np.concatenate(new_ndarray, axis=depth)

    def __flatten(self, ndarry, depth=0) -> list:
        if depth >= len(self.shape):
            return [ndarry]
        new_ndarray = []
        for sub_array in np.array_split(ndarry, self.shape[depth], axis=depth):
            new_ndarray.extend(self.__flatten(sub_array, depth + 1))
        return new_ndarray

    def callback(self, fn):
        for ele in self:
            ele = fn(ele)
            self.set(ele)
        return self.mould()

    def callback_one(self, fn):
        ele = self.get()
        ele = fn(ele)
        self.set(ele)

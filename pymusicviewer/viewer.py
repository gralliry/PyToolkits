#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Description:
import numpy as np
import pygame
from pygame import Rect


class Viewer:
    def __init__(self):
        # 窗口大小为(850,400)
        self.screen_width = 1200
        self.screen_height = 100
        # pygame初始化
        pygame.init()
        # 设置窗口标题
        pygame.display.set_caption('实时频域')
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), 0, 32)

    def reflesh(self, data):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        # 清空屏幕
        self.screen.fill((255, 255, 255))
        # 预处理
        data = self.pretreat(data)
        data_len = len(data)
        width = self.screen_width / data_len
        for n, height in enumerate(data):
            # 画矩形
            pygame.draw.rect(
                self.screen, (0, 0, 0),
                Rect(
                    (n * width, self.screen_height - height),
                    (width, height)
                )
            )
        # 更新屏幕
        pygame.display.update()

    def pretreat(self, data):
        data = np.asarray(data, dtype=np.float32)
        if data.shape[0] > self.screen_width:
            data = data[:self.screen_width]
        data_len = data.shape[0]
        argss = np.argsort(data)
        for hd, index in enumerate(argss):
            data[index] = hd / data_len
        data = data * self.screen_height
        return data.tolist()

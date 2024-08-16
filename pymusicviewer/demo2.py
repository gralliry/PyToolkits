#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Description:
import pyaudio

import numpy as np

from viewer import Viewer
import warnings

warnings.simplefilter("ignore", DeprecationWarning)  # 防止报警告
# 设置参数
FORMAT = pyaudio.paInt16  # 16-bit PCM
CHANNELS = 1  # 单声道
RATE = 44100  # 采样率（Hz）
CHUNK = 1024  # 每个块的大小

# 初始化 PyAudio
audio = pyaudio.PyAudio()

# 打开数据流  output=True表示音频输出 # 获取音频参数
stream = audio.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True)
viewer = Viewer()

try:
    while True:  # 直到音频放完
        # 读取音频数据块
        data = stream.read(CHUNK)
        data = np.frombuffer(data, dtype=np.int16)  # 把data由字符串以十六进制的方式转变为数组
        data = np.real(np.fft.fft(data))  # 傅里叶变换获取实数部分

        viewer.reflesh(data)
except Exception as e:
    print(e)
    ...
stream.stop_stream()
stream.close()
audio.terminate()

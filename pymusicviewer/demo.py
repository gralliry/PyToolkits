#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Description:
# -*- coding: utf-8 -*-
# @Time    : 2023/10/17 17:04
# @Author  : Liang Jinaye
# @File    : audio_view.py
# @Description :
# coding=gbk
from pydub import AudioSegment
import pyaudio

import numpy as np

from viewer import Viewer
import warnings

warnings.simplefilter("ignore", DeprecationWarning)  # 防止报警告

chunk_size = 256  # 我把它理解为缓冲流

audio = AudioSegment.from_mp3(r"D:\Music\QMD\倒数 - G.E.M. 邓紫棋.mp3")

# 创建播放器
p = pyaudio.PyAudio()
# 打开数据流  output=True表示音频输出 # 获取音频参数
stream = p.open(format=p.get_format_from_width(audio.sample_width),
                channels=audio.channels,
                rate=audio.frame_rate,
                output=True)

audio_data = audio.raw_data  # 音频数据初始化
offset = 0

viewer = Viewer()

while offset < len(audio_data):  # 直到音频放完
    # 读取音频数据块
    chunk = audio_data[offset:offset + chunk_size]
    if not chunk:
        break
    # 播放音频数据块
    stream.write(chunk)
    offset += chunk_size

    data = np.fromstring(chunk, dtype=np.int16)  # 把data由字符串以十六进制的方式转变为数组
    data = np.real(np.fft.fft(data))  # 傅里叶变换获取实数部分

    viewer.reflesh(data)

stream.stop_stream()
stream.close()
# 关闭流
p.terminate()

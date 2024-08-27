#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Description:
import subprocess


class ShellClient:
    """
    使用该类只适用于本地的运行当前用户的shell命令，且未做shell注入防护，在传入cmd命令时请注意安全性。
    """

    def __init__(self):
        self.exec_statu = False
        self.info = ""

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        ...

    def execute(self, cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE):
        try:
            # 使用subprocess调用FFmpeg命令进行视频转换
            # process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
            result = subprocess.run(cmd, shell=shell, stdout=stdout, stderr=stderr)
            if result.returncode != 0:
                self.info = f"{result.stdout}\n{result.stderr}"
                self.exec_statu = False
            else:
                self.exec_statu = True
        except subprocess.CalledProcessError as error:
            self.info = str(error)
            self.exec_statu = False
        return self.exec_statu

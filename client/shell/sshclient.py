#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Description:
import queue
import paramiko


# Shell连接
class ShellConfig:
    # 未使用，也不要去使用，安全性未经验证
    # 必须是127.0.0.1，即本机，不然ffmpeg生成的文件无法被用户读取
    HOST = "127.0.0.1"
    PORT = 22
    USERNAME = ""
    PASSWORD = ""
    MAX_CONNECTIONS = 10
    MIN_CONNECTIONS = 3


class SSHClient:
    """
    该类
    """
    __Pool = queue.Queue()

    def __new__(cls, *args, **kwargs):
        if cls.__Pool.qsize() < ShellConfig.MIN_CONNECTIONS:
            return super().__new__(cls)
        return cls.__Pool.get()

    def __init__(self, ip="127.0.0.1", port=22, username="root", password="root"):
        self._conn = paramiko.SSHClient()
        self._conn.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        self.info = ""
        self.conn_statu = False
        if ip and username and password:
            self.connect(ip, port=port, username=username, password=password)
        self.exec_statu = False

    def __del__(self):
        if self.__Pool.qsize() < ShellConfig.MAX_CONNECTIONS:
            self.__Pool.put(self)
        else:
            # 断开Mail连接
            self._conn.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__del__()

    def connect(self, ip, username, password, port=22):
        if not ip or not username or not password:
            raise ValueError("IP, Username, Password are Null")
        try:
            self._conn.connect(hostname=ip, port=port, username=username, password=password)
        except Exception as error:
            self.info = str(error)
            self.conn_statu = False
        self.conn_statu = True

    def execute(self, command):
        # 执行Shell命令
        stdin, stdout, stderr = self._conn.exec_command(command)
        # 等待命令执行完成
        self.exec_statu = stdout.channel.recv_exit_status() == 0
        return stdin.read(), stdout.read(), stderr.read()

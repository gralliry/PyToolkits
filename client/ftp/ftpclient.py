#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Description:

# -*- coding: utf-8 -*-
# @Time    : 2023/10/25 21:39
# @Author  : Liang Jinaye
# @Description :

import ftplib
import io
import queue


# 文件传输协议
class FtpConfig:
    HOST = "127.0.0.1"
    PORT = 21
    USERNAME = "username"
    PASSWORD = "password"
    TIMEOUT = 90
    MAX_CONNECTIONS = 10
    MIN_CONNECTIONS = 3


class FtpClient:
    """
    封装的FTP类

    已重写连接池
    """
    __Pool = queue.Queue()

    @staticmethod
    def catch_error() -> any:
        """
        用来捕获ftp类成员函数的错误
        :return:
        """

        def decoator(func):
            def wrapper(self, *args, **kwargs):
                try:
                    res_obj = func(self, *args, **kwargs)
                    self.exec_statu = True
                    return res_obj
                except ftplib.all_errors as error:
                    self.error_info = (int(str(error)[:3]), str(error)[3:])
                    self.exec_statu = False
                    return None

            return wrapper

        return decoator

    def __new__(cls, *args, **kwargs):
        if cls.__Pool.qsize() < FtpConfig.MIN_CONNECTIONS:
            return super().__new__(cls)
        return cls.__Pool.get()

    def __init__(self, start_path='/'):
        conn = ftplib.FTP()
        conn.connect(
            host=FtpConfig.HOST,
            port=FtpConfig.PORT,
            timeout=FtpConfig.TIMEOUT,
        )
        conn.login(
            user=FtpConfig.USERNAME,
            passwd=FtpConfig.PASSWORD,
        )
        # 设置为被动模式
        conn.set_pasv(True)
        # 设置启动位置
        conn.cwd(start_path)
        self.exec_statu = False
        self.conn = conn

    @catch_error()
    def __del__(self):
        if self.__Pool.qsize() < FtpConfig.MAX_CONNECTIONS:
            # 返回根目录
            self.conn.cwd('/')
            self.__Pool.put(self)
        else:
            # 断开FTP连接
            self.conn.quit()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    @catch_error()
    def dir(self, path: str = '/') -> list:
        """
        列出当前目录内容

        注意：这个函数是print信息，而非返回
        :param path: 相对ftp跟目录的路径的所有文件和文件夹信息
        :return:
        """
        dirs = []
        self.conn.dir(path, dirs.append)
        return dirs

    @catch_error()
    def cwd(self, dir_path: str = '/') -> str:
        """
        进入目录
        :param dir_path: 进入目录的路径
        :return: 返回信息
        """
        return self.conn.cwd(dir_path)

    @catch_error()
    def pwd(self) -> str:
        """
        获取当前路径
        :return: 返回当前路径
        """
        return self.conn.pwd()

    @catch_error()
    def upload(self, remote_file: str, file_obj: io.BytesIO) -> str:
        """
        以二进制方式上传文件
        :param remote_file: ftp的文件位置
        :param file_obj: 需要上传的文件对象
        :return:
        """
        return self.conn.storbinary("STOR " + remote_file, file_obj)

    @catch_error()
    def download(self, remote_file: str, file_obj: io.BytesIO) -> str:
        """
        以二进制方式下载文件
        :param remote_file: ftp的文件位置
        :param file_obj: ftp的文件对象
        :return:
        """
        info = self.conn.retrbinary("RETR " + remote_file, file_obj.write)
        # 这个很重要！！！重置指针位！！！
        file_obj.seek(0)
        return info

    @catch_error()
    def delete(self, remote_file: str) -> str:
        """
        删除文件
        :param remote_file: ftp的文件位置
        :return:
        """
        return self.conn.delete(remote_file)

    @catch_error()
    def mkd(self, dir_path: str) -> str:
        """
        创建目录
        :param dir_path: 目录位置及名字
        :return:
        """
        return self.conn.mkd(dir_path)

    @catch_error()
    def rmd(self, dir_path: str) -> str:
        """
        删除目录
        :param dir_path: 目录位置及名字
        :return:
        """
        return self.conn.rmd(dir_path)

    @catch_error()
    def nlst(self, dir_path: str) -> list[str]:
        """
        列出所有子文件
        :param dir_path: 目录位置及名字
        :return:
        """
        return self.conn.nlst(dir_path)

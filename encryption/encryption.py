#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Description:
import os
import base64

os.environ["python_encrypt_key"] = "1234567890"
KEY = str(os.getenv("python_encrypt_key"))


def xor_encrypt_decrypt(data):
    # 将密钥扩展到与数据相同的长度
    endecrypt_key = (KEY * (len(data) // len(KEY) + 1))[:len(data)]
    return bytes([b ^ k for b, k in zip(data.encode(), endecrypt_key.encode())])


def encrypt(data):
    encrypted_bytes = xor_encrypt_decrypt(str(data))
    # 将加密后的字节数据编码为 Base64 ASCII 字符串
    return base64.b64encode(encrypted_bytes).decode()


def decrypt(data, dtype=None):
    # 解码 Base64 ASCII 字符串为字节数据
    encrypted_bytes = base64.b64decode(data.encode())
    decrypted_bytes = xor_encrypt_decrypt(encrypted_bytes.decode())
    return decrypted_bytes if dtype is None else dtype(decrypted_bytes)

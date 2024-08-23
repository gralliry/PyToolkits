#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Description:
from .encryption import encrypt, decrypt

# 示例使用
message = "niganasdadsadada"

# 加密
encrypted_message = encrypt(message)
print(f"Encrypted Message: {encrypted_message}")

# 解密
decrypted_message = decrypt(encrypted_message)
print(f"Decrypted Message: {decrypted_message}")

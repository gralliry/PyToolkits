#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Description:
import argparse

from .fastfile import create_server

parser = argparse.ArgumentParser()
parser.add_argument("-p", "--port", type=int, default=9006, help="Port of server")
parser.add_argument("-u", "--user", type=str, default="user", help="Name of User")
parser.add_argument("-k", "--key", type=str, default="password", help="Password of User")
args = parser.parse_args()

PORT = args.port
USERNAME = args.user
PASSWORD = args.key

create_server(port=PORT, username=USERNAME, password=PASSWORD)

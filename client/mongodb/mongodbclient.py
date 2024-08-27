#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Description:
import pymongo


# Mongodb数据库
class MongodbConfig:
    HOST = "127.0.0.1"
    PORT = 27017
    USERNAME = "MONGODB_USERNAME"
    PASSWORD = "MONGODB_PASSWORD"
    DATABASE = "MONGODB_DATABASE"


class MongodbClient:
    #
    __Client = pymongo.MongoClient(
        f"mongodb://{MongodbConfig.USERNAME}:{MongodbConfig.PASSWORD}"
        f"@{MongodbConfig.HOST}:{MongodbConfig.PORT}/?authMechanism=DEFAULT"
    )

    # 会自动释放，不用析构
    def __init__(self, database=MongodbConfig.DATABASE):
        self.database = self.__Client[database]

    # 上下文管理
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    # 操作
    def count(self,
              collection_name: str,
              query: dict[str, any]) -> int:
        """
        用来计数一个查询相关的数据数
        :param collection_name: 集合名字
        :param query: 查询的参数
        :return: 查询相关的数据数
        """
        collection = self.database[collection_name]
        return collection.count_documents(query)

    def query(self,
              collection_name: str,
              query: dict[str, any]) -> list:
        """
        查询语句
        :param collection_name: 集合名字
        :param query: 查询集
        :return:
        """
        collection = self.database[collection_name]
        cursor = collection.find(query)
        return [document for document in cursor]

    def insert(self,
               collection_name: str,
               datas: dict[str, any]) -> int | bool:
        """
        插入
        :param collection_name: 集合名字
        :param datas: 插入数据集
        :return:
        """
        collection = self.database[collection_name]
        if isinstance(datas, list):
            return len(collection.insert_many(datas).inserted_ids)
        if isinstance(datas, dict):
            return collection.insert_one(datas).acknowledged
        return False

    def update(self,
               collection_name: str,
               query: dict[str, any],
               update: dict[str, any],
               multi: bool = True) -> int:
        """
        更新数据
        :param collection_name: 集合名字
        :param query: 匹配集
        :param update: 更新集
        :param multi: 是否多选
        :return: 被修改的数据数
        """
        collection = self.database[collection_name]
        if multi:
            result = collection.update_many(query, update)
        else:
            result = collection.update_one(query, update)
        return result.modified_count

    def delete(self,
               collection_name: str,
               query: dict[str, any],
               multi: bool = True) -> int:
        """
        删除数据
        :param collection_name: 集合名字
        :param query: 匹配集
        :param multi: 是否多选
        :return: 被删除的数据数
        """
        collection = self.database[collection_name]
        if multi:
            return collection.delete_many(query).deleted_count
        else:
            return collection.delete_one(query).deleted_count

# db = Mongodb()
# print(db.count("cache",{'name':"Aiccyxixy10"}))
# mongodb = Mongodb({
#         "HOSTNAME" : "localhost",
#         "PORT" : 27017,
#         "USERNAME" : "root",
#         "PASSWORD" : "123456",
#         "DATABASE" : "local",
# })
# mongodb.connect()
# mongodb.insert('cache',{'name':'Aiccyxixy10','age':10})
# mongodb.update('cache',{'name':"Aiccyxixy10"},{'$set':{'age':30}})
# mongodb.delete('cache',{'name':"Aiccyxixy10"})
# print(mongodb.query('cache',{'name':"Aiccyxixy10"}))
# print(mongodb.count("cache",{'name':"Aiccyxixy10"}))

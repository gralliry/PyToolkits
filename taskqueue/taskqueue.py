#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Description:
import queue
import threading


class TaskQueue:
    def __init__(self, producer_fn=None, consumer_fn=None):
        self.queue = queue.Queue()
        self.producer_fn = producer_fn
        self.consumer_fn = consumer_fn

    def start(self, num_producers=1, num_consumers=1):
        for _ in range(num_producers):
            threading.Thread(target=self.__producer_work, daemon=True).start()
        for _ in range(num_consumers):
            threading.Thread(target=self.__consumer_work, daemon=True).start()

    def __producer_work(self):
        while True:
            item = self.producer_fn()
            self.queue.put(item)

    def __consumer_work(self):
        while True:
            item = self.queue.get()
            self.consumer_fn(item)
            self.queue.task_done()

    def join(self):
        self.queue.join()



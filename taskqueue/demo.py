#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Description:


if __name__ == "__main__":
    import time
    from datetime import datetime
    from .taskqueue import TaskQueue

    producer = lambda: time.time()

    consumer = lambda item: print(datetime.fromtimestamp(item).strftime('%Y-%m-%d %H:%M:%S') + "\n", end="")

    tasks = TaskQueue(producer_fn=producer, consumer_fn=consumer)
    tasks.start(1, 3)
    tasks.join()
#!/usr/bin/env python2.7
from __future__ import print_function

import sys
from random import random
import time
from threading import Thread

from pymesos import MesosExecutorDriver, Executor, decode_data, encode_data
from addict import Dict


class PiExecutor(Executor):
    def launchTask(self, driver, task):
        def run_task(task):
            update = Dict()
            update.task_id.value = task.task_id.value
            update.state = 'TASK_RUNNING'
            update.timestamp = time.time()
            driver.sendStatusUpdate(update)

            print(decode_data(task.data), file=sys.stderr)
            N = 1000000
	    count = 0
            for i in range(N):  
                x = random()
                if x >= 0.1:  
			if x < 0.2:                
				count += 1  
            prob = count / N 
            print(prob)
            driver.sendFrameworkMessage(encode_data(str(prob)))

            time.sleep(30)

            update = Dict()
            update.task_id.value = task.task_id.value
            update.state = 'TASK_FINISHED'
            update.timestamp = time.time()
            driver.sendStatusUpdate(update)

        thread = Thread(target=run_task, args=(task,))
        thread.start()


if __name__ == '__main__':
    import logging
    logging.basicConfig(level=logging.DEBUG)
    driver = MesosExecutorDriver(PiExecutor(), use_addict=True)
    driver.run()

#!/usr/bin/env python3.6
# coding:utf-8
# maxiaobo
# 2019/05/24

import logging
import time
import os

cur_dir = os.path.dirname(__file__)

log_path = os.path.dirname(os.path.dirname(os.path.abspath(cur_dir))) + "/rocketmq_query_service/logs/"
if not os.path.isdir(log_path):
    os.mkdir(log_path)
log_filename = log_path + "rocketmq-query-backend-" + time.strftime('%Y%m%d') + ".log"


logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename=log_filename,
                    filemode='a')


log = logging.getLogger('root')

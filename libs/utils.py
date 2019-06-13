#!/usr/bin/env python3.6
# coding:utf-8
# maxiaobo
# 2019/05/24


import json
from flask import make_response
from copy import deepcopy
from libs.logger import log
import time


# 通用的成功返回
SuccessInfo = {"ActionStatus": True, "ErrorInfo": "", "ErrorCode": 0}
SuccessResponse = json.dumps(deepcopy(SuccessInfo), ensure_ascii=False)


# 格式化response
def make_resp(resp_data, code=None):
    if code is None:
        status_code = 200
    else:
        status_code = code
    json_data = json.dumps(resp_data, ensure_ascii=False)
    resp = make_response(json_data, status_code)
    return response_set_headers(resp)


# 设置response header
def response_set_headers(response):
    response.headers['Access-Control-Allow-Origin'] = 'http://0.0.0.0:9528'
    response.headers['Access-Control-Allow-Methods'] = 'PUT,GET,POST,DELETE'
    response.headers['Access-Control-Allow-Headers'] = \
        "Referer,Accept,Origin,User-Agent,Content-Type,Cache-Control,access-control-allow-headers,x-token"
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    return response


# 成功返回，无附加信息
def success_resp():
    return make_resp(deepcopy(SuccessInfo))


# 获取分页参数
def get_page_parms(req):
    page = req.args.get('page', type=int)
    per_page = req.args.get('per_page', type=int)
    if page is None or per_page is None:
        log.error("传入的参数非法，使用默认参数，page=%s, per_page=%s", page, per_page)
        return 0, 10

    start = (page - 1) * per_page
    count = per_page

    if page > 0 and per_page > 0:
        return start, count
    else:
        log.error("传入的参数非法，使用默认参数，page=%s, per_page=%s", page, per_page)
        return 0, 10


def timestamp_to_date(timestamp):
    time_array = time.localtime(timestamp)
    return time.strftime("%Y-%m-%d %H:%M", time_array)
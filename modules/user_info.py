#!/usr/bin/env python3.6
# coding:utf-8
# maxiaobo
# 2019/05/24

import requests
from libs.logger import log

OpsUrl = 'http://ops.abc.com'


class UserInfo:
    """认证"""
    def __init__(self):
        pass

    @staticmethod
    def get(pat_cookie):
        """
        获取用户信息，先从redis获取，如果获取失败，则从ops平台接口获取
        @param pat_cookie:
        @return:
        """

        return UserInfo.get_user_info_from_ops(pat_cookie)

    @staticmethod
    def get_user_info_from_ops(pat_cookie):
        """
        从运维平台获取用户信息
        @param pat_cookie:
        @return: user_info
        """
        headers = {"Cookie": "pat_session=" + pat_cookie}
        r = requests.get(OpsUrl + "/pat/userinfo/", headers=headers)
        if r.status_code != 200:
            log.error("请求ops平台接口错误，statusCode=%s", r.status_code)
            return False

        if r.json()['result'] is False:
            log.error("请求ops平台获取用户信息错误，resp-data=%s", r.json())
            return False

        user_info = r.json()['data']
        if user_info is None:
            log.error("用户信息为空，resp-data=%s", r.json())
            return False

        # 生成session信息
        if 'ops' in user_info['role']:
            user_info['role'] = 'ops'
        else:
            user_info['role'] = 'dev'

        return user_info

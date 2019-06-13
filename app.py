#!/usr/bin/env python3.6
# coding:utf-8
# maxiaobo
# 2019/05/24

from flask import Flask, redirect
from flask_cors import CORS
from flask import request, jsonify
from modules.rocketmq_query_backend import RocketmqConsole
import waitress
from libs.logger import log
import functools
import string
import random
import time
import re
from libs.utils import make_resp, response_set_headers
from modules.user_info import  UserInfo

console = RocketmqConsole()

app = Flask(__name__, static_url_path='')

CORS(app, supports_credentials=True)


def generate_event_id():
    chars = string.ascii_letters + string.digits
    event_id = str(int(time.time())) + '-' + ''.join(random.sample(chars, 10)) + '-' + ''.join(random.sample(chars, 10))
    return event_id


def request_log(func):
    @functools.wraps(func)
    def inner():
        event_id = generate_event_id()
        log.info(u'http request path:{}, params:{}, event:{}'.format(request.path, request.args.to_dict(), event_id))
        env = request.args.get('env')
        if not env:
            if request.path in ['/', '/topic_route', '/topic_status', '/topic_consumergroup', '/consumergroup_status',
                                '/consumergroup_connection', '/producergroup_connection', '/consumergroup_tag',
                                '/message_key', '/message_id']:
                return func()
            else:
                log.warning(u'env is none')
                return response_params_error()
        return func(env, event_id)
    
    return inner


def response_params_error():
    return jsonify({'status': False, 'data': 'null', 'errMsg': 'params error'})


def get_host_and_pat_cookie(req):
    host = req.headers.get("Host")
    pat_cookie = req.args.get('pat_cookie')
    if pat_cookie is None:
        log.error("url获取获取到pat_cookie失败")
        # 从cookie获取
        pat_cookie = req.cookies.get("pat_cookie")

    return host, pat_cookie


def redirect_to_401(host, pat_cookie):
    resp = redirect("http://" + host + "/#/401")
    resp.set_cookie("pat_cookie", pat_cookie)
    return response_set_headers(resp)


def redirect_to_index(host, pat_cookie, user_name):
    resp = redirect("http://" + host + "/#/")

    resp.set_cookie("pat_cookie", pat_cookie)
    resp.set_cookie("user_name", user_name)
    return response_set_headers(resp)


@app.route("/pat/auth/", methods=['GET'])
def auth():
    """
    运维平台做登录验证
    """

    host, pat_cookie = get_host_and_pat_cookie(request)
    if pat_cookie is None:
        resp = redirect("http://" + host + "/#/401")
        return response_set_headers(resp)

    # 从运维平台获取用户信息
    user_info = UserInfo.get_user_info_from_ops(pat_cookie)
    if user_info is False:
        log.error("从运维平台获取用户信息失败,pat_cookie=%s", pat_cookie)
        return redirect_to_401(host, pat_cookie)

    if user_info['depart_name'].encode('utf-8') not in ["基础运维", "大数据运维", "应用运维", "运维开发"]:
        log.error("用户不属于基础运维，user info: %s", user_info)
        return redirect_to_401(host, pat_cookie)

    return redirect_to_index(host, pat_cookie, user_info["user_name"])


@app.route('/', methods=['GET'])
@request_log
def index():
    return app.send_static_file('index.html')


@app.route('/topic_route', methods=['GET'])
@request_log
def topic_route():
    return app.send_static_file('index.html')


@app.route('/topic_status', methods=['GET'])
@request_log
def topic_status():
    return app.send_static_file('index.html')


@app.route('/topic_consumergroup', methods=['GET'])
@request_log
def topic_consumergroup():
    return app.send_static_file('index.html')


@app.route('/consumergroup_status', methods=['GET'])
@request_log
def cnosumergroup_status():
    return app.send_static_file('index.html')


@app.route('/consumergroup_connection', methods=['GET'])
@request_log
def consumergroup_connection():
    return app.send_static_file('index.html')


@app.route('/producergroup_connection', methods=['GET'])
@request_log
def producergroup_connection():
    return app.send_static_file('index.html')


@app.route('/message_key', methods=['GET'])
@request_log
def message_key():
    return app.send_static_file('index.html')


@app.route('/message_id', methods=['GET'])
@request_log
def message_id():
    return app.send_static_file('index.html')


@app.route('/consumergroup_tag', methods=['GET'])
@request_log
def consumergroup_tag():
    return app.send_static_file('index.html')


@app.route('/cluster', methods=['GET'])
@request_log
def get_cluster(env, event_id):
    return jsonify(console.get_cluster_list(env, event_id))


@app.route('/brokerConfig', methods=['GET'])
@request_log
def get_broker_config(env, event_id):
    brokerAddr = request.args.get('brokerAddr')
    if not brokerAddr:
        log.warning(u'brokerAddr is none')
        return response_params_error()
    return jsonify(console.get_broker_config(env, event_id, brokerAddr))


@app.route('/topicStatus', methods=['GET'])
@request_log
def get_topic_status(env, event_id):
    topic = request.args.get('topic')
    if not topic:
        log.warning(u'topic is none')
        return response_params_error()
    res = console.get_topic_status(env, event_id, topic)
    if res['status']:
        res_data = []
        offset_info = res['data']['offsetTable']
        for info in offset_info:
            offset_data = offset_info[info]
            info = re.split(',| |=|\[|\]', info)
            offset_data['topic'] = info[3]
            offset_data['brokerName'] = info[6]
            offset_data['queueId'] = info[9]
            res_data.append(offset_data)
        return jsonify({'status': True, 'data': res_data, 'errMsg': 'null'})
    else:
        return jsonify(res)


@app.route('/topicRoute', methods=['GET'])
@request_log
def get_topic_route(env, event_id):
    topic = request.args.get('topic')
    if not topic:
        log.warning(u'topic is none')
        return response_params_error()
    return jsonify(console.get_topic_route(env, event_id, topic))


@app.route('/topicConfig', methods=['GET'])
@request_log
def get_topic_config(env, event_id):
    topic = request.args.get('topic')
    if not topic:
        log.warning(u'topic is none')
        return response_params_error()
    return jsonify(console.get_topic_config(env, event_id, topic))


@app.route('/topicConsumerGroup', methods=['GET'])
@request_log
def get_topic_consumer_status(env, event_id):
    topic = request.args.get('topic')
    if not topic:
        log.warning(u'topic is none')
        return response_params_error()
    # return jsonify(console.get_topic_consumer_status(env, event_id, topic))
    res = console.get_topic_consumer_status(env, event_id, topic)
    if res['status']:
        res_data = []
        consumergroup_info = res['data']
        if not consumergroup_info:
            return jsonify({'status': False, 'data': 'null', 'errMsg': 'rocketmq consle response empty data'})
        for info in consumergroup_info:
            consumergroup_name = info
            topic = consumergroup_info[info]['topic']
            queuestation_info = consumergroup_info[info]['queueStatInfoList']
            diff_total = consumergroup_info[info]['diffTotal']
            for _info in queuestation_info:
                res_dict = {}
                res_dict['consumer_group'] = consumergroup_name
                res_dict['broker_name'] = _info['brokerName']
                res_dict['topic'] = topic
                res_dict['queueId'] = _info['queueId']
                res_dict['broker_offset'] = _info['brokerOffset']
                res_dict['consumer_offset'] = _info['consumerOffset']
                res_dict['diff_offset'] = _info['brokerOffset'] - _info['consumerOffset']
                res_dict['diff_total'] = diff_total
                res_dict['consumer_client'] = _info['clientInfo']
                res_dict['last_update_timestamp'] = _info['lastTimestamp']
                res_data.append(res_dict)
        return jsonify({'status': True, 'data': res_data, 'errMsg': 'null'})
    else:
        return jsonify(res)


@app.route('/consumerGroupStatus', methods=['GET'])
@request_log
def get_consumergroup_consumer_status(env, event_id):
    consumerGroup = request.args.get('consumerGroup')
    if not consumerGroup:
        log.warning(u'consumerGroup is none')
        return response_params_error()
    # return jsonify(console.get_consumergroup_consumer_status(env, event_id, consumerGroup))
    res = console.get_consumergroup_consumer_status(env, event_id, consumerGroup)
    res_data = []
    if res['status']:
        consumergroup_info = res['data']
        if not consumergroup_info:
            return jsonify({'status': False, 'data': 'null', 'errMsg': 'rocketmq consle response empty data'})
        for info in consumergroup_info:
            diff_total = info['diffTotal']
            topic = info['topic']
            queuestat_info = info['queueStatInfoList']
            for _info in queuestat_info:
                res_dict = {}
                res_dict['topic'] = topic
                res_dict['broker_name'] = _info['brokerName']
                res_dict['diff_total'] = diff_total
                res_dict['diff_offset'] = _info['brokerOffset'] - _info['consumerOffset']
                res_dict['queueId'] = _info['queueId']
                res_dict['consumer_client'] = _info['clientInfo']
                res_dict['last_update_timestamp'] = _info['lastTimestamp']
                res_dict['broker_offset'] = _info['brokerOffset']
                res_dict['consumer_offset'] = _info['consumerOffset']
                res_data.append(res_dict)
        return jsonify({'status': True, 'data': res_data, 'errMsg': 'null'})
    else:
        return jsonify(res)


@app.route('/consumerGroupClientConnection', methods=['GET'])
@request_log
def get_consumergroup_client_connection(env, event_id):
    consumerGroup = request.args.get('consumerGroup')
    if not consumerGroup:
        log.warning(u'consumerGroup is none')
        return response_params_error()
    # return jsonify(console.get_consumergroup_connection(env, event_id, consumerGroup))
    res = console.get_consumergroup_connection(env, event_id, consumerGroup)
    res_data = []
    if res['status']:
        consumerclient_info = res['data']
        if not consumerclient_info:
            return jsonify({'status': False, 'data': 'null', 'errMsg': 'rocketmq consle response empty data'})
        consumer_from_where = consumerclient_info['consumeFromWhere']
        consumer_type = consumerclient_info['consumeType']
        message_model = consumerclient_info['messageModel']
        connection_info = consumerclient_info['connectionSet']
        for info in connection_info:
            res_dict = {}
            res_dict['consumer_from_where'] = consumer_from_where
            res_dict['consumer_type'] = consumer_type
            res_dict['message_model'] = message_model
            res_dict['client_addr'] = info['clientAddr']
            res_dict['client_id'] = info['clientId']
            res_dict['language'] = info['language']
            res_dict['version'] = info['version']
            res_dict['version_desc'] = info['versionDesc']
            res_data.append(res_dict)
        return jsonify({'status': True, 'data': res_data, 'errMsg': 'null'})
    else:
        return jsonify(res)


@app.route('/producerGroupClientConnection', methods=['GET'])
@request_log
def get_producergroup_client_connection(env, event_id):
    topic = request.args.get('topic')
    producerGroup = request.args.get('producerGroup')
    if not topic or not producerGroup:
        log.warning(u'topic or producerGroup is none')
        return response_params_error()
    # return jsonify(console.get_producergroup_connection(env, event_id, topic, producerGroup))
    res = console.get_producergroup_connection(env, event_id, topic, producerGroup)
    res_data = []
    if res['status']:
        producerclient_info = res['data']['connectionSet']
        if not producerclient_info:
            return jsonify({'status': False, 'data': 'null', 'errMsg': 'rocketmq consle response empty data'})
        for info in producerclient_info:
            res_dict = {}
            res_dict['client_addr'] = info['clientAddr']
            res_dict['client_id'] = info['clientId']
            res_dict['language'] = info['language']
            res_dict['version'] = info['version']
            res_dict['version_desc'] = info['versionDesc']
            res_data.append(res_dict)
        return jsonify({'status': True, 'data': res_data, 'errMsg': 'null'})
    else:
        return jsonify(res)


@app.route('/msgByKey', methods=['GET'])
@request_log
def get_msg_by_key(env, event_id):
    topic = request.args.get('topic')
    msgKey = request.args.get('msgKey')
    if not topic or not msgKey:
        log.warning(u'topic or msgKey is none')
        return response_params_error()
    return jsonify(console.get_msg_by_msgkey(env, event_id, topic, msgKey))


@app.route('/msgById', methods=['GET'])
@request_log
def get_msg_by_id(env, event_id):
    topic = request.args.get('topic')
    msgId = request.args.get('msgId')
    if not topic or not msgId:
        log.warning(u'topic or msgId is none')
        return response_params_error()
    return jsonify(console.get_msg_by_msgid(env, event_id, topic, msgId))


@app.route('/consumerGroupByTag', methods=['GET'])
@request_log
def get_consumer_group_by_tag(env, event_id):
    topic = request.args.get('topic')
    tag = request.args.get('tag')
    if not topic or not tag:
        log.warning(u'topic or tag is none')
        return response_params_error()
    return jsonify(console.get_consumergroup_by_tag(env, event_id, topic, tag))


if __name__ == '__main__':
    # waitress.serve(app, host='172.24.1.20', port=9089, _quiet=False, threads=4)
    waitress.serve(app, host='192.168.98.201', port=5000, _quiet=False, threads=4)

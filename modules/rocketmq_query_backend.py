#!/usr/bin/env python3.6
# coding:utf-8
# maxiaobo
# 2019/05/24

import requests
from requests.auth import HTTPBasicAuth
import sys
sys.path.append("..")
from libs.logger import log
import json
from config.config import config



class RocketmqConsole(object):

    def __init__(self):

        self.http_user = 'admin'
        self.http_passwd = '&*()DSgh367eUY$32a#^'

    def return_auth(self):
        return HTTPBasicAuth(self.http_user, self.http_passwd)

    def my_get(self, env, event_id, path, params):
    
        try:
            log.info(u'request env :{}, request path:{}, params:{}, event:{}'.format(env, path, params, event_id))
            try:
                base_url = config[env]
            except Exception as e:
                return {'status': False, 'data': 'null', 'errMsg': 'get base_url failed'}
            r = requests.get(base_url + path, params=params, auth=self.return_auth())
        except Exception as e:
            log.error(u'get {} exception, params: {}, event:{}'.format(path, params, event_id), exc_info=True)
            return {'status': False, 'data': 'null', 'errMsg': e} 
        if not r.status_code == 200:
            log.error(u'get {} failed, params:{}, status_code:{}, response:{}, event:{}'.format(path, params, r.status_code, r.text, event_id))
            return {'status': False, 'data': 'null', 'errMsg': r.text}


        try:
            response = r.json()
            log.debug(u'response:{}, event_id:{}'.format(response, event_id))
            # rocketmq console查询数据失败
            # if not response['data']:
            if not response['status'] == 0:
                if response['errMsg']:
                    return {'status': False, 'data': 'null', 'errMsg': response['errMsg'].split('\n')[0]}
                return {'status': False, 'data': 'null', 'errMsg': 'rocketmq console exception'}
            return {'status': True, 'data': response['data'], 'errMsg': 'null'} 
        except json.decoder.JSONDecodeError as e:
            log.error(u'get r.json failed, exception:{}, event:{}'.format(e, event_id))
            return {'status': False, 'data': 'null', 'errMsg': e} 
 
    # def get_index(self):
    #     """获取首页dashboard"""
    #     
    #     params = None 
    #     return self.my_get(path='/', params=params)

    def get_cluster_list(self, env, event_id):
        """获取集群列表"""

        params = None 
        return self.my_get(env=env, event_id=event_id, path='/cluster/list.query', params=params)

    def get_broker_config(self, env, event_id, broker_addr):
        """获取broker配置"""
            
        params = {'brokerAddr': broker_addr}
        return self.my_get(env=env, event_id=event_id, path='/cluster/brokerConfig.query', params=params)

    # def get_topic_list(self):
    #     """获取topic列表"""
    #     
    #     params = None
    #     return self.my_get(path='topic/list.query', params=params)

    def get_topic_status(self, env, event_id, topic_name):
        """获取topic状态"""
       
        params = {'topic': topic_name}
        return self.my_get(env=env, event_id=event_id, path='/topic/stats.query', params=params)

    def get_topic_route(self, env, event_id, topic_name):
        """获取topic路由信息"""
    
        params = {'topic': topic_name}
        return self.my_get(env=env, event_id=event_id, path='/topic/route.query', params=params)

    def get_topic_config(self, env, event_id, topic_name):
        """获取topic配置信息: 队列,权限等"""

        params = {'topic': topic_name}
        return self.my_get(env=env, event_id=event_id, path='/topic/examineTopicConfig.query', params=params) 

    def get_topic_consumer_status(self, env, event_id, topic_name):
        """获取topic订阅组状态"""
      
        params = {'topic': topic_name}
        return self.my_get(env=env, event_id=event_id, path='/topic/queryConsumerByTopic.query', params=params)

    def get_consumergroup_consumer_status(self, env, event_id, consumerGroup):
        """获取订阅组消费状态"""
 
        params = {'consumerGroup': consumerGroup}
        return self.my_get(env=env, event_id=event_id, path='/consumer/queryTopicByConsumer.query', params=params)

    def get_consumergroup_connection(self, env, event_id, consumerGroup):
        """获取订阅组应用客户端链接情况"""

        params = {'consumerGroup': consumerGroup}
        return self.my_get(env=env, event_id=event_id, path='/consumer/consumerConnection.query', params=params)

    def get_producergroup_connection(self, env, event_id, topic, producerGroup):
        """获取指定topic的生产者连接情况"""

        params = {'topic': topic, 'producerGroup': producerGroup}
        return self.my_get(env=env, event_id=event_id, path='/producer/producerConnection.query', params=params)

    def get_msg_by_msgkey(self, env, event_id, topic, msg_key):
        """根据msg_key获取信息状态"""
 
        params = {'topic': topic, 'key': msg_key}
        return self.my_get(env=env, event_id=event_id, path='/message/queryMessageByTopicAndKey.query', params=params)

    def get_msg_by_msgid(self, env, event_id, topic, msg_id):
        """根据msg_id获取信息状态"""
 
        params = {'topic': topic, 'msgId': msg_id}
        return self.my_get(env=env, event_id=event_id, path='/message/viewMessage.query', params=params)
    
    def get_consumergroup_by_tag(self, env, event_id, topic, tag):
        """查询指定topic中匹配到指定tag的订阅组"""

        match_consumergroup = []
  
        # 获取topic所有订阅组
        response = self.get_topic_consumer_status(env, event_id, topic)
        if not response['status']:
            log.warning(u'get all consumergroup of topic:{} failed, event:{}'.format(topic, event_id))
            return {'status': False, 'data': None, 'errMsg': response['errMsg']}
        consumergroup_list = response['data'].keys()
        
        # 遍历订阅组,获取订阅组的客户端链接信息,从中过滤指定的topic和tag
        for consumergroup in consumergroup_list:
            response = self.get_consumergroup_connection(env, event_id, consumergroup)
            # if not response['status'] or not response['data']:
            #     log.warning(u'get consumergroup {} connection failed, event: {}'.format(consumergroup, event_id))
            #     return {'status': True, 'data': match_consumergroup, 'errMsg': 'null'}
            #     #continue
            if not response['status']:
                log.warning(u'get consumergroup {} connection failed, errMsg:{}, event:{}'.format(consumergroup, response['errMsg'], event_id))
                continue 
            consumergroup_SubExpression_info = response['data']['subscriptionTable']
            for _key in consumergroup_SubExpression_info:
                if consumergroup_SubExpression_info[_key]['topic'] == topic:
                    subString = consumergroup_SubExpression_info[topic]['subString'].replace('||', '')
                    subString = subString.split()
                    if tag in subString:
                        match_consumergroup.append(consumergroup)
        return {'status': True, 'data': match_consumergroup, 'errMsg': 'null'}
                    

if __name__ == '__main__':
    my_console = RocketmqConsole()
    #print(my_console.get_consumergroup_by_tag('order-service', '*'))
    print(my_console.get_cluster_list(env='dev_gw', event_id='1234567'))

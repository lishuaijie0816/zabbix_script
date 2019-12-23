#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import datetime
import logging
from logging.handlers import RotatingFileHandler
from pymongo import MongoClient

# logging config
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = RotatingFileHandler(
    '/tmp/nginx_info.log',
    maxBytes=1024 * 1024 * 10,
    backupCount=10,
    encoding='utf-8'
)
logger.addHandler(handler)

client = MongoClient()
db = client.fluentd
collection = db.nginx_martin_rest

now = datetime.datetime.now() - datetime.timedelta(hours=8)
one_minute_ago = datetime.datetime.now() - datetime.timedelta(hours=8) - datetime.timedelta(minutes=1)


# 过去1分钟该域名的请求总数
def total_count():
    return collection.find({'time': {'$lt': now, '$gt': one_minute_ago}}).count()


# 过去1分钟内每秒的请求数
def total_count_avg():
    return collection.find({'time': {'$lt': now, '$gt': one_minute_ago}}).count() / 60


# nginx请求时间超过1秒的个数
def ng1_count():
    return collection.find({'time': {'$lt': now, '$gt': one_minute_ago}, 'request_time': {'$gt': '1'}}).count()


# # backend后端响应时间超过1秒个数
def be1_count():
    return collection.find(
        {'time': {'$lt': now, '$gt': one_minute_ago}, 'upstream_response_time': {'$gt': '1'}}).count()


# #nginx请求总时间大于3秒的请求个数
def ng3_count():
    return collection.find({'time': {'$lt': now, '$gt': one_minute_ago}, 'request_time': {'$gt': '3'}}).count()


# backend响应时间超过3秒的个数
def be3_count():
    return collection.find(
        {'time': {'$lt': now, '$gt': one_minute_ago}, 'upstream_response_time': {'$gt': '3'}}).count()


# 4xx请求个数
def xx4_count():
    return collection.find(
        {'time': {'$lt': now, '$gt': one_minute_ago}, 'status': {'$gte': '400', '$lt': '500'}}).count()


# 5xx请求个数
def xx5_count():
    return collection.find(
        {'time': {'$lt': now, '$gt': one_minute_ago}, 'status': {'$gte': '500', '$lt': '600'}}).count()


def total(arg):
    nginx_total = collection.find({'time': {'$lt': now, '$gt': one_minute_ago}})
    result = 0

    # backend后端响应时间总和
    if arg == 'backtime_total':
        for nginx in nginx_total:
            if nginx['upstream_response_time'] != '-' and ',' not in nginx['upstream_response_time']:
                result += float(nginx['upstream_response_time'])
        return result

    # bodysize总和
    if arg == 'bodysize_total':
        for nginx in nginx_total:
            result += int(nginx['body_bytes_sent'])
        return result

    # nginx请求总时间
    if arg == 'ngxtime_total':
        for nginx in nginx_total:
            result += float(nginx['request_time'])
        return result

    # bodysize 大于 512000的个数和其详细信息
    if arg == 'bodysize_gt_512000_count':
        for nginx in nginx_total:
            if int(nginx['body_bytes_sent']) > 512000:
                result += 1
                logger.info(nginx)
        return result

    # Android user count
    if arg == 'Android':
        for nginx in nginx_total:
            if 'Android' in nginx['http_user_agent']:
                result += 1
        return result

    # iPhone user count
    if arg == 'iPhone':
        for nginx in nginx_total:
            if 'iPhone' in nginx['http_user_agent']:
                result += 1
        return result

    # nginx 状态汇总
    if arg.startswith('nginx_'):
        data = dict()
        for nginx in nginx_total:
            if nginx['status'] != '-' and ',' not in nginx['status']:
                data['nginx_' + nginx['status']] = data.get('nginx_' + nginx['status'], 0) + 1

                if nginx['status'] in ['502', '500']:
                    logger.info(nginx)
        return data.get(arg, 0)


if __name__ == '__main__':
    # 方式1
    # self_mod = __import__('test')
    # print getattr(self_mod, sys.argv[1], sys.argv[2])()
    if sys.argv[1] == 'total':
        print globals()[sys.argv[1]](sys.argv[2])

    else:
        # 方式2
        print globals()[sys.argv[1]]()

# coding=utf-8

import config
import logging
import tornado.ioloop
import tornado.options
import tornado.httpserver
from tweb.application import Application
from tornado.options import options, define
from tornado.httpclient import AsyncHTTPClient

from concurrent.futures import ThreadPoolExecutor
from asyncio import get_event_loop

from tweb import rdpool, dbpool, scheduler
from webmother.db import mongo

from webmother import routes


AsyncHTTPClient.configure(None, max_clients=1000)
get_event_loop().set_default_executor(ThreadPoolExecutor(max_workers=100))


def init():
    # 定义全局变量，命令参数
    define("port", default=config.Port, help="run on the given port", type=int)
    define("host", default=config.Host, help="run on the given host", type=str)
    define("env", default='dev', help="chose env dev or prod", type=str)

    tornado.options.parse_command_line()

    application = Application()
    http_server = tornado.httpserver.HTTPServer(application, xheaders=True)
    http_server.listen(options.port, options.host)

    print("=" * 50)
    print("* Server: Success!")
    print("* Host:   http://" + options.host + ":%s" % options.port)
    print("* Quit the server with Control-C")
    print("-" * 50)

    logging.info("=" * 50)
    logging.info("* Server: Started!")
    logging.info("* Host:   http://" + options.host + ":%s" % options.port)
    logging.info("* Quit the server with Control-C")
    logging.info("-" * 50)

    # 定时任务调度器
    scheduler.start()

    # 初始化mongodb
    mongo.init()

    # 初始化数据库连接池
    dbpool.init()

    # 初始化Redis连接池
    rdpool.init()

    # 加载路由模块
    application.load_routes(routes)

    return application


def start():
    tornado.ioloop.IOLoop.instance().start()


def stop():
    # 停止定时任务调度器
    scheduler.shutdown()

    print("-" * 50)
    print('* Server stopped!')
    print("=" * 50)

    logging.info("-" * 50)
    logging.info('* Server stopped!')
    logging.info("=" * 50)

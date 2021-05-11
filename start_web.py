# -*- coding: utf-8 -*-
"""
Created by susy at 2021/5/11
"""
import os
import common
from tornado.ioloop import IOLoop
from tornado.httpserver import HTTPServer
from middle import middle_ware
from tornado.web import Application
from settings import service
from common import stream_manager
from controller import *
import signal
import time
logger = common.get_default_logger()

guest_user = None
base_dir = os.path.dirname(__file__)
context = dict(guest=None, basepath=base_dir)
lm = None
server = None
MAX_WAIT_SECONDS_BEFORE_SHUTDOWN = 5
server_context = dict(running=True)


def sig_handler(sig, frame):
    logger.warning('Caught signal: %s', sig)
    IOLoop.instance().add_callback(shutdown)
    server_context["running"] = False


def shutdown():
    logger.debug("Stopping http server...")
    if lm:
        lm.shutdown()
    if server:
        server.stop()

    deadline = time.time() + MAX_WAIT_SECONDS_BEFORE_SHUTDOWN
    io_loop = IOLoop.instance()

    def stop_loop():
        now = time.time()
        if now < deadline and (io_loop._callbacks or io_loop._timeouts):
            io_loop.add_timeout(now + 1, stop_loop)
        else:
            io_loop.stop()  # 处理完现有的 callback 和 timeout 后，可以跳出 io_loop.start() 里的循环
            logger.info('Shutdown')

    stop_loop()


def loop_runner():
    if not server_context["running"]:
        shutdown()


if __name__ == "__main__":
    lm = stream_manager.Manager("billions_alert")
    lm.start()
    context["stream"] = lm
    settings = {
        "static_path": os.path.join(base_dir, "static"),
        "static_url_prefix": r"/static/",
        "source": os.path.join(base_dir, "source"),
        "xsrf_cookies": False,
        "login_url": "/index.html",
        "template_path": os.path.join(os.path.dirname(__file__), "templates")
    }
    middle_list = middle_ware.get_middleware()
    application = Application([
        (r"/hook/.*", HookHandler, dict(middleware=middle_list, context=context)),
        (r"/.*\.html", HtmlHandler, dict(middleware=middle_list))
    ], **settings)
    port = service['port']

    # server = HTTPServer(application, ssl_options=ssl_ctx)
    server = HTTPServer(application)
    server.listen(port)
    logger.info("Listen HTTP @ %s" % port)

    signal.signal(signal.SIGTERM, sig_handler)
    signal.signal(signal.SIGINT, sig_handler)
    _ioloop = IOLoop.instance()
    _ioloop.add_callback(loop_runner)
    _ioloop.start()


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
logger = common.get_default_logger()

guest_user = None
base_dir = os.path.dirname(__file__)
context = dict(guest=None, basepath=base_dir)


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
    IOLoop.instance().start()
    lm.shutdown()

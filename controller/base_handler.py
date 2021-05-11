# -*- coding: utf-8 -*-
"""
Created by susy at 2021/5/11
"""
from tornado.web import RequestHandler
from tornado.web import Application
from common import constant, get_default_logger, CJsonEncoder
import traceback
import sys
import json
from typing import Optional, Awaitable
logger = get_default_logger()
LOGIN_TOKEN_KEY = "BILLION-TOKEN"


class BaseHandler(RequestHandler):

    def __init__(self, application: Application, request, **kwargs):
        self.release_db = True
        self.middleware = None
        self.user_payload = None
        self.user_type = constant.USER_TYPE['SINGLE']
        self.user_id = 0
        self.ref_id = 0
        self.org_id = 0
        self.default_pan_id = 0
        self.is_web = False
        self.query_path = ''
        self.token = None
        self.context = {}
        self.guest = None
        super(BaseHandler, self).__init__(application, request, **kwargs)

    def initialize(self, middleware, context=None) -> None:
        self.middleware = middleware
        if context:
            self.context = context
            _guest = context.get('guest', None)
            if _guest:
                self.guest = _guest

    def ignore_db(self):
        self.release_db = False

    def use_db(self):
        from dao import models
        self.release_db = True
        logger.debug("use db:", models.db)

    def prepare(self):
        for middleware in self.middleware:
            middleware.process_request(self)

    def get_current_user(self):
        return True

    def _handle_request_exception(self, e):
        logger.error("request err:{}".format(traceback.format_exception(*sys.exc_info())))
        t, v, tb = sys.exc_info()
        params = {"exc_info":  "[{}]{}".format(t, v), "state": -1, "err": "parameters error!"}
        # self.write_error(404, **params)
        # self.write(json.dumps(params))
        self.to_write_json(params)

    def send_error(self, status_code=500, **kwargs) -> None:
        # self.write_error(404, **kwargs)
        logger.error("service err", exc_info=True)
        t, v, tb = sys.exc_info()
        params = {"exc_info": "[{}]{}".format(t, v), "state": -1, "err": "service error!"}
        self.to_write_json(params)

    def write_error(self, stat, **kw):
        error_trace_list = None
        if kw:
            error_trace_list = traceback.format_exception(*kw.get("exc_info"))
        if stat == 500:
            logger.error("server err:{}".format(error_trace_list))
        elif stat == 403:
            logger.error("request forbidden!")
        else:
            pass
            # if error_trace_list:
            #     traceback.print_exc()

        rs = {"status": -1, "error": error_trace_list}

        self.write(json.dumps(rs))

    def data_received(self, chunk: bytes) -> Optional[Awaitable[None]]:
        pass

    def on_finish(self):
        # print("on_response request finish.")
        self.try_release_db_conn()

    def try_release_db_conn(self):
        if self.release_db:
            from dao import models
            logger.info('need to release conn!')
            models.clean_wrap_db_for_session()
        else:
            logger.info('not need to release conn!')

    def to_write_json(self, result):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        self.write(json.dumps(result, cls=CJsonEncoder))

    def wrap_request_dict(self, raise_err=False, parse_body=True):
        get_params = self.request.arguments
        params = {}
        try:
            if get_params:
                for k in get_params:
                    d = get_params[k]
                    if isinstance(d, list):
                        if len(d) == 1:
                            params[k] = d[0].decode()
                        else:
                            params[k] = d
                    else:
                        params[k] = d
            post_params = self.request.body_arguments
            if post_params:
                for k in post_params:
                    d = post_params[k]
                    if isinstance(d, list):
                        if len(d) == 1:
                            params[k] = d[0].decode()
                        else:
                            params[k] = d
                    else:
                        params[k] = d
            if parse_body:
                bd = self.request.body
                if bd:
                    params = json.loads(bd)

        except Exception as e:
            if raise_err:
                raise e
        request = self.request
        if hasattr(request, "user_id"):
            params["user_id"] = request.user_id
        if hasattr(request, "is_anonymous"):
            params["is_anonymous"] = request.is_anonymous
        if hasattr(request, "chat_id"):
            params["chat_id"] = request.chat_id
        if hasattr(request, "mobile"):
            params["mobile"] = request.mobile
        if hasattr(request, "ip"):
            params["ip"] = request.ip
        logger.debug("request params:{}".format(params))
        return params

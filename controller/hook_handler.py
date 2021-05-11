# -*- coding: utf-8 -*-
"""
Created by susy at 2021/5/11
"""
from controller.base_handler import BaseHandler
import json


class HookHandler(BaseHandler):

    def action(self, params):
        path = self.request.path
        rs = {"status": 0}
        cmd = params.get("cmd", "")
        print("action params:", params)
        print("action path:", path)
        return rs

    def post(self):
        # self.check_header("wx post")
        params = self.wrap_request_dict()
        rs = self.action(params)
        print("rs:", rs)
        self.to_write_json(rs)

    def get(self):
        self.ignore_db()
        params = self.wrap_request_dict(parse_body=False)
        rs = self.action(params)
        self.to_write_json(rs)




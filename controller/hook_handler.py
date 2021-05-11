# -*- coding: utf-8 -*-
"""
Created by susy at 2021/5/11
"""
from controller.base_handler import BaseHandler
from settings import grafana
import json


class HookHandler(BaseHandler):

    def action(self, params):
        path = self.request.path
        rs = {"status": 0}
        cmd = params.get("cmd", "")
        print("action params:", params)
        print("action path:", path)
        state = params.get("state", None)
        if state:
            message = "恢复正常"
            tags = params.get("tags", {})
            title = params.get("ruleName", "未知")
            uri = params.get("ruleUrl", "#")
            domain = grafana.get("domain")
            page_url = "{}{}".format(domain, uri)
            if "alerting" == state:
                message = params.get("message", None)
                if not message:
                    message = "异常"

                pass
            elif "ok" == state:
                pass
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




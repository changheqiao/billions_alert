# -*- coding: utf-8 -*-
"""
Created by susy at 2021/5/11
"""
from controller.base_handler import BaseHandler
from settings import grafana
from controller.hook_service import hook_service
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
            eval_matches = params.get("evalMatches", [])
            title = params.get("ruleName", "未知")
            uri = params.get("ruleUrl", "#")
            domain = grafana.get("domain")
            page_url = "{}{}".format(domain, uri)
            if "alerting" == state:
                for em in eval_matches:
                    tags = em.get("tags", {})
                    value = em.get("value", 0)
                    message = params.get("message", None)
                    if not message:
                        message = "异常"
                    hook_service.send_wx_alert(dict(title=title, page=page_url, value=value, message=message))

            elif "ok" == state:
                hook_service.send_wx_alert_ok(dict(title=title, page=page_url, value="", message=message))
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




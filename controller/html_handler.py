# -*- coding: utf-8 -*-
"""
Created by susy at 2021/5/11
"""
from controller.base_handler import BaseHandler
from controller.html_service import html_service
import json


class HtmlHandler(BaseHandler):

    def get(self):
        wx_qrcode, expired = html_service.wx_gen_grafan_qrcode()

        self.render('index.html', **{'ref': '', 'force': '', 'qrcode': html_service.wrap_qrcode_url(wx_qrcode)})

    def post(self):
        self.get()

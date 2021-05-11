# -*- coding: utf-8 -*-
"""
Created by susy at 2021/5/11
"""
from controller.base_handler import BaseHandler
import json


class HtmlHandler(BaseHandler):

    def get(self):
        self.render('index.html', **{'ref': '', 'force': ''})

    def post(self):
        self.get()

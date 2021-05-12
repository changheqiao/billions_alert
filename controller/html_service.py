# -*- coding: utf-8 -*-
"""
Created by susy at 2021/5/11
"""
from common import singleton, wxapi
from common.access_token_cache import access_token_cache
import common
import time
import arrow
logger = common.get_default_logger()


@singleton
class HtmlService(object):

    def wx_gen_grafan_qrcode(self):
        access_token = access_token_cache.fetch_wx_access_token()
        action_name = 'QR_STR_SCENE'
        if access_token:
            fuzzy_id = "grafana"
            rs = wxapi.gen_qrcode(access_token, action_name, fuzzy_id)
            if rs:
                ticket = rs.get('ticket', None)
                if ticket:
                    expire = arrow.get(time.time() + rs['expire_seconds']).datetime
                    # update_params = {"weixin_qrcode": ticket, "weixin_qrcode_expired": expire}
                    # UserDao.update_store(store_id, update_params)
                    return ticket, expire
        return None, None

    def wrap_qrcode_url(self, wx_qrcode):
        return wxapi.wrap_qrcode_url(wx_qrcode)


html_service = HtmlService()

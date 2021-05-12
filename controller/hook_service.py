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
class HookService(object):

    def send_wx_alert(self, params, stream):
        template_id = ""

        alert_id = params.get("aid")
        key = "hs:u:alert:{platform}:{alert_id}:{tm}".format(platform="grafana", alert_id=alert_id, tm=int(common.get_now_ts()))
        plat_payload = dict(id=key, version="1_0_0_1", status=1, template=template_id)

        for k in params:
            plat_payload[k] = params[k]
        # self.__hset_item_params(key, plat_payload)
        stream.get_queue().pool(plat_payload)
        stream.trigger_check_tasks()

    def send_wx_alert_ok(self, params, stream):
        template_id = ""
        alert_id = params.get("aid")
        key = "hs:u:alert:{platform}:{alert_id}:{tm}".format(platform="grafana", alert_id=alert_id, tm=int(common.get_now_ts()))
        plat_payload = dict(id=key, version="1_0_0_1", status=0, template=template_id)
        for k in params:
            plat_payload[k] = params[k]
        # self.__hset_item_params(key, plat_payload)
        stream.get_queue().pool(plat_payload)

    # def __hset_item_params(self, key, plat_payload):
    #     logger.debug("hset_item_params key:{},payload:{}".format(key, plat_payload))
    #     if not common_r.exists(key):
    #         common_r.hset(key, "tm", common.get_now_ts(), mapping=plat_payload)
    #         common_r.expire(key, 10 * 60)

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


hook_service = HookService()

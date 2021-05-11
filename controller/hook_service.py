# -*- coding: utf-8 -*-
"""
Created by susy at 2021/5/11
"""
from common import singleton
import common
logger = common.get_default_logger()


@singleton
class HookService(object):

    def send_wx_alert(self, params, stream):
        alert_id = params.get("aid")
        key = "hs:u:alert:{platform}:{alert_id}:{tm}".format(platform="grafana", alert_id=alert_id, tm=common.get_now_ts())
        plat_payload = dict(id=key, version="1_0_0_1", status=1)

        for k in params:
            plat_payload[k] = params[k]
        # self.__hset_item_params(key, plat_payload)
        stream.get_queue().pool(plat_payload)

    def send_wx_alert_ok(self, params, stream):
        alert_id = params.get("aid")
        key = "hs:u:alert:{platform}:{alert_id}:{tm}".format(platform="grafana", alert_id=alert_id, tm=common.get_now_ts())
        plat_payload = dict(id=key, version="1_0_0_1", status=0)
        for k in params:
            plat_payload[k] = params[k]
        # self.__hset_item_params(key, plat_payload)
        stream.get_queue().pool(plat_payload)

    # def __hset_item_params(self, key, plat_payload):
    #     logger.debug("hset_item_params key:{},payload:{}".format(key, plat_payload))
    #     if not common_r.exists(key):
    #         common_r.hset(key, "tm", common.get_now_ts(), mapping=plat_payload)
    #         common_r.expire(key, 10 * 60)


hook_service = HookService()

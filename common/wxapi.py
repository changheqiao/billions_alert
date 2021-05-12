# -*- coding: utf-8 -*-
"""
Created by susy at 2020/4/26
"""
import requests
from settings import WX_API
import json
import common
logger = common.get_default_logger()


def get_openid(code):
    point = WX_API["point"]
    appid = WX_API['appid']
    appsecret = WX_API['appsecret']
    grant_type = "authorization_code"
    openid_api = "{point}/sns/jscode2session?appid={appid}&secret={secret}&js_code={code}&grant_type={gtype}".format(
        point=point, appid=appid, secret=appsecret, code=code, gtype=grant_type)
    res = requests.get(openid_api, verify=False)
    rsjson = res.json()
    return rsjson


def get_access_token(cfg=WX_API):
    point = cfg["point"]
    fresh_access_token_api = "{point}/cgi-bin/token?grant_type=client_credential&appid={appid}&secret={secret}".format(
        point=point, appid=cfg["appid"], secret=cfg["appsecret"])
    res = requests.get(fresh_access_token_api, verify=False)

    rsjson = res.json()
    return rsjson


def getkflist(access_token):
    point = WX_API["point"]
    getkflist_api = "{point}/cgi-bin/customservice/getkflist?access_token={token}".format(point=point,
                                                                                          token=access_token)
    res = requests.get(getkflist_api, verify=False)
    rsjson = res.json()
    return rsjson


def send_wx_message(access_token, template_id, open_id, url, chat_id):
    point = WX_API["point"]
    send_api = "{point}/cgi-bin/message/template/send?access_token={token}".format(point=point, token=access_token)
    params = dict(
        touser=open_id,
        template_id=template_id,
        url=url,
        data=dict(
            first=dict(value="有访客需要您前往接待", color="#173177"),
            keyword1=dict(value="{}".format(chat_id), color="#173177"),
            keyword2=dict(value="{}".format(common.get_now_datetime_format("YYYY年MM月DD日")), color="#173177"),
            remark=dict(value="贵公司有客户到访，请尽快联系并前往接待", color="#173177"),
        )
    )
    headers = {"Content-Type": "application/json"}
    res = requests.post(send_api, verify=False, headers=headers, json=params)
    rsjson = res.json()
    logger.debug("send_wx_message[{}] rsjson:{}".format(chat_id, rsjson))
    return rsjson


def wrap_qrcode_url(qrcode):
    return "https://mp.weixin.qq.com/cgi-bin/showqrcode?ticket={}".format(qrcode)


def gen_qrcode(access_token, action_name, fuzzy_id, expire_seconds=2592000):
    # action_name = QR_SCENE / QR_STR_SCENE / QR_LIMIT_SCENE / QR_LIMIT_STR_SCENE
    params = dict(
        action_name=action_name,
        action_info={}
    )
    if action_name in ['QR_SCENE', 'QR_STR_SCENE']:
        params['expire_seconds'] = expire_seconds
    if action_name in ['QR_LIMIT_STR_SCENE', 'QR_STR_SCENE']:
        params['action_info']['scene'] = dict(scene_str=fuzzy_id)
    else:
        params['action_info']['scene'] = dict(scene_id=fuzzy_id)

    point = WX_API["point"]
    send_api = "{point}/cgi-bin/qrcode/create?access_token={token}".format(point=point, token=access_token)
    res = requests.post(send_api, json=params)
    rsjson = res.json()
    ticket = rsjson.get("ticket", None)
    if ticket:
        return dict(ticket=ticket, expire_seconds=rsjson.get('expire_seconds', expire_seconds))
    return {}



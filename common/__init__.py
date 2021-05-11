# -*- coding: utf-8 -*-
"""
Created by susy at 2021/5/3
"""
from datetime import datetime, date
import settings
import pytz
import time
import json
import decimal
default_tz = pytz.timezone(settings.TIME_ZONE)


# Billions
HEADER = r"""
           ________                                                                                              
         /.         \      ======   ===        ===          ======        _-==-_      ===       ===               
        //           ）      //      ||         ||             //       //       \    || \\      ||               
        //           ）      ||      ||         ||             ||       //       )|   ||  \\     ||       +**++   
        //          ）       ||      ||         ||             ||      |(        )|   ||   \\    ||      +        
        //+     ___/        ||      ||          ||            ||       |(        )|   ||   \\    ||     +         
        //======--_         ||      ||          ||            ||       |(        )|   ||    \\   ||     /*        
        //         \        ||      ||          ||            ||       |(        )|   ||     \\  ||       |*+     
        //          )       ||      ||          ||            ||       ||        ||   ||      \\ ||          \+  
        //           )      ||      ||          ||            ||        ||       |/   ||       \\ |          |*+  
       //           )       ||       \\      \   \\      \    ||        \\_      //   ||        \\|         /+    
       /_\=======_ /     =======     =========   =========  =======      +-====-+     ==        ===    ===*+/    
"""


class CJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        elif isinstance(obj, decimal.Decimal):
            return float(obj)
        # else:
        #     raise TypeError('%r is not JSON serializable' % obj)
        return json.JSONEncoder.default(self, obj)


class Struct:
    def __init__(self, **entries):
        self.__dict__.update(entries)
        self.attr = entries

    def equals(self, struct):
        if struct and self.attr:
            for k in self.attr.keys():
                v = getattr(struct, k)
                if isinstance(v, str) or isinstance(v, int):
                    if v != self.attr[k]:
                        return False

        return True

    def __str__(self):
        return "Struct: %s" % self.attr


def to_num(s, d=None):
    try:
        return int(s)
    except ValueError:
        if d is None:
            return float(s)
        else:
            return d


def object_to_dict(instance, fields=[], excludes=[]):
    info = {}

    if not instance:
        return info

    for fn in fields:
        if excludes and fn in excludes:
            continue
        if hasattr(instance, fn):
            v = getattr(instance, fn)
            if isinstance(v, datetime):
                v = v.astimezone(default_tz)
            info[fn] = v

    return info


def dict_to_object(_dict):
    return Struct(**_dict)


def get_payload_from_token(token):
    try:
        payload = {}  # jwt.decode(token, JWT_SECRET_KEY)
        return payload
    except ValueError as e:
        raise e


def obfuscate_id(raw_id):
    return raw_id
    # return hashider.encrypt(raw_id)


def decrypt_id(fuzzy_id, is_raise_error=False):
    return fuzzy_id
    # val = hashider.decrypt(fuzzy_id)
    # if val and len(val) > 0:
    #     return val[0]
    # else:
    #     if is_raise_error:
    #         raise TypeError("fuzzy id is incorrect!")
    #     return 0


def decrypt_user_id(fuzzy_user_id, is_raise_error=True):
    return decrypt_id(fuzzy_user_id, is_raise_error)


def get_now_ts():  # seconds
    timestamp = time.time()
    return timestamp


def singleton(cls, *args, **kw):
    instances = {}

    def _singleton():
        if cls not in instances:
            instances[cls] = cls(*args, **kw)
        return instances[cls]

    return _singleton


def build_logger(log_name, config):
    import logging.config
    logging.config.dictConfig(config)
    return logging.getLogger(log_name)


def get_logger(log_name, log_file_name, fmt="text"):
    import settings
    log_cfg = settings.build_logging_config(log_name, log_file_name, fmt)
    return build_logger(log_name, log_cfg)


def get_default_logger():
    import settings
    log_name = "runner"
    log_cfg = settings.build_logging_config(log_name, log_name)
    return build_logger(log_name, log_cfg)


def to_str(bs, encoding="utf-8"):
    try:
        if bs:
            if isinstance(bs, dict):
                n_dict = {}
                for b_k in bs:
                    n_dict[to_str(b_k)] = to_str(bs[b_k])
                return n_dict
            elif isinstance(bs, bytes):
                return str(bs, encoding=encoding)
            elif isinstance(bs, str):
                return bs
            else:
                return bs
    except ValueError:
        return None

# -*- coding: utf-8 -*-
"""
Created by susy at 2020/8/18
"""
from enum import Enum, unique
# from django.utils.translation import ugettext_lazy as _

common_msg = "An unexpected error occurred. Please try again later."


@unique
class ExceptionCode(Enum):

    ERR_CODE_TOKEN_EXPIRED = 1000
    ERR_CODE_UNAUTHENTICATED = 1001
    ERR_CODE_BAD_REQUEST = 1002
    ERR_CODE_INVALID_PARAMETER = 1003
    ERR_CODE_NOT_FOUND = 1006
    ERR_CODE_GET_LOCK = 1009
    ERR_CODE_TOKEN_LOSE = 1010
    ERR_CODE_TOKEN_ILLEGAL = 1020
    ERR_CODE_CALL_SERVICE_ERROR = 1030
    ERR_CODE_SERVER_INTERNAL_ERROR = 1999

    ERR_CODE_USER_WAIT_SMS_VERIFY = 2000
    ERR_CODE_USER_HIGH_FREQUENCY = 2001
    ERR_CODE_USER_LOGIN_VERIFY_FAILED = 2002
    ERR_CODE_USER_PASSWORD_FORMAT_ERR = 2003

    ERR_CODE_SIGNATURE_VERIFY_FAILED = 9002
    ERR_CODE_TIMESTAMP_VERITY_FAILED = 9003
    ERR_CODE_NO_SIGNATURE_FAILED = 9004
    ERR_CODE_INVALID_CODE = 9005
    ERR_CODE_INVALID_ACCESS_TOKEN = 9007
    ERR_CODE_COUPON_CHECK_FAILED = 9008

    @staticmethod
    def get(value):

        for exception_code in ExceptionCode:
            if value == exception_code.value:
                return exception_code.name

        return None


class ExceptionMsg(Enum):
    COMMON_ERROR_MSG = common_msg
    ERR_CODE_SIGNATURE_VERIFY_FAILED = "Invalid signature."
    ERR_CODE_TIMESTAMP_VERITY_FAILED = "Invalid Timestamp."
    ERR_CODE_NOT_FOUND = "Not found."
    ERR_CODE_OUT_BID = "Out BID."
    ERR_CODE_BID_POSITION_EXIST = "BID position is exist."

    @staticmethod
    def get(value):

        _exception_code_name = ExceptionCode.get(value)

        if _exception_code_name:
            for exception_msg in ExceptionMsg:
                if _exception_code_name == exception_msg.name:
                    return exception_msg.value

        return common_msg





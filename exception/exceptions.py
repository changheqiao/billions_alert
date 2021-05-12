# -*- coding: utf-8 -*-
"""
Created by susy at 2020/8/18
"""
from common.helper_enum import ExceptionCode, ExceptionMsg


class ApiError(Exception):
    def __init__(self, err_code=None, err_msg=None, ext_data=None):
        if not err_code:
            err_code = ExceptionMsg.COMMON_ERROR_MSG.value
        self.err_code = err_code
        self.err_msg = err_msg if err_msg else ExceptionMsg.get(self.err_code)
        self.ext_data = ext_data

    def __str__(self):
        return u'code: {0}, msg: {1}, {2}'.format(self.err_code, self.err_msg, self.ext_data)


class AlertApiError(ApiError):
    def __init__(self, err_code, err_msg=None):
        self.err_code = err_code
        self.err_msg = err_msg if err_msg else ExceptionMsg.get(self.err_code)

    def __str__(self):
        return u'err_code: {0}, err_msg: {1}'.format(self.err_code, self.err_msg)


class UnauthorizedError(AlertApiError):
    def __init__(self, err_msg=None):
        AlertApiError.__init__(self, err_code=ExceptionCode.ERR_CODE_UNAUTHORIZED.value, err_msg=err_msg)


class UnauthenticatedError(AlertApiError):
    def __init__(self, err_msg=None):
        AlertApiError.__init__(self, err_code=ExceptionCode.ERR_CODE_UNAUTHENTICATED.value, err_msg=err_msg)


class NotFoundError(AlertApiError):
    def __init__(self, err_msg=None):
        AlertApiError.__init__(self, err_code=ExceptionCode.ERR_CODE_NOT_FOUND.value, err_msg=err_msg)


class InvalidParameterError(AlertApiError):
    def __init__(self, err_msg=None):
        AlertApiError.__init__(self, err_code=ExceptionCode.ERR_CODE_INVALID_PARAMETER.value, err_msg=err_msg)


class InvalidTokenError(AlertApiError):
    def __init__(self, err_msg=None):
        AlertApiError.__init__(self, ExceptionCode.ERR_CODE_TOKEN_ILLEGAL.value, err_msg=err_msg)


class TokenExpiredError(AlertApiError):
    def __init__(self, err_msg=None):
        AlertApiError.__init__(self, ExceptionCode.ERR_CODE_TOKEN_EXPIRED.value, err_msg=err_msg)


class InvalidCodeError(AlertApiError):
    def __init__(self, err_msg=None):
        AlertApiError.__init__(self, ExceptionCode.ERR_CODE_INVALID_CODE.value, err_msg=err_msg)


class InvalidAccessTokenError(AlertApiError):
    def __init__(self, err_msg=None):
        AlertApiError.__init__(self, ExceptionCode.ERR_CODE_INVALID_PHONE_NUMBER.value, err_msg=err_msg)


class SignError(AlertApiError):
    def __init__(self, err_msg=None):
        AlertApiError.__init__(self, err_code=ExceptionCode.ERR_CODE_SIGNATURE_VERIFY_FAILED.value, err_msg=err_msg)


class LoginError(AlertApiError):
    def __init__(self, err_msg=None):
        AlertApiError.__init__(self, err_code=ExceptionCode.ERR_CODE_USER_LOGIN_VERIFY_FAILED.value, err_msg=err_msg)


class PasswordFormatError(AlertApiError):
    def __init__(self, err_msg=None):
        AlertApiError.__init__(self, err_code=ExceptionCode.ERR_CODE_USER_PASSWORD_FORMAT_ERR.value, err_msg=err_msg)


class HighFreqError(AlertApiError):
    def __init__(self, err_msg=None):
        AlertApiError.__init__(self, err_code=ExceptionCode.ERR_CODE_USER_HIGH_FREQUENCY.value, err_msg=err_msg)


class GetLockError(AlertApiError):
    def __init__(self, err_msg=None):
        AlertApiError.__init__(self, err_code=ExceptionCode.ERR_CODE_GET_LOCK.value, err_msg=err_msg)


class UserStateWaitSMSVerifyError(AlertApiError):
    def __init__(self, err_msg=None):
        AlertApiError.__init__(self, err_code=ExceptionCode.ERR_CODE_USER_WAIT_SMS_VERIFY.value, err_msg=err_msg)


class CouponCheckError(AlertApiError):
    def __init__(self, err_msg=None):
        AlertApiError.__init__(self, err_code=ExceptionCode.ERR_CODE_COUPON_CHECK_FAILED.value, err_msg=err_msg)


class UnavailableError(Exception):
    pass


ALL_ERRORS = [
    UnauthorizedError,
    UnauthenticatedError,
    NotFoundError,
    InvalidParameterError,
    InvalidTokenError,
    InvalidCodeError,
    SignError,
    GetLockError,
    HighFreqError,
    TokenExpiredError,
    UserStateWaitSMSVerifyError,
    InvalidAccessTokenError,
    LoginError,
    PasswordFormatError,
    CouponCheckError
]

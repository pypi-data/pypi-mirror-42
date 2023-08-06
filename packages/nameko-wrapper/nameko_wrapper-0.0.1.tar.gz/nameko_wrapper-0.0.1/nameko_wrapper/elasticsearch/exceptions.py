"""
ElasticSearch Related Exception
"""
from nameko_wrapper.exceptions import ServiceException, ServiceErrorException


class UniqueException(ServiceException):
    """Unique Exception"""
    msg = '对象已存在，无法创建'
    code = 400


class UniqueTogetherException(UniqueException):
    """Unique Together Exception"""
    pass


class ObjectAlreadyExists(ServiceException):
    """Object Already Exists"""
    msg = '对象已存在'
    code = 400


class PKMissing(ServiceException):
    """PK missing"""
    msg = '主键信息缺失'
    code = 400

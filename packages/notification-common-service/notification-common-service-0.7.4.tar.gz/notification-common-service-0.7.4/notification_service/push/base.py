# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from enum import Enum

from notification_service.exceptions import ClientTypeError, RequireFieldsError

__all__ = ('ClientSystem', 'ServiceProvider', 'Sender', 'Message')


class MatchEnumMixin():

    @classmethod
    def match(cls, value):
        """Match a enum object by keyword.

        Arguments:
            value {str} -- A keyword include by enum name.

        Raises:
            KeyError -- Cannot find a suitable item.

        Returns:
            Enum -- A suitable enum object.
        """
        for enum_key in cls.__members__.iterkeys():
            if value.lower() in enum_key.lower():
                return cls[enum_key]
        raise KeyError(
            'Your key is `{}`. Cannot find a suitable item.'.format(value))


class ClientSystem(MatchEnumMixin, Enum):
    iOS = 'iOS'
    Android = 'Android'


class ServiceProvider(MatchEnumMixin, Enum):
    AWS = 'AWS'
    jigaung = 'jiguang'
    xinge = 'xinge'
    baidu = 'baidu'


class PushType(Enum):
    notification = 1
    custom_message = 2


class Environment(Enum):
    production = 'production'
    development = 'development'


class ClientInfoMixin():
    """Set up and provide target client infomation.

    Returns:
        str -- Original client_type string.
    """

    @property
    def client_type(self):
        return self._client_type

    @client_type.setter
    def client_type(self, value):
        service_provider, system = value.split('-')
        self.service_provider = ServiceProvider.match(service_provider)
        self.client_system = ClientSystem.match(system)
        self._client_type = value


class RequireFieldsCheckMixin():
    """Check fields `required_fields` is supplied."""

    def _checkrequired_fields(self):
        if not isinstance(self.required_fields, set):
            self.required_fields = set(self.required_fields)
        if not self.required_fields.issubset(self.__dict__.keys()):
            need_fields = self.required_fields - set(self.__dict__.keys())
            raise RequireFieldsError(need_fields)


class Sender(ClientInfoMixin, RequireFieldsCheckMixin, object):
    _client_type = None
    service_provider = None
    client_system = None

    access_id = ''
    secret_key = ''

    required_fields = ['access_id', 'secret_key', 'client_type']

    def __init__(self, *args, **kwargs):
        """Init Sender

        Arguments:
            access_id {str} -- [description]
            secret_key {[type]} -- [description]
            client_type {[type]} -- [description]
        """
        self.update(*args, **kwargs)
        self._checkrequired_fields()
        self._init_config()
        self._verify_info()

    def _init_config(self):
        try:
            self.client_type = self.__dict__['client_type']
        except KeyError:
            raise ClientTypeError('`client_type` should not be empty.')

    def _verify_info(self):
        pass

    def check_authorization(self):
        raise NotImplementedError

    def push_single_device(self, msg, target):
        raise NotImplementedError

    def update(self, *args, **kwargs):
        return self.__dict__.update(*args, **kwargs)


class iOSMessageMixin():

    @property
    def environment(self):
        return self._environment

    @environment.setter
    def environment(self, value):
        self._environment = value


class Message(ClientInfoMixin, iOSMessageMixin, RequireFieldsCheckMixin, object):
    """Message ready to send."""

    _client_type = None
    service_provider = None
    client_system = None

    title = ''
    content = ''
    push_type = PushType.notification
    custom_msg = {}
    _enviorment = None

    required_fields = ['client_type', ]

    def __init__(self, *args, **kwargs):
        """Init message

        Arguments:
            client_type {str} -- Client infomation. Like: jiguang-ios.
            title {str} -- Title of message.
            content {str} -- Content of message.
            push_type {PushType} -- Type of message. It would be `notification` 
                or `custom_message`.
            custom_msg {dict} -- Custom message.
            environment {Environment} -- Only iOS need this. Describe whether the
                environment in which the client is located is a production 
                environment or a development environment.
        """
        self.update(*args, **kwargs)
        self._checkrequired_fields()
        self._init_config()

    def _init_config(self):
        self.client_type = self.__dict__['client_type']
        if self.__dict__.get('custom_info'):
            self.custom_msg = self.__dict__['custom_msg']
        if self.client_system == ClientSystem.iOS:
            self.environment = self.__dict__['environment']

    def update(self, *args, **kwargs):
        return self.__dict__.update(*args, **kwargs)

    def to_msg_object(self):
        raise NotImplementedError

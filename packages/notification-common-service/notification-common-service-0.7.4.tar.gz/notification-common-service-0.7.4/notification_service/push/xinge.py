# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import xinge_push

from notification_service.result import PushResult
from notification_service.states import (
    UnknowPushState, PushExcetion, CheckAuthorizationExcetion, Success)
from notification_service.utils import update_sub_dict

from .base import (Sender, Message, ClientSystem,
                   ServiceProvider, PushType, Environment, ClientTypeError)

import sys
reload(sys)
sys.setdefaultencoding('utf-8')


class XingeMessage(Message):

    def to_msg_object(self):
        if self.client_system is ClientSystem.iOS:
            return self._to_msg_object_iOS()
        if self.client_system is ClientSystem.Android:
            return self._to_msg_object_android()

    def _to_msg_object_iOS(self):
        msg = xinge_push.MessageIOS()
        msg.raw = {
            'aps': {
                'alert': {
                    'title': self.title,
                    'body': self.content,
                }
            }
        }
        return self._apply_push_type(self._apply_custom_msg(msg))

    def _to_msg_object_android(self):
        msg = xinge_push.Message()
        msg.raw = {
            'title': self.title,
            'content': self.content,
        }
        return self._apply_push_type(self._apply_custom_msg(msg))

    def _apply_custom_msg(self, msg):
        if self.custom_msg:
            msg.raw = update_sub_dict(msg.raw, self.custom_msg)
        return msg

    def _apply_push_type(self, msg):
        if self.push_type is PushType.custom_message:
            if self.client_system is ClientSystem.iOS:
                return self._apply_push_type_iOS(msg)
            if self.client_system is ClientSystem.Android:
                return self._apply_push_type_android(msg)
        return msg

    def _apply_push_type_iOS(self, msg):
        if self.push_type == PushType.custom_message:
            msg.raw['aps']['content-available'] = 1
            msg.raw['aps'].pop('alert', None)
        return msg

    def _apply_push_type_android(self, msg):
        if self.push_type == PushType.notification:
            style = xinge_push.Style()
            msg.raw['builder_id'] = style.builderId
            msg.raw['ring'] = style.ring
            msg.raw['vibrate'] = style.vibrate
            msg.raw['clearable'] = style.clearable
            msg.raw['n_id'] = style.nId
            msg.raw['ring_raw'] = style.ringRaw
            msg.raw['lights'] = style.lights
            msg.raw['icon_type'] = style.iconType
            msg.raw['icon_res'] = style.iconRes
            msg.raw['style_id'] = style.styleId
            msg.raw['small_icon'] = style.smallIcon
        return msg

    @property
    def enviorment_value(self):
        if self.client_system is ClientSystem.Android:
            return 0
        elif self.client_system is ClientSystem.iOS:
            if self.environment is Environment.production:
                return 1
            elif self.push_type is Environment.development:
                return 2


class XingeSender(Sender):

    def _init_config(self):
        super(XingeSender, self)._init_config()
        self._client = xinge_push.XingeApp(self.access_id, self.secret_key)

    def _verify_info(self):
        super(XingeSender, self)._verify_info()
        if self.service_provider != ServiceProvider.xinge:
            raise ClientTypeError(
                'service provider `{}` is not `xinge`'.format(self.service_provider))

    def check_authorization(self):
        try:
            response = self._client.QueryDeviceCount()
        except ValueError, e:
            # 查询结果 SDK 无法加载为 JSON
            return PushResult(Success(e))
        except Exception, e:
            return PushResult(PushExcetion(e))
        if response[0] != 0:
            return PushResult(UnknowPushState(response))
        else:
            return PushResult(Success(response))

    def push_single_device(self, msg, target):
        try:
            response = self._client.PushSingleDevice(
                target, msg, msg.enviorment_value)
        except Exception, e:
            return PushResult(PushExcetion(e))
        if response[0] != 0:
            return PushResult(UnknowPushState(response))
        else:
            return PushResult(Success(response))

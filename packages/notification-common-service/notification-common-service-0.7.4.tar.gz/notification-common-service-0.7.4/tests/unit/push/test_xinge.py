# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import json
from unittest import TestCase
from operator import methodcaller

import mock
from faker import Faker

from notification_service.exceptions import ClientTypeError
from notification_service.push.xinge import XingeMessage, XingeSender
from notification_service.push.base import ClientSystem, ServiceProvider, Environment

from . import TestMessage, create_Message

faker = Faker()


def create_XingeMessage(**kwargs):
    return create_Message(XingeMessage, **kwargs)


class test_XingeMessage(TestMessage):

    def test_android(self):
        msg = create_XingeMessage(
            client_type='xinge-android', title=self.title, content=self.content)
        assert msg.client_system == ClientSystem.Android
        assert msg.service_provider == ServiceProvider.xinge

    def test_android_custom_msg(self):
        msg = create_XingeMessage(
            client_type='xinge-android', title=self.title, content=self.content,
            custom_msg={
                'title': self.new_title,
                'content': self.new_content,
            })
        msg_object = msg.to_msg_object()
        assert msg_object.raw['title'] == self.new_title
        assert msg_object.raw['content'] == self.new_content

    def test_ios(self):
        msg = create_XingeMessage(client_type='xinge-ios', title=self.title,
                                  content=self.content, environment=Environment.production)
        assert msg.client_system == ClientSystem.iOS
        assert msg.service_provider == ServiceProvider.xinge

    def test_ios_custom_msg(self):
        environment = Environment.production
        msg = create_XingeMessage(client_type='xinge-ios', title=self.title,
                                  content=self.content, environment=environment,
                                  custom_msg={
                                      'aps': {
                                          'alert': {
                                              'title': self.new_title,
                                              'body': self.new_content,
                                          }
                                      }
                                  })
        msg_object = msg.to_msg_object()
        assert msg_object.raw['aps']['alert']['title'] == self.new_title
        assert msg_object.raw['aps']['alert']['body'] == self.new_content


class test_XingeSender(TestCase):

    def setUp(self):
        self.access_id = '2200314349'
        self.secret_key = 'a5c7e5ad1ccb9314ae99e14eedd02db8'
        self.target = ''
        self.client_types = ['xinge-ios', 'xinge-android']

        self.mock_PushSingleDevice_success = mock.Mock(return_value=(0, ''))
        self.mock_QueryDeviceCount_success = mock.Mock(return_value=(0, 12))

    def test_sender(self):
        for client_type in self.client_types:
            client_type = 'xinge-ios'
            msg = create_XingeMessage(client_type=client_type)
            sender = XingeSender(
                access_id=self.access_id, secret_key=self.secret_key,
                client_type=client_type)
            sender._client.PushSingleDevice = self.mock_PushSingleDevice_success
            assert sender.push_single_device(msg, self.target).is_success

    def test_check_authorization(self):
        for clien_type in self.client_types:
            sender = XingeSender(
                access_id=self.access_id, secret_key=self.secret_key,
                client_type=clien_type)
            sender._client.QueryDeviceCount = self.mock_QueryDeviceCount_success
            assert sender.check_authorization().is_success

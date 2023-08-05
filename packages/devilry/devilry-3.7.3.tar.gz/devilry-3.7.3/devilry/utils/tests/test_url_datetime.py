# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import re

from django import test
from django.utils import timezone

from devilry.utils import datetimeutils


class TestURLDatetime(test.TestCase):

    def test_url_patternmatcher(self):
        self.assertIsNotNone(re.match(r'\w+', datetimeutils.datetime_to_url_string(timezone.now())))

    def test_url_convert_to_string_and_back(self):
        datetime_original = timezone.now().replace(microsecond=0)
        print repr(timezone.now())
        datetime_as_string = datetimeutils.datetime_to_url_string(datetime_original)
        datetime_converted_back = datetimeutils.datetime_url_string_to_datetime(datetime_as_string)
        self.assertEquals(datetime_original, datetime_converted_back)

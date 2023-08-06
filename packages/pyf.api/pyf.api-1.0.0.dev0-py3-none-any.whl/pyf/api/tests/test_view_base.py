# -*- coding: utf-8 -*-
import unittest

from pyramid import testing


class BaseTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    def test_base_result(self):
        from ..views.base import Base

        base = Base(request={})
        test_value = {"foo": "bar"}
        result = base._result(test_value)
        self.assertIn("error", result)
        self.assertEqual(result["error"], "")
        self.assertIn("result", result)
        self.assertEqual(result["result"], test_value)

        result = base._error("foo")
        self.assertIn("error", result)
        self.assertEqual(result["error"], "foo")
        self.assertIn("result", result)
        self.assertEqual(result["result"], {})

#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `openwrt_luci_rpc` package."""


import unittest
from openwrt_luci_rpc import utilities
from openwrt_luci_rpc.constants import OpenWrtConstants


class TestOpenwrtLuciRPC(unittest.TestCase):
    """Tests for `openwrt_luci_rpc` package."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_normalise_keys(self):
        """Test replacing v17 keys works as expected."""

        data = {'dev': 'br-lan',
                'stale': True,
                'HW address': '9C:20:7B:CA:A2:16',
                'IP address': "127.0.0.1",
                }

        utilities.normalise_keys(data)

        assert data[OpenWrtConstants.MODERN_KEYS["HW address"]] == '9C:20:7B:CA:A2:16'
        assert data[OpenWrtConstants.MODERN_KEYS["IP address"]] == '127.0.0.1'
        assert data['stale'] == True
        assert data['dev'] == 'br-lan'

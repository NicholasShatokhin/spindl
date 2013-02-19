#!/usr/bin/python
# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
### BEGIN LICENSE
# Copyright (C) 2013 <Zane Swafford> <zane@zaneswafford.com>
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#    http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
### END LICENSE

import sys
import os.path
import unittest
sys.path.insert(0, os.path.realpath(os.path.join(os.path.dirname(__file__), "..")))

from spindl import AboutSpindlDialog

class TestExample(unittest.TestCase):
    def setUp(self):
        self.AboutSpindlDialog_members = [
        'AboutDialog', 'AboutSpindlDialog', 'gettext', 'logger', 'logging']

    def test_AboutSpindlDialog_members(self):
        all_members = dir(AboutSpindlDialog)
        public_members = [x for x in all_members if not x.startswith('_')]
        public_members.sort()
        self.assertEqual(self.AboutSpindlDialog_members, public_members)

if __name__ == '__main__':    
    unittest.main()

# AsynQueue:
# Asynchronous task queueing based on the Twisted framework, with task
# prioritization and a powerful worker/manager interface.
#
# Copyright (C) 2006-2007, 2015 by Edwin A. Suominen,
# http://edsuom.com/AsynQueue
#
# See edsuom.com for API documentation as well as information about
# Ed's background and other projects, software and otherwise.
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the
# License. You may obtain a copy of the License at
# 
#   http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an "AS
# IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
# express or implied. See the License for the specific language
# governing permissions and limitations under the License.

"""
Unit tests for mcmandelbrot.runner
"""

import png

from twisted.internet import defer

from mcmandelbrot import main
from mcmandelbrot.test.testbase import TestCase

    
class TestRun(TestCase):
    verbose = True
    
    @defer.inlineCallbacks
    def test_basic(self):
        N = 100
        filePath = "image.png"
        runInfo = yield self.checkProducesFile(
            filePath, main.run,
            "-o", filePath, 100, -0.630, 0, 1.4,
            ignoreReactor=True)
        self.assertEqual(runInfo[1], N*N)


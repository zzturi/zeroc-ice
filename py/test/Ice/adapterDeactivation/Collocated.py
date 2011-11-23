#!/usr/bin/env python
# **********************************************************************
#
# Copyright (c) 2003-2008 ZeroC, Inc. All rights reserved.
#
# This copy of Ice is licensed to you under the terms described in the
# ICE_LICENSE file included in this distribution.
#
# **********************************************************************

import os, sys, traceback, time

for toplevel in [".", "..", "../..", "../../..", "../../../.."]:
    toplevel = os.path.normpath(toplevel)
    if os.path.exists(os.path.join(toplevel, "python", "Ice.py")):
        break
else:
    raise "can't find toplevel directory!"

import Ice
Ice.loadSlice('Test.ice')
import Test, TestI, AllTests

class TestServer(Ice.Application):
    def run(self, args):
        self.communicator().getProperties().setProperty("TestAdapter.Endpoints", "default -p 12010 -t 10000")
        adapter = self.communicator().createObjectAdapter("TestAdapter")
        locator = TestI.ServantLocatorI()

        adapter.addServantLocator(locator, "")
        adapter.activate()

        AllTests.allTests(self.communicator())

        adapter.waitForDeactivate()
        return 0

app = TestServer()
sys.exit(app.main(sys.argv))
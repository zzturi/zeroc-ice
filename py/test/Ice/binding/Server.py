#!/usr/bin/env python
# **********************************************************************
#
# Copyright (c) 2003-2011 ZeroC, Inc. All rights reserved.
#
# This copy of Ice is licensed to you under the terms described in the
# ICE_LICENSE file included in this distribution.
#
# **********************************************************************

import os, sys, traceback

import Ice
Ice.loadSlice('Test.ice')
import Test, TestI

def run(args, communicator):
    communicator.getProperties().setProperty("Ice.Warn.Connections", "0")
    communicator.getProperties().setProperty("TestAdapter.Endpoints", "default -p 12010:udp")
    adapter = communicator.createObjectAdapter("TestAdapter")
    id = communicator.stringToIdentity("communicator")
    adapter.add(TestI.RemoteCommunicatorI(), id)
    adapter.activate()

    communicator.waitForShutdown()
    return True

try:
    communicator = Ice.initialize(sys.argv)
    status = run(sys.argv, communicator)
except:
    traceback.print_exc()
    status = False

if communicator:
    try:
        communicator.destroy()
    except:
        traceback.print_exc()
        status = False

sys.exit(not status)

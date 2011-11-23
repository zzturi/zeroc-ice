#!/usr/bin/env python
# **********************************************************************
#
# Copyright (c) 2003-2008 ZeroC, Inc. All rights reserved.
#
# This copy of Ice is licensed to you under the terms described in the
# ICE_LICENSE file included in this distribution.
#
# **********************************************************************

import os, sys

for toplevel in [".", "..", "../..", "../../..", "../../../.."]:
    toplevel = os.path.normpath(toplevel)
    if os.path.exists(os.path.join(toplevel, "config", "TestUtil.py")):
        break
else:
    raise "can't find toplevel directory!"

sys.path.append(os.path.join(toplevel, "config"))
import TestUtil
TestUtil.processCmdLine()

testdir = os.path.dirname(os.path.abspath(__file__))

server = os.path.join(testdir, "server")

print "starting server...",
serverPipe = TestUtil.startServer(server, "")
TestUtil.getServerPid(serverPipe)
TestUtil.getAdapterReady(serverPipe, True, 3)
print "ok"

router = os.path.join(TestUtil.getCppBinDir(), "glacier2router")

args = r' --Glacier2.Client.Endpoints="default -p 12347 -t 10000"' + \
        r' --Ice.Admin.Endpoints="tcp -p 12348 -t 10000"' + \
        r' --Ice.Admin.InstanceName=Glacier2' + \
        r' --Glacier2.Server.Endpoints="default -p 12349 -t 10000"' + \
        r' --Glacier2.SessionManager="SessionManager:tcp -p 12010 -t 10000"' + \
        r' --Glacier2.PermissionsVerifier="Glacier2/NullPermissionsVerifier"' + \
        r' --Ice.Default.Locator="locator:default -p 12012 -t 10000"'

print "starting router...",
starterPipe = TestUtil.startServer(router, args) 
TestUtil.getServerPid(starterPipe)
TestUtil.getAdapterReady(starterPipe, True, 2)
print "ok"

client = os.path.join(testdir, "client")

print "starting client...",
clientPipe = TestUtil.startClient(client, " 2>&1")
TestUtil.ignorePid(clientPipe)
print "ok"

TestUtil.printOutputFromPipe(clientPipe)
clientStatus = TestUtil.closePipe(clientPipe)
if clientStatus:
    TestUtil.killServers()

if clientStatus or TestUtil.serverStatus():
    print >>sys.stderr, "Client status:", clientStatus
    print >>sys.stderr, "Server status:", TestUtil.serverStatus()
    sys.exit(1)

sys.exit(0)
#!/usr/bin/env python
# **********************************************************************
#
# Copyright (c) 2003-2011 ZeroC, Inc. All rights reserved.
#
# This copy of Ice is licensed to you under the terms described in the
# ICE_LICENSE file included in this distribution.
#
# **********************************************************************

import Ice, sys, threading

Ice.loadSlice('-I. --all Forward.ice ClientPrivate.ice')
import Test

def test(b):
    if not b:
        raise RuntimeError('test assertion failed')

class CallbackBase:
    def __init__(self):
        self._called = False
        self._cond = threading.Condition()

    def check(self):
        self._cond.acquire()
        try:
            while not self._called:
                self._cond.wait()
            self._called = False
        finally:
            self._cond.release()

    def called(self):
        self._cond.acquire()
        self._called = True
        self._cond.notify()
        self._cond.release()

class Callback(CallbackBase):
    def response_SBaseAsObject(self, o):
        test(o)
        test(o.ice_id() == "::Test::SBase")
        sb = o
        test(isinstance(sb, Test.SBase))
        test(sb.sb == "SBase.sb")
        self.called()

    def response_SBaseAsSBase(self, sb):
        test(sb.sb == "SBase.sb")
        self.called()

    def response_SBSKnownDerivedAsSBase(self, sb):
        sbskd = sb
        test(isinstance(sbskd, Test.SBSKnownDerived))
        test(sbskd.sbskd == "SBSKnownDerived.sbskd")
        self.called()

    def response_SBSKnownDerivedAsSBSKnownDerived(self, sbskd):
        test(sbskd.sbskd == "SBSKnownDerived.sbskd")
        self.called()

    def response_SBSUnknownDerivedAsSBase(self, sb):
        test(sb.sb == "SBSUnknownDerived.sb")
        self.called()

    def response_SUnknownAsObject(self, o):
        test(False)

    def exception_SUnknownAsObject(self, exc):
        test(exc.ice_name() == "Ice::NoObjectFactoryException")
        self.called()

    def response_oneElementCycle(self, b):
        test(b)
        test(b.ice_id() == "::Test::B")
        test(b.sb == "B1.sb")
        test(b.pb == b)
        self.called()

    def response_twoElementCycle(self, b1):
        test(b1)
        test(b1.ice_id() == "::Test::B")
        test(b1.sb == "B1.sb")

        b2 = b1.pb
        test(b2)
        test(b2.ice_id() == "::Test::B")
        test(b2.sb == "B2.sb")
        test(b2.pb == b1)
        self.called()

    def response_D1AsB(self, b1):
        test(b1)
        test(b1.ice_id() == "::Test::D1")
        test(b1.sb == "D1.sb")
        test(b1.pb)
        test(b1.pb != b1)
        d1 = b1
        test(isinstance(d1, Test.D1))
        test(d1.sd1 == "D1.sd1")
        test(d1.pd1)
        test(d1.pd1 != b1)
        test(b1.pb == d1.pd1)

        b2 = b1.pb
        test(b2)
        test(b2.pb == b1)
        test(b2.sb == "D2.sb")
        test(b2.ice_id() == "::Test::B")
        self.called()

    def response_D1AsD1(self, d1):
        test(d1)
        test(d1.ice_id() == "::Test::D1")
        test(d1.sb == "D1.sb")
        test(d1.pb)
        test(d1.pb != d1)

        b2 = d1.pb
        test(b2)
        test(b2.ice_id() == "::Test::B")
        test(b2.sb == "D2.sb")
        test(b2.pb == d1)
        self.called()

    def response_D2AsB(self, b2):
        test(b2)
        test(b2.ice_id() == "::Test::B")
        test(b2.sb == "D2.sb")
        test(b2.pb)
        test(b2.pb != b2)

        b1 = b2.pb
        test(b1)
        test(b1.ice_id() == "::Test::D1")
        test(b1.sb == "D1.sb")
        test(b1.pb == b2)
        d1 = b1
        test(isinstance(d1, Test.D1))
        test(d1.sd1 == "D1.sd1")
        test(d1.pd1 == b2)
        self.called()

    def response_paramTest1(self, b1, b2):
        test(b1)
        test(b1.ice_id() == "::Test::D1")
        test(b1.sb == "D1.sb")
        test(b1.pb == b2)
        d1 = b1
        test(isinstance(d1, Test.D1))
        test(d1.sd1 == "D1.sd1")
        test(d1.pd1 == b2)

        test(b2)
        test(b2.ice_id() == "::Test::B")        # No factory, must be sliced
        test(b2.sb == "D2.sb")
        test(b2.pb == b1)
        self.called()

    def response_returnTest1(self, r, p1, p2):
        test(r == p1)
        self.called()

    def response_returnTest2(self, r, p1, p2):
        test(r == p1)
        self.called()

    def response_returnTest3(self, b):
        self.r = b
        self.called()

    def response_paramTest3(self, ret, p1, p2):
        test(p1)
        test(p1.sb == "D2.sb (p1 1)")
        test(p1.pb == None)
        test(p1.ice_id() == "::Test::B")

        test(p2)
        test(p2.sb == "D2.sb (p2 1)")
        test(p2.pb == None)
        test(p2.ice_id() == "::Test::B")

        test(ret)
        test(ret.sb == "D1.sb (p2 2)")
        test(ret.pb == None)
        test(ret.ice_id() == "::Test::D1")
        self.called()

    def response_paramTest4(self, ret, b):
        test(b)
        test(b.sb == "D4.sb (1)")
        test(b.pb == None)
        test(b.ice_id() == "::Test::B")

        test(ret)
        test(ret.sb == "B.sb (2)")
        test(ret.pb == None)
        test(ret.ice_id() == "::Test::B")
        self.called()

    def response_sequenceTest(self, ss):
        self.r = ss
        self.called()

    def response_dictionaryTest(self, r, bout):
        self.r = r
        self.bout = bout
        self.called()

    def exception_throwBaseAsBase(self, ex):
        test(ex.ice_name() == "Test::BaseException")
        e = ex
        test(isinstance(e, Test.BaseException))
        test(e.sbe == "sbe")
        test(e.pb)
        test(e.pb.sb == "sb")
        test(e.pb.pb == e.pb)
        self.called()

    def exception_throwDerivedAsBase(self, ex):
        test(ex.ice_name() == "Test::DerivedException")
        e = ex
        test(isinstance(e, Test.DerivedException))
        test(e.sbe == "sbe")
        test(e.pb)
        test(e.pb.sb == "sb1")
        test(e.pb.pb == e.pb)
        test(e.sde == "sde1")
        test(e.pd1)
        test(e.pd1.sb == "sb2")
        test(e.pd1.pb == e.pd1)
        test(e.pd1.sd1 == "sd2")
        test(e.pd1.pd1 == e.pd1)
        self.called()

    def exception_throwDerivedAsDerived(self, ex):
        test(ex.ice_name() == "Test::DerivedException")
        e = ex
        test(isinstance(e, Test.DerivedException))
        test(e.sbe == "sbe")
        test(e.pb)
        test(e.pb.sb == "sb1")
        test(e.pb.pb == e.pb)
        test(e.sde == "sde1")
        test(e.pd1)
        test(e.pd1.sb == "sb2")
        test(e.pd1.pb == e.pd1)
        test(e.pd1.sd1 == "sd2")
        test(e.pd1.pd1 == e.pd1)
        self.called()

    def exception_throwUnknownDerivedAsBase(self, ex):
        test(ex.ice_name() == "Test::BaseException")
        e = ex
        test(isinstance(e, Test.BaseException))
        test(e.sbe == "sbe")
        test(e.pb)
        test(e.pb.sb == "sb d2")
        test(e.pb.pb == e.pb)
        self.called()

    def response_useForward(self, f):
        test(f)
        self.called()

    def response(self):
        test(False)

    def exception(self, exc):
        test(False)

def allTests(communicator):
    obj = communicator.stringToProxy("Test:default -p 12010")
    t = Test.TestIntfPrx.checkedCast(obj)

    print "base as Object... ",
    o = None
    try:
        o = t.SBaseAsObject()
        test(o)
        test(o.ice_id() == "::Test::SBase")
    except Ice.Exception:
        test(False)
    sb = o
    test(isinstance(sb, Test.SBase))
    test(sb)
    test(sb.sb == "SBase.sb")
    print "ok"

    print "base as Object (AMI)... ",
    cb = Callback()
    t.begin_SBaseAsObject(cb.response_SBaseAsObject, cb.exception)
    cb.check()
    print "ok"

    print "base as base... ",
    try:
        sb = t.SBaseAsSBase()
        test(sb.sb == "SBase.sb")
    except Ice.Exception:
        test(False)
    print "ok"

    print "base as base (AMI)... ",
    cb = Callback()
    t.begin_SBaseAsSBase(cb.response_SBaseAsSBase, cb.exception)
    cb.check()
    print "ok"

    print "base with known derived as base... ",
    try:
        sb = t.SBSKnownDerivedAsSBase()
        test(sb.sb == "SBSKnownDerived.sb")
    except Ice.Exception:
        test(False)
    sbskd = sb
    test(isinstance(sbskd, Test.SBSKnownDerived))
    test(sbskd)
    test(sbskd.sbskd == "SBSKnownDerived.sbskd")
    print "ok"

    print "base with known derived as base (AMI)... ",
    cb = Callback()
    t.begin_SBSKnownDerivedAsSBase(cb.response_SBSKnownDerivedAsSBase, cb.exception)
    cb.check()
    print "ok"

    print "base with known derived as known derived... ",
    try:
        sbskd = t.SBSKnownDerivedAsSBSKnownDerived()
        test(sbskd.sbskd == "SBSKnownDerived.sbskd")
    except Ice.Exception:
        test(False)
    print "ok"

    print "base with known derived as known derived (AMI)... ",
    cb = Callback()
    t.begin_SBSKnownDerivedAsSBSKnownDerived(cb.response_SBSKnownDerivedAsSBSKnownDerived, cb.exception)
    cb.check()
    print "ok"

    print "base with unknown derived as base... ",
    try:
        sb = t.SBSUnknownDerivedAsSBase()
        test(sb.sb == "SBSUnknownDerived.sb")
    except Ice.Exception:
        test(False)
    print "ok"

    print "base with unknown derived as base (AMI)... ",
    cb = Callback()
    t.begin_SBSUnknownDerivedAsSBase(cb.response_SBSUnknownDerivedAsSBase, cb.exception)
    cb.check()
    print "ok"

    print "unknown with Object as Object... ",
    try:
        o = t.SUnknownAsObject()
        test(False)
    except Ice.NoObjectFactoryException:
        pass
    except Ice.Exception:
        test(False)
    print "ok"

    print "unknown with Object as Object (AMI)... ",
    try:
        cb = Callback()
        t.begin_SUnknownAsObject(cb.response_SUnknownAsObject, cb.exception_SUnknownAsObject)
        cb.check()
    except Ice.NoObjectFactoryException:
        pass
    except Ice.Exception:
        test(False)
    print "ok"

    print "one-element cycle... ",
    try:
        b = t.oneElementCycle()
        test(b)
        test(b.ice_id() == "::Test::B")
        test(b.sb == "B1.sb")
        test(b.pb == b)
    except Ice.Exception:
        test(False)
    print "ok"

    print "one-element cycle (AMI)... ",
    cb = Callback()
    t.begin_oneElementCycle(cb.response_oneElementCycle, cb.exception)
    cb.check()
    print "ok"

    print "two-element cycle... ",
    try:
        b1 = t.twoElementCycle()
        test(b1)
        test(b1.ice_id() == "::Test::B")
        test(b1.sb == "B1.sb")

        b2 = b1.pb
        test(b2)
        test(b2.ice_id() == "::Test::B")
        test(b2.sb == "B2.sb")
        test(b2.pb == b1)
    except Ice.Exception:
        test(False)
    print "ok"

    print "two-element cycle (AMI)... ",
    cb = Callback()
    t.begin_twoElementCycle(cb.response_twoElementCycle, cb.exception)
    cb.check()
    print "ok"

    print "known derived pointer slicing as base... ",
    try:
        b1 = t.D1AsB()
        test(b1)
        test(b1.ice_id() == "::Test::D1")
        test(b1.sb == "D1.sb")
        test(b1.pb)
        test(b1.pb != b1)
        d1 = b1
        test(isinstance(d1, Test.D1))
        test(d1.sd1 == "D1.sd1")
        test(d1.pd1)
        test(d1.pd1 != b1)
        test(b1.pb == d1.pd1)

        b2 = b1.pb
        test(b2)
        test(b2.pb == b1)
        test(b2.sb == "D2.sb")
        test(b2.ice_id() == "::Test::B")
    except Ice.Exception:
        test(False)
    print "ok"

    print "known derived pointer slicing as base (AMI)... ",
    cb = Callback()
    t.begin_D1AsB(cb.response_D1AsB, cb.exception)
    cb.check()
    print "ok"

    print "known derived pointer slicing as derived... ",
    try:
        d1 = t.D1AsD1()
        test(d1)
        test(d1.ice_id() == "::Test::D1")
        test(d1.sb == "D1.sb")
        test(d1.pb)
        test(d1.pb != d1)

        b2 = d1.pb
        test(b2)
        test(b2.ice_id() == "::Test::B")
        test(b2.sb == "D2.sb")
        test(b2.pb == d1)
    except Ice.Exception:
        test(False)
    print "ok"

    print "known derived pointer slicing as derived (AMI)... ",
    cb = Callback()
    t.begin_D1AsD1(cb.response_D1AsD1, cb.exception)
    cb.check()
    print "ok"

    print "unknown derived pointer slicing as base... ",
    try:
        b2 = t.D2AsB()
        test(b2)
        test(b2.ice_id() == "::Test::B")
        test(b2.sb == "D2.sb")
        test(b2.pb)
        test(b2.pb != b2)

        b1 = b2.pb
        test(b1)
        test(b1.ice_id() == "::Test::D1")
        test(b1.sb == "D1.sb")
        test(b1.pb == b2)
        d1 = b1
        test(isinstance(d1, Test.D1))
        test(d1.sd1 == "D1.sd1")
        test(d1.pd1 == b2)
    except Ice.Exception:
        test(False)
    print "ok"

    print "unknown derived pointer slicing as base (AMI)... ",
    cb = Callback()
    t.begin_D2AsB(cb.response_D2AsB, cb.exception)
    cb.check()
    print "ok"

    print "param ptr slicing with known first... ",
    try:
        b1, b2 = t.paramTest1()

        test(b1)
        test(b1.ice_id() == "::Test::D1")
        test(b1.sb == "D1.sb")
        test(b1.pb == b2)
        d1 = b1
        test(isinstance(d1, Test.D1))
        test(d1.sd1 == "D1.sd1")
        test(d1.pd1 == b2)

        test(b2)
        test(b2.ice_id() == "::Test::B")        # No factory, must be sliced
        test(b2.sb == "D2.sb")
        test(b2.pb == b1)
    except Ice.Exception:
        test(False)
    print "ok"

    print "param ptr slicing with known first (AMI)... ",
    cb = Callback()
    t.begin_paramTest1(cb.response_paramTest1, cb.exception)
    cb.check()
    print "ok"

    print "param ptr slicing with unknown first... ",
    try:
        b2, b1 = t.paramTest2()

        test(b1)
        test(b1.ice_id() == "::Test::D1")
        test(b1.sb == "D1.sb")
        test(b1.pb == b2)
        d1 = b1
        test(isinstance(d1, Test.D1))
        test(d1.sd1 == "D1.sd1")
        test(d1.pd1 == b2)

        test(b2)
        test(b2.ice_id() == "::Test::B")        # No factory, must be sliced
        test(b2.sb == "D2.sb")
        test(b2.pb == b1)
    except Ice.Exception:
        import traceback
        traceback.print_exc()
        test(False)
    print "ok"

    print "return value identity with known first... ",
    try:
        r, p1, p2 = t.returnTest1()
        test(r == p1)
    except Ice.Exception:
        test(False)
    print "ok"

    print "return value identity with known first (AMI)... ",
    cb = Callback()
    t.begin_returnTest1(cb.response_returnTest1, cb.exception)
    cb.check()
    print "ok"

    print "return value identity with unknown first... ",
    try:
        r, p1, p2 = t.returnTest2()
        test(r == p1)
    except Ice.Exception:
        test(False)
    print "ok"

    print "return value identity with unknown first (AMI)... ",
    cb = Callback()
    t.begin_returnTest2(cb.response_returnTest2, cb.exception)
    cb.check()
    print "ok"

    print "return value identity for input params known first... ",
    try:
        d1 = Test.D1()
        d1.sb = "D1.sb"
        d1.sd1 = "D1.sd1"
        d3 = Test.D3()
        d3.pb = d1
        d3.sb = "D3.sb"
        d3.sd3 = "D3.sd3"
        d3.pd3 = d1
        d1.pb = d3
        d1.pd1 = d3

        b1 = t.returnTest3(d1, d3)

        test(b1)
        test(b1.sb == "D1.sb")
        test(b1.ice_id() == "::Test::D1")
        p1 = b1
        test(isinstance(p1, Test.D1))
        test(p1.sd1 == "D1.sd1")
        test(p1.pd1 == b1.pb)

        b2 = b1.pb
        test(b2)
        test(b2.sb == "D3.sb")
        test(b2.ice_id() == "::Test::B")        # Sliced by server
        test(b2.pb == b1)
        p3 = b2
        test(not isinstance(p3, Test.D3))

        test(b1 != d1)
        test(b1 != d3)
        test(b2 != d1)
        test(b2 != d3)
    except Ice.Exception:
        test(False)
    print "ok"

    print "return value identity for input params known first (AMI)... ",
    try:
        d1 = Test.D1()
        d1.sb = "D1.sb"
        d1.sd1 = "D1.sd1"
        d3 = Test.D3()
        d3.pb = d1
        d3.sb = "D3.sb"
        d3.sd3 = "D3.sd3"
        d3.pd3 = d1
        d1.pb = d3
        d1.pd1 = d3

        cb = Callback()
        t.begin_returnTest3(d1, d3, cb.response_returnTest3, cb.exception)
        cb.check()
        b1 = cb.r

        test(b1)
        test(b1.sb == "D1.sb")
        test(b1.ice_id() == "::Test::D1")
        p1 = b1
        test(isinstance(p1, Test.D1))
        test(p1.sd1 == "D1.sd1")
        test(p1.pd1 == b1.pb)

        b2 = b1.pb
        test(b2)
        test(b2.sb == "D3.sb")
        test(b2.ice_id() == "::Test::B")        # Sliced by server
        test(b2.pb == b1)
        p3 = b2
        test(not isinstance(p3, Test.D3))

        test(b1 != d1)
        test(b1 != d3)
        test(b2 != d1)
        test(b2 != d3)
    except Ice.Exception:
        test(False)
    print "ok"

    print "return value identity for input params unknown first... ",
    try:
        d1 = Test.D1()
        d1.sb = "D1.sb"
        d1.sd1 = "D1.sd1"
        d3 = Test.D3()
        d3.pb = d1
        d3.sb = "D3.sb"
        d3.sd3 = "D3.sd3"
        d3.pd3 = d1
        d1.pb = d3
        d1.pd1 = d3

        b1 = t.returnTest3(d3, d1)

        test(b1)
        test(b1.sb == "D3.sb")
        test(b1.ice_id() == "::Test::B")        # Sliced by server
        p1 = b1
        test(not isinstance(p1, Test.D3))

        b2 = b1.pb
        test(b2)
        test(b2.sb == "D1.sb")
        test(b2.ice_id() == "::Test::D1")
        test(b2.pb == b1)
        p3 = b2
        test(isinstance(p3, Test.D1))
        test(p3.sd1 == "D1.sd1")
        test(p3.pd1 == b1)

        test(b1 != d1)
        test(b1 != d3)
        test(b2 != d1)
        test(b2 != d3)
    except Ice.Exception:
        test(False)
    print "ok"

    print "return value identity for input params unknown first (AMI)... ",
    try:
        d1 = Test.D1()
        d1.sb = "D1.sb"
        d1.sd1 = "D1.sd1"
        d3 = Test.D3()
        d3.pb = d1
        d3.sb = "D3.sb"
        d3.sd3 = "D3.sd3"
        d3.pd3 = d1
        d1.pb = d3
        d1.pd1 = d3

        cb = Callback()
        t.begin_returnTest3(d3, d1, cb.response_returnTest3, cb.exception)
        cb.check()
        b1 = cb.r

        test(b1)
        test(b1.sb == "D3.sb")
        test(b1.ice_id() == "::Test::B")        # Sliced by server
        p1 = b1
        test(not isinstance(p1, Test.D3))

        b2 = b1.pb
        test(b2)
        test(b2.sb == "D1.sb")
        test(b2.ice_id() == "::Test::D1")
        test(b2.pb == b1)
        p3 = b2
        test(isinstance(p3, Test.D1))
        test(p3.sd1 == "D1.sd1")
        test(p3.pd1 == b1)

        test(b1 != d1)
        test(b1 != d3)
        test(b2 != d1)
        test(b2 != d3)
    except Ice.Exception:
        test(False)
    print "ok"

    print "remainder unmarshaling (3 instances)... ",
    try:
        ret, p1, p2 = t.paramTest3()

        test(p1)
        test(p1.sb == "D2.sb (p1 1)")
        test(p1.pb == None)
        test(p1.ice_id() == "::Test::B")

        test(p2)
        test(p2.sb == "D2.sb (p2 1)")
        test(p2.pb == None)
        test(p2.ice_id() == "::Test::B")

        test(ret)
        test(ret.sb == "D1.sb (p2 2)")
        test(ret.pb == None)
        test(ret.ice_id() == "::Test::D1")
    except Ice.Exception:
        test(False)
    print "ok"

    print "remainder unmarshaling (3 instances) (AMI)... ",
    cb = Callback()
    t.begin_paramTest3(cb.response_paramTest3, cb.exception)
    cb.check()
    print "ok"

    print "remainder unmarshaling (4 instances)... ",
    try:
        ret, b = t.paramTest4()

        test(b)
        test(b.sb == "D4.sb (1)")
        test(b.pb == None)
        test(b.ice_id() == "::Test::B")

        test(ret)
        test(ret.sb == "B.sb (2)")
        test(ret.pb == None)
        test(ret.ice_id() == "::Test::B")
    except Ice.Exception:
        test(False)
    print "ok"

    print "remainder unmarshaling (4 instances) (AMI)... ",
    cb = Callback()
    t.begin_paramTest4(cb.response_paramTest4, cb.exception)
    cb.check()
    print "ok"

    print "param ptr slicing, instance marshaled in unknown derived as base... ",
    try:
        b1 = Test.B()
        b1.sb = "B.sb(1)"
        b1.pb = b1

        d3 = Test.D3()
        d3.sb = "D3.sb"
        d3.pb = d3
        d3.sd3 = "D3.sd3"
        d3.pd3 = b1

        b2 = Test.B()
        b2.sb = "B.sb(2)"
        b2.pb = b1

        r = t.returnTest3(d3, b2)

        test(r)
        test(r.ice_id() == "::Test::B")
        test(r.sb == "D3.sb")
        test(r.pb == r)
    except Ice.Exception:
        test(False)
    print "ok"

    print "param ptr slicing, instance marshaled in unknown derived as base (AMI)... ",
    try:
        b1 = Test.B()
        b1.sb = "B.sb(1)"
        b1.pb = b1

        d3 = Test.D3()
        d3.sb = "D3.sb"
        d3.pb = d3
        d3.sd3 = "D3.sd3"
        d3.pd3 = b1

        b2 = Test.B()
        b2.sb = "B.sb(2)"
        b2.pb = b1

        cb = Callback()
        t.begin_returnTest3(d3, b2, cb.response_returnTest3, cb.exception)
        cb.check()
        r = cb.r

        test(r)
        test(r.ice_id() == "::Test::B")
        test(r.sb == "D3.sb")
        test(r.pb == r)
    except Ice.Exception:
        test(False)
    print "ok"

    print "param ptr slicing, instance marshaled in unknown derived as derived... ",
    try:
        d11 = Test.D1()
        d11.sb = "D1.sb(1)"
        d11.pb = d11
        d11.sd1 = "D1.sd1(1)"
        d11.pd1 = None

        d3 = Test.D3()
        d3.sb = "D3.sb"
        d3.pb = d3
        d3.sd3 = "D3.sd3"
        d3.pd3 = d11

        d12 = Test.D1()
        d12.sb = "D1.sb(2)"
        d12.pb = d12
        d12.sd1 = "D1.sd1(2)"
        d12.pd1 = d11

        r = t.returnTest3(d3, d12)
        test(r)
        test(r.ice_id() == "::Test::B")
        test(r.sb == "D3.sb")
        test(r.pb == r)
    except Ice.Exception:
        test(False)
    print "ok"

    print "param ptr slicing, instance marshaled in unknown derived as derived (AMI)... ",
    try:
        d11 = Test.D1()
        d11.sb = "D1.sb(1)"
        d11.pb = d11
        d11.sd1 = "D1.sd1(1)"
        d11.pd1 = None

        d3 = Test.D3()
        d3.sb = "D3.sb"
        d3.pb = d3
        d3.sd3 = "D3.sd3"
        d3.pd3 = d11

        d12 = Test.D1()
        d12.sb = "D1.sb(2)"
        d12.pb = d12
        d12.sd1 = "D1.sd1(2)"
        d12.pd1 = d11

        cb = Callback()
        t.begin_returnTest3(d3, d12, cb.response_returnTest3, cb.exception)
        cb.check()
        r = cb.r

        test(r)
        test(r.ice_id() == "::Test::B")
        test(r.sb == "D3.sb")
        test(r.pb == r)
    except Ice.Exception:
        test(False)
    print "ok"

    print "sequence slicing... ",
    try:
        ss = Test.SS()
        ss1b = Test.B()
        ss1b.sb = "B.sb"
        ss1b.pb = ss1b

        ss1d1 = Test.D1()
        ss1d1.sb = "D1.sb"
        ss1d1.sd1 = "D1.sd1"
        ss1d1.pb = ss1b

        ss1d3 = Test.D3()
        ss1d3.sb = "D3.sb"
        ss1d3.sd3 = "D3.sd3"
        ss1d3.pb = ss1b

        ss2b = Test.B()
        ss2b.sb = "B.sb"
        ss2b.pb = ss1b

        ss2d1 = Test.D1()
        ss2d1.sb = "D1.sb"
        ss2d1.sd1 = "D1.sd1"
        ss2d1.pb = ss2b

        ss2d3 = Test.D3()
        ss2d3.sb = "D3.sb"
        ss2d3.sd3 = "D3.sd3"
        ss2d3.pb = ss2b

        ss1d1.pd1 = ss2b
        ss1d3.pd3 = ss2d1

        ss2d1.pd1 = ss1d3
        ss2d3.pd3 = ss1d1

        ss1 = Test.SS1()
        ss1.s = (ss1b, ss1d1, ss1d3)

        ss2 = Test.SS2()
        ss2.s = (ss2b, ss2d1, ss2d3)

        ss = t.sequenceTest(ss1, ss2)

        test(ss.c1)
        ss1b = ss.c1.s[0]
        ss1d1 = ss.c1.s[1]
        test(ss.c2)
        ss1d3 = ss.c1.s[2]

        test(ss.c2)
        ss2b = ss.c2.s[0]
        ss2d1 = ss.c2.s[1]
        ss2d3 = ss.c2.s[2]

        test(ss1b.pb == ss1b)
        test(ss1d1.pb == ss1b)
        test(ss1d3.pb == ss1b)

        test(ss2b.pb == ss1b)
        test(ss2d1.pb == ss2b)
        test(ss2d3.pb == ss2b)

        test(ss1b.ice_id() == "::Test::B")
        test(ss1d1.ice_id() == "::Test::D1")
        test(ss1d3.ice_id() == "::Test::B")

        test(ss2b.ice_id() == "::Test::B")
        test(ss2d1.ice_id() == "::Test::D1")
        test(ss2d3.ice_id() == "::Test::B")
    except Ice.Exception:
        test(False)
    print "ok"

    print "sequence slicing (AMI)... ",
    try:
        ss = Test.SS()
        ss1b = Test.B()
        ss1b.sb = "B.sb"
        ss1b.pb = ss1b

        ss1d1 = Test.D1()
        ss1d1.sb = "D1.sb"
        ss1d1.sd1 = "D1.sd1"
        ss1d1.pb = ss1b

        ss1d3 = Test.D3()
        ss1d3.sb = "D3.sb"
        ss1d3.sd3 = "D3.sd3"
        ss1d3.pb = ss1b

        ss2b = Test.B()
        ss2b.sb = "B.sb"
        ss2b.pb = ss1b

        ss2d1 = Test.D1()
        ss2d1.sb = "D1.sb"
        ss2d1.sd1 = "D1.sd1"
        ss2d1.pb = ss2b

        ss2d3 = Test.D3()
        ss2d3.sb = "D3.sb"
        ss2d3.sd3 = "D3.sd3"
        ss2d3.pb = ss2b

        ss1d1.pd1 = ss2b
        ss1d3.pd3 = ss2d1

        ss2d1.pd1 = ss1d3
        ss2d3.pd3 = ss1d1

        ss1 = Test.SS1()
        ss1.s = (ss1b, ss1d1, ss1d3)

        ss2 = Test.SS2()
        ss2.s = (ss2b, ss2d1, ss2d3)

        cb = Callback()
        t.begin_sequenceTest(ss1, ss2, cb.response_sequenceTest, cb.exception)
        cb.check()
        ss = cb.r

        test(ss.c1)
        ss1b = ss.c1.s[0]
        ss1d1 = ss.c1.s[1]
        test(ss.c2)
        ss1d3 = ss.c1.s[2]

        test(ss.c2)
        ss2b = ss.c2.s[0]
        ss2d1 = ss.c2.s[1]
        ss2d3 = ss.c2.s[2]

        test(ss1b.pb == ss1b)
        test(ss1d1.pb == ss1b)
        test(ss1d3.pb == ss1b)

        test(ss2b.pb == ss1b)
        test(ss2d1.pb == ss2b)
        test(ss2d3.pb == ss2b)

        test(ss1b.ice_id() == "::Test::B")
        test(ss1d1.ice_id() == "::Test::D1")
        test(ss1d3.ice_id() == "::Test::B")

        test(ss2b.ice_id() == "::Test::B")
        test(ss2d1.ice_id() == "::Test::D1")
        test(ss2d3.ice_id() == "::Test::B")
    except Ice.Exception:
        test(False)
    print "ok"

    print "dictionary slicing... ",
    try:
        bin = {}
        for i in range(0, 10):
            d1 = Test.D1()
            s = "D1." + str(i)
            d1.sb = s
            d1.pb = d1
            d1.sd1 = s
            d1.pd1 = None
            bin[i] = d1

        r, bout = t.dictionaryTest(bin)

        test(len(bout) == 10)
        for i in range(0, 10):
            b = bout[i * 10]
            test(b)
            s = "D1." + str(i)
            test(b.sb == s)
            test(b.pb)
            test(b.pb != b)
            test(b.pb.sb == s)
            test(b.pb.pb == b.pb)

        test(len(r) == 10)
        for i in range(0, 10):
            b = r[i * 20]
            test(b)
            s = "D1." + str(i * 20)
            test(b.sb == s)
            if i == 0:
                test(b.pb == None)
            else:
                test(b.pb == r[(i - 1) * 20])
            d1 = b
            test(isinstance(d1, Test.D1))
            test(d1.sd1 == s)
            test(d1.pd1 == d1)
    except Ice.Exception:
        test(False)
    print "ok"

    print "dictionary slicing (AMI)... ",
    try:
        bin = {}
        for i in range(0, 10):
            d1 = Test.D1()
            s = "D1." + str(i)
            d1.sb = s
            d1.pb = d1
            d1.sd1 = s
            d1.pd1 = None
            bin[i] = d1

        cb = Callback()
        t.begin_dictionaryTest(bin, cb.response_dictionaryTest, cb.exception)
        cb.check()
        bout = cb.bout
        r = cb.r

        test(len(bout) == 10)
        for i in range(0, 10):
            b = bout[i * 10]
            test(b)
            s = "D1." + str(i)
            test(b.sb == s)
            test(b.pb)
            test(b.pb != b)
            test(b.pb.sb == s)
            test(b.pb.pb == b.pb)

        test(len(r) == 10)
        for i in range(0, 10):
            b = r[i * 20]
            test(b)
            s = "D1." + str(i * 20)
            test(b.sb == s)
            if i == 0:
                test(b.pb == None)
            else:
                test(b.pb == r[(i - 1) * 20])
            d1 = b
            test(isinstance(d1, Test.D1))
            test(d1.sd1 == s)
            test(d1.pd1 == d1)
    except Ice.Exception:
        test(False)
    print "ok"

    print "base exception thrown as base exception... ",
    try:
        t.throwBaseAsBase()
        test(False)
    except Test.BaseException, e:
        test(e.ice_name() == "Test::BaseException")
        test(e.sbe == "sbe")
        test(e.pb)
        test(e.pb.sb == "sb")
        test(e.pb.pb == e.pb)
    except Ice.Exception:
        test(False)
    print "ok"

    print "base exception thrown as base exception (AMI)... ",
    cb = Callback()
    t.begin_throwBaseAsBase(cb.response, cb.exception_throwBaseAsBase)
    cb.check()
    print "ok"

    print "derived exception thrown as base exception... ",
    try:
        t.throwDerivedAsBase()
        test(False)
    except Test.DerivedException, e:
        test(e.ice_name() == "Test::DerivedException")
        test(e.sbe == "sbe")
        test(e.pb)
        test(e.pb.sb == "sb1")
        test(e.pb.pb == e.pb)
        test(e.sde == "sde1")
        test(e.pd1)
        test(e.pd1.sb == "sb2")
        test(e.pd1.pb == e.pd1)
        test(e.pd1.sd1 == "sd2")
        test(e.pd1.pd1 == e.pd1)
    except Ice.Exception:
        test(False)
    print "ok"

    print "derived exception thrown as base exception (AMI)... ",
    cb = Callback()
    t.begin_throwDerivedAsBase(cb.response, cb.exception_throwDerivedAsBase)
    cb.check()
    print "ok"

    print "derived exception thrown as derived exception... ",
    try:
        t.throwDerivedAsDerived()
        test(False)
    except Test.DerivedException, e:
        test(e.ice_name() == "Test::DerivedException")
        test(e.sbe == "sbe")
        test(e.pb)
        test(e.pb.sb == "sb1")
        test(e.pb.pb == e.pb)
        test(e.sde == "sde1")
        test(e.pd1)
        test(e.pd1.sb == "sb2")
        test(e.pd1.pb == e.pd1)
        test(e.pd1.sd1 == "sd2")
        test(e.pd1.pd1 == e.pd1)
    except Ice.Exception:
        test(False)
    print "ok"

    print "derived exception thrown as derived exception (AMI)... ",
    cb = Callback()
    t.begin_throwDerivedAsDerived(cb.response, cb.exception_throwDerivedAsDerived)
    cb.check()
    print "ok"

    print "unknown derived exception thrown as base exception... ",
    try:
        t.throwUnknownDerivedAsBase()
        test(False)
    except Test.BaseException, e:
        test(e.ice_name() == "Test::BaseException")
        test(e.sbe == "sbe")
        test(e.pb)
        test(e.pb.sb == "sb d2")
        test(e.pb.pb == e.pb)
    except Ice.Exception:
        test(False)
    print "ok"

    print "unknown derived exception thrown as base exception (AMI)... ",
    cb = Callback()
    t.begin_throwUnknownDerivedAsBase(cb.response, cb.exception_throwUnknownDerivedAsBase)
    cb.check()
    print "ok"

    print "forward-declared class... ",
    try:
        f = t.useForward()
        test(f)
    except Ice.Exception:
        test(False)
    print "ok"

    print "forward-declared class (AMI)... ",
    cb = Callback()
    t.begin_useForward(cb.response_useForward, cb.exception)
    cb.check()
    print "ok"

    return t

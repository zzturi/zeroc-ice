// **********************************************************************
//
// Copyright (c) 2003-2008 ZeroC, Inc. All rights reserved.
//
// This copy of Ice is licensed to you under the terms described in the
// ICE_LICENSE file included in this distribution.
//
// **********************************************************************

using System.Diagnostics;
using Test;

public sealed class HoldI : HoldDisp_
{
    private static void test(bool b)
    {
        if(!b)
        {
            throw new System.Exception();
        }
    }

    public HoldI(Ice.ObjectAdapter adapter)
    {
        _adapter = adapter;
    }

    public override void
    putOnHold(int milliSeconds, Ice.Current current)
    {
        if(milliSeconds <= 0)
        {
            _adapter.hold();
            _adapter.activate();
        }
        else
        {
            System.Timers.Timer timer = new System.Timers.Timer(milliSeconds);
            timer.AutoReset = false;
            timer.Elapsed += new System.Timers.ElapsedEventHandler(
                delegate(object source, System.Timers.ElapsedEventArgs e)
                {
                    try
                    {
                        putOnHold(0, null);
                    }
                    catch(Ice.ObjectAdapterDeactivatedException)
                    {
                    }
                });
            timer.Enabled = true;
        }
    }

    public override int
    set(int value, int delay, Ice.Current current)
    {
        System.Threading.Thread.Sleep(delay);

        lock(this)
        {
            int tmp = _last;
            _last = value;
            return tmp;
        }
    }

    public override void
    setOneway(int value, int expected, Ice.Current current)
    {
        lock(this)
        {
            test(_last == expected);
            _last = value;
        }
    }

    public override void
    shutdown(Ice.Current current)
    {
        _adapter.hold();
        _adapter.getCommunicator().shutdown();
    }

    private Ice.ObjectAdapter _adapter;
    private int _last = 0;
}
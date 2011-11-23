// **********************************************************************
//
// Copyright (c) 2003-2005 ZeroC, Inc. All rights reserved.
//
// This copy of Ice is licensed to you under the terms described in the
// ICE_LICENSE file included in this distribution.
//
// **********************************************************************

#ifndef GLACIER2_ROUTER_I_H
#define GLACIER2_ROUTER_I_H

#include <Ice/Ice.h>
#include <Glacier2/Router.h>
#include <Glacier2/ClientBlobject.h>
#include <Glacier2/ServerBlobject.h>

namespace Glacier2
{

class RouterI;
typedef IceUtil::Handle<RouterI> RouterIPtr;

class RouterI : public Router, public IceUtil::Mutex
{
public:

    RouterI(const Ice::ObjectAdapterPtr&, const Ice::ObjectAdapterPtr&, const Ice::ConnectionPtr&,
	    const std::string&, const SessionPrx&);
    virtual ~RouterI();
    void destroy();

    virtual Ice::ObjectPrx getClientProxy(const Ice::Current&) const;
    virtual Ice::ObjectPrx getServerProxy(const Ice::Current&) const;
    virtual void addProxy(const Ice::ObjectPrx&, const Ice::Current&);
    virtual SessionPrx createSession(const std::string&, const std::string&, const Ice::Current&);
    virtual void destroySession_async(const AMD_Router_destroySessionPtr&, const ::Ice::Current&);

    ClientBlobjectPtr getClientBlobject() const;
    ServerBlobjectPtr getServerBlobject() const;

    SessionPrx getSession() const;

    IceUtil::Time getTimestamp() const;

    std::string toString() const;

private:

    const Ice::CommunicatorPtr _communicator;
    const IceInternal::RoutingTablePtr _routingTable;
    const int _routingTableTraceLevel;
    const Ice::ObjectPrx _clientProxy;
    const Ice::ObjectPrx _serverProxy;
    const ClientBlobjectPtr _clientBlobject;
    const ServerBlobjectPtr _serverBlobject;
    const Ice::ConnectionPtr _connection;
    const std::string _userId;
    const SessionPrx _session;
    mutable IceUtil::Time _timestamp;
    bool _destroy;
};

}

#endif
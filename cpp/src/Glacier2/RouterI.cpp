// **********************************************************************
//
// Copyright (c) 2003-2011 ZeroC, Inc. All rights reserved.
//
// This copy of Ice is licensed to you under the terms described in the
// ICE_LICENSE file included in this distribution.
//
// **********************************************************************

#include <IceUtil/Random.h>

#include <Glacier2/FilterManager.h>
#include <Glacier2/RoutingTable.h>
#include <Glacier2/RouterI.h>
#include <Glacier2/Session.h>

using namespace std;
using namespace Ice;
using namespace Glacier2;

Glacier2::RouterI::RouterI(const InstancePtr& instance, const ConnectionPtr& connection, const string& userId, 
                           const SessionPrx& session, const Identity& controlId, const FilterManagerPtr& filters,
                           const Ice::Context& context) :
    _instance(instance),
    _clientBlobject(new ClientBlobject(_instance, filters, context)),
    _connection(connection),
    _userId(userId),
    _session(session),
    _controlId(controlId),
    _context(context),
    _timestamp(IceUtil::Time::now(IceUtil::Time::Monotonic))
{
    //
    // If Glacier2 will be used with pre 3.2 clients, then the client proxy must be set.
    // Otherwise getClientProxy just needs to return a nil proxy.
    //
    if(_instance->properties()->getPropertyAsInt("Glacier2.ReturnClientProxy") > 0)
    {
        const_cast<Ice::ObjectPrx&>(_clientProxy) = 
            _instance->clientObjectAdapter()->createProxy(_instance->communicator()->stringToIdentity("dummy"));
    }

    if(_instance->serverObjectAdapter())
    {
        ObjectPrx& serverProxy = const_cast<ObjectPrx&>(_serverProxy);
        Identity ident;
        ident.name = "dummy";
        ident.category.resize(20);
        char buf[20];
        IceUtilInternal::generateRandom(buf, static_cast<int>(sizeof(buf)));
        for(unsigned int i = 0; i < sizeof(buf); ++i)
        {
            const unsigned char c = static_cast<unsigned char>(buf[i]); // A value between 0-255
            ident.category[i] = 33 + c % (127-33); // We use ASCII 33-126 (from ! to ~, w/o space).
        }
        serverProxy = _instance->serverObjectAdapter()->createProxy(ident);

        ServerBlobjectPtr& serverBlobject = const_cast<ServerBlobjectPtr&>(_serverBlobject);
        serverBlobject = new ServerBlobject(_instance, _connection);
    }
}

Glacier2::RouterI::~RouterI()
{
}

void
Glacier2::RouterI::destroy(const AMI_Session_destroyPtr& amiCB)
{
    if(_session)
    {
        if(_instance->serverObjectAdapter())
        {
            try
            {
                //
                // Remove the session control object.
                //
                _instance->serverObjectAdapter()->remove(_controlId);
            }
            catch(const NotRegisteredException&)
            {
            }
            catch(const ObjectAdapterDeactivatedException&)
            {
                //
                // Expected if the router has been shutdown.
                //
            }
        }

        if(_context.size() > 0)
        {
            _session->destroy_async(amiCB, _context);
        }
        else
        {
            _session->destroy_async(amiCB);
        }
    }
}

ObjectPrx
Glacier2::RouterI::getClientProxy(const Current&) const
{
    // No mutex lock necessary, _clientProxy is immutable and is never destroyed.
    return _clientProxy;
}

ObjectPrx
Glacier2::RouterI::getServerProxy(const Current&) const
{
    // No mutex lock necessary, _serverProxy is immutable and is never destroyed.
    return _serverProxy;
}

void
Glacier2::RouterI::addProxy(const ObjectPrx& proxy, const Current& current)
{
    ObjectProxySeq proxies;
    proxies.push_back(proxy);
    addProxies(proxies, current);
}

ObjectProxySeq
Glacier2::RouterI::addProxies(const ObjectProxySeq& proxies, const Current& current)
{
    updateTimestamp();
    return _clientBlobject->add(proxies, current);
}

string
Glacier2::RouterI::getCategoryForClient(const Ice::Current&) const
{
    assert(false); // Must not be called in this router implementation.
    return 0;
}

void
Glacier2::RouterI::createSession_async(const AMD_Router_createSessionPtr&, const std::string&, const std::string&,
                                       const Current&)
{
    assert(false); // Must not be called in this router implementation.
}

void
Glacier2::RouterI::createSessionFromSecureConnection_async(const AMD_Router_createSessionFromSecureConnectionPtr&,
                                                           const Current&)
{
    assert(false); // Must not be called in this router implementation.
}

void
Glacier2::RouterI::refreshSession(const Current&)
{
    assert(false); // Must not be called in this router implementation.
}

void
Glacier2::RouterI::destroySession(const Current&)
{
    assert(false); // Must not be called in this router implementation.
}

Ice::Long
Glacier2::RouterI::getSessionTimeout(const Current&) const
{
    assert(false); // Must not be called in this router implementation.
    return 0;
}

ClientBlobjectPtr
Glacier2::RouterI::getClientBlobject() const
{
    updateTimestamp();
    return _clientBlobject;
}

ServerBlobjectPtr
Glacier2::RouterI::getServerBlobject() const
{
    //
    // We do not update the timestamp for callbacks from the
    // server. We only update the timestamp for client activity.
    //

    return _serverBlobject;
}

SessionPrx
Glacier2::RouterI::getSession() const
{
    return _session; // No mutex lock necessary, _session is immutable.
}

IceUtil::Time
Glacier2::RouterI::getTimestamp() const
{
    IceUtil::Mutex::TryLock lock(_timestampMutex);
    if(lock.acquired())
    {
        return _timestamp;
    }
    else
    {
        return IceUtil::Time::now(IceUtil::Time::Monotonic);
    }
}

void
Glacier2::RouterI::updateTimestamp() const
{
    IceUtil::Mutex::Lock lock(_timestampMutex);
    _timestamp = IceUtil::Time::now(IceUtil::Time::Monotonic);
}

string
Glacier2::RouterI::toString() const
{
    ostringstream out;

    out << "id = " << _userId << '\n';
    if(_serverProxy)
    {
        out << "category = " << _serverProxy->ice_getIdentity().category << '\n';
    }
    out << _connection->toString();

    return out.str();
}

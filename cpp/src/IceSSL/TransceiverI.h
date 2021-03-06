// **********************************************************************
//
// Copyright (c) 2003-2011 ZeroC, Inc. All rights reserved.
//
// This copy of Ice is licensed to you under the terms described in the
// ICE_LICENSE file included in this distribution.
//
// **********************************************************************

#ifndef ICE_SSL_TRANSCEIVER_I_H
#define ICE_SSL_TRANSCEIVER_I_H

#include <IceSSL/InstanceF.h>
#include <IceSSL/Plugin.h>

#include <Ice/LoggerF.h>
#include <Ice/StatsF.h>
#include <Ice/Transceiver.h>

typedef struct ssl_st SSL;
typedef struct bio_st BIO;

namespace IceSSL
{

class ConnectorI;
class AcceptorI;

class TransceiverI : public IceInternal::Transceiver, public IceInternal::NativeInfo
{
    enum State
    {
        StateNeedConnect,
        StateConnectPending,
        StateConnected,
        StateHandshakeComplete
    };

public:

    virtual IceInternal::NativeInfoPtr getNativeInfo();
#ifdef ICE_USE_IOCP
    virtual IceInternal::AsyncInfo* getAsyncInfo(IceInternal::SocketOperation);
#endif
    
    virtual IceInternal::SocketOperation initialize();
    virtual void close();
    virtual bool write(IceInternal::Buffer&);
    virtual bool read(IceInternal::Buffer&);
#ifdef ICE_USE_IOCP
    virtual bool startWrite(IceInternal::Buffer&);
    virtual void finishWrite(IceInternal::Buffer&);
    virtual void startRead(IceInternal::Buffer&);
    virtual void finishRead(IceInternal::Buffer&);
#endif
    virtual std::string type() const;
    virtual std::string toString() const;
    virtual Ice::ConnectionInfoPtr getInfo() const;
    virtual void checkSendSize(const IceInternal::Buffer&, size_t);

private:

    TransceiverI(const InstancePtr&, SOCKET, const std::string&, const struct sockaddr_storage&);
    TransceiverI(const InstancePtr&, SOCKET, const std::string&);
    virtual ~TransceiverI();

    virtual NativeConnectionInfoPtr getNativeConnectionInfo() const;
 
#ifdef ICE_USE_IOCP
    bool send();
    bool receive();
#endif

    friend class ConnectorI;
    friend class AcceptorI;

    const InstancePtr _instance;
    const Ice::LoggerPtr _logger;
    const Ice::StatsPtr _stats;
    
    SSL* _ssl;

    const std::string _host;

    const bool _incoming;
    const std::string _adapterName;

    State _state;
    std::string _desc;
    struct sockaddr_storage _connectAddr;
#ifdef ICE_USE_IOCP
    int _maxSendPacketSize;
    int _maxReceivePacketSize;
    BIO* _iocpBio;
    IceInternal::AsyncInfo _read;
    IceInternal::AsyncInfo _write;
    std::vector<char> _writeBuffer;
    std::vector<char>::iterator _writeI;
    std::vector<char> _readBuffer;
    std::vector<char>::iterator _readI;
    int _sentBytes;
    int _sentPacketSize;
#endif
};
typedef IceUtil::Handle<TransceiverI> TransceiverIPtr;

}

#endif

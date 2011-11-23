// **********************************************************************
//
// Copyright (c) 2003
// ZeroC, Inc.
// Billerica, MA, USA
//
// All Rights Reserved.
//
// Ice is free software; you can redistribute it and/or modify it under
// the terms of the GNU General Public License version 2 as published by
// the Free Software Foundation.
//
// **********************************************************************

#ifndef ICE_SSL_SERVER_TRANSCEIVER_H
#define ICE_SSL_SERVER_TRANSCEIVER_H

#include <IceSSL/SslTransceiver.h>

namespace IceSSL
{

class SslServerTransceiver : public SslTransceiver
{
public:
    virtual int handshake(int timeout = 0);
    virtual void write(IceInternal::Buffer&, int);

protected:
    virtual void showConnectionInfo();
    SslServerTransceiver(const OpenSSLPluginIPtr&, SOCKET, const CertificateVerifierPtr&, SSL*);
    friend class ServerContext;
};

}

#endif


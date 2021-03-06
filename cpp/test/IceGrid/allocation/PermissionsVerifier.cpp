// **********************************************************************
//
// Copyright (c) 2003-2011 ZeroC, Inc. All rights reserved.
//
// This copy of Ice is licensed to you under the terms described in the
// ICE_LICENSE file included in this distribution.
//
// **********************************************************************

#include <Ice/Ice.h>
#include <Glacier2/PermissionsVerifier.h>

using namespace std;

class PermissionsVerifierI : public Glacier2::PermissionsVerifier
{
public:

    virtual bool
    checkPermissions(const string& userId, const string& passwd, string&, const Ice::Current& c) const
    {
        return true;
    }
};

class PermissionsVerifierServer : public Ice::Application
{
public:

    virtual int run(int, char*[])
    {
        Ice::ObjectAdapterPtr adapter = communicator()->createObjectAdapter("PermissionsVerifier");
        adapter->add(new PermissionsVerifierI, communicator()->stringToIdentity("PermissionsVerifier"));
        adapter->activate();
        communicator()->waitForShutdown();
        return EXIT_SUCCESS;
    }
};

int
main(int argc, char* argv[])
{
    PermissionsVerifierServer app;
    return app.main(argc, argv);
}

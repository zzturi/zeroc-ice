# **********************************************************************
#
# Copyright (c) 2003-2011 ZeroC, Inc. All rights reserved.
#
# This copy of Ice is licensed to you under the terms described in the
# ICE_LICENSE file included in this distribution.
#
# **********************************************************************

top_srcdir	= ../../..

CLIENT		= client
SERVER		= server
VERIFIER	= verifier

TARGETS		= $(CLIENT) $(SERVER) $(VERIFIER)

COBJS		= Client.o \
		  AllTests.o

SOBJS		= Server.o

VOBJS		= PermissionsVerifier.o

SRCS		= $(COBJS:.o=.cpp) \
		  $(VOBJS:.o=.cpp) \
		  $(SOBJS:.o=.cpp)

GENPIC          = no

include $(top_srcdir)/config/Make.rules

CPPFLAGS	:= -I. -I../../include $(CPPFLAGS)
LINKWITH	:= $(BZIP2_RPATH_LINK) -lIce -lIceUtil

$(CLIENT): $(COBJS)
	rm -f $@
	$(CXX) $(LDFLAGS) -o $@ $(COBJS) $(OPENSSL_RPATH_LINK) -lIceGrid -lGlacier2 $(LIBS)

$(VERIFIER): $(VOBJS)
	rm -f $@
	$(CXX) $(LDFLAGS) -o $@ $(VOBJS) -lGlacier2 $(LIBS)

$(SERVER): $(SOBJS)
	rm -f $@
	$(CXX) $(LDFLAGS) -o $@ $(SOBJS) -lGlacier2 -lIceSSL $(LIBS) $(OPENSSL_RPATH_LINK)

clean::
	-rm -rf db/node db/registry db/node-1 db/replica-*

include .depend

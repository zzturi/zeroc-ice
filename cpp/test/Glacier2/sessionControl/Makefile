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

TARGETS		= $(CLIENT) $(SERVER) 

COBJS		= Client.o \
		  Session.o

SOBJS		= Server.o \
		  Session.o \
		  SessionI.o

SRCS		= $(COBJS:.o=.cpp) \
		  $(SOBJS:.o=.cpp)

SLICE_SRCS	= Session.ice

include $(top_srcdir)/config/Make.rules

CPPFLAGS	:= -I. -I../../include $(CPPFLAGS)

$(CLIENT): $(OBJS) $(COBJS)
	rm -f $@
	$(CXX) $(LDFLAGS) -o $@ $(OBJS) $(COBJS) -lGlacier2 $(LIBS)

$(SERVER): $(OBJS) $(SOBJS)
	rm -f $@
	$(CXX) $(LDFLAGS) -o $@ $(OBJS) $(SOBJS) -lGlacier2 $(LIBS)

include .depend

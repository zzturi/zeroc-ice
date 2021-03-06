# **********************************************************************
#
# Copyright (c) 2003-2011 ZeroC, Inc. All rights reserved.
#
# This copy of Ice is licensed to you under the terms described in the
# ICE_LICENSE file included in this distribution.
#
# **********************************************************************

top_srcdir	= ..\..\..

SERVER		= server.exe

TARGETS		= $(SERVER)

OBJS		= Server.obj

SRCS		= $(OBJS:.obj=.cpp) \

!include $(top_srcdir)/config/Make.rules.mak

CPPFLAGS	= $(CPPFLAGS) -DWIN32_LEAN_AND_MEAN

!if "$(GENERATE_PDB)" == "yes"
SPDBFLAGS        = /pdb:$(SERVER:.exe=.pdb)
!endif

$(SERVER): $(OBJS)
	$(LINK) $(LD_EXEFLAGS) $(SPDBFLAGS) $(SETARGV) $(OBJS) $(PREOUT)$@ $(PRELIBS)$(LIBS)
	@if exist $@.manifest echo ^ ^ ^ Embedding manifest using $(MT) && \
	    $(MT) -nologo -manifest $@.manifest -outputresource:$@;#1 && del /q $@.manifest

clean::
	if exist db\node rmdir /s /q db\node 
	if exist db\registry rmdir /s /q db\registry 
	if exist db\replica-1 rmdir /s /q db\replica-1

!include .depend.mak

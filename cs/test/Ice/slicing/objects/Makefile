# **********************************************************************
#
# Copyright (c) 2003-2011 ZeroC, Inc. All rights reserved.
#
# This copy of Ice is licensed to you under the terms described in the
# ICE_LICENSE file included in this distribution.
#
# **********************************************************************

top_srcdir	= ../../../..

TARGETS		= client.exe server.exe serveramd.exe

C_SRCS		= AllTests.cs Client.cs
S_SRCS		= Server.cs TestI.cs
SAMD_SRCS	= ServerAMD.cs TestAMDI.cs

SLICE_SRCS	= $(SDIR)/Test.ice $(SDIR)/Forward.ice
SLICE_C_SRCS	= $(SDIR)/ClientPrivate.ice
SLICE_S_SRCS	= $(SDIR)/ServerPrivate.ice
SLICE_AMD_SRCS	= $(SDIR)/TestAMD.ice $(SDIR)/Forward.ice
SLICE_SAMD_SRCS	= $(SDIR)/ServerPrivateAMD.ice

SDIR		= .

GDIR		= generated

include $(top_srcdir)/config/Make.rules.cs

MCSFLAGS	:= $(MCSFLAGS) -target:exe

SLICE2CSFLAGS	:= $(SLICE2CSFLAGS) -I.

client.exe: $(C_SRCS) $(GEN_SRCS) $(CGEN_SRCS)
	$(MCS) $(MCSFLAGS) -out:$@ $(call ref,Ice) $(subst /,$(DSEP),$^)

server.exe: $(S_SRCS) $(GEN_SRCS) $(SGEN_SRCS)
	$(MCS) $(MCSFLAGS) -out:$@ $(call ref,Ice) $(subst /,$(DSEP),$^)

serveramd.exe: $(SAMD_SRCS) $(GEN_AMD_SRCS) $(SAMD_GEN_SRCS)
	$(MCS) $(MCSFLAGS) -out:$@ $(call ref,Ice) $(subst /,$(DSEP),$^)

include .depend

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

#include <IceUtil/Unicode.h>
#include <algorithm>

using namespace std;

string
IceUtil::wstringToString(const wstring& str)
{
    string result;
    result.reserve(str.length() * 2);

    for(unsigned int i = 0; i < str.length(); ++i)
    {
	wchar_t wc;
	wc = str[i];

	if(wc < 0x80)
	{
	    result += static_cast<char>(wc);
	}
	else if(wc < 0x800)
	{
	    result += 0xc0 | (wc>>6);
	    result += 0x80 | (wc & 0x3f);
	}
	else if(wc < 0x10000)
	{
	    result += 0xe0 | (wc>>12);
	    result += 0x80 | ((wc>>6) & 0x3f);
	    result += 0x80 | (wc & 0x3f);
	}
	else if(wc < 0x10FFFF)
	{
	    result += 0xf0 | (wc>>18);
	    result += 0x80 | ((wc>>12) & 0x3f);
	    result += 0x80 | ((wc>>6) & 0x3f);
	    result += 0x80 | (wc & 0x3f);
	}
	else
	{
	    return result; // Error, not encodable.
	}
    }

    return result;
}

wstring
IceUtil::stringToWstring(const string& str)
{
    wstring result;
    result.reserve(str.length());

    unsigned int len;
    for(unsigned int i = 0; i < str.length(); i += len)
    {
	unsigned char c = str[i];
	wchar_t wc;
	int minval;

	if(c < 0x80)
	{
	    wc = c;
	    len = 1;
	    minval = 0;
	}
	else if(c < 0xc0) // Lead byte must not be 10xxxxxx
	{
	    return result; // Error, not encodable.
	}
	else if(c < 0xe0) // 110xxxxx
	{
	    wc = c & 0x1f;
	    len = 2;
	    minval = 0x80;
	}
	else if(c < 0xf0) // 1110xxxx
	{
	    wc = c & 0xf;
	    len = 3;
	    minval = 0x800;
	}
#if SIZEOF_WCHAR_T >= 4
	else if(c < 0xf8) // 11110xxx
	{
	    wc = c & 7;
	    len = 4;
	    minval = 0x10000;
	}
	else if(c < 0xfc) // 111110xx
	{
	    // Length 5 and 6 is declared invalid in Unicode 3.1 and ISO 10646:2003.
	    wc = c & 3;
	    len = 5;
	    minval = 0x110000;
	}
	else if(c < 0xfe) // 1111110x
	{
	    // Length 5 and 6 is declared invalid in Unicode 3.1 and ISO 10646:2003.
	    wc = c & 1;
	    len = 6;
	    minval = 0x4000000;
	}
#endif
	else
	{
	    return result; // Error, not encodable.
	}

	if(i + len - 1 < str.length())
	{
	    for(unsigned int j = 1; j < len; ++j)
	    {
		if((str[i + j] & 0xc0) != 0x80) // All other bytes must be 10xxxxxx
		{
		    return result; // Error, not encodable.
		}
		
		wc <<= 6;
		wc |= str[i + j] & 0x3f;
	    }

	    if(wc < minval)
	    {
		return result; // Error, non-shortest form.
	    }
	    else
	    {
		result += wc;
	    }
	}
	else
	{
	    return result; // Error, not encodable.
	}
    }

    return result;
}

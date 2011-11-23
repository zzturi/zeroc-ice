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

#ifndef ICE_SSL_CERTIFICATE_DESC_H
#define ICE_SSL_CERTIFICATE_DESC_H

#include <IceUtil/Config.h>
#include <openssl/ssl.h>
#include <vector>

namespace IceSSL
{

class CertificateFile
{
public:

    CertificateFile();
    CertificateFile(const std::string&, const int);
    CertificateFile(const CertificateFile&);

    std::string getFileName() const;
    int getEncoding() const;

protected:

    std::string _fileName;
    int _encoding;
};

class DiffieHellmanParamsFile : public CertificateFile
{
public:

    DiffieHellmanParamsFile();
    DiffieHellmanParamsFile(const int, const std::string&, const int);
    DiffieHellmanParamsFile(const DiffieHellmanParamsFile&);

    int getKeySize() const;

protected:

    int _keySize;
};

class CertificateDesc
{
public:

    CertificateDesc();
    CertificateDesc(const int, const CertificateFile&, const CertificateFile&);
    CertificateDesc(const CertificateDesc&);

    int getKeySize() const;

    const CertificateFile& getPublic() const;
    const CertificateFile& getPrivate() const;

protected:

    int _keySize;
    CertificateFile _public;
    CertificateFile _private;
};

typedef std::vector<CertificateDesc> RSAVector;
typedef std::vector<CertificateDesc> DSAVector;
typedef std::vector<DiffieHellmanParamsFile> DHVector;

template<class Stream>
inline Stream& operator << (Stream& target, const CertificateFile& certFile)
{
    if(certFile.getEncoding() == SSL_FILETYPE_PEM)
    {
        target << "[PEM]: " << certFile.getFileName();
    }
    else if(certFile.getEncoding() == SSL_FILETYPE_ASN1)
    {
        target << "[ASN1]: " << certFile.getFileName();
    }

    return target;
}

template<class Stream>
inline Stream& operator << (Stream& target, const DiffieHellmanParamsFile& dhParams)
{
    if(dhParams.getKeySize() != 0)
    {
        target << "Keysize: " << dhParams.getKeySize() << "\n";
        target << "File:    ";
        IceSSL::operator<<(target, ((CertificateFile&)dhParams));
        target << "\n";
    }

    return target;
}

template<class Stream>
inline Stream& operator << (Stream& target, const CertificateDesc& certDesc)
{
    if(certDesc.getKeySize() != 0)
    {
        target << "Keysize: " << certDesc.getKeySize() << "\n";
        target << "Public:  ";
        IceSSL::operator<<(target,  certDesc.getPublic());
        target << "\n";
        target << "Private: ";
        IceSSL::operator<<(target, certDesc.getPrivate());
        target << "\n";
    }

    return target;
}

}

#endif

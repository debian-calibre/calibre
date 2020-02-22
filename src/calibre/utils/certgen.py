#!/usr/bin/env python2
# vim:fileencoding=utf-8
from __future__ import absolute_import, division, print_function, unicode_literals

__license__ = 'GPL v3'
__copyright__ = '2015, Kovid Goyal <kovid at kovidgoyal.net>'

import socket
#from calibre.constants import plugins
#from polyglot.builtins import unicode_type
from OpenSSL import crypto

#certgen, err = plugins['certgen']
#if err:
#    raise ImportError('Failed to load the certgen module with error: %s' % err)


def create_key_pair(size=2048):
    pkey = crypto.PKey()
    pkey.generate_key(crypto.TYPE_RSA, size)
    return pkey


def create_cert_request(
    key_pair, common_name,
    country='IN', state='Maharashtra', locality='Mumbai', organization=None,
    organizational_unit=None, email_address=None, alt_names=(), basic_constraints=None
):
    def enc(x):
        if isinstance(x, unicode_type):
            x = x.encode('ascii')
        return x or None

    req = crypto.X509Req()
    subj = req.get_subject()

    setattr(subj, "CN", common_name)
    setattr(subj, "C", country)
    setattr(subj, "ST", state)
    setattr(subj, "L", locality)
    #setattr(subj, "O", organization)
    #setattr(subj, "OU", organizational_unit)
    #setattr(subj, "emailAddress", email_address)

    req.set_pubkey(key_pair)
    req.sign(key_pair, "sha256")

    return req

def create_cert(req, ca_cert, ca_keypair, expire=365, not_before=0):
    cert = crypto.X509()
    cert.set_serial_number(0)
    cert.gmtime_adj_notBefore(not_before)
    cert.gmtime_adj_notAfter((60 * 60 * 24) * expire)
    cert.set_issuer(ca_cert.get_subject())
    cert.set_subject(req.get_subject())
    cert.set_pubkey(req.get_pubkey())

    cert.sign(ca_keypair, "sha256")
    return cert


def create_ca_cert(req, ca_keypair, expire=365, not_before=0):
    cert = crypto.X509()
    cert.set_serial_number(0)
    cert.gmtime_adj_notBefore(not_before)
    cert.gmtime_adj_notAfter((60 * 60 * 24) * expire)
    cert.set_issuer(req.get_subject())
    cert.set_subject(req.get_subject())
    cert.set_pubkey(req.get_pubkey())

    cert.sign(ca_keypair, "sha256")
    return cert


def serialize_cert(cert):
    return certgen.serialize_cert(cert)


def serialize_key(key_pair, password=None):
    return certgen.serialize_rsa_key(key_pair, password)


def cert_info(cert):
    return crypto.dump_certificate(crypto.FILETYPE_PEM, cert).decode('utf-8')


def create_server_cert(
    domain_or_ip, ca_cert_file=None, server_cert_file=None, server_key_file=None,
    expire=365, ca_key_file=None, ca_name='Dummy Certificate Authority', key_size=2048,
    country='IN', state='Maharashtra', locality='Mumbai', organization=None,
    organizational_unit=None, email_address=None, alt_names=(), encrypt_key_with_password=None,
):
    is_ip = False
    try:
        socket.inet_pton(socket.AF_INET, domain_or_ip)
        is_ip = True
    except Exception:
        try:
            socket.inet_aton(socket.AF_INET6, domain_or_ip)
            is_ip = True
        except Exception:
            pass
    if not alt_names:
        prefix = 'IP' if is_ip else 'DNS'
        alt_names = ('{}:{}'.format(prefix, domain_or_ip),)

    # Create the Certificate Authority
    cakey = create_key_pair(key_size)
    careq = create_cert_request(cakey, ca_name, basic_constraints='CA:TRUE')
    cacert = create_ca_cert(careq, cakey)

    # Create the server certificate issued by the newly created CA
    pkey = create_key_pair(key_size)
    req = create_cert_request(pkey, domain_or_ip, country, state, locality, organization, organizational_unit, email_address, alt_names)
    cert = create_cert(req, cacert, cakey, expire=expire)

    def export(dest, obj, func, *args):
        if dest is not None:
            data = func(obj, *args)
            if isinstance(data, unicode_type):
                data = data.encode('utf-8')
            if hasattr(dest, 'write'):
                dest.write(data)
            else:
                with open(dest, 'wb') as f:
                    f.write(data)
    export(ca_cert_file, cacert, serialize_cert)
    export(server_cert_file, cert, serialize_cert)
    export(server_key_file, pkey, serialize_key, encrypt_key_with_password)
    export(ca_key_file, cakey, serialize_key, encrypt_key_with_password)
    return cacert, cakey, cert, pkey


if __name__ == '__main__':
    cacert, cakey, cert, pkey = create_server_cert('test.me', alt_names=['1.test.me', '*.all.test.me'])
    print("CA Certificate")
    print(cert_info(cacert).encode('utf-8'))
    print(), print(), print()
    print('Server Certificate')
    print(cert_info(cert).encode('utf-8'))

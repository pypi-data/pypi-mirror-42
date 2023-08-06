"""
Ax_Handoff Utility functions.

This module is not intended for public use.

------------------------------------------------------------------------------
Author: Dan Kamins <dos at axonchisel dot net>
Copyright (c) 2011 Dan Kamins, AxonChisel.net
"""


# ----------------------------------------------------------------------------


from base64 import b64encode, b64decode
import re


# ----------------------------------------------------------------------------


#
# Internal Utility Functions
#


def rpad_string(s, block_size=16, pad_char='\0'):
    """Return right-padded version of string with length as multiple of block size."""
    mod = len(s) % block_size
    return s if not mod else (s + (block_size - mod) * pad_char)


def rpad_bytes_crypto(b, block_size=16):
    """
    Return special right-padded version of bytes with length as multiple of block size.
    Padding is ALWAYS applied even if already block size multiple.
    Padding is single byte repeated indicating number of padding bytes 
    (0x01 - 0x10 for block size 16).
    Based on recommendation from RFC 3852, PKCS #5, PKCS #7.
    """
    if block_size > 255:
        raise ValueError("Block size {0} too large (>255)".format(block_size))
    padcnt = block_size - len(b) % block_size
    pad_byte = bytes([padcnt])
    return b + pad_byte * padcnt


def unrpad_bytes_crypto(b, block_size=16):
    """
    Undo rpad_bytes_crypto and return unpadded version of bytes.
    Removes trailing pad bytes as applied by rpad_bytes_crypto.
    """
    if len(b) < block_size:
        raise ValueError("Data ({0}) shorter than block size ({1})".format(len(b), block_size))
    padcnt = b[-1]
    if padcnt > block_size:
        raise ValueError("Detected pad count ({0}) larger than block size ({1})".format(padcnt, block_size))
    if padcnt == 0:
        raise ValueError("Detected pad count ({0}) must be gt 0".format(padcnt))
    pad_byte = padcnt
    for p in range(padcnt):
        if b[-p-1] != pad_byte:
            raise ValueError("Padding contains invalid byte '{0}' when expecting '{1}'".format(repr(b[-p]), repr(pad_char)))
    return b[:-p-1]


def pretty_bytes(bstr):
    """Return interpretation of bytes suitable for printing/logging."""
    return "[{len}] {repr}".format(len=len(bstr), repr=repr(bstr))


def ub64encode(bstr):
    """Return 'base64url' encoding (URL-safe) str of bytes."""
    bstr2 = b64encode(bstr).rstrip(b'=').replace(b'+',b'-').replace(b'/',b'_')
    return bstr2.decode('utf-8')


def ub64decode(estr):
    """Return decoded bytes from 'base64url' encoded (URL-safe) str."""
    estr = estr.replace('-','+').replace('_','/')
    estr = rpad_string(estr, 4, '=')
    if not re.match('^[A-Za-z0-9+/]*={0,2}$', estr):
        raise ValueError("ub64decode str contains invalid chars")
    return b64decode(estr)
    

#!/usr/bin/env python3

"""Decode an input string for N number of encodings. Decoding criteria can be specified in arbitrary order."""

from io import StringIO
from urllib.parse import unquote
import argparse
import base64
import functools
import gzip
import sys
import zipfile


# from https://mathieularose.com/function-composition-in-python/
def compose(*functions):
    def compose2(f, g):
        return lambda x: f(g(x))
    return functools.reduce(compose2, functions, lambda x: x)


def base64_decode(string):
    return base64.b64decode(string)


def zipfile_decode(string):
    decoded_string = ''
    fp = StringIO(string)
    zfp = zipfile.ZipFile(fp, 'r')
    for name in zfp.namelist():
        with zfp.open(name) as m:
            decoded_string += m.read()
    return decoded_string


def gzip_decode(string):
    fp = StringIO(string)
    f = gzip.GzipFile(fileobj=fp)
    return f.read()


def url_decode(string):
  return unquote(string)


decoding_methods = {
    'b64': base64_decode,
    'gz': gzip_decode,
    'z': zipfile_decode,
    'u': url_decode,
}


def decode_string(encoded_string, decoding_args):
    functions = reversed(list(map(lambda x: decoding_methods[x], decoding_args)))
    decoding_function = compose(*functions)

    return decoding_function(encoded_string)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Base64 encode/decode a string\nPossible decoding methods:\n-b\tBase 64\n-z\tZipped")
    parser.add_argument('-s', '--string', help='string to decode')
    parser.add_argument('-f', '--filename', help='file to decode')
    parser.add_argument('decoding_methods', help='Decoding methods. Executed from left to right', nargs='+')

    args = parser.parse_args()

    encoded_string = None
    if args.string:
        encoded_string = args.string
    elif args.filename:
        with open(args.filename, 'r') as f:
            encoded_string = f.read()
    else:
        print('Either --string or --filename is required.')
        sys.exit()

    print(decode_string(encoded_string, args.decoding_methods))

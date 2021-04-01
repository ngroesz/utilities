"""Decode an input string. Decoding criteria can be specified in arbitrary order."""

import sys
import base64
import argparse
from cStringIO import StringIO
import zipfile

import functools

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

decoding_methods = {
    'b': base64_decode,
    'z': zipfile_decode,
}

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = "Base64 encode/decode a string\nPossible decoding methods:\n-b\tBase 64\n-z\tZipped")
    parser.add_argument('-s', '--string', help='string to decode')
    parser.add_argument('-f', '--filename', help='file to decode')
    parser.add_argument('decoding_methods', help='Decoding methods. Executed from left to right', nargs='+')

    args = parser.parse_args()

    string = None
    if args.string:
        string = args.string
    elif args.filename:
        with open(args.filename, 'r') as f:
            string = f.readlines()
    else:
        print('Either --string or --filename is required.')
        sys.exit()

    functions = list(reversed(map(lambda x: decoding_methods[x], args.decoding_methods)))

    decoding_function = compose(*functions)

    print(decoding_function(string))

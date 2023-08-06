#!/user/bin/env python
"""
This utility helps create OAuth2 key file from OAuth2 client id file

(c) dlancer, 2019

"""

import argparse
import sys

from oauth2client import tools
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage


def main():
    parser = argparse.ArgumentParser(parents=[tools.argparser])
    parser.add_argument('--scope', required=True, default=None, help='path to file with required google api scopes')
    parser.add_argument('--source', required=True, default=None, help='path to source oath2 client id file')
    parser.add_argument('--destination', required=True, default=None, help='path to destination oath2 client key file')
    flags = parser.parse_args()

    try:
        infile = open(flags.scope)
        scopes = infile.readlines()
        scopes = [scope.strip(' \r\n') for scope in scopes]
    except IOError:
        sys.exit('file with required scopes missed')

    print(type(scopes), scopes)

    flow = flow_from_clientsecrets(flags.source, scope=scopes)
    storage = Storage(flags.destination)
    tools.run_flow(flow, storage, flags)


if __name__ == '__main__':
    main()

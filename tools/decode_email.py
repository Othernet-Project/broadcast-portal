#!/usr/bin/env python

import sys
import base64


def main():
    message = sys.argv[1]
    message = ''.join(l.strip() for l in message.split())
    print(base64.b64decode(message))

if __name__ == '__main__':
    main()

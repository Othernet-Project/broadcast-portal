import gevent.monkey
gevent.monkey.patch_all(aggressive=True)

import os

from util.application import Application

PKGDIR = os.path.dirname(__file__)
CONF = os.path.join(PKGDIR, 'broadcast.ini')


def start(config):
    app = Application(config=config, root=PKGDIR)
    app.start()


def main():
    import argparse

    parser = argparse.ArgumentParser('Broadcast portal server')
    parser.add_argument('--conf', '-c', help='alternative configuration path',
                        default=CONF)
    args = parser.parse_args()
    start(args.conf)


if __name__ == '__main__':
    main()

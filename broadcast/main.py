import gevent.monkey
gevent.monkey.patch_all(aggressive=True)

# For more details on the below see: http://bit.ly/18fP1uo
import gevent.hub
gevent.hub.Hub.NOT_ERROR = (Exception,)

import os

from broadcast.app.application import Application


PKGDIR = os.path.dirname(__file__)
CONF = os.path.join(PKGDIR, 'broadcast.ini')


def start(config, args):
    app = Application(config=config, args=args, root=PKGDIR)
    app.start()


def main():
    import argparse

    parser = argparse.ArgumentParser('Broadcast portal server')
    parser.add_argument('--conf', '-c', help='alternative configuration path',
                        default=CONF)
    parser.add_argument('--su', action='store_true', help='create superuser')
    parser.add_argument('--assets', action='store_true', help='rebuild assets')
    args = parser.parse_args()
    start(args.conf, args)


if __name__ == '__main__':
    main()

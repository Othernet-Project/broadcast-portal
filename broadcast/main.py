######## MONKEY PATCHES ########

import gevent.monkey
gevent.monkey.patch_all(aggressive=True)

# For more details on the below see: http://bit.ly/18fP1uo
import gevent.hub
gevent.hub.Hub.NOT_ERROR = (Exception,)

import shutilwhich

######## NORMAL IMPORTS ########

import os

from broadcast.app.application import Application


PKGDIR = os.path.dirname(__file__)


def main():
    Application(root=PKGDIR).start()


if __name__ == '__main__':
    main()

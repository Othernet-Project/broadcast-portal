import datetime

from greentasks import Task

from ..app.exts import container as exts
from ..models.bins import Bin
from ..models.items import ContentItem


class BinPackagerTask(Task):
    """
    Find the currently active / open bin instance, keep adding the best item
    candidates to it as long as the bin is either filled or all the good
    candidates are consumed, close the bin and open a new one in place of it.
    """
    name = 'bins'
    periodic = True

    def get_start_delay(self):
        return exts.config['bins.check_interval']

    def get_delay(self, previous_delay):
        return exts.config['bins.check_interval']

    def run(self):
        # get the currently open bin
        instance = Bin.current()
        # check if it's now or past closing time
        lifetime = exts.config['bin.lifetime']
        closing = instance.created + datetime.timedelta(seconds=lifetime)
        if datetime.datetime.utcnow() < closing:
            # it is not yet bin closing time, come back later
            return
        # bin is ready to be closed, add best candidates to it and wrap it up
        for item in ContentItem.binless_items(kind=ContentItem.CANDIDATES):
            try:
                instance.add(item)
            except Bin.NotEnoughSpace:
                # bin is full, finalize and upload
                break
        # close the old bin
        instance.close()
        # open new bin in place of the old one
        Bin.new(config=exts.config)

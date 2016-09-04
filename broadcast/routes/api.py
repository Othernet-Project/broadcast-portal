from ..models.bins import Bin
from ..models.items import ContentItem
from ..app.exts import container as exts
from ..util.routes import APIMixin, JsonRoute, StaticRoute


# API version 1


class FinalizeBin(APIMixin, JsonRoute):
    """
    Retrieve bin list and finalize current bin.

    - ``GET /api/v1/bins/``
    - ``POST /api/v1/bins/``

    The ``GET`` request responds with the following structure::

        [
            {
                "id": bin_id,
                "created": bin_timestamp
            },
            ...
        ]

    The ``POST`` request does not require any input, and responds with::

        {
            "id": bin_id,
            "created": bin_timestamp,
            "size": bin_size,
            "count": file_count
        }

    When creating a new bin, if there are no candidates, server responds with
    404.
    """

    path = '/api/v1/bins/'

    def get(self):
        return [{
            'id': b.id,
            'created': b.created
        } for b in Bin.list()]

    def post(self):
        bin = Bin.new()
        if not bin:
            self.abort(404)
        return bin.to_dict()


class BinItems(APIMixin, JsonRoute):
    """
    Retrieve infomation for specific bin or last created bin.

    - ``GET /api/v1/bins/<BIN_ID>``
    - ``GET /api/v1/bins/last``

    Return data is in the following format::

        {
            "id": bin_id,
            "created": bin_timestamp,
            "size": bin_size,
            "count": number_of_items,
            "items": [
                {
                    "id": item_id,
                    "created": item_teimstamp,
                    "size": file_size,
                    "votes": vote_count,
                    "category": category,
                    "filename": item_filename
                },
                ...
            ]
        }

    """

    path = '/api/v1/bins/<bin_id:re:([0-9a-f]{32}|last)>'

    @staticmethod
    def item_to_dict(item):
        """
        Remove useless info and add info that is only available as properties
        """
        d = item.to_dict()
        d.pop('username')
        d.pop('email')
        d.pop('ipaddr')
        d.pop('path')
        d.pop('bin')
        d['filename'] = item.filename
        return d

    def get(self, bin_id):
        try:
            if bin_id == 'last':
                bin = Bin.last()
            else:
                bin = Bin.get(bin_id)
        except Bin.NotFound:
            self.abort(404)
        data = bin.to_dict()
        data['items'] = [self.item_to_dict(i) for i in bin.items]
        return data


class BinFile(APIMixin, StaticRoute):
    """
    Retrieve content file.

    - ``GET /api/v1/download/<ITEM_ID>``

    This endpoint returns the file data as is. The file name is returned
    in the ``Content-Dispoition`` header.
    """

    path = '/api/v1/download/<item_id:re:[0-9a-f]{32}>'
    force_download = True

    def get_base_dirs(self):
        return [exts.config['content.upload_root']]

    def get(self, item_id):
        try:
            item = ContentItem.get(item_id)
        except ContentItem.NotFound:
            self.abort(404)
        return self.create_file_response(item.path)


def route():
    return (FinalizeBin, BinItems, BinFile)

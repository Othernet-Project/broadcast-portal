import os

from ..util.basemodel import Model


class BaseItem(Model):
    PROCESSING = 'PROCESSING'
    ACCEPTED = 'ACCEPTED'
    REJECTED = 'REJECTED'

    order = ['date(created)']

    def accept(self):
        return self.update(status=self.ACCEPTED)

    def reject(self):
        return self.update(status=self.REJECTED)

    @property
    def is_accepted(self):
        return self.status == self.ACCEPTED

    @property
    def is_rejected(self):
        return self.status == self.REJECTED

    @property
    def type(self):
        return self.table


class ContentItem(BaseItem):
    database = 'main'
    table = 'content'
    columns = (
        'id',
        'created',
        'email',
        'path',
        'size',
        'title',
        'license',
        'language',
        'notified',
        'status',
        'url',
        'bin',
    )
    pk_field = 'id'

    @property
    def filename(self):
        return os.path.basename(self.path)

    def save_file(self, file_object, upload_root):
        # make sure folder with id exists
        upload_dir = os.path.join(upload_root, self.id)
        if not os.path.exists(upload_dir):
            os.makedirs(upload_dir)

        upload_path = os.path.join(upload_dir, file_object.filename)
        if os.path.exists(upload_path):
            # remove file if already exists
            os.remove(upload_path)

        file_object.save(upload_path)
        return self.update(path=os.path.relpath(upload_path, upload_root))


class TwitterItem(BaseItem):
    database = 'main'
    table = 'twitter'
    columns = (
        'id',
        'created',
        'email',
        'handle',
        'notified',
        'status',
    )
    pk_field = 'id'


"""
broadcast.py: Manage content entries

Copyright 2014-2015, Outernet Inc.
Some rights reserved.

This software is free software licensed under the terms of GPLv3. See COPYING
file that comes with the source code, or http://www.gnu.org/licenses/gpl.txt.
"""

import datetime
import hmac
import hashlib
import os
import uuid

from bottle import request


def get_content_id():
    return uuid.uuid4().hex


def sign(data, secret_key):
    return hmac.new(secret_key, data, hashlib.sha256).hexdigest()


def get_content_by_url(url):
    db = request.db.sessions
    query = db.Select(sets='content', where='url = :url')
    db.query(query, url=url)
    return db.result


def save_upload(content_id, uploaded_file, upload_root=None):
    file_path = os.path.join(content_id, uploaded_file.filename)
    upload_root = upload_root or request.app.config['content.upload_root']
    upload_path = os.path.join(upload_root, file_path)
    # make sure folder with content_id exists
    os.makedirs(os.path.dirname(upload_path))
    uploaded_file.save(upload_path)
    return file_path


def save_content(content_id, email, name, file_path, title, license, url,
                 is_priority=False, db=None):
    content = {'content_id': content_id,
               'email': email,
               'name': name,
               'file_path': file_path,
               'title': title,
               'license': license,
               'url': url,
               'created': datetime.datetime.utcnow(),
               'is_priority': is_priority}
    db = db or request.db.main
    query = db.Insert('content', cols=content.keys())
    db.execute(query, content)

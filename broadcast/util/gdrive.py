import functools
import json
import os

import apiclient.discovery
import apiclient.http

from httplib2 import Http
from oauth2client.client import SignedJwtAssertionCredentials


class DriveClient(object):
    SCOPE = 'https://www.googleapis.com/auth/drive'

    def protect(func):
        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            if self._service is None:
                raise RuntimeError("Call `start` before invoking this method.")
            return func(self, *args, **kwargs)
        return wrapper

    def __init__(self, auth_data_path, owner_email):
        with open(auth_data_path) as auth_data_file:
            self._auth_data = json.load(auth_data_file)

        self._permission = {'type': 'user',
                            'role': 'writer',
                            'value': owner_email}
        self._service = None

    def _authenticate(self):
        creds = SignedJwtAssertionCredentials(self._auth_data['client_email'],
                                              self._auth_data['private_key'],
                                              self.SCOPE)
        return creds.authorize(Http())

    def _build_service(self):
        http_auth = self._authenticate()
        return apiclient.discovery.build('drive', 'v2', http=http_auth)

    def start(self):
        self._service = self._build_service()

    @protect
    def upload(self, file_path):
        media_body = apiclient.http.MediaFileUpload(file_path, resumable=True)
        body = {'title': os.path.basename(file_path)}
        file_data = (self._service.files()
                                  .insert(body=body, media_body=media_body)
                                  .execute())
        (self._service.permissions()
                      .insert(fileId=file_data['id'], body=self._permission)
                      .execute())
        return file_data


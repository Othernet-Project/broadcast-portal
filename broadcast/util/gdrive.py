import json
import os

import apiclient.discovery
import apiclient.http

from httplib2 import Http
from oauth2client.client import SignedJwtAssertionCredentials


class DriveClient(object):
    SCOPE = 'https://www.googleapis.com/auth/drive'

    def __init__(self, auth_data_path, owner_email=None):
        with open(auth_data_path) as auth_data_file:
            self._auth_data = json.load(auth_data_file)

        self._permission = {'type': 'user',
                            'role': 'writer',
                            'value': owner_email} if owner_email else None
        self._service = self._build_service()

    def _authenticate(self):
        creds = SignedJwtAssertionCredentials(self._auth_data['client_email'],
                                              self._auth_data['private_key'],
                                              self.SCOPE)
        return creds.authorize(Http())

    def _build_service(self):
        http_auth = self._authenticate()
        return apiclient.discovery.build('drive', 'v2', http=http_auth)

    def _set_permission(self, file_id):
        (self._service.permissions()
             .insert(fileId=file_id, body=self._permission)
             .execute())

    def _upload(self, body, media_body=None, parent_id=None):
        if parent_id:
            body['parents'] = [{'id': parent_id}]

        file_data = (self._service.files()
                                  .insert(body=body, media_body=media_body)
                                  .execute())
        if self._permission:
            self._set_permission(file_data['id'])

        return file_data

    def upload(self, file_path, parent_id=None):
        media_body = apiclient.http.MediaFileUpload(file_path, resumable=True)
        body = {'title': os.path.basename(file_path)}
        return self._upload(body, media_body=media_body, parent_id=parent_id)

    def touch(self, title, mime_type, parent_id=None):
        body = {'title': title, 'mimeType': mime_type}
        return self._upload(body, parent_id=parent_id)


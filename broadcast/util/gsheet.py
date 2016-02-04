import functools
import json

import gspread

from oauth2client.client import SignedJwtAssertionCredentials


class SheetClient(object):
    SCOPE = 'https://spreadsheets.google.com/feeds'

    def protect(func):
        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            if self._service is None:
                raise RuntimeError("Call `start` before invoking this method.")
            return func(self, *args, **kwargs)
        return wrapper

    def __init__(self, auth_data_path):
        with open(auth_data_path) as auth_data_file:
            self._auth_data = json.load(auth_data_file)

        self._service = None

    def _build_service(self):
        creds = SignedJwtAssertionCredentials(self._auth_data['client_email'],
                                              self._auth_data['private_key'],
                                              self.SCOPE)
        return gspread.authorize(creds)

    def start(self):
        self._service = self._build_service()

    @protect
    def insert(self, spreadsheet_id, worksheet_index, values):
        spreadsheet = self._service.open_by_key(spreadsheet_id)
        worksheet = spreadsheet.get_worksheet(worksheet_index)
        worksheet.append_row(values)


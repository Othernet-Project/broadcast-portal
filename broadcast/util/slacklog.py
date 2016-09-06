import json
import logging

try:
    from urllib.request import urlopen, Request
except ImportError:
    from urllib2 import urlopen, Request


class Slack:
    """
    Build and send requests towards a slack incoming webhook endpoint
    specified by ``url``, targeted at ``channel``.
    """
    default_headers = {'content-type': 'application/json'}

    def __init__(self, url, channel=None):
        self.url = url
        self.channel = channel

    def build_request(self, payload, headers=None, encoding='utf8'):
        data = json.dumps(payload).encode(encoding)
        headers = headers or self.default_headers
        return Request(self.url, data=data, headers=headers)

    def send_message(self, text):
        payload = {'text': text}
        if self.channel:
            payload['channel'] = self.channel
        req = self.build_request(payload)
        try:
            return urlopen(req)
        except Exception:
            pass


class SlackLog(logging.StreamHandler):
    """
    Standard python stream log handler which outputs it's messages to slack.
    """
    def __init__(self, url, channel=None, level=logging.NOTSET):
        super(SlackLog, self).__init__()
        self.level = level
        self.slack = Slack(url, channel)

    def flush(self):
        """
        No flushing is necessary since messages are sent out immediately as
        they come in.
        """
        pass

    def emit(self, record):
        if record.levelno < self.level:
            return
        try:
            msg = self.format(record)
            self.slack.send_message(msg)
        except Exception:
            self.handleError(record)

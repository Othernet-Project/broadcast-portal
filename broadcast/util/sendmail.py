"""
email.py: Wrapper for sending email messages

Copyright 2014 Outernet Inc <hello@outernet.is>
All rights reserved.

No part of this code can be used or distributed with or without modifications
without express written permission.
"""

from __future__ import unicode_literals, print_function

import smtplib
import logging
from email.mime.text import MIMEText

try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse

from bottle import request, mako_template as template


def send_multiple(to_list, subject, text=None, data={},
                  is_async=False, config=None):
    """
    Sends out text/HTML email with specified templates

    `to_list` is a list of tuples containing an email and a name. This
    is historical from BD (Before Docstrings). `subject` is a single line
    string used as the subject of the message. `text` is a string that
    specifies what template to use in combination with the data. It is named
    `text` and a keyword argument for historical reasons. `data` is a dict that
    is passed to the template to create the message. `config` is an initialized
    config object (see main module) if not provided, the call must be part of a
    request context.
    """
    # As described in the docstring, you must provide a template
    if text is None:
        with ValueError('no template specified') as ex:
            logging.exception('Error sending email: %s' % ex)
        return None

    # Because this is a bottle app we can get the config through request
    # context
    conf = config or request.app.config

    # Prepare host_url for emails that offer links
    url = request.url if config is None else conf.get('app.url', '')
    parsed = urlparse(url)
    data['protocol'] = parsed.scheme
    data['host'] = parsed.netloc
    data['host_url'] = parsed.scheme + '://' + parsed.netloc

    # Obtain the SMTP info
    server = conf['smtp.server']
    port = conf['smtp.port']
    user = conf['smtp.user']
    pwd = conf['smtp.pass']

    # Process the data with the chosen template
    message = template(text, **data)

    # Construct message object
    msg = MIMEText(message, 'plain', 'utf-8')
    msg['subject'] = subject
    msg['from'] = user
    # As described in the docstring, we only use the first item in whatever
    # objects make up the to_list. This is historical, BD (Before Docstrings).
    msg['to'] = ', '.join([e[0] for e in to_list])

    # For more information on how preamble is used, see
    # https://docs.python.org/2/library/email.message.html#email.message.Message.preamble
    msg.preamble = subject + '\n'

    if not server:
        # SMTP is not configured, so log the message that would be sent and
        # quit.
        logging.debug('SMTP server not configured. Would send message:\n%s',
                      msg.as_string())
        return

    # Open SMTP connection
    smtp = smtplib.SMTP('{}:{}'.format(server, port))
    smtp.starttls()  # Calls `ehlo` if it hasn't been already
    # Calls `ehlo` if it needs to be, which it does because starttls was called
    smtp.login(user, pwd)
    try:
        smtp.sendmail(msg['from'], msg['to'], msg.as_string())
    except Exception as e:
        logging.exception('Error sending email: %s' % e)
    else:
        logging.debug("Sent message to %s" % msg['to'])
    finally:
        smtp.quit()


def send_mail(to, subject, text=None, data={}, is_async=False, config=None):
    """
    Create a single message with send_multiple. For detailed usage, see that.

    `to` is a string, an email address to send to. `subject` is a string, and
    will be the subject of the email. `text` is a string that specifies a
    template to use for the email. `is_async` is kept for historical reasons,
    but does not do anything. `config` is either a Config object or None. If
    None, the Config object is retrieved from the request context.
    """
    return send_multiple(
        [(to, '')], subject, text, data, is_async, config)

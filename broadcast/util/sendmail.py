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

from bottle import request

from ..util.template import render
from ..app.exts import container as exts


def send_multiple(to_list, subject, template=None, data={}):
    """
    Sends out text/HTML email with specified templates

    ``to_list`` is a list of tuples containing an email and a name. This is
    historical from BD (Before Docstrings). ``subject`` is a single line string
    used as the subject of the message. ``template`` is a the name of the
    template to use in combination with the data. ``data`` is a dict that is
    passed to the template to create the message. ``config`` is an initialized
    config object (see main module) if not provided, the call must be part of a
    request context.
    """
    # Because this is a bottle app we can get the config through request
    # context
    conf = exts.config

    # Prepare host_url for emails that offer links
    parts = request.urlparts
    data['protocol'] = parts.scheme
    data['host'] = parts.netloc
    data['host_url'] = parts.scheme + '://' + parts.netloc

    # Obtain the SMTP info
    server = conf['smtp.server']
    port = conf['smtp.port']
    user = conf['smtp.user']
    pwd = conf['smtp.pass']

    # Process the data with the chosen template
    message = render(template, data)

    # Construct message object
    msg = MIMEText(message, 'plain', 'utf-8')
    msg['subject'] = subject
    msg['from'] = conf.get('smtp.sender', user)
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


def send_mail(to, subject, template=None, data={}):
    """
    Create a single message with send_multiple. For detailed usage, see that.
    Arguments are the same as for ``send_multiple()`` except that ``to`` is a
    single email address.
    """
    return send_multiple([(to, '')], subject, template, data)

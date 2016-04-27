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
from email.mime.multipart import MIMEMultipart

from bottle import request, template


def send_multiple(to_list, subject, text=None, data={},
                  is_async=False, config=None):
    """
    Sends out text/HTML email with specified templates

    `to_list` is a list of tuples containing an email and a name. This
    is historical from BD (Before Docstrings). `subject` is a single line
    string used as the subject of the message. `text` is a string that
    specifies what template to use in combination with the data. It is a
    keyword argument for historical reasons. `data` is a dict that is passed to
    the template to create the message. `config` is an initialized config
    object (see main module) if not provided, the call must be part of a
    request context.
    """
    if text is None:
        with Exception('no template specified') as ex:
            logging.exception('Error sending email: %s' % ex)
        return None
    conf = config or request.app.config

    # Construct message object
    msg = MIMEMultipart()
    msg['subject'] = subject
    msg['from'] = conf['smtp.user']
    msg['to'] = ', '.join([e[0] for e in to_list])
    msg.preamble = subject + '\n'

    message = ''.join(template(text, **data))
    plain = MIMEText(message, 'plain', 'utf-8')
    msg.attach(plain)
    logging.debug("Prepared message")

    # Open SMTP connection
    smtp = smtplib.SMTP('%s:%s' % (conf['smtp.server'], conf['smtp.port']))
    smtp.starttls()
    smtp.login(conf['smtp.user'], conf['smtp.pass'])
    try:  # Try to send the message
        smtp.sendmail(msg['from'], msg['to'], msg.as_string())
        smtp.quit()
        return
    except Exception as e:
        smtp.quit()
        logging.exception('Error sending email: %s' % e)
        return None


def send_mail(to, subject, text=None, html=None, to_name='',
              data={}, mandrill_args={'preserve_recipients': False},
              use_template=None, is_async=False, config=None):
    """ Send out text/HTML email with specified templates """
    return send_multiple([(to, to_name)], subject, text, html, data,
                         mandrill_args, use_template, is_async, config)

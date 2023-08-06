# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, division, unicode_literals
import os
import six
import logging
from django.core.files.base import ContentFile
from django.template import Context, Template
from post_office import mail
from post_office.utils import get_email_template
from post_office.mail import send, send_queued

from exchangelib import (
    Account,
    Message,
    Mailbox,
    Configuration,
    Credentials,
    HTMLBody,
    Body,
    FileAttachment,
)
from exchangelib.credentials import (
    IMPERSONATION,
    DELEGATE,
)
from exchangelib.transport import (
    NTLM,
    BASIC,
    DIGEST,
    GSSAPI,
)
from exchangelib.version import (
    Version,
    Build,
    EXCHANGE_2007,
    EXCHANGE_2007_SP1,
    EXCHANGE_2010,
    EXCHANGE_2010_SP1,
    EXCHANGE_2010_SP2,
    EXCHANGE_2013,
    EXCHANGE_2013_SP1,
    EXCHANGE_2016,
)

__all__ = [
    "send_exchange_mail",
    "send_exchange_template_mail",
    "send",
    "send_queued",
    "send_mail",
    "send_mail_template",
    "send_mail_message",
    "send_mail_queued",
]

logger = logging.getLogger(__name__)


def create_file_attackments(attachment_files):
    attachments = []
    for filepath in attachment_files.items():
        if not os.path.isfile(filepath):
            continue
        name = os.path.basename(filepath)
        content = ContentFile(open(filepath).read())
        attachments.append(FileAttachment(name=name, content=content))
    return attachments


def create_attachments(attachment_files):
    attachments = []
    attachment_files = dict([(name, content) for name, content, _ in attachment_files])
    for filename, content in attachment_files.items():
        attachment = FileAttachment(name=filename, content=content)
        attachments.append(attachment)
    return attachments


def send_exchange_mail(recipients, subject, message=None, html_message=None,
                       from_email=None, reply_to=None, cc=None, bcc=None, attachments=None,
                       username="", password="", host="", smtp_addr="", fullname=None,
                       autodiscover=False, use_ssl=True, service_endpoint=None,
                       access_type=DELEGATE, auth_type=None, version=None):
    """
    用exchangelib发送exchange邮件
    :param recipients:
    :param subject:
    :param message:
    :param html_message:
    :param from_email:
    :param reply_to:
    :param cc:
    :param bcc:
    :param attachments:
    :param username:
    :param password:
    :param host:
    :param smtp_addr:
    :param fullname:
    :param autodiscover:
    :param use_ssl:
    :param service_endpoint:
    :param access_type:
    :param auth_type:
    :param version:

    :return:
    """
    credentials = Credentials(
        username=username,
        password=password
    )
    config = Configuration(
        credentials=credentials,
        server=host,
        has_ssl=use_ssl,
        service_endpoint=service_endpoint,
        auth_type=auth_type,
        version=version,
    )
    account = Account(
        primary_smtp_address=smtp_addr,
        fullname=fullname,
        access_type=access_type,
        credentials=credentials,
        autodiscover=autodiscover,
        config=None if autodiscover else config,
    )
    recipients = ([recipients] if isinstance(recipients, six.string_types) else recipients) or []
    cc = ([cc] if isinstance(cc, six.string_types) else cc) or []
    bcc = ([bcc] if isinstance(cc, six.string_types) else bcc) or []
    attachments = ([attachments] if isinstance(attachments, six.string_types) else attachments) or []

    sender = Mailbox(email_address=from_email)
    to_recipients = [Mailbox(email_address=recipient) for recipient in recipients]
    cc_recipients = [Mailbox(email_address=recipient) for recipient in cc]
    bcc_recipients = [Mailbox(email_address=recipient) for recipient in bcc]
    body = HTMLBody(html_message) if html_message else Body(message)
    # text_body = Body(message)
    attachments = create_file_attackments(attachments)

    kwargs = dict(
        account=account,
        # folder=account.sent,
        # headers=headers,
        subject=subject,
        # text_body=text_body,
        body=body,
        sender=sender,
        to_recipients=to_recipients,
        cc_recipients=cc_recipients,
        bcc_recipients=bcc_recipients,
    )
    if reply_to:
        kwargs["reply_to"] = Mailbox(email_address=reply_to)
    message = Message(**kwargs)
    if attachments:
        message.attach(attachments)
    re = message.send(save_copy=False)
    return re


def send_exchange_template_mail(recipients, template, context, language="en", sender=None, username="", password="", host="", smtp_addr=""):
    """
    用exchangelib发送post_office中的模板邮件
    :param recipients:
    :param template:
    :param context:
    :param language:
    :param sender:
    :param username:
    :param password:
    :param host:
    :param smtp_addr:
    :return:
    """
    if not context:
        logger.error("send_exchange_template_mail context empty")
        return False

    template_context = Context(context)
    email_template = get_email_template(template, language)
    subject = Template(email_template.subject).render(template_context)
    html_message = Template(email_template.html_content).render(template_context)
    return send_exchange_mail(recipients, subject, None, html_message, sender, username, password, host, smtp_addr)


def send_mail(recipients=None, sender=None, template=None, context=None, subject='',
              message='', html_message='', scheduled_time=None, headers=None,
              priority=None, attachments=None, render_on_delivery=False,
              log_level=None, commit=True, cc=None, bcc=None, language='',
              backend=''):
    """
    封装 post_office 发送邮件的方法
    mail.send()
    :param recipients:
    :param sender:
    :param template:
    :param context:
    :param subject:
    :param message:
    :param html_message:
    :param scheduled_time:
    :param headers:
    :param priority:
    :param attachments:
    :param render_on_delivery:
    :param log_level:
    :param commit:
    :param cc:
    :param bcc:
    :param language:
    :param backend:
    :return:
    """
    re = mail.send(
        recipients=recipients,
        sender=sender,
        template=template,
        context=context,
        subject=subject,
        message=message,
        html_message=html_message,
        scheduled_time=scheduled_time,
        headers=headers,
        priority=priority,
        attachments=attachments,
        render_on_delivery=render_on_delivery,
        log_level=log_level,
        commit=commit,
        cc=cc,
        bcc=bcc,
        language=language,
        backend=backend,
    )
    return re


def send_mail_template(recipients=None, sender=None, template=None, context=None,
                       scheduled_time=None, headers=None,
                       priority=None, attachments=None, render_on_delivery=False,
                       log_level=None, commit=True, cc=None, bcc=None, language='',
                       backend=''):
    """
    发送模版消息
    :param recipients:
    :param sender:
    :param template:
    :param context:
    :param scheduled_time:
    :param headers:
    :param priority:
    :param attachments:
    :param render_on_delivery:
    :param log_level:
    :param commit:
    :param cc:
    :param bcc:
    :param language:
    :param backend:
    :return:
    """
    return send_mail(recipients=recipients,
                     sender=sender,
                     template=template,
                     context=context,
                     scheduled_time=scheduled_time,
                     headers=headers,
                     priority=priority,
                     attachments=attachments,
                     render_on_delivery=render_on_delivery,
                     log_level=log_level,
                     commit=commit,
                     cc=cc,
                     bcc=bcc,
                     language=language,
                     backend=backend,
                     )


def send_mail_message(recipients=None, sender=None, subject='', message='', html_message='',
                      scheduled_time=None, headers=None,
                      priority=None, attachments=None, render_on_delivery=False,
                      log_level=None, commit=True, cc=None, bcc=None, language='',
                      backend=''):
    """
    发送普通消息
    :param recipients:
    :param sender:
    :param subject:
    :param message:
    :param html_message:
    :param scheduled_time:
    :param headers:
    :param priority:
    :param attachments:
    :param render_on_delivery:
    :param log_level:
    :param commit:
    :param cc:
    :param bcc:
    :param language:
    :param backend:
    :return:
    """
    return send_mail(recipients=recipients,
                     sender=sender,
                     subject=subject,
                     message=message,
                     html_message=html_message,
                     scheduled_time=scheduled_time,
                     headers=headers,
                     priority=priority,
                     attachments=attachments,
                     render_on_delivery=render_on_delivery,
                     log_level=log_level,
                     commit=commit,
                     cc=cc,
                     bcc=bcc,
                     language=language,
                     backend=backend,
                     )


def send_mail_queued(processes=1, log_level=None):
    """
    封装 post_office 发送待发送状态(queued)邮件的方法
    mail.send_queued()
    :param processes:
    :param log_level:
    :return:
    """
    re = mail.send_queued(processes, log_level)
    return re


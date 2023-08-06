#!/usr/bin/python
# coding:utf-8
import config
import logging
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from tweb.error_exception import ErrException, ERROR
from ucenter.services import user_indicate
from asyncio import get_event_loop

# 第三方 SMTP 服务
_mail_host = config.EMAIL['mail_host']
_mail_user = config.EMAIL['mail_user']
_mail_pass = config.EMAIL['mail_pass']
_mail_title = config.EMAIL['mail_title']
_mail_tpl = config.EMAIL['mail_tpl']


async def send_email_sync(email, code):
    args = email, code
    return await get_event_loop().run_in_executor(None, send_email, *args)


def send_email(email, code):
    if not user_indicate.is_email(email):
        raise ErrException(ERROR.E40003)

    try:
        smtp = smtplib.SMTP_SSL(_mail_host, 465, keyfile=config.EMAIL['cert_key'], certfile=config.EMAIL['cert_pem'])
    except FileNotFoundError:
        logging.warning('not found %s or %s, will use port 25 to send email!' % (config.EMAIL['cert_key'], config.EMAIL['cert_pem']))
        smtp = smtplib.SMTP(_mail_host, 25)

    smtp.ehlo()
    smtp.login(_mail_user, _mail_pass)

    receivers = [email]  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱

    message = MIMEText(_mail_tpl.format(code), 'plain', 'utf-8')
    message['From'] = Header(_mail_user, 'utf-8')
    message['To'] = Header(email, 'utf-8')

    subject = _mail_title.format(code)
    message['Subject'] = Header(subject, 'utf-8')

    try:
        smtp.sendmail(_mail_user, receivers, message.as_string())
    except smtplib.SMTPException as e:
        raise ErrException(ERROR.E50001, extra=e.args[0], e=e)
    finally:
        smtp.quit()

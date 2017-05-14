"""
こちらを参考
http://uxmilk.jp/20274
"""

import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email import charset
from setting import private

from_address = private.FROM_ADDRESS
to_address = private.TO_ADDRESS
smtpsv = private.SMTP_SV
PW = private.MAIL_PASSWORD

def send_mail(subject, text):
    sender = smtplib.SMTP_SSL(smtpsv)
    sender.login(from_address, PW)

    message = MIMEText(text)  # 本文
    message['Subject'] = subject         # 件名
    message['From'] = from_address  # 送信元
    message['To'] = to_address      # 送信先
    sender.sendmail(from_address, to_address, message.as_string())
    sender.quit()

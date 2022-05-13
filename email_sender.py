# coding=utf-8

from email.mime.text import MIMEText
from email.header import Header
from smtplib import SMTP_SSL


class EmailSender:
    def __init__(self, host, username, password):
        self.__username = username
        # ssl login
        self.__smtp = SMTP_SSL(host)
        # set_debuglevel() for debug, 1 enable debug, 0 for disable
        # smtp.set_debuglevel(1)
        self.__smtp.ehlo(host)
        self.__smtp.login(username, password)

    def send(self, receiver, mail_title='', mail_content=''):
        # construct message
        msg = MIMEText(mail_content, "plain", 'utf-8')
        msg["Subject"] = Header(mail_title, 'utf-8')
        msg["From"] = self.__username
        msg["To"] = receiver
        self.__smtp.sendmail(self.__username, receiver, msg.as_string())

    def quit(self):
        self.__smtp.quit()

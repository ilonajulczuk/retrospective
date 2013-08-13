import smtplib
from email.mime.text import MIMEText
from mailing.models import MailConfiguration
import datetime


def people_who_need_mailing():
    """Get people who should get email with reminder"""
    today_day = datetime.datetime.today().day
    print today_day
    in_need = MailConfiguration.objects.filter(
        every_week=True,
        day_of_the_week=today_day,
    ).values_list('user__address')
    return in_need


def send_mails():
    msg_body = "I'm sending all the mails, here!"

    msg = MIMEText(msg_body)

    sender_address = 'buster@retrospectively.me'
    msg['Subject'] = 'Retrospectives reminder'
    msg['From'] = sender_address
    msg['To'] = reciever_address

    s = smtplib.SMTP('localhost')
    s.sendmail(sender_address, [reciever_address], msg.as_string())
    s.quit()
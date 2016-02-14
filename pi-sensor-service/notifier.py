#!/usr/bin/env python
# -*- coding: utf-8 -*-
from smtplib import SMTP
from email.mime.text import MIMEText


class Notifier:
    def __init__(self):
        try:
            conf = {}
            execfile("/etc/pi-sensor-service/config", conf)

            self.__smtpAddress = conf["smtp_address"]
            self.__smtpPort = conf["smtp_port"]
            self.__fromAddress = conf["from_address"]
            self.__destinationAddress = conf["destination_address"]

        except Exception, e:
            print 'Unable to read config file, using default e-mail params\n%s' % e

            self.__smtpAddress = '192.168.1.113'
            self.__smtpPort = 25
            self.__fromAddress = 'pi-sensors-notify@barser.com'
            self.__destinationAddress = 'bartee.88@gmail.com'

    def send_temp_warning(self, message):
        if message is None:
            return False
        return self.__send_warning(message, 'OSTRZEŻENIE o wysokiej temperaturze')

    def send_hum_warning(self, message):
        if message is None:
            return False
        return self.__send_warning(message, 'OSTRZEŻENIE o wysokiej wilgotności')

    def __send_warning(self, message, subject):
        try:
            msg = MIMEText(message, 'plain')
            msg['Subject'] = subject
            msg['From'] = self.__fromAddress

            conn = SMTP()
            conn.set_debuglevel(False)
            conn.connect(self.__smtpAddress, self.__smtpPort)
            try:
                conn.sendmail(self.__fromAddress, self.__destinationAddress, msg.as_string())
            finally:
                conn.close()

            return True
        except Exception, e:
            print 'Blad wysylki wiadomosci:\n' % e
            return False
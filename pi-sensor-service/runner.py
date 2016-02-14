#!/usr/bin/env python
# -*- coding: utf-8 -*-
from threading import Thread
import Adafruit_DHT
from notifier import Notifier
import time

notifier = Notifier()

conf = {}
execfile("/etc/pi-sensor-service/config", conf)


class SensorsRunner(Thread):
    def __init__(self):
        self.__lastResults = {}
        self.__last_t_max = None
        self.__last_h_max = None
        Thread.__init__(self)

    def get_last_results(self):
        return self.__lastResults

    def run(self):
        while True:
            h1, t1 = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, 23)
            h2, t2 = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, 24)

            if t1 >= conf["temp_notification_threshold"] or t2 >= conf["temp_notification_threshold"]:
                if self.__last_t_max is None or self.__last_t_max < conf["temp_notification_threshold"]:
                    message = 'ODNOTOWANO PODWYŻSZONĄ TEMPERATURĘ O WARTOŚCI: %s STOPNI' % '{0:0.1f}'.format(max(t1, t2))
                    notifier.send_temp_warning(message)
            if h1 >= conf["humidity_notification_threshold"] or h2 >= conf["humidity_notification_threshold"]:
                if self.__last_h_max is None or self.__last_h_max < conf["humidity_notification_threshold"]:
                    message = 'ODNOTOWANO PODWYŻSZONĄ WILGOTNOŚĆ O WARTOŚCI: %s PROCENT' % '{0:0.1f}'.format(max(h1, h2))
                    notifier.send_hum_warning(message)

            result = {}

            if h1 is not None and t1 is not None:
                result['Sensor1'] = {}
                result['Sensor1']['temperature'] = '{0:0.1f}'.format(t1)
                result['Sensor1']['humidity'] = '{0:0.1f}'.format(h1)

            if h2 is not None and t2 is not None:
                result['Sensor2'] = {}
                result['Sensor2']['temperature'] = '{0:0.1f}'.format(t2)
                result['Sensor2']['humidity'] = '{0:0.1f}'.format(h2)

            self.__lastResults = result
            self.__last_t_max = max(t1, t2)
            self.__last_h_max = max(h1, h2)

            time.sleep(10)
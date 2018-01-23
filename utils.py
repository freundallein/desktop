# -*- coding: utf-8 -*-
import datetime


class Logger:
    TAG = None

    def log(self, message):
        if self.TAG is None:
            raise NotImplementedError('Set TAG in {}'.format(
                self.__class__.__name__))
        t = datetime.datetime.now().strftime("%Y.%m.%d %H:%M:%S")
        print('{} - [{}]: {}'.format(t, self.TAG, message))


class Configurator:
    protocol = None
    server = None
    port = None
    debug = None
    credentials = None
    MACHINE_NAME = None

    def get_config(self):
        with open('config.ini') as file:
            for line in file.readlines():
                if line.startswith('protocol'):
                    self.protocol = line.split('=')[1].strip()
                if line.startswith('server'):
                    self.server = line.split('=')[1].strip()
                if line.startswith('port'):
                    self.port = line.split('=')[1].strip()
                if line.startswith('DEBUG'):
                    value = line.split('=')[1].strip()
                    self.debug = value in ('True', 1, 'yes')
                if line.startswith('MACHINE_NAME'):
                    self.MACHINE_NAME = line.split('=')[1].strip()
        return self


class FormValidator:
    def __init__(self):
        pass

    def clean(self):
        pass

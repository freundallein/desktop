# -*- coding: utf-8 -*-
import datetime

import requests


class HttpRequester:
    def __init__(self, config):
        self.requester = requests
        self.config = config

    @property
    def dsn(self):
        return "{}://{}:{}".format(self.config.protocol,
                                   self.config.server,
                                   self.config.port)

    def form_link(self, url):
        return "{}/{}".format(self.dsn, url)

    def server_exchange(self, inner_status):
        url = self.form_link('server_status')
        data = {'machine': self.config.MACHINE_NAME,
                'inner': inner_status,
                'datetime': datetime.datetime.now().strftime(
                    "%Y.%m.%d %H:%M:%S")}
        try:
            response = self.requester.post(url, data=data)
            result = response.json().get('status')
        except requests.RequestException:
            result = False
        return result

    def get_types(self):
        url = self.form_link('card_types')
        try:
            response = self.requester.get(url)
            result = response.json()
        except requests.RequestException:
            result = []
        return result

    def send(self):
        pass

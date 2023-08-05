#!/usr/bin/env python
# -*- coding: utf-8 -*-

__all__ = ['EkylibreApi']

from mycroft.configuration import ConfigurationManager
from mycroft.util.log import LOG
# from mycroft_ekylibre_utils.tls_adapter import TlsAdapter
import requests


class EkylibreApi:
    """Ekylibre API class"""

    def __init__(self):
        self.config_api = ConfigurationManager.get().get("ekylibre_api")
        self.ip = "https://{ip}/api/v1/".format(ip=self.config_api.get('ip'))
        self.host = self.config_api.get('host')
        self.user = self.config_api.get('user')
        self.password = self.config_api.get('password')
        # self.token = self.config_api.get('token')
        self.session = requests.Session()
        self.session.headers.update({'Host': self.host})
        # self.session.mount("https://", TlsAdapter())
        self.session.verify = False
        self.auth = None
        self.get_token()

    def close_session(self):
        if self.session:
            self.session.close()

    def get(self, endpoint, payload=None):
        LOG.debug("GET")

        try:
            url = self.ip + endpoint
            LOG.debug("PAYLOAD -> {}".format(str(payload)))
            r = self.session.get(url, json=payload)
        except Exception as err:
            LOG.error("API POST error: {}".format(err))
            return "API GET error: {}".format(err)
        return r.json()

    def post(self, endpoint, payload):
        LOG.debug("POST")

        try:
            url = self.ip + endpoint
            LOG.debug("PAYLOAD -> {}".format(str(payload)))
            r = self.session.post(url, json=payload)
        except Exception as err:
            LOG.error("API POST error: {}".format(err))
            return "API POST error: {}".format(err)
        return r.json()

    def get_token(self):
        LOG.info("GET TOKEN (simple_token={})".format(self.auth))
        try:
            endpoint = self.ip + "tokens"
            payload = {'email': self.user, 'password': self.password}

            r = self.session.post(endpoint, data=payload)
            r.encoding = 'utf-8'
            LOG.info("response " + r.text)

            if r.status_code == requests.codes.ok:
                token = r.json()
                self.auth = "simple-token {} {}".format(self.user, token['token'])
                self.session.headers.update({'Authorization': self.auth})
            else:
                LOG.error(r.status_code, r.content)

        except Exception as err:
            LOG.error("Unable to get token: {0}".format(err))
            return "Unable to get token: {0}".format(err)

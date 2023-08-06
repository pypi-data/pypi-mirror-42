import logging

from munch import munchify

import requests


logging.basicConfig()

config = None
url = None


class Dictionaries():
    @staticmethod
    def dictionary_config():

        config = dict()

        base = 'https://api.sbif.cl/api-sbifv3/recursos_api/tmc/'

        config['ENDPOINTTMC'] = base + '{}/{}'

        config['ENDPOINTTMCANTERIORES'] = base + 'anteriores/{}/{}'

        config['ENDPOINTTMCPOSTERIORES'] = base + 'posteriores/{}/{}'

        config['ENDPOINTTMCPERIODO'] = base + 'periodo/{}/{}/{}/{}'

        config['APIKEY'] = ''

        return config


class TMC():

    def __init__(self):
        self.__config = Dictionaries.dictionary_config()

    def get_tmc(self, year, month, tipo=None):

        url_endpoint = self.__config['ENDPOINTTMC'].format(year, month)

        url_query_strings = {'apikey': self.__config['APIKEY'],
                             'formato': 'json'}

        response = munchify(requests.get(url_endpoint,
                                         params=url_query_strings).json())

        if tipo:
            for operacion in response.TMCs:
                if operacion.Tipo == tipo:
                    return operacion

        return response

    def get_tmc_anteriores(self, year, month):

        url_endpoint = self.__config['ENDPOINTTMCANTERIORES'].format(year,
                                                                     month)

        url_query_strings = {'apikey': self.__config['APIKEY'],
                             'formato': 'json'}

        response = munchify(requests.get(url_endpoint,
                                         params=url_query_strings).json())

        return response

    def get_tmc_posteriores(self, year, month):

        url_endpoint = self.__config['ENDPOINTTMCPOSTERIORES'].format(year,
                                                                      month)

        url_query_strings = {'apikey': self.__config['APIKEY'],
                             'formato': 'json'}

        response = munchify(requests.get(url_endpoint,
                                         params=url_query_strings).json())

        return response

    def get_tmc_periodo(self, from_year, from_month, to_year, to_month):

        url_endpoint = self.__config['ENDPOINTTMCPERIODO'].format(from_year,
                                                                  from_month,
                                                                  to_year,
                                                                  to_month)

        url_query_strings = {'apikey': self.__config['APIKEY'],
                             'formato': 'json'}

        response = munchify(requests.get(url_endpoint,
                                         params=url_query_strings).json())

        return response

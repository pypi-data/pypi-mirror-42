import logging

from django.conf import settings

from munch import munchify

import requests


logger = logging.getLogger(__name__)

if not hasattr(settings, 'APISBIF_APIKEY'):
    raise ValueError('Debe agregar configuracion APISBIF en settings de django')
apikey = settings.APISBIF_APIKEY
endpoint = 'https://api.sbif.cl/api-sbifv3/recursos_api'


class TMC():

    def __request_apisbif(self, url_endpoint):

        url_query_strings = {'apikey': apikey,
                             'formato': 'json'}

        response = requests.get(url_endpoint, params=url_query_strings)

        if not response.ok:
            logger.error('ERROR APISBIF Response: {}'.format(response.text))
            return None
        response = munchify(response.json())

        return response

    def get_tmc(self, year, month):

        url_endpoint = endpoint + '/tmc/{}/{}'.format(year, month)

        return self.__request_apisbif(url_endpoint)

    def get_tmc_anteriores(self, year, month):

        url_endpoint = endpoint + '/tmc/anteriores/{}/{}'.format(year, month)

        return self.__request_apisbif(url_endpoint)

    def get_tmc_posteriores(self, year, month):

        url_endpoint = endpoint + '/tmc/posteriores/{}/{}'.format(year, month)

        return self.__request_apisbif(url_endpoint)

    def get_tmc_periodo(self, from_year, from_month, to_year, to_month):

        url_endpoint = endpoint + '/tmc/periodo/{}/{}/{}/{}'.format(from_year,
                                                                    from_month,
                                                                    to_year,
                                                                    to_month)

        return self.__request_apisbif(url_endpoint)

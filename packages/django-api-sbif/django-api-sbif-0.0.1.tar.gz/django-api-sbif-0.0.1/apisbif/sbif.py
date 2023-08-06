from configuration import Configuration
from sbif_tmc import TMC


class SBIF:

        def __init__(self, params):
            self.__configuration = params
            return None

        def get_tmc(self):
            tmc = TMC(self.__configuration)
            return tmc

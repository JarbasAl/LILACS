from requests.exceptions import HTTPError


class NotTrained(Exception):
    """ Model not trained"""


class InvalidMetric(Exception):
    """ Unrecognized metric """


class SpotlightDown(HTTPError):
    """ Spotlight seems to be down again"""

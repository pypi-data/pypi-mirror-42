import json
import logging
import aiohttp
import sys
import urllib.parse as urllib


log = logging.getLogger(__name__)

class FullContactRespoonse(object):
    def __init__(self, status_code, rate_limit_remaining, json_response):
        self.status_code = status_code
        self.rate_limit_remaining = rate_limit_remaining
        self.json_response = json_response


class FullContact(object):
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = 'https://api.fullcontact.com/v2/'
        self.get_endpoints = {
            'person': 'person.json',
            'company': 'company/lookup.json',
            'company_search': 'company/search.json',
            'disposable': 'email/disposable.json',
            'name_normalizer': 'name/normalizer.json',
            'name_deducer': 'name/deducer.json',
            'name_similarity': 'name/similarity.json',
            'name_stats': 'name/stats.json',
            'name_parser': 'name/parser.json',
            'address_locationNormalizer': 'address/locationNormalizer.json',
            'address_locationEnrichment': 'address/locationEnrichment.json',
            'account_stats': 'stats.json'
        }
        self.post_endpoints = {
            'batch': 'batch.json'
        }
        for endpoint in self.get_endpoints:
            method = lambda endpoint=endpoint, **kwargs: self.api_get(endpoint, **kwargs)
            setattr(self, endpoint, method)

    async def api_get(self, endpoint, **kwargs):
        """ Makes a FullContact API call

        Formats and submits a request to the specified endpoint, appending
        any key-value pairs passed in kwargs as a url query parameter.

        Args:
            endpoint: shortname of the API endpoint to use.
            strict: if True, throw an error
            **kwargs: a dict of query parameters to append to the request.

        Returns:
            A Requests object containing the result of the API call. Interact
            with the return value of this function as you would with any
            other Requests object.

        Raises:
            KeyError: the specified endpoint was not recognized. Check the
                docs.
            Requests.Exceptions.*: an error was raised by the Requests
                module.
        """

        headers = {'X-FullContact-APIKey': self.api_key}
        endpoint = self.base_url + self.get_endpoints[endpoint]
        async with aiohttp.ClientSession() as session:
            async with session.get(endpoint, params=kwargs, headers=headers) as request:
                try:
                    rate_limit_remaining = request.headers["x-rate-limit-remaining"]
                except KeyError:
                    rate_limit_remaining = "Failed to get the remaining rate"
                status_code = request.status
                to_json = await request.json()
                return FullContactRespoonse(status_code, rate_limit_remaining, to_json)

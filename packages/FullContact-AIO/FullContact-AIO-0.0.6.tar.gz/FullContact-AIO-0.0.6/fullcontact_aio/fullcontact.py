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

    async def person(self, **kwargs):
        result = await self.api_get("person", **kwargs)
        return result

    async def company(self, **kwargs):
        result = await self.api_get("company")
        return result

    async def company_search(self, **kwargs):
        result = await self.api_get("company_search", **kwargs)
        return result

    async def disposable(self, **kwargs):
        result = await self.api_get("disposable", **kwargs)
        return result

    async def name_normalizer(self, **kwargs):
        result = await self.api_get("name_normalizer", **kwargs)
        return result

    async def name_deducer(self, **kwargs):
        result = await self.api_get("name_deducer", **kwargs)
        return result

    async def name_similarity(self, **kwargs):
        result = await self.api_get("name_similarity", **kwargs)
        return result

    async def name_stats(self, **kwargs):
        result = await self.api_get("name_stats", **kwargs)
        return result

    async def name_parser(self, **kwargs):
        result = await self.api_get("name_parser", **kwargs)
        return result

    async def address_locationNormalizer(self, **kwargs):
        result = await self.api_get("address_locationNormalizer", **kwargs)
        return result

    async def address_locationEnrichment(self, **kwargs):
        result = await self.api_get("address_locationEnrichment", **kwargs)
        return result

    async def account_stats(self, **kwargs):
        result = await self.api_get("account_stats", **kwargs)
        return result

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

    def _prepare_batch_url(self, b):
        """ Format a url to submit to the batch API

        Args:
            b: a tuple of (str, dict) containing the endpoint for
                the request and a dict of url parameters (note:
                the api key doesn't need to be included for
                individual requests within a batch since it is
                appended to the batch API call.

        Returns:
            A formatted url to append to the batch request's payload.
        """
        ep = self.get_endpoints[b[0]]
        qu = urllib.urlencode(b[1])
        batch_url = '{0}{1}?{2}'.format(self.base_url, ep, qu)
        log.debug('Prepared batch url: {0}'.format(batch_url))

        return batch_url

    async def query_emails(self, *emails):
        """
        Accept one or many email addresses, and place a single or batch query
        for all to fetch contact information. Returns a list of results.
        """
        # TODO: Validate emails?
        if len(emails) == 0:
            raise ValueError("Must provide at least one email to use.")
        elif len(emails) == 1:
            # Single API call
            r = await self.api_get('person', email=emails[0])

            o = {emails[0]: await r}
        else:
            # Batch API call
            r = await self.api_batch([('person', {'email': e}) for e in emails])
            responses = await r.json()['responses']
            o = {}
            for e in emails:
                req = self._prepare_batch_url(('person', {'email': e}))
                if req in responses:
                    o[e] = responses[req]
        # API returns 404 for absent data.. restful, but may break batch?
        # r.raise_for_status()
        return

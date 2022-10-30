import json
import re

from urllib.parse import urlparse

import httpx
import parsel
import pyjq

class ScrapeTarget:
    def __init__(self, product_name, url, selector, target_name=None, regex=None, parser=None):
        self.product_name = product_name
        self.target_name = target_name if target_name else urlparse(url).hostname
        self.url = url
        self.selector = selector
        self.regex = re.compile(regex if regex else r'[0-9]+(\.[0-9]{2})?')
        self.parser = parser if parser else 'html'
        self.headers = {}

    def query_target(self):
        print('Query product %s, target %s' % (self.product_name, self.target_name))
        # some sites get suspicious if we talk to them in HTTP/1.1
        # we use httpx to have HTTP2 support and circumvent that issue
        query_response = httpx.get(
            url=self.url,
            headers=self.headers,
            follow_redirects=True,
        ).text

        # parse the response and match the selector
        selector_match = ''
        if self.parser == 'html':
            # parse response as html
            selector = parsel.Selector(text=query_response)
            selector_match = selector.css(self.selector).get()
        elif self.parser == 'json':
            # parse response as json
            query_response_json = json.loads(query_response)
            selector_match = str(pyjq.first(self.selector, query_response_json))
        else:
            # TODO: better error handling
            print('invalid parser!')
            return None

        if not selector_match:
            # TODO: better error handling
            print('no selector_match!')
            return None

        # match the regex
        regex_match = self.regex.search(selector_match)
        if regex_match:
            str_result = regex_match.group(0)
            # convert the result to float
            float_result = float(str_result)
            return float_result
        else:
            # TODO: better error handling
            print('no regex match!')
            return None
import re

import httpx
import parsel

class ScrapeTarget:
    def __init__(self, product_name, target_name, url, selector, regex=None):
        self.product_name = product_name
        self.target_name = target_name
        self.url = url
        self.selector = selector+'::text'
        self.regex = re.compile(regex if regex else r'[0-9]+(\.[0-9]{2})?')
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
        selector = parsel.Selector(text=query_response)

        # Match the selector
        selector_match = selector.css(self.selector).get()
        if selector_match:
            # Match the regex
            regex_match = self.regex.search(selector_match)
            if regex_match:
                str_result = regex_match.group(0)
                # Convert the reult to float
                float_result = float(str_result)
                return float_result
        return None
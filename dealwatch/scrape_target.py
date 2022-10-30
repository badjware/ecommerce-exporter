import re

class ScrapeTarget:
    def __init__(self, product_name, target_name, url, selector, regex=None):
        self.product_name = product_name
        self.target_name = target_name
        self.url = url
        self.selector = selector
        self.regex = re.compile(regex if regex else r'[0-9]+(\.[0-9]{2})?')
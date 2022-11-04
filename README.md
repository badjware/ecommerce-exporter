# ecommerce-exporter

ecommerce-exporter is a [prometheus](https://prometheus.io/) exporter that webscrape the storefront of various e-commerces and expose the price of their products as prometheus metrics. These metrics can then be used to graph the pricing evolution over time, send alerts when the price drop, or to easily compare the price of a product on many e-commerces at once.

## Install

An aarch64 and an amd64 docker images are available on [docker hub](https://hub.docker.com/r/badjware/ecommerce-exporter). You can pull it using:
``` sh
docker pull badjware/ecommerce-exporter
```

This is the recommended way of running the exporter. 

## Usage

Download the [example configuration file](ecommerce-exporter.example.yml) and edit it to configure the e-commerce sites you wish to scrape. You can configure multiple products and multiple targets in the same configuration file.

Assuming you named your configuration file `ecommerce-exporter.yml`, you can use the following command to run the exporter with docker:
``` sh
docker run -v "$PWD/ecommerce-exporter.yml:/ecommerce-exporter.yml" -p 8000:8000 badjware/ecommerce-exporter
```

The prices of the configured products will start being scraped and exposed on http://localhost:8000/metrics. You can then configure [prometheus to scrape that endpoint](https://prometheus.io/docs/prometheus/latest/configuration/configuration/#scrape_config). It is recommended to set the scrape interval to be the same as the webscrape interval of the exporter (15m by default). 

A full list of available flags can be printed using `-h`:
```
usage: An utility to scrape e-commerce product price and expose them as prometheus metrics
       [-h] [-c CONFIG] [-i INTERVAL] [--user-agent USER_AGENT]
       [-p LISTEN_PORT] [-a LISTEN_ADDRESS]

options:
  -h, --help            show this help message and exit
  -c CONFIG, --config CONFIG
                        The configuration file. (default: ecommerce-
                        exporter.yml)
  -i INTERVAL, --interval INTERVAL
                        The target scrape interval, in minutes. (default: 15)
  --user-agent USER_AGENT
                        The user-agent to spoof. (default: Mozilla/5.0 (X11;
                        Linux x86_64; rv:106.0) Gecko/20100101 Firefox/106.0)
  -p LISTEN_PORT, --listen-port LISTEN_PORT
                        The listen port for the http server. (default: 8000)
  -a LISTEN_ADDRESS, --listen-address LISTEN_ADDRESS
                        The listen address for the http server. (default:
                        0.0.0.0)
```

## Configuring the selectors

Finding the correct value for a selector will require some effort. Once you find the correct selector to use, you should be able to use the same one across the whole site.

## html parser

The general procedure to figure out the selector for a site using an html parser is as follow:
1. Open up the product page in your browser.
2. Right-click the price of the product and select "inspect element" in the drop-down.
3. Take note of the `class`, the `id`, and the type of the element containing the price of the product.
4. Build a CSS selector to select the element with the price of the product you wish to extract.

Refer to the documentation on how to build a CSS selector: https://www.w3schools.com/CSS/css_selectors.asp

Below is a table with examples of some CSS selectors that match the html element containing the price of a product. Keep in mind that if the design of the site changes in the future, these selector may stop working.

| site | selector |
| --- | --- |
| amazon.ca | `.priceToPay .a-offscreen::text` |
| canadacomputer.com | `.price-show-panel .h2-big strong::text` |
| memoryexpress.com | `.GrandTotal` |

## json parser

The general procedure to figure out the selector for a site using an json parser is as follow:
1. Open up the development tool of your browser using the F12 key.
2. Open up the product page in your favorite browser.
3. Go to the "network" tab in your development tool and dig through the resources of the page to find the api call that returned the price of the product.
4. Take note of the url of this api call.
5. Use the commands `curl http://url_you_found_in_your_dev_tool | jq 'some_selector'` and build a selector to extract the price of the product from the json response.

Refer to the documentation of jq on how to build a selector for it: https://stedolan.github.io/jq/manual/#Basicfilters

Below is a table with examples of some jq selectors that match the json field containing the price of a product. Keep in mind that if the backend/api of the site changes in the future, these selector may stop working. Finding correct url of your product may require some digging in the developper tools of your browser.

| site | selector | url example |
| --- | --- | --- |
| newegg.ca | `.MainItem.UnitCost` | https://www.newegg.ca/product/api/ProductRealtime?ItemNumber=19-118-343&RecommendItem=&BestSellerItemList=9SIAA4YGC82324%2C9SIADGEGMY7603%2C9SIAVH1J0A6685&IsVATPrice=true |
| bestbuy.ca | `.[] \| .salePrice,.regularPrice` | https://www.bestbuy.ca/api/offers/v1/products/15778672/offers |

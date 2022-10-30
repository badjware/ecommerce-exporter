import argparse

import yaml

from prometheus_client import start_http_server

from dealwatch.scrape_target import ScrapeTarget

def main():
    parser = argparse.ArgumentParser("An utility to scrape e-commerce product price and expose them as prometheus metrics")
    parser.add_argument(
        '-c', '--config',
        help='The configuration file. (default: %(default)s)',
        type=str,
        default='dealwatch.yml',
    )
    parser.add_argument(
        '--user-agent',
        help='The user-agent to spoof. (default: %(default)s)',
        type=str,
        default='Mozilla/5.0 (X11; Linux x86_64; rv:106.0) Gecko/20100101 Firefox/106.0',
    )
    parser.add_argument(
        '-p', '--listen-port',
        help='The listen port for the http server. (default: %(default)s)',
        type=int,
        default=8000,
    )
    parser.add_argument(
        '-a', '--listen-address',
        help='The listen address for the http server. (default: %(default)s)',
        type=str,
        default='0.0.0.0',
    )

    args = parser.parse_args()
    scrape_targets = parse_config(args.config)

    # setup the headers for each scrape targets
    for scrape_target in scrape_targets:
        scrape_target.headers = {
            'Accept': '*/*',
            'User-Agent': args.user_agent,
        }

    # start the http server to server the prometheus metrics
    start_http_server(args.listen_port, args.listen_address)

    for scrape_target in scrape_targets:
        print(scrape_target.query_target())

def parse_config(config_filename):
    result = []
    print('Loading configurations from %s' % config_filename)
    with open(config_filename, 'r') as f:
        config = yaml.safe_load(f)

        # iterate through products listed in the configuration
        products = get_field_or_die(config, 'products')
        for product in products:
            product_name = get_field_or_die(product, 'name')

            # iterate through the targets listed for each products in the configuration
            targets = get_field_or_die(product, 'targets')
            for target in targets:
                # Create a ScrapeTarget for each targets to scrape
                result.append(ScrapeTarget(
                    product_name=product_name,
                    target_name=get_field_or_die(target, 'name'),
                    url=get_field_or_die(target, 'url'),
                    selector=get_field_or_die(target, 'selector'),
                    regex=target.get('regex'),
                ))
    return result

def get_field_or_die(mapping, field_name):
    value = mapping.get(field_name)
    if value is None:
        raise Exception('Missing required field: %s' % field_name)
    else:
        return value

if __name__ == '__main__':
    main()
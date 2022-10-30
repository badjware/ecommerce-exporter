import argparse

import yaml

from dealwatch.scrape_target import ScrapeTarget

def main():
    parser = argparse.ArgumentParser("An utility to scrape e-commerce target price fluctuations")
    parser.add_argument(
        '-c', '--config',
        help='The configuration file. (default: %(default)s)',
        type=str,
        default='dealwatch.yml',
    )

    args = parser.parse_args()
    products = parse_config(args.config)
    print(products)

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
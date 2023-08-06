import logging
import yaml
import argparse
from importer import import_feeds_to_mysql_table

logger_handler = logging.StreamHandler()  # Handler for the logger
logger_handler.setFormatter(logging.Formatter('%(levelname)s [%(name)s:%(lineno)s] %(message)s'))
logger = logging.getLogger()
logger.addHandler(logger_handler)
logger.setLevel(logging.INFO)


def import_feeds():
    parser = argparse.ArgumentParser()
    parser.add_argument('config_file', help='config YAML file')
    args = parser.parse_args()
    with open(args.config_file, "r") as stream:
        settings = yaml.load(stream) 
    storage = settings['destination']['storage']
    storage_config = settings['destination']['config']
    importers = settings['source']
    logger.info('Importers settings: {}'.format(importers))
    logger.info('Destination settings: {}'.format(settings['destination']))
    if storage == 'mysql':
        import_feeds_to_mysql_table(importers, storage_config)
    else:
        print('Storage {} not implemented'.format(storage))


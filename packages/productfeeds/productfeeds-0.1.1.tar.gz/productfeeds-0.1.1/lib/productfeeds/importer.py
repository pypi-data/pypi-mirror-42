from api.webepartnersapi import WebepartnersAPI
from api.convertiserapi import ConvertiserAPI
from storage.mysqlstorage import MySQLStorage
import logging

logger = logging.getLogger(__name__)

IMPORTERS = {
    'webepartners': {
        'class': WebepartnersAPI,
        'prefix': 'web_',
    },

    'convertiser': {
        'class': ConvertiserAPI,
        'prefix': 'con_',
    },
}


def get_importer_instance(importer, config, storage=None):
    return IMPORTERS[importer]['class'](storage=storage, prefix=IMPORTERS[importer]['prefix'], **config)


def import_feeds_to_mysql_table(importers_config, mysql_config):
    for importer in importers_config:
        s = MySQLStorage(mysql_config)
        s.clear()
        api = get_importer_instance(importer['api'], importer['config'], storage=s)
        rs = api.import_products()
        logger.info("Import status: {}".format(rs))

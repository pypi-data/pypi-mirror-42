import requests
import logging
import json

from ..models import Product

logger = logging.getLogger(__name__)

PRODUCTS_URL = 'https://api.convertiser.com/publisher/products/v2/?key={}'
PAGE_SIZE = 20000
REQUEST_TIMEOUT = 120


class ConvertiserAPI(object):

    def __init__(self, token=None, offers=None, website_key=None, storage=None, prefix=''):
        self.storage = storage
        self.website_key = website_key
        self.offers = offers
        self.articlecode_prefix = prefix
        self.token = token

    def import_products(self):
        rs = {'status': 1}
        imported = 0
        offers_count = len(self.offers)
        for offer in self.offers:
            try:
                response = requests.post(
                    PRODUCTS_URL.format(self.website_key),
                    headers={'Authorization': 'Token {}'.format(self.token), 'Content-Type': 'application/json'},
                    data=json.dumps({
                        "filters": {"offer_id": {"lookup": "exact", "value": offer}},
                        "page": 1, "page_size": PAGE_SIZE
                    }),
                    timeout=REQUEST_TIMEOUT
                )
            except Exception, e:
                logger.error(e)
                continue

            results = response.json()
            logger.info('Returned {} products'.format(len(results['data'])))
            for product in results['data']:
                p = Product()
                p.product_data['client'] = product['offer']
                p.product_data['articlecode'] = '%s%s_%s' % (
                self.articlecode_prefix, product['offer_id'], product['id'])
                p.product_data['title'] = product['title'].encode('utf-8')
                p.product_data['brand'] = product['brand'].encode('utf-8')
                categories = product['product_type'].encode('utf-8').split('/')
                p.product_data['category'] = categories[0]
                try:
                    p.product_data['subcategory1'] = categories[1]
                except:
                    pass
                try:
                    p.product_data['subcategory2'] = categories[2]
                except:
                    pass
                p.product_data['description'] = product['description'].encode('utf-8')
                p.product_data['producturl'] = product['link']
                p.product_data['thumburl'] = product['images']['thumb_180']
                p.product_data['imageurl'] = product['images']['default']
                p.product_data['price'] = product['price'].replace('PLN ', '')

                if self.storage is not None:
                    self.storage.save_product(p)
            imported += 1
        rs['success_percent'] = 100 * imported / offers_count

        return rs

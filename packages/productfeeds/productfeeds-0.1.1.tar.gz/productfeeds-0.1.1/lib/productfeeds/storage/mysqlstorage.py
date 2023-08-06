import MySQLdb
import warnings

import logging

logger = logging.getLogger(__name__)


def create_table_if_not_exists(cur, db, table):
    query = 'CREATE TABLE IF NOT EXISTS {}  (\
		id int(10) NOT NULL AUTO_INCREMENT,\
		articlecode varchar(255) CHARACTER SET utf8 DEFAULT NULL ,\
		title varchar(255) CHARACTER SET utf8 DEFAULT NULL ,\
		producturl text CHARACTER SET utf8,\
		price varchar(12) DEFAULT NULL,\
		status int(1) DEFAULT NULL,\
		description text CHARACTER SET utf8,\
		imageurl varchar(255) CHARACTER SET utf8,\
		thumburl varchar(255) CHARACTER SET utf8,\
		parent_id varchar(45) CHARACTER SET utf8 DEFAULT "PARENT",\
		brand varchar(255) CHARACTER SET utf8 DEFAULT NULL ,\
		category varchar(255) CHARACTER SET utf8 DEFAULT NULL,\
		subcategory2 text CHARACTER SET utf8,\
		subcategory1 text CHARACTER SET utf8,\
		uzip_id varchar(8) CHARACTER SET utf8 DEFAULT "NA",\
		delivery varchar(255) CHARACTER SET utf8 DEFAULT NULL ,\
		client varchar(255) CHARACTER SET utf8 DEFAULT NULL ,\
	PRIMARY KEY (id),\
	KEY articlecode (articlecode),\
	KEY status (status)\
	)'.format(table)

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        cur.execute(query)
        db.commit()

        cur.execute("truncate table {}".format(table))
        db.commit()
    logger.info("runlog DB table ready")


class MySQLStorage(object):

    def __init__(self, config=None):
        self.db = MySQLdb.connect(host=config['host'],  # your host, usually localhost
                                  user=config['user'],  # your username
                                  passwd=config['passwd'],  # your password
                                  db=config['db'])  # name of the data base
        self.table = config['table']

        self.cur = self.db.cursor()
        self.db.set_character_set('utf8')
        self.cur.execute('SET NAMES utf8;')
        self.cur.execute('SET CHARACTER SET utf8;')
        self.cur.execute('SET character_set_connection=utf8;')

    def clear(self):
        create_table_if_not_exists(self.cur, self.db, self.table)

    def save_product(self, product):
        self.cur.execute("INSERT INTO runlog (status,description,title,price,imageurl,thumburl,producturl,\
            articlecode,brand,category,subcategory1,subcategory2, uzip_id, delivery, client)\
            VALUES (%(status)s,%(description)s,%(title)s,%(price)s,%(imageurl)s,%(thumburl)s,%(producturl)s,\
            %(articlecode)s,%(brand)s,%(category)s,%(subcategory1)s,%(subcategory2)s,%(uzip_id)s,\
            %(delivery)s,%(client)s)", product.to_dict())

        self.db.commit()

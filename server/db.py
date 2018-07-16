# -*- coding: utf-8 -*-

import csv
import logging
from time import time

from flask import current_app

from model import Shop, Product


log = logging.getLogger(__name__)


def load_data(data_path):
    """
     (str) -> set

     Loads the data from the csv file.
     It creates and returns a set of all the Products.
    """
    shop_dict = {}

    log.info('Loading data...')
    start_time = int(round(time() * 1000))
#   Load shops
    try:
        with open(data_path + '/shops.csv') as shop_file:
            reader = csv.DictReader(shop_file)
            for row in reader:
                shop = Shop(row['id'], row['name'], row['lat'], row['lng'])
                shop_dict[shop.id] = shop
    except IOError as e:
        log.error(e)

    shop_time = int(round(time() * 1000))
    log.debug('Loaded shops in {0} ms'.format((shop_time - start_time)))

#   Load tags
    tag_dict = {}
    try:
        with open(data_path + '/tags.csv') as tag_file:
            reader = csv.DictReader(tag_file)
            for row in reader:
                tag_dict[row['id']] = row['tag']
        with open(data_path + '/taggings.csv') as taggings_file:
            reader = csv.DictReader(taggings_file)
            for row in reader:
                if row['shop_id'] in shop_dict:
                    shop_dict[row['shop_id']].tags.add(tag_dict[row['tag_id']])
    except IOError as e:
        log.error(e)

    tag_time = int(round(time() * 1000))
    log.debug('Loaded tags in {0} ms'.format((tag_time - start_time)))

#   Load products
    products = set()
    try:
        with open(data_path + '/products.csv') as product_file:
            reader = csv.DictReader(product_file)
            for row in reader:
                product = Product(
                              row['id'],
                              row['title'],
                              row['popularity'],
                              row['quantity']
                          )
                if row['shop_id'] in shop_dict:
                    product.shop = shop_dict[row['shop_id']]
                products.add(product)
    except IOError as e:
        log.error(e)

    product_time = int(round(time() * 1000))
    log.debug('Loaded products in {0} ms'.format((product_time - tag_time)))

    end_time = int(round(time() * 1000))
    log.info('Loaded data in {0} ms'.format((end_time - start_time)))

    return products

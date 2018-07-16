# -*- coding: utf-8 -*-

from flask.json import JSONEncoder

from model import Product, Shop


class CustomJSONEncoder(JSONEncoder):
    """
       Custom JSONEncoder to handle
       the encoding of the model classes.
    """

    def default(self, obj):
        if isinstance(obj, Product):
            return {
                'id': obj.id,
                'title': obj.title,
                'popularity': obj.popularity,
                'quantity': obj.quantity,
                'shop': obj.shop
            }
        if isinstance(obj, Shop):
            return {
                'id': obj.id,
                'lat': obj.lat,
                'lng': obj.lng,
                'tags': list(obj.tags)
            }
        return super(CustomJSONEncoder, self).default(obj)

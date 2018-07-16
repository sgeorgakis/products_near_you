# -*- coding: utf-8 -*-


class Shop:

    def __init__(self, id="", name="", lat=0, lng=0, tags=set()):
        self.id = id
        self.name = name
        self.lat = lat
        self.lng = lng
        self.tags = tags

    def __str__(self):
        return 'id: {}, name: {}, lat: {}, lng: {}, tags: {}'.format(
                self.id,
                self.name,
                self.lat,
                self.lng,
                self.tags)


class Product:

    def __init__(self, id, title, popularity, quantity, shop=None):
        self.id = id
        self.title = title
        self.popularity = popularity
        self.quantity = quantity
        self.shop = shop

    def __str__(self):
        return 'id: {}, title: {}, popularity: {}, '
        + 'quantity: {}, shop: {}'.format(self.id,
                                          self.title,
                                          self.popularity,
                                          self.quantity,
                                          self.shop)

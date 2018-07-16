# -*- coding: utf-8 -*-

from geopy.distance import vincenty


def get_matching_products(products, lat, lng, radius, tags):
    """
     (Set, float, float, int, str) -> list

     Filters a set of Products according to the parameters.
     This function is responsible to determine
     if filtering with tags should be applied or not.
    """
    if tags:
        tag_list = tags.split(',')
        return list([
                   product for product in products
                   if is_matching_product_with_tags(
                       product,
                       lat,
                       lng,
                       radius,
                       tag_list
                   )
               ])
    else:
        return list([
                   product for product in products
                   if is_matching_product(
                       product,
                       lat,
                       lng,
                       radius
                   )
               ])


def is_matching_product(product, lat, lng, radius):
    """
     (Product, float, float, radius) -> boolean

     Check if the coordinates of a shop is within a radius
     (in meters) using the Vincenty's formulae.
    """
    return vincenty(
               (lat, lng),
               (product.shop.lat, product.shop.lng)
           ).meters <= radius


def is_matching_product_with_tags(product, lat, lng, radius, tags):
    """
     (Product, float, float, radius, list) -> boolean

     Check if the coordinates of a shop is within a radius
     (in meters) using the Vincenty's formulae and if the shop
     contains any of the tags provided.
    """
    return vincenty(
               (lat, lng),
               (product.shop.lat, product.shop.lng)
           ).meters <= radius and any(tag in product.shop.tags for tag in tags)

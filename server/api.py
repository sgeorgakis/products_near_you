# -*- coding: utf-8 -*-

import logging

from flask import Blueprint, current_app, jsonify, request
from flask_cors import cross_origin

import server.db
from server.exceptions import InvalidParameterException
import server.product_filter as product_filter


api = Blueprint('api', __name__)
log = logging.getLogger(__name__)


@api.route('/search', methods=['GET'])
@cross_origin()
def search():
    """
     Finds all the products that match the request arguments,
     sorts them by popularity and returns the number of products
     that was requested.
     If there is an error in an argument,
     an InvalidParameterException is raised.
    """

    products = current_app.products

    try:
        count = int(request.args.get('count'))
    except ValueError as e:
        log.error('Error while trying to cast count argument to int. {}'
                  .format(e))
        raise InvalidParameterException('Parameter {} is invalid'
                                        .format('count'))
    try:
        radius = int(request.args.get('radius'))  # radius in meters
    except ValueError as e:
        log.error('Error while trying to cast count argument to int. {}'
                  .format(e))
        raise InvalidParameterException('Parameter {} is invalid'
                                        .format('radius'))
    try:
        lat = float(request.args.get('lat'))
    except ValueError as e:
        log.error('Error while trying to cast lat argument to float. {}'
                  .format(e))
        raise InvalidParameterException('Parameter {} is invalid'
                                        .format('lat'))
    try:
        lng = float(request.args.get('lng'))
    except ValueError as e:
        log.error('Error while trying to cast lng argument to float. {}'
                  .format(e))
        raise InvalidParameterException('Parameter {} is invalid'
                                        .format('lng'))
    tags = request.args.get('tags')

    log.debug('Request with arguments ' +
              'count: {}, radius: {}, lat: {}, lng: {}, tags: {}'
              .format(count, radius, lat, lng, tags))
    matching_products = product_filter.get_matching_products(
                            products,
                            lat,
                            lng,
                            radius,
                            tags
                        )

    log.debug('Found {} matching products'
              .format(len(matching_products)))
    log.debug('Sorting products by popularity...')
    matching_products.sort(key=lambda product: product.popularity,
                           reverse=True)
    return jsonify({'products': matching_products[:count]})


@api.errorhandler(InvalidParameterException)
def handle_invalid_usage(error):
    """
     (Exception) -> response_class

     Handles InvalidParameterException.
     A bad request status code is returned
     with a message containing the name of the invalid parameter
     in json encoding.
    """
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

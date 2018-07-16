# -*- coding: utf-8 -*-

from geopy.distance import vincenty
from flask import request

from . import conftest

stockholm_lat = 59.33258
stockholm_lng = 18.0649


class TestInvalidParameters(object):

    def test_invalid_count_parameter(self, app):
        with conftest.client(app, None) as client:
            url = '/search?count=aa&radius=10&lng=0&lat=0'

            response = conftest.get(client)(url)
            assert request.args['count'] == 'aa'
            assert request.args['radius'] == '10'
            assert request.args['lat'] == '0'
            assert request.args['lng'] == '0'
            assert response.json['message'] == 'Parameter count is invalid'
            assert response.status_code == 400

    def test_invalid_radius_parameter(self, app):
        with conftest.client(app, None) as client:
            url = '/search?count=10&radius=a&lng=0&lat=0'

            response = conftest.get(client)(url)
            assert request.args['count'] == '10'
            assert request.args['radius'] == 'a'
            assert request.args['lat'] == '0'
            assert request.args['lng'] == '0'
            assert response.json['message'] == 'Parameter radius is invalid'
            assert response.status_code == 400

    def test_invalid_radius_parameter(self, app):
        with conftest.client(app, None) as client:
            url = '/search?count=10&radius=500&lng=a&lat=0'

            response = conftest.get(client)(url)
            assert request.args['count'] == '10'
            assert request.args['radius'] == '500'
            assert request.args['lat'] == '0'
            assert request.args['lng'] == 'a'
            assert response.json['message'] == 'Parameter lng is invalid'
            assert response.status_code == 400

    def test_invalid_radius_parameter(self, app):
        with conftest.client(app, None) as client:
            url = '/search?count=10&radius=500&lng=0&lat=a'

            response = conftest.get(client)(url)
            assert request.args['count'] == '10'
            assert request.args['radius'] == '500'
            assert request.args['lat'] == 'a'
            assert request.args['lng'] == '0'
            assert response.json['message'] == 'Parameter lat is invalid'
            assert response.status_code == 400


class TestAppResponses(object):

    def test_products_not_found(self, app):
        with conftest.client(app, None) as client:
            url = '/search?count=10&radius=10&lng=0&lat=0'

            response = conftest.get(client)(url)
            assert request.args['count'] == '10'
            assert request.args['radius'] == '10'
            assert request.args['lat'] == '0'
            assert request.args['lng'] == '0'
            assert response.status_code == 200
            assert len(response.json['products']) == 0

    def test_find_products__without_tags(self, app):
        with conftest.client(app, None) as client:
            url = '/search?radius=500&lat={}&lng={}&count=10'.format(
                  stockholm_lat,
                  stockholm_lng)

            response = conftest.get(client)(url)
            assert request.args['count'] == '10'
            assert request.args['radius'] == '500'
            assert request.args['lat'] == str(stockholm_lat)
            assert request.args['lng'] == str(stockholm_lng)
            is_valid_response(stockholm_lat, stockholm_lng, 10, 500, response)

    def test_find_products__with_tag(self, app):
        with conftest.client(app, None) as client:
            tag = 'home'
            url = '/search?radius=500&lat={}&lng={}&count=10&tags={}'.format(
                   stockholm_lat,
                   stockholm_lng,
                   tag)

            response = conftest.get(client)(url)
            assert request.args['count'] == '10'
            assert request.args['radius'] == '500'
            assert request.args['lat'] == str(stockholm_lat)
            assert request.args['lng'] == str(stockholm_lng)
            assert request.args['tags'] == tag
            is_valid_response(stockholm_lat, stockholm_lng, 10, 500, response)
            for product in response.json['products']:
                assert tag in product['shop']['tags']

    def test_find_products__with_many_tags(self, app):
        with conftest.client(app, None) as client:
            tags = 'home,shirts'
            url = '/search?radius=500&lat={}&lng={}&count=10&tags={}'.format(
                  stockholm_lat,
                  stockholm_lng,
                  tags)

            response = conftest.get(client)(url)
            assert request.args['count'] == '10'
            assert request.args['radius'] == '500'
            assert request.args['lat'] == str(stockholm_lat)
            assert request.args['lng'] == str(stockholm_lng)
            assert request.args['tags'] == tags
            is_valid_response(stockholm_lat, stockholm_lng, 10, 500, response)
            for product in response.json['products']:
                assert any(tag in product['shop']['tags']
                           for tag in tags.split(','))


def is_valid_response(lat, lng, count, radius, response):
    assert response.status_code == 200
    assert len(response.json['products']) == 10
    for product in response.json['products']:
        assert 'id' in product
        assert 'title' in product
        assert vincenty((lat, lng),
                        (product['shop']['lat'], product['shop']['lng'])
                        ).meters <= radius

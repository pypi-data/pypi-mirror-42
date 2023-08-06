#!/usr/bin/env python

# -*- coding: utf-8 -*-
# Copyright 2017-2018 CS Systemes d'Information (CS SI)
# All rights reserved

from __future__ import absolute_import, unicode_literals

import os
import sys
from collections import namedtuple
from functools import wraps

import dateutil.parser
import flask
import markdown
from flask import Markup, jsonify, make_response, render_template, request

import eodag
from eodag.api.core import DEFAULT_ITEMS_PER_PAGE, DEFAULT_PAGE
from eodag.api.search_result import SearchResult
from eodag.plugins.crunch.filter_latest_intersect import FilterLatestIntersect
from eodag.plugins.crunch.filter_latest_tpl_name import FilterLatestByName
from eodag.plugins.crunch.filter_overlap import FilterOverlap
from eodag.utils.exceptions import (
    MisconfiguredError, UnsupportedProductType, UnsupportedProvider, ValidationError,
)


app = flask.Flask(__name__)
app.config.from_object('eodag.rest.settings')
# Allows to override settings from a json file
app.config.from_json('eodag_server_settings.json', silent=True)

eodag_api = eodag.EODataAccessGateway(user_conf_file_path=app.config['EODAG_CFG_FILE'])
Cruncher = namedtuple('Cruncher', ['clazz', 'config_params'])
crunchers = {
    'latestIntersect': Cruncher(FilterLatestIntersect, []),
    'latestByName': Cruncher(FilterLatestByName, ['name_pattern']),
    'overlap': Cruncher(FilterOverlap, ['minimum_overlap']),
}


def _get_date(date):
    """Check if the input date can be parsed as a date"""
    if date:
        app.logger.info('checking input date: %s', date)
        try:
            date = dateutil.parser.parse(date).isoformat()
        except ValueError as e:
            exc = ValidationError('invalid input date: %s' % e)
            app.logger.error(exc.message)
            raise exc
        app.logger.info('successfully parsed date: %s', date)
    return date


def _get_int(val):
    """Check if the input can be parsed as an integer"""
    if val:
        try:
            val = int(val)
        except ValueError as e:
            raise ValidationError('invalid input integer value: %s' % e)
        app.logger.info('successfully parsed integer: %s', val)
    return val


def _get_pagination_info():
    page = _get_int(request.args.get('page', DEFAULT_PAGE))
    items_per_page = _get_int(request.args.get('itemsPerPage', DEFAULT_ITEMS_PER_PAGE))
    if page is not None and page < 0:
        raise ValidationError('invalid page number. Must be positive integer')
    if items_per_page is not None and items_per_page < 0:
        raise ValidationError('invalid number of items per page. Must be positive integer')
    return page, items_per_page


def _search_bbox():
    search_bbox = None
    search_bbox_keys = ['lonmin', 'latmin', 'lonmax', 'latmax']
    request_bbox = request.args.get('box')

    if request_bbox:

        try:
            request_bbox_list = [float(coord) for coord in request_bbox.split(',')]
        except ValueError as e:
            raise ValidationError('invalid box coordinate type: %s' % e)

        search_bbox = dict(zip(search_bbox_keys, request_bbox_list))
        if len(search_bbox) != 4:
            raise ValidationError('input box is invalid: %s' % request_bbox)
        app.logger.info('search bounding box is: %s', search_bbox)

    else:
        app.logger.debug('box request param not set')

    return search_bbox


def _filter(products, **kwargs):
    filter = request.args.get('filter')
    if filter:
        app.logger.info('applying "%s" filter on search results', filter)
        cruncher = crunchers.get(filter)
        if not cruncher:
            return jsonify({'error': 'unknown filter name'}), 400

        cruncher_config = dict()
        for config_param in cruncher.config_params:
            config_param_value = request.args.get(config_param)
            if not config_param_value:
                raise ValidationError('filter additional parameters required: %s'
                                      % ', '.join(cruncher.config_params))
            cruncher_config[config_param] = config_param_value

        try:
            products = products.crunch(cruncher.clazz(cruncher_config), **kwargs)
        except MisconfiguredError as e:
            raise ValidationError(e)

    return products


def _format_product_types(product_types):
    """Format product_types

    :param list product_types: A list of EODAG product types as returned by the core api
    """
    result = []
    for pt in product_types:
        result.append('* *__{ID}__*: {desc}'.format(**pt))
    return '\n'.join(sorted(result))


def cross_origin(request_handler):
    @wraps(request_handler)
    def wrapper(*args, **kwargs):
        resp = make_response(request_handler(*args, **kwargs))
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp

    return wrapper


@app.route('/<product_type>/', methods=['GET'])
@cross_origin
def search(product_type):
    try:
        page, items_per_page = _get_pagination_info()
        criteria = {
            'geometry': _search_bbox(),
            'startTimeFromAscendingNode': _get_date(request.args.get('dtstart')),
            'completionTimeFromAscendingNode': _get_date(request.args.get('dtend')),
            'cloudCover': _get_int(request.args.get('cloudCover')),
        }

        if items_per_page is None:
            items_per_page = DEFAULT_ITEMS_PER_PAGE
        if page is None:
            page = DEFAULT_PAGE
        products, total = eodag_api.search(product_type, page=page, items_per_page=items_per_page, raise_errors=True,
                                           **criteria)

        products = _filter(products, **criteria)
        response = SearchResult(products).as_geojson_object()
        response.update({
            'properties': {
                'page': page,
                'itemsPerPage': items_per_page,
                'totalResults': total
            }
        })
        return jsonify(response), 200
    except ValidationError as e:
        return jsonify({'error': e.message}), 400
    except RuntimeError as e:
        return jsonify({'error': e}), 400
    except UnsupportedProductType as e:
        return jsonify({'error': 'Not Found: {}'.format(e.product_type)}), 404
    except Exception as e:
        return jsonify({'error': 'Server error from provider: {}'.format(e)}), 500


@app.route('/', methods=['GET'])
@cross_origin
def home():
    with open(os.path.join(os.path.dirname(__file__), 'description.md'), 'rt') as fp:
        content = fp.read()
    content = content.format(
        base_url=request.base_url,
        product_types=_format_product_types(
            eodag_api.list_product_types()
        ),
        ipp=DEFAULT_ITEMS_PER_PAGE
    )
    content = Markup(markdown.markdown(content))
    return render_template('index.html', content=content)


@app.route('/product-types/', methods=['GET'])
@app.route('/product-types/<provider>', methods=['GET'])
@cross_origin
def list_product_types(provider=None):
    try:
        product_types = eodag_api.list_product_types() if provider is None else eodag_api.list_product_types(provider)
    except UnsupportedProvider:
        return jsonify({"error": "Unknown provider: %s" % (provider,)}), 400
    except Exception:
        return jsonify({"error": "Unknown server error"}), 500
    return jsonify(product_types)


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="""Script for starting EODAG server""",
        epilog=""""""
    )
    parser.add_argument('-d', '--daemon',
                        action='store_true', help='run in daemon mode')
    parser.add_argument('-a', '--all-addresses',
                        action='store_true',
                        help='run flask using IPv4 0.0.0.0 (all network interfaces), ' +
                             'otherwise bind to 127.0.0.1 (localhost). ' +
                             'This maybe necessary in systems that only run Flask')
    args = parser.parse_args()

    if args.all_addresses:
        bind_host = '0.0.0.0'
    else:
        bind_host = '127.0.0.1'

    if args.daemon:
        pid = None
        try:
            pid = os.fork()
        except OSError as e:
            raise Exception('%s [%d]' % (e.strerror, e.errno))

        if pid == 0:
            os.setsid()
            app.run(threaded=True, host=bind_host)
        else:
            sys.exit(0)
    else:
        # For development
        app.run(debug=True, use_reloader=True)


if __name__ == '__main__':
    main()

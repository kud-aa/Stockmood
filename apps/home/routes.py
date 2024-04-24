# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from apps.home import blueprint
from flask import render_template, request, jsonify
from flask_login import login_required
from jinja2 import TemplateNotFound
from apps.get_data import sqlHelper


@blueprint.route('/index')
@login_required
def index():
    obj = sqlHelper()
    stock_list = obj.get_stock_list()
    obj.close()
    return render_template('home/table.html', segment='table', stock_list=stock_list, selected='')

@blueprint.route('/<template>')
@login_required
def route_template(template):

    try:

        if not template.endswith('.html'):
            pass

        # Detect the current page
        segment = get_segment(request)
        obj = sqlHelper()
        stock_list = obj.get_stock_list()
        default_stock = stock_list[0]['Name']
        print(stock_list)
        stock_data = None
        obj.close()
        ###TODO: return amazon data for default visualizations
        

        # Serve the file (if exists) from app/templates/home/FILE.html
        return render_template("home/" + template, segment=segment, stock_list=stock_list, selected=default_stock, default_data=stock_data)

    except TemplateNotFound:
        return render_template('home/page-404.html'), 404

    except:
        return render_template('home/page-500.html'), 500

# Helper - Extract current page name from request
def get_segment(request):

    try:

        segment = request.path.split('/')[-1]

        if segment == '':
            segment = 'table'

        return segment

    except:
        return None

# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask_migrate import Migrate
from sys import exit
from decouple import config

from apps.config import config_dict
from apps import create_app, db
from flask import render_template, request, jsonify, current_app
from apps.get_data import sqlHelper
import matplotlib
matplotlib.use('Agg')

# WARNING: Don't run with debug turned on in production!
DEBUG = config('DEBUG', default=True, cast=bool)

# The configuration
get_config_mode = 'Debug' if DEBUG else 'Production'

try:

    # Load the configuration using the default values
    app_config = config_dict[get_config_mode.capitalize()]

except KeyError:
    exit('Error: Invalid <config_mode>. Expected values [Debug, Production] ')

app = create_app(app_config)
Migrate(app, db)

if DEBUG:
    app.logger.info('DEBUG       = ' + str(DEBUG))
    app.logger.info('Environment = ' + get_config_mode)
    app.logger.info('DBMS        = ' + app_config.SQLALCHEMY_DATABASE_URI)

@app.route('/get_stock_data', methods=['GET'])
def reload_visualizations():
    stock_id = request.args.get('selectedStockId')
    obj = sqlHelper()
    #heat_map = obj.get_heat_map_data(stock_id)
    bar_chart_positive, bar_chart_negative = obj.get_bar_chart_data(stock_id)
    word_cloud = obj.get_word_cloud_data(stock_id)
    time_line_trend = obj.get_time_line_data_trend(stock_id)
    time_line_avg_score = obj.get_time_line_data_avg_score(stock_id)
    tweet_display = obj.get_tweet_display_data(stock_id)
    emotion_graph = obj.get_emotion_graph_data(stock_id)
    
    obj.close()
    stock_data = {
        #'heat_map': heat_map,
        'bar_chart_positive': bar_chart_positive,
        'bar_chart_negative': bar_chart_negative,
        'word_cloud': word_cloud,
        'time_line_trend': time_line_trend,
        'time_line_avg_score': time_line_avg_score,
        'tweet_display': tweet_display,
        'emotion_display': emotion_graph
    }
    return jsonify(stock_data)

@app.route('/get_heat_map', methods=['GET'])
def get_heat_map():
    obj = sqlHelper()
    heat_map = obj.get_heat_map_data()
    obj.close()
    return jsonify(heat_map)

if __name__ == "__main__":
    app.run()

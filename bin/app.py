# -*- coding: utf-8 -*-
import os
from os import listdir
import sys
reload(sys)
sys.setdefaultencoding('UTF8')

from flask import Flask
from flask_bootstrap import Bootstrap
from flask.ext.sqlalchemy import SQLAlchemy
from flask import render_template, redirect
from flask import send_from_directory, request, Response
import re

app = Flask(__name__, static_folder="../data/", template_folder="../data/obj_html/")

@app.route('/')
def index():
    all_file_list = listdir("../data/obj_html")
    flash_list = [ f for f in all_file_list if re.search('flash_', f)]
    print str(flash_list)
    return render_template('flash.html', flash_list=flash_list)

@app.route('/<path:filename>')
def send_file(filename):
    return send_from_directory(app.static_folder, filename)


@app.route('/assets/swf/templates/tool_normal.swf')
def starter():
    return send_from_directory(app.static_folder, 'tool_normal.swf')

# @app.route('/upload/img/')
# def img_provider():
#     return send_from_directory(app.static_folder + "/creative/", 'tool_normal.swf')

app.run(debug=True, port=7777, host="0.0.0.0")

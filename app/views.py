#!/usr/bin/env python
# -*- coding=UTF-8 -*-
#*************************************************************************
#   Copyright © 2015 JiangLin. All rights reserved.
#   File Name: views.py
#   Author:JiangLin
#   Mail:xiyang0807@gmail.com
#   Created Time: 2016-03-18 20:19:52
#*************************************************************************
from flask import (jsonify,send_from_directory,render_template,
                   Blueprint,request,abort,Markup,
                   url_for,redirect)
from .forms import return_errors,QuestionForm,PhotoForm
from werkzeug import secure_filename
from app import app
import os
from time import time
from random import randint
import re

site = Blueprint('index', __name__)

def safe_clean(text):
    from flask import Markup
    from bleach import clean
    tags = ['b','i','font','br','blockquote']
    attrs = {
        '*':['style'],
        'font':['color']
    }
    styles = ['color']
    return Markup(clean(text,tags = tags,
                        attributes = attrs,
                        styles = styles))

@site.route('/')
def index():
    form = QuestionForm()
    fileform = PhotoForm()
    return render_template('editor.html',form=form,fileform=fileform)

@site.route('/preview', methods=['GET', 'POST'])
def preview():
    if request.method == "POST":
        from misaka import Markdown, HtmlRenderer
        choice = request.values.get('choice')
        content = request.values.get('content')
        if choice == 'Default':
            return safe_clean(content)
        else:
            html = HtmlRenderer()
            markdown = Markdown(html)
            return Markup(markdown(content))
    else:
        abort(404)

@site.route('/question', methods=['GET', 'POST'])
def question():
    form = QuestionForm()
    if form.validate_on_submit():
        content = form.content.data
        print(content)
        #  a = re.sub("""<img\s.*?\s?src\s*=\s*['|"]?([^\s'"]+).*?>""",'@sql',content)
        a = re.compile("""<img\s.*?\s?src\s*=\s*['|"]?([^\s'"]+)\s.*?\s?alt\s*=\s*['|"]?([^\s'"]+).*?>""")
        #  b = re.match(r"*<img\s+src=\"(?P<src>.*)\"\s+alt=\"(?P<alt>.*)\">*",'''<img src="/uploads/114583789086143" alt="photo">''')
        #  b = re.match(r"<img\s+src=\"(?P<src>.*)\"\s+alt=\"(?P<alt>.*)\".*?>",content)
        b = re.compile(r"^<img\s+src=\"(?P<src>.*)\"\s+alt=\"(?P<alt>.*)\".*?>")
        c = a.findall(content)
        print(c)
        return jsonify(judge=True,error='提交成功')
    else:
        if form.errors:
            return return_errors(form)
        else:
            return redirect(url_for('index.index'))

@site.route('/uploads', methods=('GET', 'POST'))
def upload():
    form = PhotoForm()
    if form.validate_on_submit():
        filename = secure_filename(form.photo.data.filename)
        filename ='1' + str(int(time())) + str(randint(1000,9999))
        print(filename)
        form.photo.data.save(os.path.join(app.static_folder,filename + '.png'))
        return jsonify(judge=True,error=filename)
    else:
        if form.errors:
            return return_errors(form)
        else:
            return jsonify(judge=False,error='上传失败')


@site.route('/uploads/<filename>')
def send_file(filename):
    filename = filename + '.png'
    return send_from_directory(app.static_folder,filename)



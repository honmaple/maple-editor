#*************************************************************************
#   Copyright © 2015 JiangLin. All rights reserved.
#   File Name: index.py
#   Author:JiangLin
#   Mail:xiyang0807@gmail.com
#   Created Time: 2015-11-25 02:21:04
#*************************************************************************
#!/usr/bin/env python
# -*- coding=UTF-8 -*-
from flask import (Blueprint, request, abort,
                   flash, Markup, jsonify,
                   redirect, url_for, send_from_directory)
from flask_login import current_user, login_required
from maple.question.models import Collector, Lover
from maple.main.filters import safe_clean
from maple.main.utils import random_gift, load_qid
from maple.main.models import RedisData
from maple.main.permissions import allow
from maple.question.forms import ReplyForm, PhotoForm
from maple.question.models import Replies
from maple.forms.forms import return_errors
from maple import db, app
from datetime import datetime
from werkzeug import secure_filename
import os

site = Blueprint('question', __name__)


@site.route('/preview', methods=['GET', 'POST'])
@login_required
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


@site.route('/uploads', methods=('GET', 'POST'))
def upload():
    form = PhotoForm()
    if form.validate_on_submit():
        filedata = form.photo.data
        print(filedata)
        filename = secure_filename(form.photo.data.filename)
        print(filename)
        form.photo.data.save(os.path.join(app.static_folder,filename))
        return jsonify(judge=True,error=filename)
    else:
        if form.errors is not None:
            return return_errors(form)
        else:
            return jsonify(judge=False,error='上传失败')


@site.route('/uploads/<filename>')
def send_file(filename):
    return send_from_directory(app.static_folder,filename)


@site.route('/collect', methods=['GET', 'POST'])
@login_required
def collect():
    if request.method == "POST":
        qid = request.values.get('qid')
        collect = Collector.load(qid, current_user.id)
        if collect is not None:
            db.session.delete(collect)
            db.session.commit()
            RedisData.set_collect(current_user, -1)
            return jsonify(judge=True)
        else:
            collect = Collector()
            collect.question_id = qid
            collect.user_id = current_user.id
            db.session.add(collect)
            db.session.commit()
            RedisData.set_collect(current_user, 1)
            return jsonify(judge=True)
    else:
        abort(404)


@site.route('/love', methods=['GET', 'POST'])
@login_required
def love():
    '''点赞'''
    if request.method == "POST":
        rid = request.values.get('rid')
        print(rid)
        love = Lover.load(rid, current_user.id)
        if love is not None:
            db.session.delete(love)
            db.session.commit()
            RedisData.set_love(current_user, -1)
            flash('成功取消赞')
            return jsonify(judge=True)
        else:
            love = Lover()
            love.reply_id = rid
            love.user_id = current_user.id
            db.session.add(love)
            db.session.commit()
            RedisData.set_love(current_user, 1)
            flash('赞成功')
            return jsonify(judge=True)
    else:
        abort(404)


@site.route('/reply', methods=['GET', 'POST'])
@login_required
@allow.requires('replies')
def reply():
    #  if not writer_permission.can():
        #  error = u'你尚未验证账户,不能回复'
        #  return jsonify(judge=False, error=error)
    error = None
    form = ReplyForm()
    if form.validate_on_submit() and request.method == "POST":
        qid = request.args.get('qid')
        qid = load_qid(qid)
        quote = request.get_json()['quote']
        #  question = Questions.load_by_id(qid)
        #  question.last_reply = current_user.name
        content = form.content.data.replace('\n', '<br>')
        reply = Replies(content=content,
                        quote=quote)
        reply.question_id = qid
        reply.author_id = current_user.id
        #  current_user.infor.score -= 1
        '''随机赠送'''
        random_gift()
        db.session.add(reply)
        db.session.commit()
        reply.question.last_author = current_user.name
        reply.question.last_time = datetime.now()
        db.session.commit()
        '''使用redis记录'''
        #  RedisData.set_replies(qid)
        #  if current_user.name != question.author:
        #  '''提醒'''
        #  user = User.load_by_name(question.author)
        #  RedisData.set_notice(user)
        return jsonify(judge=True, error=error)
    else:
        if form.content.errors:
            error = form.content.errors
            return jsonify(judge=False, error=error)
        else:
            return redirect(url_for('forums.forums'))


@site.route('/rreply', methods=['GET', 'POST'])
@login_required
def rreply():
    if request.method == "POST":
        rid = request.values.get('rid')
        reply = Replies.load_by_id(rid)
        if reply.quote is None:
            content = '<blockquote>引用了<b>%s</b> 的回复:<br>%s</blockquote>\n' % (
                reply.author.name, reply.content)
        else:
            content = '<blockquote>引用了<b>%s</b> 的回复:<br>%s%s</blockquote>\n' % (
                reply.author.name, reply.quote, reply.content)
        #  if current_user.name != reply.author:
            #  '''提醒'''
            #  user = User.get_by_name(reply.author)
            #  RedisData.set_notice(user)
        return content
    else:
        abort(404)

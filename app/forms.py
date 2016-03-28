#*************************************************************************
#   Copyright © 2015 JiangLin. All rights reserved.
#   File Name: askform.py
#   Author:JiangLin
#   Mail:xiyang0807@gmail.com
#   Created Time: 2015-11-27 17:54:07
#*************************************************************************
#!/usr/bin/env python
# -*- coding=UTF-8 -*-
from flask import jsonify
from flask_wtf import Form
from wtforms import TextAreaField,SelectField
from wtforms.validators import Required, Length
from flask_wtf.file import FileField, FileAllowed, FileRequired


def return_errors(form):
    for field, errors in form.errors.items():
        data = (u"%s %s" % (getattr(form, field).label.text, errors[0]))
        break
    return jsonify(judge=False, error=data)


class QuestionForm(Form):
    content = TextAreaField('问题:',
                            [Required(message='内容不能为空'),
                             Length(min=6,
                                    message=u'描述不能少于6个字符')])
    choice = SelectField('文本标记语法',
                         choices=[('Default', 'Default'),
                                  ('Markdown', 'Markdown')])


class PhotoForm(Form):
    photo = FileField('上传图片', validators=[FileRequired(message='不能为空'),
                                          FileAllowed(['jpg', 'png'],
                                                      '上传文件只能为图片且图片格式为jpg,png')])

#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 @Time    : 2017/9/11 14:09
 @Author  : Kiristingna
 @File    : apis.py
 @Software: PyCharm
"""
from utils.box_model import *
import web
import json
S = BOX_Model()

def get_type_cnt():
    return S.get_type_cnt()

def get_type_cnt_top5():
    return S.get_type_cnt_top5()

def get_type_cnt_last5():
    return S.get_type_cnt_last5()

def get_schedule_cnt():
    return S.get_schedule_cnt()

def get_year_cnt():
    return S.get_year_cnt()

def get_issequel_cnt():
    return S.get_issequel_cnt()

def get_type_box():
    return S.get_type_box()

def get_schedule_box():
    return S.get_schedule_box()

def get_year_box():
    return S.get_year_box()

def get_issequel_box():
    return S.get_issequel_box()

def get_actor_box():
    return S.get_actor_box()

def get_actor_cnt():
    return S.get_actor_cnt()

def get_actor_score():
    return S.get_actor_score()


def get_query_box():
    query = u'三生三世十里桃花'
    return S.get_query_box(query)

def post_query_box():
    data = web.data()
    payload = eval(data)
    moviename = str(payload["moviename"]).decode('utf8')
    return S.get_query_box(moviename)

def get_predict():
    dirlist = []
    actlist = [u'杨幂miniyang', u'李易峰yifengli']
    yr = 2017
    sd = 1
    return S.get_predict(dirlist, actlist, yr, sd)

def post_predict():
    data = web.data()
    payload = eval(data)
    dirlist = [x.decode('utf8') for x in payload['dirlist']]
    actlist = [x.decode('utf8') for x in payload['actlist']]
    yr = int(payload['year'])
    sd = int(payload['schedule'])
    return S.get_predict(dirlist, actlist, yr, sd)

def get_act_context():
    ac = u'杨幂miniyang'
    return S.get_act_context(ac)

def post_act_context():
    data = web.data()
    payload = eval(data)
    ac = str(payload["actorname"]).decode('utf8')
    return S.get_act_context(ac)

def get_act_pic():
    ac = u'杨幂miniyang'
    return S.get_act_pic(ac)

def post_act_pic():
    data = web.data()
    payload = eval(data)
    ac = str(payload["actorname"]).decode('utf8')
    return S.get_act_pic(ac)

def get_dir_context():
    dr = u'周星驰stephenchow'
    return S.get_dir_context(dr)

def post_dir_context():
    data = web.data()
    payload = eval(data)
    ac = str(payload["directorname"]).decode('utf8')
    return S.get_dir_context(ac)

def get_dir_pic():
    dr = u'周星驰stephenchow'
    return S.get_dir_pic(dr)

def post_dir_pic():
    data = web.data()
    payload = eval(data)
    ac = str(payload["directorname"]).decode('utf8')
    return S.get_dir_pic(ac)


def get_actor_list():
    return S.get_actor_list()

def get_actor_list_similar():
    return S.get_actor_list_similar()

def get_similar_actor():
    acname=u'\u5434\u4eacjingwu'
    return S.Similaractor(acname)

def post_similar_actor():
    data = web.data()
    payload = eval(data)
    ac = str(payload["actorname"]).decode('utf8')
    return S.Similaractor(ac)

def get_director_list():
    return S.get_director_list()

def get_sentence_analysis():
    moviename = u'建军大业'
    sentence = u'鹿哥演的真的很不错啊，张艺兴也棒棒哒，刘烨社长也是帅炸了'
    return S.get_sentence_analysis(moviename,sentence)

def post_sentence_analysis():
    data = web.data()

    payload = eval(data)

    moviename = str(payload["moviename"]).decode('utf8')
    sentence = str(payload["sentence"]).decode('utf8')

    return S.get_sentence_analysis(moviename,sentence)


# - * - coding: utf-8 - * - -
'''
@ Author: Tinkle G
'''
import re
import pandas as pd
import collections
import numpy as np

def load(path):
    import json
    with open(path,'r') as json_file:
        data = json.load(json_file)
        return data


event = pd.read_csv('events.csv', sep='|', encoding='utf8')
film_data = load('filmdata.json')
actor_data = load('actor.json')
weibo =  pd.read_csv('weibo.csv', sep='|', encoding='utf8')

def cal_contributer(moviename):
    for film in film_data:
        if film['name'] == moviename:
            actors = film['actors']

    # step1 : 主创吸引力质量系数
    for actor in actors:
        if actor in actor_data:
            ac = re.sub('[a-zA-z]+', '', actor)
            act_score = 0.5 * actor_data[actor]['sc'] + 0.5 * actor_data[actor]['gsc']
            print ac, act_score

    # step2 : 媒体主创曝光率
    # step3 : 社交网络讨论度
    event_contribution = collections.defaultdict(float)
    weibo_contribution = collections.defaultdict(float)
    e_sum_ = 0
    w_sum_ = 0
    for wk in range(5):
        contribution = collections.defaultdict(list)
        ct = event['count'][event.movieName == moviename][event.week == wk].tolist()
        nm = event['name'][event.movieName == moviename][event.week == wk].tolist()
        e_sum_ = e_sum_+sum(ct)
        for c, n in zip(ct, nm):
            event_contribution[n] += c
        ct = weibo['count'][weibo.movieName == moviename][weibo.week == wk].tolist()
        nm = weibo['name'][weibo.movieName == moviename][weibo.week == wk].tolist()
        w_sum_ = w_sum_ + sum(ct)
        for c, n in zip(ct, nm):
            weibo_contribution[n] += c
        for n in event_contribution:
            contribution[n]+=[event_contribution[n]/e_sum_]
        for n in weibo_contribution:
            contribution[n]+=[weibo_contribution[n]/w_sum_]
        print wk
        for a in contribution:
            print a,np.mean(contribution[a])


moviename = u'三生三世十里桃花'
cal_contributer(moviename)
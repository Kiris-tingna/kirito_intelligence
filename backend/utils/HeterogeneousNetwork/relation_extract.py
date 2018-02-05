#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 @Time    : 2018/1/11 19:56
 @Author  : Kiristingna
 @File    : relation_extract.py
 @Software: PyCharm
"""
import pandas as pd
import collections
import pickle

os_path = '../../../data/'

def network_generate():
    films = pd.read_json(os_path+'filmdata.json')

    index_number = 0
    actors_dict = collections.OrderedDict()
    directors_dict = collections.OrderedDict()
    movie_dict = collections.OrderedDict()

    actors = films['actors'].values
    for atrs in actors:
        for a in atrs:
            if a not in actors_dict:
                actors_dict[a] = index_number
                index_number += 1

    directors = films['director'].values
    for dtrs in directors:
        for d in dtrs:
            if d not in directors_dict:
                directors_dict[d] = index_number
                index_number += 1

    movies = films['name'].values
    for m in movies:
        if m not in movie_dict:
            movie_dict[m] = index_number
            index_number += 1

    years = films['year'].values

    df = [pd.DataFrame({"name": list(actors_dict.keys()), "group": 1, "order": list(actors_dict.values())}),
          pd.DataFrame({"name": list(directors_dict.keys()), "group": 2, "order": list(directors_dict.values())}),
          pd.DataFrame({"name": list(movies), "group": 3, "order": list(movie_dict.values())})]

    # all objects in films
    objects = pd.concat(df)

    links = []

    # all link information in films
    for i, j, k, y in zip(actors, directors, movies, years):
        for a in i:
            links.append({"source": int(objects[(objects['group'] == 1) & (objects['name'] == a)]['order']), "target": int(objects[(objects['group'] == 3) & (objects['name'] == k)]['order']), "year": y})
        for d in j:
            links.append({"source": int(objects[(objects['group'] == 2) & (objects['name'] == d)]['order']), "target": int(objects[(objects['group'] == 3) & (objects['name'] == k)]['order']), "year": y})

    relation = pd.DataFrame(links)

    # restore
    objects.to_json('../data/networks/nodes.json', orient='records')
    relation.to_json('../data/networks/links.json', orient='records')


def bi_network_generate():
    films = pd.read_json(os_path+'filmdata.json')

    index_number = 0
    actors_dict = collections.OrderedDict()
    directors_dict = collections.OrderedDict()
    movie_dict = collections.OrderedDict()
    type_dict = collections.OrderedDict()

    actors_number, directors_number, movie_number, type_number = 0, 0, 0, 0
    # ------------1----------------
    actors = films['actors'].values
    for atrs in actors:
        for a in atrs:
            if a not in actors_dict:
                actors_dict[a] = index_number
                index_number += 1

    j = pickle.dumps(actors_dict)
    f = open(os_path+'actors', 'wb')
    f.write(j)
    f.close()
    actors_number = index_number
    # ------------2----------------
    directors = films['director'].values
    index_number = 0
    for dtrs in directors:
        for d in dtrs:
            if d not in directors_dict:
                directors_dict[d] = index_number
                index_number += 1
    directors_number = index_number
    # ------------3----------------
    movies = films['name'].values
    index_number = 0
    for m in movies:
        if m not in movie_dict:
            movie_dict[m] = index_number
            index_number += 1
    movie_number = index_number
    # ------------4----------------
    types = films['type'].apply(lambda x: x.split('/')).values
    index_number = 0
    for ts in types:
        for t in ts:
            if t not in type_dict:
                type_dict[t] = index_number
                index_number += 1
    type_number = index_number


    # ------------5----------------
    df = [pd.DataFrame({"name": list(actors_dict.keys()), "group": 1, "order": list(actors_dict.values())}),
           pd.DataFrame({"name": list(directors_dict.keys()), "group": 2, "order": list(directors_dict.values())}),
           pd.DataFrame({"name": list(movies), "group": 3, "order": list(movie_dict.values())}),
           pd.DataFrame({"name": list(type_dict.keys()), "group": 4, "order": list(type_dict.values())})
           ]
    # # all objects in films
    objects = pd.concat(df)
    am_links = []
    dm_links = []
    tm_links = []
    # # all link information in films
    for i, j, k, l in zip(actors, directors, movies, types):
        for a in i:
            am_links.append({"source": int(objects[(objects['group'] == 1) & (objects['name'] == a)]['order']),
                           "target": int(objects[(objects['group'] == 3) & (objects['name'] == k)]['order'])})
        for d in j:
            dm_links.append({"source": int(objects[(objects['group'] == 2) & (objects['name'] == d)]['order']),
                           "target": int(objects[(objects['group'] == 3) & (objects['name'] == k)]['order'])})
        for t in l:
            tm_links.append({"source": int(objects[(objects['group'] == 4) & (objects['name'] == t)]['order']),
                           "target": int(objects[(objects['group'] == 3) & (objects['name'] == k)]['order'])})

    am = pd.DataFrame(am_links)
    am.to_csv(os_path+'AM.csv', encoding='utf-8', index=None)
    dm = pd.DataFrame(dm_links)
    dm.to_csv(os_path+'DM.csv', encoding='utf-8', index=None)
    tm = pd.DataFrame(tm_links)
    tm.to_csv(os_path+'TM.csv', encoding='utf-8', index=None)

    # ------------6----------------
    pd.DataFrame({'actors': actors_number, 'directors': directors_number, 'movies': movie_number, 'types': type_number}, index=[0])\
        .to_csv(os_path+'network_information.csv', encoding='utf-8', index=None)

if __name__ == '__main__':
    # 抽取力学导向图网络的结构
    # network_generate()

    # 双类别的网络存放
    bi_network_generate()


#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 @Time    : 2018/1/23 17:54
 @Author  : Kiristingna
 @File    : pathsim.py
 @Software: PyCharm
"""
import numpy as np
import pandas as pd
from scipy import sparse
import time
import pickle
import json



def sparse_matrix(link_file, type_nodes, movie_nodes):
    """
    function to construct a single sparse matrix
    :param link_file: link matrix file
    :param type_nodes: featured node length
    :param movie_nodes: movie length
    :return:
    """
    # link matrix
    matrix = np.zeros((type_nodes, movie_nodes), dtype=np.int)

    # construct matrix
    links = pd.read_csv(link_file)
    for index, row in links.iterrows():
        matrix[row['source']][row['target']] = 1
    sparse_link_matrix = sparse.csc_matrix(matrix)
    return sparse_link_matrix, sparse.csc_matrix.transpose(sparse_link_matrix)

def pathsim(query, hin, k, entities):
    """
    :param query: query entity
    :param hin: multi layer heterogeneous network
    :param k: top-k result
    :param num: number of entities with same query type
    :return: rank list
    """
    rank = []

    for i in range(entities):
        value = 2.0 * hin[query, i] / (hin[query, query] + hin[i, i])
        rank.append((value, querys[i]))

    rank.sort()
    rank.reverse()
    return rank[1:k+1]

def SimiliarActor(acname):
    #{'label':'type','value':}
    idx = querys.index(acname)
    ans = []
    ret = []
    for vals in pathsim(idx, AMTMA, 5, acts):
        ret.append({'name':vals[1],'val':vals[0]})
    ans.append({'label': 'types', 'value':ret[:]})
    ret = []
    for vals in pathsim(idx, AMDMA, 5, acts):
        ret.append({'name': vals[1], 'val': vals[0]})
    ans.append({'label': 'directors', 'value':ret[:]})
    return json.dumps(ans,indent=4)

def ActorsList():
    ret = {'name': 'actorList', 'value': querys}
    return json.dumps(ret, indent=4)

os_path = '../data/'
f = open(os_path + 'actors', 'rb')
data = pickle.loads(f.read())  # 等价于data=pickle.load(f)
querys = data.keys()

information = pd.read_csv(os_path + 'network_information.csv')
am_file = os_path + "AM.csv"
dm_file = os_path + "DM.csv"
tm_file = os_path + "TM.csv"

acts = information['actors'][0]
dirs = information['directors'][0]
movs = information['movies'][0]
typs = information['types'][0]

start = time.time()
# construct bi type network
AM, MA = sparse_matrix(am_file, acts, movs)
DM, MD = sparse_matrix(dm_file, dirs, movs)
TM, MT = sparse_matrix(tm_file, typs, movs)

AMTMA = (AM * MT * TM * MA).todense()
AMDMA = (AM * MD * DM * MA).todense()

#print('types', pathsim(0, AMTMA, 5, acts))

if __name__ == '__main__':
    # network basic information
    # mid = time.time()
    # print('types', pathsim(0, AMTMA, 5, acts))
    # print('directors', pathsim(0, AMDMA, 5, acts))
    # end = time.time()
    # print("Time:generate MP matrix:{}s \t PathSim:{}s".format(round(mid - start, 4), round(end - mid, 4)))
    acname = querys[10]
    # print SimiliarActor(acname)
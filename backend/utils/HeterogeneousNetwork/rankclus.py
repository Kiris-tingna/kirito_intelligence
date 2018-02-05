#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 @Time    : 2018/1/23 13:17
 @Author  : Kiristingna
 @File    : rankclus.py
 @Software: PyCharm
"""
import numpy as np
import pandas as pd
from scipy import sparse


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


if __name__ == '__main__':
    # network basic information
    os_path = '../../../data/'
    information = pd.read_csv(os_path+'network_information.csv')
    am_file = os_path+"AM.csv"
    dm_file = os_path+"DM.csv"
    tm_file = os_path+"TM.csv"

    acts = information['actors'][0]
    dirs = information['directors'][0]
    movs = information['movies'][0]
    typs = information['types'][0]

    # construct bi type network
    AM, MA = sparse_matrix(am_file, acts, movs)
    DM, MD = sparse_matrix(dm_file, dirs, movs)
    TM, MT = sparse_matrix(tm_file, typs, movs)

    AMTMA = (AM * MT * TM * MA).todense()
    AMDMA = (AM * MD * DM * MA).todense()
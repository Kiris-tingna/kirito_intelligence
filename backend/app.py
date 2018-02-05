#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 @Time    : 2017/9/11 13:53
 @Author  : Kiristingna
 @File    : app.py
 @Software: PyCharm
"""

import web
import apis


def cors_middleware(handler):
    web.header('Access-Control-Allow-Origin', "*")
    web.header("Access-Control-Allow-Methods", "POST, GET, OPTIONS, PUT, DELETE")
    web.header("Access-Control-Allow-Headers", "Accept, Content-Type, Content-Length, Accept-Encoding,"
                                               " X-CSRF-Token, Authorization")

    result = handler()
    return result

mapping = (
    "/api/GetPredict",apis.get_predict,
    "/api/GetActContext",apis.get_act_context,
    "/api/GetActPic",apis.get_act_pic,
    "/api/GetDirContext",apis.get_dir_context,
    "/api/GetDirPic",apis.get_dir_pic,
    "/api/ActorList",apis.get_actor_list,
    "/api/DirectorList",apis.get_director_list,
    "/api/SentenceAnalysis",apis.get_sentence_analysis,
    "/api/PostAnalysis", apis.post_sentence_analysis,
    "/api/PostActorContext",apis.post_act_context,
    "/api/PostPredict",apis.post_predict,
    "/api/PostActorPic",apis.post_act_pic,
    "/api/PostDirectorContext",apis.post_dir_context,
    "/api/PostDirectorPic",apis.post_dir_pic,
    "/api/ActorListSim",apis.get_actor_list_similar,
    "/api/GetSimAct",apis.get_similar_actor,
    "/api/PostSimAct",apis.post_similar_actor,



)

if __name__ == "__main__":
    app = web.subdir_application(mapping)
    app.add_processor(cors_middleware)
    app.run()
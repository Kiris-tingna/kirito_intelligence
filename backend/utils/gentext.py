# - * - coding: utf-8 - * - -
'''
@ Author : Tinkle G
'''

def gen_dir_text(dr, content):
    r_text = []
    text = u'导演 ' + dr
    if content['award'] == 1:
        text += u',是一名获得过中国大陆／台湾／香港的电影最佳导演奖或者近5年来指导超过5部电影的导演\r\n'
    elif content['award'] == 2:
        text += u',跨界导演，是一名有超过300万粉丝基础的演员\r\n'
    elif content['award'] == 2:
        text += u',跨界导演，是一名有超过300万粉丝基础的娱乐圈人士\r\n'
    else:
        text += '\r\n'
    text += '\r\n'

    text += u'该名导演在' + str(len(content['tplist'])) + u'种题材有所涉猎，分别是\r\n'
    for i in sorted(content['tplist'], key=lambda x: x[1], reverse=True):
        text += i[0] + ' ' + str(i[1]) + u'部, '
    text += '\r\n\n'
    #r_text.append(text)

    #text = ''
    text += u'在2012至2017年间，共指导了' + str(content['nm']) + u'部电影\r\n\n'
    r_text.append(text)
    for i in content['film_details']:
        text = ''
        text += str(i[2]) + u'年导演作品《' + i[0] + u'》，票房'
        if i[4] / 10000 > 1:
            text += str(i[4] / 10000) + u'亿'
        else:
            text += str(i[4]) + u'万'
        text += u', 票房得分为 ' + str(i[3])
        text += u', 口碑得分为 ' + str(i[5]) + '\r\n\n'
        #r_text.append(text)
        # i[3],i[4]
    #r_text.append(text)
    text = ''
    text += u'\r\n从电影票房成绩来看, ' + u'指导电影的平均票房得分为' + str(content['sc']) + '   '
    if content['sc'] <= 6:
        text += u'不甚理想'
    elif content['sc'] <= 7.5:
        text += u'表现一般'
    elif content['sc'] <= 8.5:
        text += u'表现尚可'
    elif content['sc'] <= 9:
        text += u'表现较好'
    else:
        text += u'表现优秀'
    if content['nm'] >= 3:
        text += u'\r\n波动指数为: ' + str(content['std'])
        if content['std'] >= 0.95:
            text += u', 反映出该名导演在近五年指导电影的票房质量不是很能保障\r\n'
        else:
            text += u', 反映出该名导演在近五年指导电影的票房质量能够保障\r\n'
    text += '\r\n'

    text += u'\r\n从电影口碑成绩来看, ' + u'指导电影的口碑得分为' + str(content['gsc']) + '   '
    if content['gsc'] <= 6:
        text += u'不甚理想'
    elif content['gsc'] <= 7.5:
        text += u'表现一般'
    elif content['gsc'] <= 8.5:
        text += u'表现尚可'
    elif content['gsc'] <= 9:
        text += u'表现较好'
    else:
        text += u'表现优秀'
    if content['nm'] >= 3:
        text += u'\r\n波动指数为: ' + str(content['gstd'])
        if content['gstd'] >= 0.95:
            text += u', 反映出该名导演在近五年指导电影的口碑波动较大\r\n'
        else:
            text += u', 反映出该名导演在近五年指导电影的口碑波动较小\r\n'
    r_text.append(text)
    return r_text

def gen_act_text(dr, content):
    r_text = []
    text = u'演员 ' + dr
    if content['award'] == 1:
        text += u',是一名获得过中国大陆／台湾／香港的电影最佳女演员／男演员奖的优秀演员\r\n'
    if content['fansnum']!=-1:
        text += u'\r\n该演员拥有'+str(content['fansnum'])+u'名微博粉丝, '
        if content['fans']==1:
            text +=u'是一名有着顶级流量的演员,在社交网络中有很大的影响力\r\n'
        else:
            text +=u'在社交网络中有的一定的影响力\r\n'
    text += '\r\n'
    text += u'该名演员在' + str(len(content['tplist'])) + u'种题材有所涉猎，分别是\r\n'
    for i in sorted(content['tplist'], key=lambda x: x[1], reverse=True):
        text += i[0] + ' ' + str(i[1]) + u'部, '
    text += '\r\n\n'

    #r_text.append(text)
    #text = ''
    text += u'在2012至2017年间，共主演了' + str(content['nm']) + u'部电影\r\n\n'
    r_text.append(text)
    for i in content['film_details_focus']:
        text += str(i[2]) + u'年主演作品《' + i[0] + u'》，票房'
        if i[4] / 10000 > 1:
            text += str(i[4] / 10000) + u'亿'
        else:
            text += str(i[4]) + u'万'
        text += u', 票房得分为 ' + str(i[3])
        text += u', 口碑得分为 ' + str(i[5]) + '\r\n'

        # i[3],i[4]

    #r_text.append(text)
    text = ''
    text += u'\r\n从电影票房成绩来看, ' + u'指导电影的平均票房得分为' + str(content['sc']) + '   '
    if content['sc'] <= 6:
        text += u'不甚理想'
    elif content['sc'] <= 7.5:
        text += u'表现一般'
    elif content['sc'] <= 8.5:
        text += u'表现尚可'
    elif content['sc'] <= 9:
        text += u'表现较好'
    else:
        text += u'表现优秀'
    text += '\r\n'

    if content['nm'] >= 3:
        text += u'波动指数为: ' + str(content['std'])
        if content['std'] >= 1.3:
            text += u', 反映出该名演员在近五年指导电影的票房质量不是很能保障\r\n'
        else:
            text += u', 反映出该名演员在近五年指导电影的票房质量能够保障\r\n'

    text += u'从电影口碑成绩来看, ' + u'指导电影的口碑得分为' + str(content['gsc']) + '   '
    if content['gsc'] <= 6:
        text += u'不甚理想'
    elif content['gsc'] <= 7.5:
        text += u'表现一般'
    elif content['gsc'] <= 8.5:
        text += u'表现尚可'
    elif content['gsc'] <= 9:
        text += u'表现较好'
    else:
        text += u'表现优秀'
    if content['nm'] >= 3:
        text += u'\r\n波动指数为: ' + str(content['gstd'])
        if content['gstd'] >= 1:
            text += u', 反映出该名演员在近五年参加电影的口碑波动较大\r\n'
        else:
            text += u', 反映出该名演员在近五年参加电影的口碑波动较小\r\n'
    r_text.append(text)
    return r_text

#ac = u'杨幂miniyang'
#print gen_act_text(ac, actor_new[ac])
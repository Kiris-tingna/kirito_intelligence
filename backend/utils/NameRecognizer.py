# - * - coding:utf-8  - * - -
'''
@ Author: Tinkle G
'''
from settings import *

def transfer(str_):
    str_ = ' '.join(str_.split('、'))
    str_ = ' '.join(str_.split('，'))
    str_ = ' '.join(str_.split('/'))
    str_ = ' '.join(str_.split('；'))
    return str_
def getname_act():
    flag = True
    data = {}
    with open(os_path+'actor_roles.txt','r') as lines:
        for line in lines:
            if flag:
                flag = False
            else:
                line = line.strip('\r\n')
                if line.split('|')[1]!='[]':
                    ret = []
                    name = line.split('|')[0]
                    tmp = line.split('|')[1]
                    tmp = re.sub('\[','',tmp)
                    tmp = re.sub('\]', '', tmp)
                    tmp = re.sub('\(', '', tmp)
                    tmp = re.sub('\)', '', tmp)
                    tmp = re.sub("\'", '', tmp)
                    tmp = re.sub('\xa0','',tmp)
                    tmp = tmp.split(',')
                    for i in range(len(tmp) / 2):
                        ret.append(tmp[2 * i + 1])

                    if line.split('|')[4]!='无':
                        ret.extend(transfer(line.split('|')[4]).split())
                    if line.split('|')[5] != '无':
                        ret.append(line.split('|')[5].strip())
                    data[name.decode('utf8')]=ret#[ix.decode('utf8') for ix in ret]
    return data
name_recognizer = getname_act()

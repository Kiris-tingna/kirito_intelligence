# - * - coding:utf-8  - * - -
'''
@ Author: Tinkle G
'''
from settings import *
import NameRecognizer
import BiLSTM
from HeterogeneousNetwork import pathsim

def getschedule(x):
    if x.month<=3:
        return 1
    if x.month<=5:
        return 2
    if x.month<=8:
        return 3
    if x.month<=10:
        return 4
    return 5

class BOX_Model(object):
    def __init__(self):
        self.film_data = pd.read_json(os_path+'filmdata.json')
        self.actor = json.load(open(os_path+'actor.json'))
        self.director = json.load(open(os_path + 'directors.json'))
        self.film_data['Issequel']=[random.randint(0,1) for i in range(len(self.film_data))]
        self.film_data['Schedule']=self.film_data.release_time.map(getschedule)

        self.review = pd.read_csv(os_path + 'review.csv', encoding='utf8')
        self.douban = pd.read_csv(os_path+'douban_score.csv',encoding='utf8')

        self.event = pd.read_csv(os_path+'events.csv', sep='|', encoding='utf8')
        self.weibo = pd.read_csv(os_path+'weibo.csv', sep='|', encoding='utf8')

        self.gen_type_cnt()
        self.generate_df = self.gen_model_weekly_metric()
        self.df = self.gen_model_metric()

    def transfer_json(self,dic):
        ans = []
        for d in dic:
            tmp = {}
            tmp['name']=d
            tmp['value']=dic[d]
            ans.append(tmp)
        ret = json.dumps(ans, indent=4)
        return ret

    ###############################################
    #                统计模块
    # get_type_cnt : 类型个数统计
    # get_type_box : 类型票房统计
    # get_type_cnt_top5 : 类型个数统计，返回top5
    # get_type_cnt_last5 : 类型个数统计，返回last5
    # get_year_cnt : 年份统计
    # get_year_box : 年份票房统计
    # get_actor_cnt : 演员统计
    # get_actor_box : 演员票房统计
    # get_actor_score : 演员口碑统计
    # get_issequel_cnt : 电影系列统计
    # get_issequel_box : 电影系列票房统计
    # get_schedule_cnt : 上映档期统计
    # get_schedule_box : 档期票房
    # get_grade_score : 票房——口碑
    #################################################

    def get_grade_score(self):
        '''
        :return:json
        '''
        ret = []
        for i in range(len(self.film_data)):
            tmp1 ={}
            tmp1['name'] = self.film_data.name[i]
            tmp1['value'] = self.film_data.grade_score[i]
            tmp2={}
            tmp2['name'] = self.film_data.name[i]
            tmp2['value'] = self.film_data.box_score[i]
            ret.append([tmp1,tmp2])
        return json.dumps(ret,indent=4)

    def gen_type_cnt(self):
        self.type_cnt = collections.defaultdict(int)
        for type_ in self.film_data.type:
            type_ = type_.split('/')
            for t in type_:
                self.type_cnt[t]+=1

    # 类型个数统计
    def get_type_cnt(self):
        '''
        :return: json
        '''
        return self.transfer_json(self.type_cnt)

    # 类型票房统计
    def get_type_box(self):
        '''
        :return: json
        '''
        dic = collections.defaultdict(list)
        type_box = collections.defaultdict(list)
        for box,type_ in zip(self.film_data.total_box,self.film_data.type):
            if not isinstance(type_,float):
                type_ = type_.split('/')
                for t in type_:
                    t = t.strip("'")
                    type_box[t] +=[box]
        for t_b in type_box:
            if len(type_box[t_b]) >= 5:
                dic[t_b] = type_box[t_b]
        return self.transfer_json(dic)

    # 类型个数统计，返回top5的类型
    def get_type_cnt_top5(self):
        '''
        :return:json
        '''
        type_box = collections.defaultdict(list)
        for box, type_ in zip(self.film_data.total_box, self.film_data.type):
            if not isinstance(type_, float):
                type_ = type_.split('/')
                for t in type_:
                    t = t.strip("'")
                    type_box[t] += [box]
        ans = sorted(type_box.items(),key=lambda x:len(x[1]),reverse=True)
        type_cnt = {}
        for i in range(5):
            type_cnt[ans[i][0]] = len(ans[i][1])
        return self.transfer_json(type_cnt)

    # 类型个数统计，返回last5的类型
    def get_type_cnt_last5(self):
        '''
        :return:json
        '''
        type_box = collections.defaultdict(list)
        for box, type_ in zip(self.film_data.total_box, self.film_data.type):
            if not isinstance(type_, float):
                type_ = type_.split('/')
                for t in type_:
                    t = t.strip("'")
                    type_box[t] += [box]
        ans = sorted(type_box.items(), key=lambda x: len(x[1]))
        type_cnt = {}
        for i in range(5):
            type_cnt[ans[i][0]] = len(ans[i][1])
        return self.transfer_json(type_cnt)

    # 年份统计
    def get_year_cnt(self):
        '''
        :return: json
        '''
        year_cnt = self.film_data.year.value_counts()
        data = {}
        for lb,count in zip(year_cnt.index,list(year_cnt)):
            if lb !=-1:
                data[lb] = count
        return self.transfer_json(data)

    # 年份票房统计
    def get_year_box(self):
        '''
        :return:json
        '''
        data = {}
        year_cnt = self.film_data.year.value_counts().index
        for lb in year_cnt:
            if lb!=-1:
                data[lb] = list(self.film_data.total_box[self.film_data.year==lb])
        return self.transfer_json(data)

    # 演员统计
    def get_actor_cnt(self):
        '''
        :return: json
        '''
        act_box = collections.defaultdict(list)
        for box, actors in zip(self.film_data.total_box, self.film_data.actors):
            for act in actors[0:min(4,len(actors))]:
                act_box[act]+=[box]

        ans = sorted(act_box.items(), key=lambda x:len(x[1]),reverse=True)
        ret = []
        i = 0
        while(len(ans) and i<20):
            tmp = {}
            tmp['name']=ans[i][0]+' / '+str(np.mean(ans[i][1]))
            tmp['value']=len(ans[i][1])
            ret.append(tmp)
            i+=1
        ret = json.dumps(ret, indent=4)
        return ret

    # 演员票房统计
    def get_actor_box(self):
        '''
        :return: json
        '''
        act_box = collections.defaultdict(list)
        for box, actors in zip(self.film_data.total_box, self.film_data.actors):
            for act in actors[0:min(4,len(actors))]:
                act_box[act]+=[box]

        return self.transfer_json(act_box)

    # 演员口碑统计
    def get_actor_score(self):
        '''
        :return: json
        '''
        act_box = collections.defaultdict(list)
        act_score= collections.defaultdict(list)

        for box, actors in zip(self.film_data.total_box, self.film_data.actors):
            for act in actors[0:min(4, len(actors))]:
                act_box[act] += [box]

        for grade, actors in zip(self.film_data.grade_score, self.film_data.actors):
            for act in actors[0:min(4, len(actors))]:
                act_score[act] += [grade]


        ans = sorted(act_score.items(), key=lambda x: np.mean(x[1]),reverse=True)
        ret = []
        i = 0
        while(i<20):
            tmp = {}
            tmp['name']=ans[i][0]+' / '+str(np.mean(act_box[ans[i][0]]))
            tmp['value']=len(ans[i][1])
            ret.append(tmp)
            i+=1
        ret = json.dumps(ret, indent=4)
        return ret

    # 电影系列统计
    def get_issequel_cnt(self):
        '''
        :return:json
        '''

        sequel_cnt = self.film_data.Issequel.value_counts()
        data = {}
        for lb,count in zip(sequel_cnt.index,list(sequel_cnt)):
            data[lb] = count
        return self.transfer_json(data)

    # 电影系列票房统计
    def get_issequel_box(self):
        '''
        :return:json
        '''
        data = {}
        sequel_cnt = self.film_data.Issequel.value_counts().index
        for lb in sequel_cnt:
            data[lb] = list(self.film_data.total_box[self.film_data.Issequel == lb])
        return self.transfer_json(data)

    # 上映档期统计
    def get_schedule_cnt(self):
        '''
        :return: json
        '''
        sch_dic = {1:u'贺岁档',2:u'五一档',3:u'暑假档',4:u'国庆档',5:u'其它'}
        schedule_cnt = self.film_data.Schedule.value_counts()
        data = {}
        for lb,count in zip(schedule_cnt.index,list(schedule_cnt)):
            if lb in sch_dic:
                data[sch_dic[lb]] = count
        return self.transfer_json(data)

    # 档期票房统计
    def get_schedule_box(self):
        '''
        :return:json
        '''
        data = {}
        sch_dic = {1: u'贺岁档', 2: u'五一档', 3: u'暑假档', 4: u'国庆档', 5: u'其它'}
        for lb in sch_dic:
            data[sch_dic[lb]] = list(self.film_data.total_box[self.film_data.Schedule==lb])
        return self.transfer_json(data)

    ###############################################
    #                信息获取模块
    # get_actor_list : 获取演员列表
    # get_director_list : 获取导演列表
    # get_movie_list :  获取电影列表
    ###############################################

    # 获取演员列表
    def get_actor_list(self):
        '''
        :return:
        '''
        query = []
        for actor in self.actor:
            if self.actor[actor]['award']==1 or len(self.actor[actor]['film_details_focus'])>=5 or \
                self.actor[actor]['fans']<2:
                query.append(actor)
        ret = {'name':'actor list','value':query}
        return json.dumps(ret,indent=4)

    def get_actor_list_similar(self):
        return pathsim.ActorsList()

    def Similaractor(self,acname=u'\u5434\u4eacjingwu'):
        return pathsim.SimiliarActor(acname)

    # 获取导演列表
    def get_director_list(self):
        '''
        :return:
        '''
        query = []
        for director in self.director:
            if self.director[director]['award'] !=0  or len(self.director[director]['film_details']) >= 5:
                query.append(director)
        ret = {'name': 'director list', 'value': query}
        return json.dumps(ret, indent=4)

    # 获取电影列表
    def get_movie_list(self):
        '''
        :return:
        '''
        ret = {'name': 'movie list', 'value': self.weibo['movieName'].unique().tolist()}
        return json.dumps(ret, indent=4)


    def get_query_box(self,query):  # To modify
        '''
        :return: json
        '''
        if query in self.film_data['name'].tolist():
            w1 = self.film_data['week_0'][self.film_data['name']==query].tolist()[0]
            w2 = self.film_data['week_1'][self.film_data['name'] == query].tolist()[0]
            w3 = self.film_data['week_2'][self.film_data['name'] == query].tolist()[0]
            w4 = self.film_data['week_3'][self.film_data['name'] == query].tolist()[0]
            ret=[{'name':u'上映第一周','value':w1},{'name':u'上映第二周','value':w2},
                 {'name':u'上映第三周','value':w3},{'name':u'上映第四周','value':w4}]
            return json.dumps(ret,indent=4)
        else:
            ret = [{'name':'error','value':u'您的输入有误'}]
            return json.dumps(ret,indent=4)


    ###############################################
    #                查询模块
    # get_contribute ： 查询一部电影的主创贡献度
    # get_sentence_analysis : 对输入句子进行命名实体识别和情感分析
    # get_act_context :
    # get_act_context : 获取演员画像
    # get_dir_context : 获取导演画像
    # get_act_pic : 获取演员历史趋势
    # get_dir_pic : 获取导演历史趋势
    ###############################################

    def reviewsmovies(self):
        ret = []
        for moviename in self.weibo.movieName.unique():
            ret.append({'label':moviename,'value':moviename})
        return json.dumps(ret, indent=4)

    def moviessentiment(self):
        from datetime import datetime
        MN = []
        DT = []
        STATE = []
        SC = []

        self.rawweibo = pd.read_csv(os_path + 'weibo_concrete.csv', encoding='utf8')

        ans = []
        for moviename in self.weibo.movieName.unique():
            datestampList = self.rawweibo.datestamp[self.rawweibo.moviename==moviename].unique()
            datestampList.sort()
            ret = []
            releaseTime = self.film_data['release_time'][self.film_data.name==moviename].tolist()[0]
            for d in datestampList:

                p5 = pd.to_datetime(datetime.strptime(d,'%Y-%m-%d'))
                delta = abs((p5-releaseTime).days)
                if delta<30:
                    score = self.rawweibo.score[self.rawweibo.datestamp==d]\
                    [self.rawweibo.moviename == moviename].tolist()
                    tmp = self.rawweibo.sentiment[self.rawweibo.datestamp == d] \
                        [self.rawweibo.moviename == moviename].tolist()

                    MN += [moviename]
                    DT += [d]
                    STATE += [0]
                    SC += [float(sum(tmp))*10/sum(score)]
                    MN += [moviename]
                    DT += [d]
                    STATE += [1]
                    SC += [float(len(tmp)-sum(tmp)) * 10 / sum(score)]

                    ret.append({'label':d,'value':float(sum(tmp))/sum(score)})
            ans.append({'name':moviename,'value':ret})
        data = {'name':MN,'timestamp':DT,'state':STATE,'score':SC}
        pd.DataFrame(data).to_csv(os_path+'sentiscore.csv',index=None,encoding='utf8')
        return json.dumps(ans, indent=4)

    # 查询一部电影的主创贡献度
    def get_contributelist(self):
        ret = []
        for moviename in self.weibo.movieName.unique():
            tmp = {}
            tmp['name']=moviename
            tmp['value']=self.get_contribute(moviename)
            ret.append(tmp)
        return json.dumps(ret, indent=4)

    def get_contribute(self,moviename):
        '''
        :return:
        '''

        #moviename = u'三生三世十里桃花'
        #print len(self.weibo.movieName.unique())

        if moviename not in self.film_data['name'].tolist():
            ret = [{'name':'null','value':u'您输入的参数有误'}]
            return json.dumps(ret, indent=4)
        else:

            actors =  self.film_data['actors'][self.film_data['name']==moviename].tolist()[0]
            directors = self.film_data['director'][self.film_data['name'] == moviename].tolist()[0]

            creator = collections.defaultdict(list)

            names = collections.defaultdict(str)
            # step1 : 主创吸引力质量系数
            for idx,actor in enumerate(actors):
                if actor in self.actor and (self.actor[actor]['award']==1 or self.actor[actor]['fans']<=3):
                    ac = re.sub('[a-zA-z]+', '', actor)
                    acc = re.sub(ac,'',actor)
                    act_score = self.actor[actor]['sc'] * self.actor[actor]['gsc']
                    if idx<10:
                        ratio = 1-idx/2*0.2
                    else:
                        ratio = 0.1
                    creator[ac]+=[act_score*ratio]
                    names[ac] = acc

            for idx,director in enumerate(directors):
                if director in self.director and (self.director[director]['award']!=0):
                    ac = re.sub('[a-zA-z]+', '', director)
                    acc = re.sub(ac,'',director)

                    act_score = self.director[director]['sc'] * self.director[director]['gsc']
                    creator[ac] += [act_score]
                    names[ac] = acc

            sum_ = 0
            for ac in creator:
                sum_ += np.mean(creator[ac])

            contribution_ = collections.defaultdict(float)
            for ac in creator:
                contribution_[ac]= np.mean(creator[ac])/sum_*0.1


            ret = []
            # step2 : 媒体主创曝光率
            # step3 : 社交网络讨论度
            event_contribution = collections.defaultdict(float)
            weibo_contribution = collections.defaultdict(float)
            e_sum_ = 0
            w_sum_ = 0
            good = collections.defaultdict(int)
            total = collections.defaultdict(int)

            for wk in range(5):
                contribution = collections.defaultdict(list)
                ct = self.event['count'][self.event.movieName == moviename][self.event.week == wk].tolist()
                nm = self.event['name'][self.event.movieName == moviename][self.event.week == wk].tolist()
                e_sum_ = e_sum_ + sum(ct)
                for c, n in zip(ct, nm):
                    event_contribution[n] += c

                ct = self.weibo['count'][self.weibo.movieName == moviename][self.weibo.week == wk].tolist()
                nm = self.weibo['name'][self.weibo.movieName == moviename][self.weibo.week == wk].tolist()
                st = self.weibo['senti'][self.weibo.movieName == moviename][self.weibo.week == wk].tolist()
                w_sum_ = w_sum_ + sum(ct)
                for c, n in zip(ct, nm):
                    weibo_contribution[n] += c

                for i in range(len(ct)):
                    good[nm[i]]+=ct[i]
                    total[nm[i]]+=int(ct[i]/st[i])

                for n in event_contribution:
                    contribution[n] += [event_contribution[n] / e_sum_*0.2]
                for n in weibo_contribution:
                    contribution[n] += [weibo_contribution[n] / w_sum_*0.7]
                tmp = {}
                tmp['name']=wk
                tmp['value']=[[],[]]

                tmpcnt = 0
                for a in contribution_:
                    if names[a]!='':
                        tmp['value'][0].append(a+names[a])
                        tmp['value'][1].append(np.sum(contribution[a])+contribution_[a])
                        tmpcnt+=tmp['value'][1][-1]
                if tmpcnt<1:
                    tmp['value'][0].append('Others')
                    tmp['value'][1].append(1-tmpcnt)
                    #tmp['value'][2].append(float(good[a])/total[a] if total[a]!=0 else 0.5)
                    #tmp['value'][3].append(1-float(good[a])/total[a] if total[a]!=0 else 0.5)
                ret.append(tmp)

            return ret #json.dumps(ret, indent=4)

    # 对输入句子进行命名实体识别和情感分析
    def get_sentence_analysis(self,moviename,sentence):
        #moviename = u'建军大业'
        #sentence = u'鹿哥演的真的很不错啊，张艺兴也棒棒哒，刘烨社长也是帅炸了'
        #print sentence.encode('utf8')
        #print sentence
        senti =  BiLSTM.load_lstm_and_evalute(sentence)#.encode('utf8'))

        tag = set([])
        if moviename in self.film_data['name'].tolist():
            namelist = self.film_data['actors'][self.film_data['name']==moviename].tolist()[0]\
                       +self.film_data['director'][self.film_data['name']==moviename].tolist()[0]
            namelist = list(set(namelist))
            for nm in namelist:
                nm = re.sub('[a-zA-Z]','',nm)
                if nm in sentence:
                    tag.add(nm)

                if nm in NameRecognizer.name_recognizer:
                    for nmm in NameRecognizer.name_recognizer[nm]:
                        try:
                            if nmm.strip().decode('utf8') in sentence :
                                tag.add(nm)
                        except:
                            pass
            ret = []
            ret.append({'name':u'人名','value':list(tag)})
            ret.append({'name':u'情感','value':str(senti)})
            return json.dumps(ret, indent=4)
        else:
            ret = []
            ret.append({'name': u'人名', 'value': list([u'您输入的参数有误'])})
            return json.dumps(ret, indent=4)

    # 获取演员画像
    def get_act_context(self,ac):
        if ac not in self.actor:
            ret = {'name':ac,'value':[u'您输入的参数有误']}
            return json.dumps(ret, indent=4)
        else:
            ret = {'name':ac,'value':gentext.gen_act_text(ac, self.actor[ac])}
            return json.dumps(ret, indent=4)

    # 获取导演画像
    def get_dir_context(self,dr):
        if dr not in self.director:
            ret = {'name': dr, 'value': [u'您输入的参数有误']}
            return json.dumps(ret, indent=4)
        else:
            ret = {'name':dr,'value':gentext.gen_dir_text(dr, self.director[dr])}
            return json.dumps(ret, indent=4)

    # 获取演员历史趋势
    def get_act_pic(self,ac):
        if ac not in self.actor:
            ret = {'name': ac, 'value': [u'您输入的参数有误']}
            return json.dumps(ret, indent=4)
        else:
            ret = [];tmp0 = [];tmp1 = [];tmp2 = [];tmp3 = [];tmp4 = []
            for i in self.actor[ac]['film_details_focus']:
                tmp0.append(i[0]);tmp1.append(i[4]);tmp2.append(i[3])
                tmp3.append(i[5]);tmp4.append(i[2])

            ret+=[{'name':u'电影名称','value':tmp0}]
            ret+=[{'name':u'上映年份','value':tmp4}]
            ret+=[{'name':u'票房','value':tmp1}]
            ret+=[{'name':u'票房得分','value':tmp2}]
            ret+=[{'name':u'口碑得分','value':tmp3}]

            return json.dumps(ret, indent=4)

    # 获取导演历史趋势
    def get_dir_pic(self,dr=u'周星驰stephenchow'):
        if dr not in self.director:
            ret = {'name': dr, 'value': [u'您输入的参数有误']}
            return json.dumps(ret, indent=4)
        else:
            ret = [];tmp0 = [];tmp1 = [];tmp2 = [];tmp3 = [];tmp4 = []
            for i in self.director[dr]['film_details']:
                tmp0.append(i[0]);tmp1.append(i[4]);tmp2.append(i[3])
                tmp3.append(i[5]);tmp4.append(i[2])

            ret += [{'name': u'电影名称', 'value': tmp0}]
            ret += [{'name': u'上映年份', 'value': tmp4}]
            ret += [{'name': u'票房', 'value': tmp1}]
            ret += [{'name': u'票房得分', 'value': tmp2}]
            ret += [{'name': u'口碑得分', 'value': tmp3}]

            return json.dumps(ret, indent=4)

    ###############################################
    #                模型预测与评估模块
    # gen_model_metric : 模型评估
    # get_predict : 模型预测
    # get_model_metric： 获取模型评估结果
    # gen_model_weekly_metric : 分周票房评估
    # get_week_model_metric ： 获取分周票房模型结果

    def get_compare(self):
        df =self.generate_df[self.generate_df['week_3'] != 0.0]

        train_num, test_num = train_test_split(np.arange(len(df)), test_size=0.3, random_state=1)

        dict_ = {}

        # week_1
        new_df = preprocessing.scale(df[['SC', 'GSC', 'STD', 'GSTD', 'weibo_0']])
        train_x = new_df[train_num]
        train_y = np.array(df['week_0'].tolist())[train_num]
        test_x = new_df[test_num]
        clf = models['SVR']
        clf.fit(train_x,train_y)
        pred = clf.predict(test_x)
        test_y = np.array(df['week_0'].tolist())[test_num]


        for i in range(len(test_num)):
            moviename = df['films'].tolist()[test_num[i]]
            dict_.setdefault(moviename,[[],[]])
            dict_[moviename][0].append(math.e**(pred[i]))
            dict_[moviename][1].append(math.e**(test_y[i]))


        # week_2
        new_df = preprocessing.scale(df[['SC', 'GSC', 'STD', 'GSTD', 'weibo_0',
                                         'week_0', 'weibo_1']])
        train_x = new_df[train_num]
        train_y = np.array(df['week_1'].tolist())[train_num]
        test_x = new_df[test_num]
        clf = models['Lasso']
        clf.fit(train_x, train_y)
        pred = clf.predict(test_x)
        test_y = np.array(df['week_1'].tolist())[test_num]
        for i in range(len(test_num)):
            moviename = df['films'].tolist()[test_num[i]]
            dict_.setdefault(moviename,[[],[]])
            dict_[moviename][0].append(math.e**(pred[i]))
            dict_[moviename][1].append(math.e**(test_y[i]))


        # week_3
        new_df = preprocessing.scale(df[['SC', 'GSC', 'STD', 'GSTD', 'weibo_0',
                                         'week_0', 'weibo_1','weibo_2','week_1']])
        train_x = new_df[train_num]
        train_y = np.array(df['week_2'].tolist())[train_num]
        test_x = new_df[test_num]
        clf = models['Lasso']
        clf.fit(train_x, train_y)
        pred = clf.predict(test_x)
        test_y = np.array(df['week_2'].tolist())[test_num]
        for i in range(len(test_num)):
            moviename = df['films'].tolist()[test_num[i]]
            dict_.setdefault(moviename, [[], []])
            dict_[moviename][0].append(math.e ** (pred[i]))
            dict_[moviename][1].append(math.e ** (test_y[i]))

        # week_4
        new_df = preprocessing.scale(df[['SC', 'GSC', 'STD', 'GSTD', 'weibo_0',
                                         'week_0', 'weibo_1', 'weibo_2', 'week_1','weibo_3','week_2']])
        train_x = new_df[train_num]
        train_y = np.array(df['week_3'].tolist())[train_num]
        test_x = new_df[test_num]
        clf = models['Lasso']
        clf.fit(train_x, train_y)
        pred = clf.predict(test_x)
        test_y = np.array(df['week_3'].tolist())[test_num]
        for i in range(len(test_num)):
            moviename = df['films'].tolist()[test_num[i]]
            dict_.setdefault(moviename, [[], []])
            dict_[moviename][0].append(math.e ** (pred[i]))
            dict_[moviename][1].append(math.e ** (test_y[i]))

        ret = []
        for key in dict_:
            ret += [{'filmname':key,
                     'value': [{'name': 'predict', 'value': dict_[key][0]}, {'name': 'test', 'value': dict_[key][1]}]}]
        return json.dumps(ret, indent=4)

    # 模型评估
    def gen_model_metric(self):  # to modify
        import math

        idx = 0
        box = []
        year = []
        schedule = []
        SC = []
        GSC = []
        STD = []
        GSTD = []
        StarCounts = []

        for i in range(len(self.film_data)):
            if self.film_data['week_0'][i]>1000:
                has_stars = 0
                sc = []
                gsc = []
                std = []
                gstd = []
                for actor in self.film_data['actors'][i]:
                    if actor in self.actor and (self.actor[actor]['award']==1 or self.actor[actor]['fans']<3):
                        sc+=[self.actor[actor]['sc']]
                        gsc+=[self.actor[actor]['gsc']]
                        std+=[self.actor[actor]['std']]
                        gstd+=[self.actor[actor]['std']]
                        has_stars += 1
                for director in self.film_data['director'][i]:
                    if director in self.director and self.director[director]['award']!=0:
                        sc += [self.director[director]['sc']]
                        gsc += [self.director[director]['gsc']]
                        std+=[self.director[director]['std']]
                        gstd+=[self.director[director]['std']]
                        has_stars +=1
                if has_stars:
                    box.append(math.log(self.film_data['week_0'][i]))
                    year.append(self.film_data['year'][i])
                    schedule.append(self.film_data['Schedule'][i])
                    SC.append(np.mean(sc))
                    GSC.append(np.mean(gsc))
                    STD.append(np.mean(std))
                    GSTD.append(np.mean(gstd))
                    StarCounts.append(has_stars)
                    idx +=1

        df = pd.DataFrame({'box':box,'year':year,'schedule':schedule,'sc':SC,'gsc':GSC,'starcounts':StarCounts,
                           'gstd':GSTD,'std':STD})#,'event':event})
        df1 = pd.get_dummies(df[['schedule', 'year']], columns=['schedule', 'year'])
        new_df = pd.concat([df.ix[:, ['sc','gsc','std','gstd','starcounts']], df1], axis=1).fillna(0)
        #new_df = preprocessing.scale(new_df)

        y = df.index
        train_num, test_num = train_test_split(y, test_size=0.3, random_state=1)
        train_x = new_df.ix[train_num]
        train_y = df.ix[train_num, ['box']]
        test_x = new_df.ix[test_num]
        test_y = df.ix[test_num, ['box']]

        self.model_metric = []

        for clf_name in models:
            m_t =dict()
            m_t['model_name'] = clf_name
            m_t['value'] = []
            for m_d in metrics_dict:
                tmp = {}
                tmp['metric_name'] = m_d
                clf = models[clf_name]
                clf.fit(train_x,train_y)
                y_pred = clf.predict(test_x)
                tmp['metric_value'] = metrics_dict[m_d](test_y,y_pred)
                m_t['value'].append(tmp.copy())
            self.model_metric.append(m_t.copy())

        return df


    # 模型预测
    def get_predict(self,dirlist,actlist,yr,sd):  # to modify

        sc = []
        gsc = []
        std = []
        gstd =[]
        for director in dirlist:
            if director in self.director:
                sc += [self.director[director]['sc']]
                gsc += [self.director[director]['gsc']]
                std += [self.director[director]['std']]
                gstd += [self.director[director]['std']]
        for actor in actlist:
            if actor in self.actor:
                sc += [self.actor[actor]['sc']]
                gsc += [self.actor[actor]['gsc']]
                std += [self.actor[actor]['std']]
                gstd += [self.actor[actor]['std']]

        df = self.df.copy()
        df.loc[len(df)] = {'box':0,'year':yr,'schedule':sd,'sc':np.mean(sc),'gsc':
            np.mean(gsc),'starcounts':len(dirlist)+len(actlist),
                                     'gstd':np.mean(gstd),'std':np.mean(std)}
        df1 = pd.get_dummies(df[['schedule', 'year']], columns=['schedule', 'year'])
        new_df = pd.concat([df.ix[:, ['sc', 'gsc', 'std', 'gstd', 'starcounts']], df1], axis=1).fillna(0)
        # new_df = preprocessing.scale(new_df)

        train_num = [i for i in range(len(df)-1)]
        test_num = [i for i in range(len(df)-1,len(df))]
        train_x = new_df.ix[train_num]
        train_y = df.ix[train_num, ['box']]
        test_x = new_df.ix[test_num]

        clf = models['LR']
        clf.fit(train_x,train_y)
        ret = {'name':'predict','value':math.e**(clf.predict(test_x)[0][0])}

        return json.dumps(ret,indent=4)

    # 获取模型评估结果
    def get_model_metric(self):
        '''
        :return: json
        '''
        return json.dumps(self.model_metric, indent=4)

    # 获取分周模型评估结果
    def get_week_model_metric(self):
        return json.dumps(self.week_model,indent=4)

    # 分周票房评估
    def gen_model_weekly_metric(self):
        SC = []
        GSC = []
        STD = []
        GSTD = []
        HAS_STARS = []
        weibo_0 = []
        weibo_1 = []
        weibo_2 =[]
        weibo_3 = []
        week_0 = []
        week_1 = []
        week_2 = []
        week_3 = []
        films = []
        for movie in self.weibo.movieName.unique().tolist():
            if self.film_data['week_0'][self.film_data.name==movie].tolist()[0]>0.0:
                sc = []
                gsc = []
                std = []
                gstd = []
                has_stars = 0
                for actor in self.film_data['actors'][self.film_data['name']==movie].tolist()[0]:
                    if actor in self.actor and (self.actor[actor]['award'] == 1 or self.actor[actor]['fans'] < 3):
                        sc += [self.actor[actor]['sc']]
                        gsc += [self.actor[actor]['gsc']]
                        std += [self.actor[actor]['std']]
                        gstd += [self.actor[actor]['std']]
                        has_stars +=1
                for director in self.film_data['director'][self.film_data['name']==movie].tolist()[0]:
                    if director in self.director and self.director[director]['award'] != 0:
                        sc += [self.director[director]['sc']]
                        gsc += [self.director[director]['gsc']]
                        std += [self.director[director]['std']]
                        gstd += [self.director[director]['std']]
                        has_stars +=1
                #print np.mean(sc),np.mean(gsc),np.mean(std),np.mean(gstd),has_stars
                SC += [np.mean(sc)]
                GSC += [np.mean(gsc)]
                STD += [np.mean(std)]
                GSTD += [np.mean(gstd)]
                HAS_STARS += [has_stars]
                #tmp = 0
                #event = []
                #for wk in range(4):
                #    tmp +=sum(self.event['count'][self.event['movieName']==movie][self.event['week']==wk].tolist())
                #    event.append(tmp)
                #print event

                pos = 0
                total = 0
                weibo = []
                for wk in range(4):
                    count = self.weibo['count'][self.weibo.movieName==movie][self.weibo.week==wk].tolist()
                    senti = self.weibo['senti'][self.weibo.movieName==movie][self.weibo.week==wk].tolist()
                    pos += sum(count)
                    for ct,st in zip(count,senti):
                        if st !=0.0:
                            total += int(ct/st)
                    weibo.append(float(pos)/total)
                weibo_0 +=[weibo[0]]
                weibo_1 +=[weibo[1]]
                weibo_2 +=[weibo[2]]
                weibo_3 +=[weibo[3]]


                week_0 += [self.film_data['week_0'][self.film_data.name==movie].tolist()[0]]
                week_1 += [self.film_data['week_1'][self.film_data.name == movie].tolist()[0]]
                week_2 += [self.film_data['week_2'][self.film_data.name == movie].tolist()[0]]
                week_3 += [self.film_data['week_3'][self.film_data.name == movie].tolist()[0]]
                films += [movie]

        df = pd.DataFrame({'SC':SC,'GSC':GSC,'STD':STD,'GSTD':GSTD,
                           'HAS_STARS':HAS_STARS,'weibo_0':weibo_0,'weibo_1':weibo_1,
                           'weibo_2':weibo_2,'weibo_3':weibo_3,'week_0':week_0,'week_1':week_1,
                           'week_2':week_2,'week_3':week_3,'films':films})
        def log_(x):
            if x<=0:
                return 0
            else:
                return math.log(x)

        df['week_0']=df['week_0'].map(log_)
        df['week_1']=df['week_1'].map(log_)
        df['week_2']=df['week_2'].map(log_)
        df['week_3']=df['week_3'].map(log_)


        def evaluate(new_df,query):
            y = np.arange(len(query))
            train_num, test_num = train_test_split(y, test_size=0.3, random_state=1)
            train_x = new_df[train_num]
            train_y = query[train_num]  # df.ix[train_num, ['week_2']]
            test_x = new_df[test_num]
            test_y = query[test_num]  # df.ix[test_num, ['week_2']]
            model_metric = []
            for clf_name in models:
                m_t = dict()
                m_t['model_name'] = clf_name
                m_t['value'] = []
                for m_d in metrics_dict:
                    tmp = {}
                    tmp['metric_name'] = m_d
                    clf = models[clf_name]
                    clf.fit(train_x, train_y)
                    y_pred = clf.predict(test_x)
                    tmp['metric_value'] = metrics_dict[m_d](test_y, y_pred)
                    m_t['value'].append(tmp.copy())
                model_metric.append(m_t.copy())
            return model_metric
        self.week_model = []

        # week_1
        new_df = preprocessing.scale(df[['SC', 'GSC', 'STD', 'GSTD', 'weibo_0']][df['week_0'] != 0.0])

        query = np.array(df['week_0'][df['week_0'] != 0].tolist())
        self.week_model.append({'name':u'第一周票房','value':evaluate(new_df,query)})

        # week_2
        new_df = preprocessing.scale(df[['SC', 'GSC', 'STD', 'GSTD', 'weibo_0',
                                         'week_0', 'weibo_1',]][df['week_1'] != 0.0])

        query = np.array(df['week_1'][df['week_1'] != 0].tolist())
        self.week_model.append({'name':u'第二周票房','value':evaluate(new_df,query)})

        # week_3
        new_df = preprocessing.scale(df[['SC', 'GSC', 'STD', 'GSTD', 'weibo_0',
                                         'week_0', 'weibo_1','weibo_2','week_1']][df['week_2'] != 0.0])

        query = np.array(df['week_2'][df['week_2'] != 0].tolist())
        self.week_model.append({'name':u'第三周票房','value':evaluate(new_df,query)})

        # week_4
        new_df = preprocessing.scale(df[['SC', 'GSC', 'STD', 'GSTD', 'weibo_0',
                                         'week_0', 'weibo_1', 'weibo_2', 'week_1','weibo_3','week_2']][df['week_3'] != 0.0])

        query = np.array(df['week_3'][df['week_3'] != 0].tolist())
        self.week_model.append({'name': u'第四周票房', 'value': evaluate(new_df, query)})
        return df





    ###############################################
    #                待开发
    ###############################################

    def get_series_score(self): # to modify
        '''
        :return: json
        '''
        query = u'七月与安生'
        self.film_data.release_time = pd.to_datetime(self.film_data.release_time)
        release_time = list(self.film_data.release_time[self.film_data.name==query])[0]
        self.douban.Time = pd.to_datetime(self.douban.Time)
        data = np.zeros((5,5))
        for c,t in zip(self.douban.CNT[self.douban.MovieName==query],self.douban.Time[self.douban.MovieName==query]):
            day = (t-release_time).days/7
            if day<4:
                if day<0:
                    day = -1
                c = list(map(int,c.split()))
                for idx in range(len(c)):
                    data[day+1][idx] += c[idx]
        dic = {0:u'上映前',1:u'上映第一周',2:u'上映第二周',3:u'上映第三周',4:u'上映第四周'}
        dic_m = {5:u'力荐', 4:u'推荐', 3:u'还行', 2:u'较差', 1:u'很差'}

        ret = []
        for idx in range(len(data)):
            if sum(data[idx])!=0:
                value = []
                for i in range(5):
                    tmp={}
                    tmp['name'] = dic_m[i+1]
                    tmp['value'] = data[idx][i]
                    value.append(tmp.copy())
                ret.append({'name':dic[idx],'value':value})
        return json.dumps(ret,indent=4)

    def get_series_senti(self): # To modify
        '''
        :return: json
        '''
        query = u'三生三世十里桃花'
        self.film_data.release_time = pd.to_datetime(self.film_data.release_time)
        release_time = list(self.film_data.release_time[self.film_data.name==query])[0]
        self.review.Time = pd.to_datetime(self.review.Time)

        data = np.zeros((5,2))
        for c,t in zip(self.review.Pos[self.review.MovieName==query],self.review.Time[self.review.MovieName==query]):
            day = (t-release_time).days/7
            if day<4:
                if day<0:
                    day = -1
                data[day+1][0] += c
        for c,t in zip(self.review.Neg[self.review.MovieName==query],self.review.Time[self.review.MovieName==query]):
            day = (t-release_time).days/7
            if day<4:
                if day<0:
                    day = -1
                data[day+1][1] += c

        dic = {0:u'上映前',1:u'上映第一周',2:u'上映第二周',3:u'上映第三周',4:u'上映第四周'}
        dic_m = {1:u'消极', 0:u'积极'}

        ret = []
        for idx in range(len(data)):
            value = []
            for i in range(2):
                tmp={}
                tmp['name'] = dic_m[i]
                tmp['value'] = data[idx][i]
                value.append(tmp.copy())
            ret.append({'name':dic[idx],'value':value})
        return json.dumps(ret,indent=4)
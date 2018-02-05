#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 @Time    : 2017/11/4 11:27
 @Author  : Kiristingna
 @File    : BiLSTM.py
 @Software: PyCharm
"""
import yaml
import numpy as np
import pandas as pd
import jieba
from keras.preprocessing import sequence
from keras.models import model_from_yaml
from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout, Embedding
from keras.layers import Bidirectional, LSTM
from sklearn.model_selection import train_test_split
from gensim.corpora.dictionary import Dictionary
from gensim.models.word2vec import Word2Vec
from keras import backend as K
#from sentiment.classifier import precision, recall

def precision(y_true, y_pred):
    """Precision metric.

    Only computes a batch-wise average of precision.

    Computes the precision, a metric for multi-label classification of
    how many selected items are relevant.
    """
    true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
    predicted_positives = K.sum(K.round(K.clip(y_pred, 0, 1)))
    precision = true_positives / (predicted_positives + K.epsilon())
    return precision


def recall(y_true, y_pred):
    """Recall metric.

    Only computes a batch-wise average of recall.

    Computes the recall, a metric for multi-label classification of
    how many relevant items are selected.
    """
    true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
    possible_positives = K.sum(K.round(K.clip(y_true, 0, 1)))
    recall = true_positives / (possible_positives + K.epsilon())
    return recall

os_path = '../data/'
def tokenizer_and_save():
    neg = pd.read_csv(os_path+'sentiment/neg_film.csv',  header=None, index_col=False)
    pos = pd.read_csv(os_path+'sentiment/pos_film.csv', header=None, index_col=False)

    cw = lambda x: jieba.lcut(str(x).replace('\n', ''))
    pos['words'] = pos[0].apply(cw)
    neg['words'] = neg[0].apply(cw)
    y = np.concatenate((np.ones(len(pos)), np.zeros(len(neg))))

    data = np.concatenate((pos['words'], neg['words']))
    np.save(os_path+'lstm_data/data.npy', data)
    np.save(os_path+'lstm_data/y.npy', y)


def load_pre_croup():
    '''
    直接拿取数据
    :return:
    '''
    data = np.load(os_path+'lstm_data/data.npy')
    y = np.load(os_path+'lstm_data/y.npy')

    return data, y


def _senquence(index_dict, data):
    '''
    处理语料
    :return:
    '''
    _res = []
    for sequence in data:
        _pad = []
        for w in sequence:  # every word
            try:
                _pad.append(index_dict[w])
            except:
                _pad.append(0)  # 小于10的为0
        _res.append(_pad)
    return _res


def word_dict(w2v, data, max_length=100):
    '''
    构建词典
    :param w2v:
    :param data:
    :param max_length:
    :return:
    '''

    _dict = Dictionary()
    # 将一个raw string 转换为根据本词典构构造的向量
    _dict.doc2bow(w2v.wv.vocab.keys(), allow_update=True)
    # w2index is a dict of {word: index} and w2vector is a dict of {word : vector(np.array)}
    w2index = {v: k + 1 for k, v in _dict.items()}  # 所有频数超过10的词语的索引
    w2vector = {word: w2v[word] for word in w2index.keys()}  # 所有频数超过10的词语向量

    # 填充序列
    _seq = _senquence(w2index, data)  # _seq is a set of list index for w

    # 每个句子所含词语对应的索引，所以句子中含有频数小于10的词语，索引为0(默认)
    _pseq = sequence.pad_sequences(_seq, maxlen=max_length)  # _pesq shape is (n x max_length)

    return w2index, w2vector, _pseq


def word_vector(data, vocab_dim=100, n_exposures=10, window_size=7, cpu_count=4, n_iterations=3):
    '''
    创建词语字典，并返回每个词语的索引，词向量，以及每个句子所对应的词语索引
    :param data:
    :param vocab_dim:
    :param n_exposures:
    :param window_size:
    :param cpu_count:
    :param n_iterations:
    :return:
    '''
    w2v = Word2Vec(size=vocab_dim, min_count=n_exposures, window=window_size,
                     workers=cpu_count, iter=n_iterations)

    w2v.build_vocab(data)
    w2v.train(data, total_examples=w2v.corpus_count)#, epochs=w2v.iter)
    w2v.save(os_path+'lstm_data/Word2Vec.pkl')

    index_dict, word_vectors, sequences = word_dict(w2v=w2v, data=data)
    np.save(os_path+'lstm_data/IndexDict.npy', index_dict)
    np.save(os_path+'lstm_data/WordVectors.npy', word_vectors)
    np.save(os_path+'lstm_data/Sequences.npy', sequences)


def load_word_vector():
    index_dict = np.load(os_path+'lstm_data/IndexDict.npy')
    word_vectors = np.load(os_path+'lstm_data/WordVectors.npy')
    sequences = np.load(os_path+'lstm_data/Sequences.npy')  # pad之后的序列词典量

    return index_dict, word_vectors, sequences


def lstm_wv(index_dict, word_vectors, sequences, y, vocab_dim=100, lstm_hidden_dims=125, max_input_length=100, batch_size=64, n_epoch=8):
    '''
    keras 实现 LSTM 网络
    :param sequences:
    :param y:
    :param lstm_hidden_dims:
    :param max_input_length:
    :param batch_size:
    :param n_epoch:
    :param index_dict:
    :param word_vectors:
    :param vocab_dim:
    :return:
    '''
    # index_dict 只包括1-n词, 而在原始数据中还有 0型(频度不足10的词) n_symbol 代表所有单词的索引数，频数小于10的词语索引为0，所以加1
    n_symbols = len(index_dict) + 1
    # 索引为0的词语，词向量全为0
    embedding_weights = np.zeros((n_symbols, vocab_dim))
    # 从索引为1的词语开始，对每个词语对应其词向量
    for word, index in index_dict.items():
        embedding_weights[index, :] = word_vectors[word]

    # 划分数据集和测试集
    x_train, x_test, y_train, y_test = train_test_split(sequences, y, test_size=0.2)

    print('Building a Simple Keras Model...')

    # 建立模型
    model = Sequential()
    model.add(Embedding(output_dim=vocab_dim, input_dim=n_symbols,
                        weights=[embedding_weights], mask_zero=True,
                        input_length=max_input_length))

    model.add(Bidirectional(LSTM(units=lstm_hidden_dims, activation='sigmoid')))
    model.add(Dropout(0.5))
    model.add(Dense(1))
    model.add(Activation('sigmoid'))

    print('Compiling the Model...')
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=[precision, recall,'accuracy'])  #  每批次结束后的计算准确度 召回率等
    print('Train the model....')
    model.fit(x_train, y_train, batch_size=batch_size, epochs=n_epoch, validation_data=(x_test, y_test))
    print('Evalute the model....')
    score = model.evaluate(x_test, y_test, batch_size=batch_size)

    # 保存
    yaml_string = model.to_yaml()
    with open(os_path+'lstm_data/lstm_model.yaml', 'w') as outfile:
        outfile.write(yaml_string)
    model.save_weights(os_path+'lstm_data/lstm_weights.h5')

    for i in zip(model.metrics_names, score):
        print('the {} is {} '.format(i[0], i[1]))


with open(os_path + 'lstm_data/lstm_model.yaml', 'r') as f:
    yaml_string = yaml.dump(yaml.load(f))
model = model_from_yaml(yaml_string)

model.load_weights(os_path + 'lstm_data/lstm_weights.h5')

model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
_pad_sequence = np.array([0]*100)
model.predict_classes(_pad_sequence.reshape(1, -1))

def load_lstm_and_evalute(sentence):
    '''
    单个句子的分类
    :param sentence:
    :param batch_size:
    :return:
    '''

    # 分词之后的words
    words = jieba.lcut(sentence)
    #print(words)
    # input [[w1, w2, w3....]]
    words = np.array(words).reshape(1, -1)
    # load word2vec model
    w2v = Word2Vec.load(os_path+'lstm_data/Word2Vec.pkl')
    _, _, pad_sequence = word_dict(w2v, words)
    #print pad_sequence
    _class = model.predict_classes(pad_sequence.reshape(1, -1))

    return (_class[0][0])

def load_lstm_and_classify():
    comments = pd.read_csv(os_path+'sentiment/weibo_union.csv', index_col=False, sep='|')
    cw = lambda x: jieba.lcut(str(x).replace('\n', ''))
    words = comments['content'].apply(cw)
    # print(comments.head())

    print('load model from disk...')
    with open(os_path+'lstm_data/lstm_model.yaml', 'r') as f:
        yaml_string = yaml.dump(yaml.load(f))
    model = model_from_yaml(yaml_string)

    print('load weights from disk......')
    model.load_weights(os_path+'lstm_data/lstm_weights.h5')

    print('rebuild model from disk......')
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
    # load word2vec model
    w2v = Word2Vec.load(os_path+'lstm_data/Word2Vec.pkl')
    _, _, pad_sequence = word_dict(w2v, words)

    _class = model.predict_classes(pad_sequence)
    comments['sentiment'] = _class

    comments.to_csv(os_path+'sentiment/weibo_total_by_lstm.csv', sep='|', index=False, encoding="utf_8_sig")


if __name__ == '__main__':
    # note1: 去停用词和标点会提高分类准确度
    # note2: 不同领域的训练数据有影响

    # 全部数据的分词并存储
    #tokenizer_and_save()
    # 加载序列化的数据
    #data, y = load_pre_croup()

    # 全部数据建立word2vec模型并存储
    #word_vector(data)
    # 加载word2vector数据
    #index_dict, word_vectors, sequences = load_word_vector()

    # lstm训练并存储
    #lstm_wv(index_dict.tolist(), word_vectors.tolist(), sequences, y)

    # 从硬盘恢复模型
    load_lstm_and_evalute('杨洋有三宝，眼神哭戏打戏好。旋风少女中沉稳如山的若白至今还被观众称呼“若白爸爸”，足以见得他对沉稳角色的演绎能力。参演的IP作品好评如潮，人物性格拿捏的分毫不差，')
    # load_lstm_and_classify()

    #K.clear_session()

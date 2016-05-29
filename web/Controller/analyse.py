from web.Model.database import My,Public,Lab
import numpy as np
import os
import jieba

from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
import re


def anayse():
    datas = Lab.query.limit(1000).all()
    arraylist = []
    for one in datas:
        arraylist.append(fenci(one.text))

    Tfidf(arraylist,datas)

r = re.compile(r'[\u4e00-\u9fa5]+')


# 对文档进行分词处理
def fenci(text):
    clear_content = re.sub(r"\[(.+?)\]", "", text)
    clear_content = re.sub(r" @(.+?) |(HTTP|http)s?://[^,， ]+", "", clear_content)
    clear_content = " ".join(r.findall(clear_content))
    sFilePath = './segfile'
    if not os.path.exists(sFilePath):
        os.mkdir(sFilePath)
    seg_list = jieba.cut(clear_content, cut_all=True)
    result = []
    for seg in seg_list:
        seg = ''.join(seg.split())
        if seg != '' and seg != "\n" and seg != "\n\n":
            result.append(seg)
    return " ".join(result)


def Tfidf(arraylist,datas):
    corpus = []
    for ff in arraylist:
        corpus.append(ff)

    vectorizer = CountVectorizer()
    transformer = TfidfTransformer()
    tfidf = transformer.fit_transform(vectorizer.fit_transform(corpus))

    word = vectorizer.get_feature_names()  # 所有文本的关键字
    weight = tfidf.toarray()  # 对应的tfidf矩阵

    # sFilePath = '/Volumes/RamDisk/tfidffile'
    # if not os.path.exists(sFilePath):
    #     os.mkdir(sFilePath)

    # print(proweight)
    # print(weight)
    # print('----------')
    # print(weight[0].sort())
    anasy2(weight,word,datas)
    # for i in range(len(weight)):
    #     f = open(sFilePath + '/' + str(i).zfill(5) + '.txt', 'w+')
    #     res = []
    #     for j in range(len(word)):
    #         res.append((word[j], weight[i][j]))
    #     res.sort(key=lambda x: x[1], reverse=True)
    #     for o in range(5):
    #         f.write(res[o][0] + '    '+str(res[o][1])+'\n')
    #     f.close()


def get_cos_vaule(x,y):
    Lx = np.sqrt(x.dot(x))
    Ly = np.sqrt(y.dot(y))
    return x.dot(y) / (Lx * Ly)


def get_time_similarity(x,y):
    t = (x-y).seconds
    if t > 259200:
        return 0
    else:
        return 1 - t/259200


def anasy2(vectors, words, datas):
    cou = 0
    topics = [{'vector':vectors[0],'wids':[datas[0].wid],'time':datas[0].time}]
    for i in range(1, len(vectors)):
        match = False
        for j in range(len(topics)):
            cou+=1
            time_similarity = get_time_similarity(datas[i].time,topics[j]['time'])
            cos_value = get_cos_vaule(vectors[i], topics[j]['vector'])
            res = time_similarity*0.25 + cos_value*0.75
            if res > 0.6:
                match = True

                topics[j]['vector'] = (topics[j]['vector'] + vectors[i]) / 2
                topics[j]['time'] = max(topics[j]['time'],datas[i].time)
                topics[j]['wids'].append(datas[i].wid)
        if not match:
            topics.append({'vector': vectors[i],'wids':[datas[i].wid],'time':datas[i].time})
    print(cou)
    print(len(topics))

    for one in topics:
        if len(one['wids'])>1:
            print(one['wids'],one['time'])

if __name__ == '__main__':
    anayse()
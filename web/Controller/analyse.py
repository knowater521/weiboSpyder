from web.Model.database import My,Public
import numpy as np
import os
import jieba

from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
import re

def anayse():
    datas = Public.query.limit(400).all()
    arraylist = []
    for one in datas:
        arraylist.append(fenci(one.text))

    Tfidf(arraylist)

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


def Tfidf(arraylist):
    corpus = []
    for ff in arraylist:
        corpus.append(ff)

    vectorizer = CountVectorizer()
    transformer = TfidfTransformer()
    tfidf = transformer.fit_transform(vectorizer.fit_transform(corpus))

    word = vectorizer.get_feature_names()  # 所有文本的关键字
    weight = tfidf.toarray()  # 对应的tfidf矩阵

    sFilePath = '/Volumes/RamDisk/tfidffile'
    if not os.path.exists(sFilePath):
        os.mkdir(sFilePath)

    proweight = np.argsort(weight, axis=1)[::-1]
    # print(proweight)
    # print(weight)
    # print('----------')
    # print(weight[0].sort())
    anasy2(weight,word)
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

def anasy2(datas,words):
    cou = 0
    topics = [datas[0]]
    for i in range(1,len(datas)):
        match = False
        for j in range(len(topics)):
            cou+=1
            res = get_cos_vaule(datas[i], topics[j])
            if res > 0.5:
                match = True


                for k in range(0,len(datas[j])):
                    if datas[j][k] > 0:
                        print(words[k])

                print('---')

                topics[j] = (topics[j] + datas[i])/2
        if not match:
            topics.append(datas[i])
    # print(topics)
    print(cou)
    print(len(topics))


anayse()
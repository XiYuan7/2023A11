# -*- coding: gbk -*-
import numpy as np
import pandas as pd
import math
import codecs
import json
import jieba
import jieba.analyse


def data_clear():
    d = pd.read_csv('policyinfo.tsv', sep='\t', encoding='gb18030', encoding_errors='ignore')

    data = np.array(d)

    dd = []
    for i in range(d.shape[0]):
        flag = True
        for s in data[i]:
            if isinstance(s, str) and len(s) >= 50 and s is not data[i][9]:
                flag = False
                break
        if flag:
            if isinstance(data[i][9], float):
                continue
            if len(data[i][9]) >= 100:
                dd.append(data[i])
        else:
            continue
        # flag = False
        # for s in data[i]:
        #     if isinstance(s, float) and math.isnan(s):
        #         flag = True
        #         break
        # if not flag:
        #     dd.append(data[i])

    da = np.array(dd)

    df = pd.DataFrame(da)

    df.to_csv('./good_data.csv', sep='\t', encoding='gb18030')


def policy_body():
    d = pd.read_csv('good_data.csv', sep='\t', encoding='gb18030', encoding_errors='ignore')
    data = np.array(d)
    pbs = {}
    for i in range(d.shape[0]):
        pbs[data[i][1]] = data[i][10]
    with codecs.open("policy_body.json", 'w', encoding='utf-8') as f:
        json.dump(pbs, f)


def create_idf():
    d = open("policy_body.json", "r", encoding='utf-8')
    pbs = json.load(d)
    e = open("idf.txt", "w", encoding='utf-8')
    c = open('key_count.json', 'r', encoding='utf-8')
    count = json.load(c)

    total = len(pbs)
    for k,v in count.items():
        s = str(k) + " " + str(math.log(total/(v+1))) + '\n'
        e.write(s)
    e.close()
    # 自定义idf库


def tcreate_idf():
    d = open("policy_body.json", "r", encoding='utf-8')
    pbs = json.load(d)
    co = open("key_count.json", 'r+', encoding='utf-8')
    count = json.load(co)
    c = 0
    m = 50000
    for k,v in pbs.items():
        newls = []
        if c < m:
            c += 1
            continue
        c += 1
        ls = jieba.lcut(v)
        for i in ls:
            if len(i)>1:
                newls.append(i)
        ds = pd.Series(newls).value_counts()
        for ks,vs in ds.items():
            if ks in count.keys():
                count[ks] += 1
            else:
                count[ks] = 1

    with codecs.open("key_count.json", 'w', encoding='utf-8') as f:
        json.dump(count, f)
    # 词出现的文章数


def tf_idf():
    d = open("policy_body.json", "r", encoding='utf-8')
    pbs = json.load(d)
    jieba.analyse.set_idf_path("idf.txt")
    key_words = {}
    for k,v in pbs.items():
        words = jieba.analyse.extract_tags(v, topK=5, withWeight=True, allowPOS=())
        key_words[k] = words

    with codecs.open("key_words.json", 'w', encoding='utf-8') as f:
        json.dump(key_words, f)

# d = open("policy_body.json", 'r', encoding='utf-8')
# pbs = json.load(d)
# d.close()
# i = 0
# for p in pbs:
#     if i > 10:
#         break
#     i += 1
#     print(p)

# ss = '我是谁，我在哪，我好厉害，我的天哪，哈哈哈哈，厉害了'
# l = jieba.lcut(ss)
# d = pd.Series(l).value_counts()
# print(type(d))
# for k,v in d.items():
#     print(k)
# count = {}
# with codecs.open("key_count.json", 'w', encoding='utf-8') as f:
#     json.dump(count, f)


# k = open('key_words.json', 'r', encoding='utf-8')
# kw = json.load(k)
# i = 0
# for key,value in kw.items():
#     if i >10:
#         break
#     i += 1
#     print(key, value)
#
# k.close()

def create_data():
    k = open('key_words.json', 'r', encoding='utf-8')
    kw = json.load(k)
    d = pd.read_csv('good_data.csv', sep='\t', encoding='gb18030', encoding_errors='ignore')
    data = np.array(d)
    tk = open("cpolicy.json", 'w', encoding='utf-8')
    i = 0
    for j in range(1002):
        for k in range(15):
            if isinstance(data[j][k], float):
                data[j][k] = "无"

    for key, value in kw.items():
        s1 = {"index": {"_id":str(i)}}
        d1 = {'policy_id': data[i][1], 'policy_title': data[i][2], 'policy_grade': data[i][3], 'policy_agency_id': data[i][4], 'pub_agency': data[i][5], 'pub_agency_fullname': data[i][6], 'pub_number': data[i][7], 'pub_time': data[i][8], 'policy_type': data[i][9], 'policy_body': data[i][10], 'province': data[i][11], 'city': data[i][12], 'policy_source': data[i][13], 'update_date': data[i][14], 'key_words_f': value[0][0],  'key_words_s': value[1][0], 'key_words_t': value[2][0]}
        tk.write(str(s1))
        tk.write('\n')
        tk.write(str(d1))
        tk.write('\n')
        i += 1
        if i >= 1000:
            break

    tk.close()
    # with codecs.open("apolicy.json", 'w', encoding='utf-8') as f:
    #     json.dump(s, f)

create_data()
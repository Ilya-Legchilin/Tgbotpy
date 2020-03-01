import pandas as pd
import json
import os
import numpy as np

PATH = os.getcwd()

with open(PATH + '/PARSED_QUESTIONS.json') as f:
     quastions = json.load(f)

questions = pd.DataFrame(quastions).drop(['QUESTION', 'AUTHOR'], axis=1).dropna()
questions['TITLE'] = questions.TITLE + ' ' +questions.DISCRIPTION
questions.drop(['DISCRIPTION'], axis=1, inplace=True)

questions = questions.append({'CATEGORY':'',
                  'TITLE': 'контакты и номер приемной комиссии',
                  'DATE':'',
                  'ANSWER':'https://pk.mipt.ru/contacts/'}, ignore_index=True);

questions = questions.append({'CATEGORY':'',
                  'TITLE': 'контакты приемной комиссии',
                  'DATE':'',
                  'ANSWER':'https://pk.mipt.ru/contacts/'}, ignore_index=True);

questions = questions.append({'CATEGORY':'',
                  'TITLE': 'номер приемной комиссии',
                  'DATE':'',
                  'ANSWER':'https://pk.mipt.ru/contacts/'}, ignore_index=True);

questions = questions.append({'CATEGORY':'',
                  'TITLE': 'Где находится приёмная комиссия?',
                  'DATE':'',
                  'ANSWER':'https://pk.mipt.ru/contacts/'}, ignore_index=True);

questions = questions.append({'CATEGORY':'',
                  'TITLE': 'Как добраться до приемной комиссии?',
                  'DATE':'',
                  'ANSWER':'https://pk.mipt.ru/contacts/'}, ignore_index=True);

questions = questions.append({'CATEGORY':'',
                  'TITLE': 'когда работает приемная комиссия',
                  'DATE':'',
                  'ANSWER':'https://pk.mipt.ru/bachelor/2020_schedule/'}, ignore_index=True);

questions = questions.append({'CATEGORY':'',
                  'TITLE': 'время работы приемная комиссия',
                  'DATE':'',
                  'ANSWER':'https://pk.mipt.ru/bachelor/2020_schedule/'}, ignore_index=True);

questions = questions.append({'CATEGORY':'',
                  'TITLE': 'часы работы приемная комиссия',
                  'DATE':'',
                  'ANSWER':'https://pk.mipt.ru/bachelor/2020_schedule/'}, ignore_index=True);

questions = questions.append({'CATEGORY':'',
                  'TITLE': 'СТОИМОСТЬ ОБУЧЕНИЯ',
                  'DATE':'',
                  'ANSWER':'https://pk.mipt.ru/bachelor/2020_cost/'}, ignore_index=True);

questions = questions.append({'CATEGORY':'',
                  'TITLE': 'ПРАВИЛА ПРИЁМА',
                  'DATE':'',
                  'ANSWER':'https://pk.mipt.ru/bachelor/2020_rules/'}, ignore_index=True);

questions = questions.append({'CATEGORY':'',
                  'TITLE': 'ЦЕЛЕВОЕ ОБУЧЕНИЕ',
                  'DATE':'',
                  'ANSWER':'https://pk.mipt.ru/bachelor/corp/'}, ignore_index=True);

questions = questions.append({'CATEGORY':'',
                  'TITLE': 'ПРИКАЗЫ И СПИСКИ',
                  'DATE':'',
                  'ANSWER':'https://pk.mipt.ru/bachelor/2019_decree/'}, ignore_index=True);

words = ['кого', 'что', 'да', 'ты', 'а', ',', '.', 'но', 'и', 'в', 'я', 'при', 'был', 'ли', 'на', 'если', 'по', 'не', 'к', 'могу', 'этой']

titles = list(questions.TITLE)
for w in words:
    for title in titles:
        title = title.replace(w, '')
titles = [np.unique(title.lower().split()) for title in titles]

embeddings = pd.read_table(PATH+'/model.txt', chunksize=10000)

chunk = embeddings.get_chunk()
titles_vec = np.zeros((len(titles), 300), dtype='float32')
num_of_vecs = np.zeros((len(titles), 300), dtype='float32')
for k in range(18):
    chunk = chunk.values
    chunk = {x[0].split(' ')[0].split('_')[0]: x[0].split(' ')[1:] for x in chunk}
    for i, title in enumerate(titles):
        for word in title:
            x = chunk.get(word, [0])
            if len(x) != 1:
                titles_vec[i] += np.array(x, dtype=np.float)
                num_of_vecs[i, :] += 1
    chunk = embeddings.get_chunk()
titles_vec /= num_of_vecs

def find_nearest_seq(seq):
    embeddings = pd.read_table(PATH+'/model.txt', chunksize=10000)
    chunk = embeddings.get_chunk()
    vec = np.zeros((300), dtype='float32')
    num_of_vecs = np.zeros((300), dtype='float32')
    seq = seq.lower().split()
    for k in range(18):
        chunk = chunk.values
        chunk = {x[0].split(' ')[0].split('_')[0]: x[0].split(' ')[1:] for x in chunk}
        for word in seq:
            x = chunk.get(word, [0])
            if len(x) != 1:
                vec += np.array(x, dtype=np.float)
                num_of_vecs += 1
        chunk = embeddings.get_chunk()

    vec /= num_of_vecs
    if num_of_vecs[0] == 0:
        return 'No such question'
    else:
        res = np.sum((titles_vec - vec)**2, axis=-1)
        args = np.argsort(res)

    return {questions.TITLE.iloc[i]: questions.ANSWER.iloc[i] for i in args[:3]}

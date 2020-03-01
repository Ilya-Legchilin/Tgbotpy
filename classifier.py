import pandas as pd
import numpy as np
import os

from sklearn.ensemble import RandomForestClassifier

def classifier(person):
    ask_dict = {"Выбери любимые предметы": ['физика', 'математика', 'информатика', 'биология', 'химия'],
            "Знаешь что такое машина Тьюринга?": ['Да', 'Нет'],
            "Призер/победитель физтех-олимпиады(М/Ф)?": ['Да', 'Нет'],
            "Любимый цвет": ['Красный', 'Желтый', 'Синий', 'Зеленый', 'Белый'],
            "Знаешь когда родился Ландау?": ['Да', 'Нет'],
            "Знаешь когда родился Капица?": ['Да', 'Нет'],
            "Знаешь когда создали Физтех?": ['Да', 'Нет'],
            "Любишь играть в футбол?": ['Да', 'Нет'],
            "Пол": ['М', 'Ж', 'Неизвестно'],
            "Кто такой Овчинкин?": ["Математик", 'Физик', 'Физрук', 'Не знаю'],
            "Какие разделы математики интересуют вас больше всего?": ["геометрия", "алгебра", "теорвер, комбинаторика"],
            "Какие разделы физики в школе были интересны?": ["Механика", "Электричество", "Оптика", "Термодинамика"],
            "Какие разделы программирования в школе были вам интересны?": ["никакие", "олимпиадные алгоритмы",
            "проектное программирование", "программирование микроконтроллеров"]}

    PATH = os.getcwd()
    data = pd.read_csv(PATH+'/data2.csv')

    p = data.head(1).copy()
    for ans, column in zip(person, list(data.columns)[1:-1]):
            p[column] = ''
            for i in ans:
                print(ans)
                print(column)
                print(ask_dict[column][int(i) - 1])
                p[column] = p[column] + ask_dict[column][int(i) - 1] + ' '

    p[p.columns[2]] = p[p.columns[2]].apply(lambda x: 1 if x == 'Да' else 0)
    p[p.columns[3]] = p[p.columns[3]].apply(lambda x: 1 if x == 'Да' else 0)
    p[p.columns[4]] = p[p.columns[4]].apply(lambda x: 1 if x == 'Да' else 0)
    p[p.columns[6]] = p[p.columns[6]].apply(lambda x: 1 if x == 'Да' else 0)
    p[p.columns[7]] = p[p.columns[7]].apply(lambda x: 1 if x == 'Да' else 0)
    p[p.columns[8]] = p[p.columns[8]].apply(lambda x: 1 if x == 'Да' else 0)

    data[data.columns[2]] = data[data.columns[2]].apply(lambda x: 1 if x == 'Да' else 0)
    data[data.columns[3]] = data[data.columns[3]].apply(lambda x: 1 if x == 'Да' else 0)
    data[data.columns[4]] = data[data.columns[4]].apply(lambda x: 1 if x == 'Да' else 0)
    data[data.columns[6]] = data[data.columns[6]].apply(lambda x: 1 if x == 'Да' else 0)
    data[data.columns[7]] = data[data.columns[7]].apply(lambda x: 1 if x == 'Да' else 0)
    data[data.columns[8]] = data[data.columns[8]].apply(lambda x: 1 if x == 'Да' else 0)

    p['Физика'] = p[p.columns[1]].apply(lambda x: 1 if 'Физика' else 0)
    p['Математика'] = p[p.columns[1]].apply(lambda x: 1 if 'Математика' in x else 0)
    p['Информатика'] = p[p.columns[1]].apply(lambda x: 1 if 'Информатика' in x else 0)
    p['Биология'] = p[p.columns[1]].apply(lambda x: 1 if 'Биология' in x else 0)
    p['Химия'] = p[p.columns[1]].apply(lambda x: 1 if 'Химия' in x else 0)

    data['Физика'] = data[data.columns[1]].apply(lambda x: 1 if 'Физика' else 0)
    data['Математика'] = data[data.columns[1]].apply(lambda x: 1 if 'Математика' in x else 0)
    data['Информатика'] = data[data.columns[1]].apply(lambda x: 1 if 'Информатика' in x else 0)
    data['Биология'] = data[data.columns[1]].apply(lambda x: 1 if 'Биология' in x else 0)
    data['Химия'] = data[data.columns[1]].apply(lambda x: 1 if 'Химия' in x else 0)

    p['Красный'] = p[p.columns[5]].apply(lambda x: 1 if 'Красный' in x else 0)
    p['Желтый'] = p[p.columns[5]].apply(lambda x: 1 if 'Желтый' in x else 0)
    p['Синий'] = p[p.columns[5]].apply(lambda x: 1 if 'Синий' in x else 0)
    p['Зеленый'] = p[p.columns[5]].apply(lambda x: 1 if 'Зеленый' in x else 0)
    p['Белый'] = p[p.columns[5]].apply(lambda x: 1 if 'Белый' in x else 0)

    data['Красный'] = data[data.columns[5]].apply(lambda x: 1 if 'Красный' in x else 0)
    data['Желтый'] = data[data.columns[5]].apply(lambda x: 1 if 'Желтый' in x else 0)
    data['Синий'] = data[data.columns[5]].apply(lambda x: 1 if 'Синий' in x else 0)
    data['Зеленый'] = data[data.columns[5]].apply(lambda x: 1 if 'Зеленый' in x else 0)
    data['Белый'] = data[data.columns[5]].apply(lambda x: 1 if 'Белый' in x else 0)

    p['M'] = p[p.columns[9]].apply(lambda x: 1 if 'М' in x else 0)
    p['F'] = p[p.columns[9]].apply(lambda x: 1 if 'F' in x else 0)
    p['U'] = p[p.columns[9]].apply(lambda x: 1 if 'U' in x else 0)

    data['M'] = data[data.columns[9]].apply(lambda x: 1 if 'М' in x else 0)
    data['F'] = data[data.columns[9]].apply(lambda x: 1 if 'F' in x else 0)
    data['U'] = data[data.columns[9]].apply(lambda x: 1 if 'U' in x else 0)

    p['Физик'] = p[p.columns[10]].apply(lambda x: 1 if 'Физик' in x else 0)
    p['Математик'] = p[p.columns[10]].apply(lambda x: 1 if 'Математик' in x else 0)
    p['Физрук'] = p[p.columns[10]].apply(lambda x: 1 if 'Физрук' in x else 0)
    p['Не знаю'] = p[p.columns[10]].apply(lambda x: 1 if 'Не знаю' in x else 0)

    data['Физик'] = data[data.columns[10]].apply(lambda x: 1 if 'Физик' in x else 0)
    data['Математик'] = data[data.columns[10]].apply(lambda x: 1 if 'Математик' in x else 0)
    data['Физрук'] = data[data.columns[10]].apply(lambda x: 1 if 'Физрук' in x else 0)
    data['Не знаю'] = data[data.columns[10]].apply(lambda x: 1 if 'Не знаю' in x else 0)

    p['алгебра'] = p[p.columns[11]].apply(lambda x: 1 if 'алгебра' in x else 0)
    p['теорвер'] = p[p.columns[11]].apply(lambda x: 1 if 'теорвер' in x else 0)
    p['геометрия'] = p[p.columns[11]].apply(lambda x: 1 if 'геометрия' in x else 0)

    data['алгебра'] = data[data.columns[11]].apply(lambda x: 1 if 'алгебра' in x else 0)
    data['теорвер'] = data[data.columns[11]].apply(lambda x: 1 if 'теорвер' in x else 0)
    data['геометрия'] = data[data.columns[11]].apply(lambda x: 1 if 'геометрия' in x else 0)

    p['механика'] = p[p.columns[12]].apply(lambda x: 1 if 'механика' in x else 0)
    p['электричество'] = p[p.columns[12]].apply(lambda x: 1 if 'электричество' in x else 0)
    p['оптика'] = p[p.columns[12]].apply(lambda x: 1 if 'оптика' in x else 0)
    p['термодинамика'] = p[p.columns[12]].apply(lambda x: 1 if 'термодинамика' in x else 0)

    data['механика'] = data[data.columns[12]].apply(lambda x: 1 if 'механика' in x else 0)
    data['электричество'] = data[data.columns[12]].apply(lambda x: 1 if 'электричество' in x else 0)
    data['оптика'] = data[data.columns[12]].apply(lambda x: 1 if 'оптика' in x else 0)
    data['термодинамика'] = data[data.columns[12]].apply(lambda x: 1 if 'термодинамика' in x else 0)

    p['никакие'] = p[p.columns[13]].apply(lambda x: 1 if 'никакие' in x else 0)
    p['олимпиадные алгоритмы'] = p[p.columns[13]].apply(lambda x: 1 if 'олимпиадные алгоритмы' in x else 0)
    p['проектное программирование'] = p[p.columns[13]].apply(lambda x: 1 if 'проектное программирование' in x else 0)
    p['программирование микроконтроллеров'] = p[p.columns[13]].apply(lambda x: 1 if 'программирование микроконтроллеров' in x else 0)

    data['никакие'] = data[data.columns[13]].apply(lambda x: 1 if 'никакие' in x else 0)
    data['олимпиадные алгоритмы'] = data[data.columns[13]].apply(lambda x: 1 if 'олимпиадные алгоритмы' in x else 0)
    data['проектное программирование'] = data[data.columns[13]].apply(lambda x: 1 if 'проектное программирование' in x else 0)
    data['программирование микроконтроллеров'] = data[data.columns[13]].apply(lambda x: 1 if 'программирование микроконтроллеров' in x else 0)

    columns = data.columns

    p.drop(columns[0], axis=1, inplace=True)
    p.drop(columns[1], axis=1, inplace=True)
    p.drop(columns[5], axis=1, inplace=True)
    p.drop(columns[9], axis=1, inplace=True)
    p.drop(columns[10], axis=1, inplace=True)
    p.drop(columns[11], axis=1, inplace=True)
    p.drop(columns[12], axis=1, inplace=True)
    p.drop(columns[13], axis=1, inplace=True)

    data.drop(columns[0], axis=1, inplace=True)
    data.drop(columns[1], axis=1, inplace=True)
    data.drop(columns[5], axis=1, inplace=True)
    data.drop(columns[9], axis=1, inplace=True)
    data.drop(columns[10], axis=1, inplace=True)
    data.drop(columns[11], axis=1, inplace=True)
    data.drop(columns[12], axis=1, inplace=True)
    data.drop(columns[13], axis=1, inplace=True)

    y = data['В какой физтех-школе вы учитесь?'].values
    x = data.drop(['В какой физтех-школе вы учитесь?'], axis=1).values
    p = p.drop(['В какой физтех-школе вы учитесь?'], axis=1).values

    clf = RandomForestClassifier()
    clf.fit(x, y)

    args = np.argsort(-clf.predict_proba(np.array(p).reshape(1, 34)))

    return list(clf.classes_[args[0, :2]])

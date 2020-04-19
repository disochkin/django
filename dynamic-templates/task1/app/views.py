from django.shortcuts import render
import csv

import csv

def get_cell_color(value):
    return {
        value < 0: 'Green',
        0.0 <= value <1: 'White',
        1.0 <= value < 2.0: 'Darksalmon',
        2.0 <= value < 5.0: 'Salmon',
        5.0 <= value: 'Indianred'
    }[True]


def add_color(data_item):
    if len(data_item) > 0:
        tmp = (data_item, get_cell_color(float(data_item)))
    else:
        tmp = ('-', 'white')
    return tmp


def custom_csv2dict(filename):
    payload = []
    with open(filename, 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter=';', quotechar='"')
        result = {'header': next(reader)}
        for row in reader:
            tmp = [(row[0], 'White')]
            tmp.extend(list(map(add_color, row[1:-1])))
            tmp.append((row[-1], 'Gray'))
            payload.append(tmp)
        result.update({'payload': payload})
        return result


def inflation_view(request):
    template_name = 'inflation.html'
    # чтение csv-файла и заполнение контекста
    context = custom_csv2dict('inflation_russia.csv')
    return render(request, template_name,
                  context)


from django.db.models import query
import numpy as np
import datetime
import json
from . import models
'''
Нужно добавить страницу выбора по годам. Как это лучше сделать? 
'''


def make_json_data(brand, model):
    '''Создает джейсон для построения графика год:цена, вариант для каталога'''
    lables = []

    selected_cars = models.Cars.objects.filter(
        brand=brand, model=model).order_by('-year')
    try:
        current_year = selected_cars[0].year
    except:
        current_year = '2020'

    price_for_specific_year = []
    lables = []
    data_price = []

    for i in selected_cars:
        if current_year == i.year:
            price_for_specific_year.append(i.price)
        else:
            lables.append(str(current_year))
            data_price.append(int(np.median(price_for_specific_year)))
            price_for_specific_year = []
            current_year = i.year
            price_for_specific_year.append(i.price)
    lables.append(str(current_year))
    data_price.append(int(np.median(price_for_specific_year)))

    lables = json.dumps(lables)
    data_price = json.dumps(data_price)
    return lables, data_price


def make_json_data_years(brand, model, year):
    '''Создает джейсон для построения графика ПОТЕРИИ СТОИМОСТИ, 
    где начальным отсчетом считается переданный год'''
    current_year = datetime.date.today().year
    lables = [current_year + i for i in range(11)]
    selected_cars = models.Cars.objects.filter(
        brand=brand, model=model, year__lte=year)

    print(len(selected_cars))
    price_in_point = []
    for point in range(11):
        year_for_query_in_point = int(year) - point
        print('year_for_query_in_point', year_for_query_in_point)
        query_spec_year = selected_cars.filter(year=year_for_query_in_point)
        print('LEN: ', len(query_spec_year))
        if len(query_spec_year) != 0:
            price_li = [query_spec_year[i].price for i in range(
                len(query_spec_year))]
            price_in_point.append(np.median(price_li))
        else:
            a = price_in_point[-2]
            b = price_in_point[-1]
            c = b-(a-b)
            price_in_point.append(c)

    lables = json.dumps(lables)
    data_price = json.dumps(price_in_point)
    return lables, data_price

# from views import brand, year
import numpy as np
import datetime
import json
from . import models


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
    temp_var_for_test = json.dumps(f"""{
            'label': {name},
            'backgroundColor': 'rgba(255, 99, 132, 0.5)',
            'borderColor': 'rgba(255, 9, 13, 0.8)',
            'data': {data_price},
            'order': '2',}""")
    return lables, data_price, temp_var_for_test


# def make_json_lost_of_value(brand, model, year):
#     '''Создает джейсон для построения графика ПОТЕРИИ СТОИМОСТИ,
#     где началом координат по оси абцисс считается переданный год'''
#     current_year = datetime.date.today().year
#     lables = [current_year + i for i in range(11)]
#     selected_cars = models.Cars.objects.filter(
#         brand=brand, model=model, year__lte=year)

#     price_in_point = []
#     for point in range(11):
#         year_for_query_in_point = int(year) - point
#         query_spec_year = selected_cars.filter(year=year_for_query_in_point)
#         if len(query_spec_year) != 0:
#             price_li = [query_spec_year[i].price for i in range(
#                 len(query_spec_year))]
#             price_in_point.append(np.median(price_li))
#         else:
#             # Рассчет недостающих точек на графике
#             # Когда в базе нет таких данных
#             # Например не существует киа рио 1998 года выпуска
#             # Решение плохое, требует проработки (может уйти в отрицательную стоимость)
#             # слишком линейно показывает падения для совсем новых машин возрастом 2 года
#             # ПАДАЕТ когда марка первогодка
#             a = price_in_point[-2]
#             b = price_in_point[-1]
#             # 0.75 просто сгругляшка временная
#             c = b-((a-b)*0.75)
#             price_in_point.append(c)

#     lables = json.dumps(lables)
#     data_price = json.dumps(price_in_point)
#     return lables, data_price
"""
Размышления как действовать.

Нужно передать в темплейт список контекстов, а в самом темплейте итерироваться по ним.

Собрать контекст от каждого запроса. Передать его в переменную сессии.
Вернуть какой-то объект в темплейт чтобы он понял что это и распарсил на n графиков.

# """


class Grap:
    def __init__(self, brand, model, year):
        self.brand = brand
        self.model = model
        self.year = year

    def __make_json_lost_of_value(self):
        '''Создает джейсон для построения графика ПОТЕРИИ СТОИМОСТИ,
        где началом координат по оси абцисс считается переданный КУДА? ОТКУДА? год'''
        current_year = datetime.date.today().year
        lables = [current_year + i for i in range(11)]
        selected_cars = models.Cars.objects.filter(
            brand=self.brand, model=self.model, year__lte=self.year).values('year', 'price').order_by('year')
        price_in_point = []

        temp_cars_dict = {}
        for i in selected_cars:
            current_year = i['year']

            if current_year in temp_cars_dict:
                temp_cars_dict[i["year"]].append(i["price"])
            else:
                temp_cars_dict[i["year"]] = [i["price"]]

        # Приходится прозодится по словарю дважды, чтобы посчитать медиану
        for j in temp_cars_dict:
            price = int(np.median(temp_cars_dict[j]))
            price_in_point.append(price)

        price_in_point.reverse()
        # ВНИМАНИЕ Добавить предсказание цены в пустые ячейки

        json_res = json.dumps({
            "labels": lables,
            "datasets": [{
                "backgroundColor": 'rgba(255, 99, 132, 0.5)',
                "borderColor": 'rgba(255, 9, 13, 0.8)',
                "data": price_in_point,
                "order": '2', }],
        }
        )

        return json_res

    def get_context(self):
        json_res = self.__make_json_lost_of_value()
        context = {
            'year': self.year,
            'brand_name': self.brand,
            'model_name': self.model,
            'temp_var_for_test': json_res,
        }
        return context

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
    return lables, data_price


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


# def get_context(brand, model, year):
#     js_lables, js_price = make_json_lost_of_value(brand, model, year)
#     context = {
#         'year': year,
#         'brand_name': brand,
#         'model_name': model,
#         'js_lables': js_lables,
#         'js_price': js_price,
#     }
#     return context


class Grap:
    def __init__(self, brand, model, year):
        self.brand = brand
        self.model = model
        self.year = year

    # def get_lable():
    #     current_year = datetime.date.today().year
    #     lables = [current_year + i for i in range(11)]
    #     return lables

    def __make_json_lost_of_value(self):
        '''Создает джейсон для построения графика ПОТЕРИИ СТОИМОСТИ, 
        где началом координат по оси абцисс считается переданный год'''
        current_year = datetime.date.today().year
        lables = [current_year + i for i in range(11)]
        selected_cars = models.Cars.objects.filter(
            brand=self.brand, model=self.model, year__lte=self.year)
        price_in_point = []
        for point in range(11):
            year_for_query_in_point = int(self.year) - point
            # FIX ME SLOW QUERY FIX ME #
            query_spec_year = selected_cars.filter(
                year=year_for_query_in_point)
            if len(query_spec_year) != 0:
                price_li = [query_spec_year[i].price for i in range(
                    len(query_spec_year))]
                price_in_point.append(np.median(price_li))
            else:
                # Рассчет недостающих точек на графике
                # Когда в базе нет таких данных
                # Например не существует киа рио 1998 года выпуска
                # Решение плохое, требует проработки (может уйти в отрицательную стоимость)
                # слишком линейно показывает падения для совсем новых машин возрастом 2 года
                # ПАДАЕТ когда марка первогодка
                a = price_in_point[-2]
                b = price_in_point[-1]
                # 0.75 просто сгругляшка, временная
                c = b-((a-b)*0.75)
                price_in_point.append(c)

        lables = json.dumps(lables)
        data_price = json.dumps(price_in_point)
        return lables, data_price

    def get_context(self):
        js_lables, js_price = self.__make_json_lost_of_value()
        context = {
            'year': self.year,
            'brand_name': self.brand,
            'model_name': self.model,
            'js_lables': js_lables,
            'js_price': js_price,
        }
        return context

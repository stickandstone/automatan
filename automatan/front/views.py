from django.shortcuts import render
import sqlite3
from . import graps, slopes_calc
from django.http import HttpResponse
# from front.forms import IndexForm
from django import forms
from . import models
import numpy as np
import json
# Create your views here.


def index(request):
    brands_list = list(models.Manufactories.objects.all())
    brands = []
    check_letter = []
    super_list = []

    # первая инициализация
    first_init = str(brands_list[0])
    first_letter = first_init[0]
    check_letter.append(first_letter)

    for i in brands_list:
        temp_list = []
        letter = str(i)[0]
        url = str(i).replace(' ', '_')
        # добавляем заглавную букву для навигации
        if letter not in check_letter:
            previous_letter = check_letter[-1]
            super_list.append({"letter": previous_letter, "brands": brands})
            check_letter.append(letter)
            brands = []
            brands.append({'name': i, 'link': url})
        else:
            brands.append({'name': i, 'link': url})

    context = {
        'brands': super_list,
        'iter_list': check_letter
    }

    return render(request, 'front/index.html', context)


def brand(request, brand):
    models_list = []
    brand_name = brand.replace('_', ' ')
    query_list = models.CarNames.objects.filter(brand_name=brand_name)

    for i in query_list:
        print(i.model_name[0])
        models_list.append(
            {'name': i.model_name.replace('_', ' '), 'url': i.model_name.replace(' ', '_')})
    brand_link = brand.replace(' ', '_')

    context = {
        'brand_name': brand_name,
        'brand_link': brand_link,
        'models': models_list
    }

    return render(request, 'front/brand.html', context)


def model(request, brand, model):
    brand = brand.replace('_', ' ')
    model = model.replace('_', ' ')
    js_lables, js_price = graps_JSON(brand, model)
    # graps.build_grap(brand, model)
    slope_index = slopes_calc.slope_starter(brand, model)

    context = {
        'brand_name': brand,
        'model_name': model,
        'slope_index': slope_index,
        # 'js_data': js_data,
        'js_lables': js_lables,
        'js_price': js_price,
    }
    return render(request, 'front/car.html', context)


def about(request):
    return render(request, 'front/about.html')


def graps_JSON(brand, model):
    print(brand, model)
    # create JSON for graps on page
    lables = []

    selected_cars = models.Cars.objects.filter(
        brand=brand, model=model).order_by('-year')
    current_year = selected_cars[0].year
    price_for_specific_year = []
    # resultList = []
    lables = []
    data_price = []
    # print(current_year)

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

    # print(lables)
    # print(data_price)
    # lables_js = json.dumps
    # data_to_JSON = {'data': {'labels': lables}, 'datasets': [{'lablel': brand + ' ' + model,
    #                                                           'backgroundColor': 'rgb(255, 99, 132)',
    #                                                           'borderColor': 'rgb(255, 9, 13)',
    #                                                           'data': data_price, }]}

    # js_data = json.dumps(data_to_JSON)
    lables = json.dumps(lables)
    data_price = json.dumps(data_price)
    # return json.dumps({"data": js_data})
    return lables, data_price
    # print(resultList)
    # print(np.median())
    # print(selected_cars)


# def get_brands_from_DB():
#     conn = sqlite3.connect('MyData.db')
#     c = conn.cursor()
#     c.execute('SELECT company_name FROM manufactories')
#     raw_list = c.fetchall()
#     brands_list = []
#     for i in raw_list:
#         brands_list.append(i[0])
#     return brands_list


# def brand(request, brand):
#     models_list, brand_name, brand_link = query_to_DB('models', brand)

#     context = {
#         'brand_name': brand_name,
#         'brand_link': brand_link,
#         'models': models_list
#     }
#     return render(request, 'front/brand.html', context)


# def index(request):
#     return HttpResponse('<h1>Test karatest!</h1>')
# Вот чтобы такую ебобятину не писать, как сверху, существует модуль шорткаты
# Чтобы не писать функцию ХттпРеспонс
#
# Надо чертые листа, list_of_Brands_for_link, list_of_Models_for_link
# list_Of_Brand_Name, list_Of_Model_Name
#

# def get(request):
#     form = IndexForm
# return render HttpResponse('<h1>Test karatest!</h1>')


# def query_to_DB(kinde, brand):
#     conn = sqlite3.connect('MyData.db')
#     c = conn.cursor()
#     brands_list = []
#     models_list = []

#     if kinde == 'brands':
#         c.execute('SELECT company_name FROM manufactories')
#         raw_list = c.fetchall()
#         for i in raw_list:
#             temp = i[0]
#             # Чтобы линк с пробелом не подавать в рендер
#             temp = temp.replace(' ', '_')
#             brands_list.append({'name': i[0], 'url': temp})
#             # тут у нас на выходе лист со словорями [{'name': Land rover, url: Land_rover}]
#         return brands_list

#     if kinde == 'models':
#         # А это просто оббосться как смешно, такой костыль дичайший.
#         brand_link = brand.replace(' ', '_')
#         brand_name = brand.replace('_', ' ')
#         print('BRAND', brand)
#         c.execute(
#             'SELECT Model_name FROM car_names WHERE Brand_name=? AND Quantity>10', (brand_name,))
#         raw_list = c.fetchall()
#         for i in raw_list:
#             temp = i[0]
#             temp = temp.replace(' ', '_')
#             models_list.append({'name': i[0], 'url': temp})
#         return models_list, brand_name, brand_link

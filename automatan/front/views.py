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
    # NOT DRY ENOUGH
    # Приходится повторятся, чтобы добавить модель на последнюю букву см issues #12
    previous_letter = check_letter[-1]
    super_list.append({"letter": previous_letter, "brands": brands})

    context = {
        'brands': super_list,
        'iter_list': check_letter
    }

    return render(request, 'front/index.html', context)


def brand(request, brand):
    models_list = []
    super_list = []
    brand_name_with_spaces = brand.replace('_', ' ')
    query_list = models.CarNames.objects.filter(
        brand_name=brand_name_with_spaces, quantity__gt=10).order_by('model_name')
    # Извлечение первой буквы\цифры названия модели
    check_letter = []
    try:
        check_letter.append(query_list[0].model_name[0])

        for i in query_list:

            letter = i.model_name[0]
            model_name = i.model_name.replace('_', ' ')
            model_url = i.model_name.replace(' ', '_')
            if letter not in check_letter:
                previous_letter = check_letter[-1]
                super_list.append(
                    {"letter": previous_letter, "models": models_list})
                check_letter.append(letter)
                models_list = []

            print(i.model_name)
            models_list.append(
                {'name': model_name, 'url': model_url})

        # NOT DRY ENOUGH
        # Приходится повторятся, чтобы добавить модель на последнюю букву см issues #12
        previous_letter = check_letter[-1]
        super_list.append(
            {"letter": previous_letter, "models": models_list})

        brand_link = brand.replace(' ', '_')
        # for i in super_list:
        #     print(i)

        context = {
            'brand_name': brand_name_with_spaces,
            'brand_link': brand_link,
            'models': super_list
        }
        return render(request, 'front/brand.html', context)
    except:
        print('pizda')
        context = {
            "error": True
        }
        return render(request, 'front/brand.html', context)


def model(request, brand, model):
    print(model)
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
    # print(brand, model)
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

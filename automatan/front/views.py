from django.shortcuts import render, redirect
import sqlite3
# from . import graps, slopes_calc
from django.http import HttpResponse
# from front.forms import IndexForm
from django import forms
from . import models
import numpy as np
import json
from django.contrib.auth.decorators import login_required

# Create your views here.


@login_required
def index(request):

    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits+1

    brands_list = list(models.Manufactories.objects.all())
    brands = []
    check_letter = []
    super_list = []

    # первая инициализация
    first_init = str(brands_list[0])
    first_letter = first_init[0]
    check_letter.append(first_letter)

    for i in brands_list:
        print(i)
        temp_list = []
        letter = str(i)[0]
        url = str(i).replace(' ', '_')

        # добавляем заглавную букву для навигации
        if letter not in check_letter:
            print(letter, i)
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
        'iter_list': check_letter,
        'num_visits': num_visits
    }

    return render(request, 'front/index.html', context)


@login_required
def brand(request, brand):
    models_list = []
    super_list = []
    brand_name_with_spaces = brand.replace('_', ' ')
    query_list = models.CarNames.objects.filter(
        brand_name=brand_name_with_spaces, quantity__gt=10).order_by('model_name')
    # Извлечение первой буквы\цифры названия модели
    check_letter_list = []
    try:
        first_letter = query_list[0].model_name[0]
        check_letter_list.append(first_letter)

        for i in query_list:

            letter = i.model_name[0]
            model_name = i.model_name.replace('_', ' ')
            model_url = i.model_name.replace(' ', '_')
            if letter not in check_letter_list:
                previous_letter = check_letter_list[-1]
                super_list.append(
                    {"letter": previous_letter, "models": models_list})
                check_letter_list.append(letter)
                models_list = []

            models_list.append(
                {'name': model_name, 'url': model_url})

        # NOT DRY ENOUGH
        # Приходится повторятся, чтобы добавить модель на последнюю букву см issues #12
        previous_letter = check_letter_list[-1]
        super_list.append(
            {"letter": previous_letter, "models": models_list})

        brand_link = brand.replace(' ', '_')

        context = {
            'brand_name': brand_name_with_spaces,
            'brand_link': brand_link,
            'models': super_list
        }
        return render(request, 'front/brand.html', context)
    except:
        context = {
            "error": True
        }
        return render(request, 'front/brand.html', context)


@login_required
def model(request, brand, model):
    print(model)
    brand = brand.replace('_', ' ')
    model = model.replace('_', ' ')
    js_lables, js_price = graps_JSON(brand, model)
    # graps.build_grap(brand, model)
    # slope_index = slopes_calc.slope_starter(brand, model)

    context = {
        'brand_name': brand,
        'model_name': model,
        # 'slope_index': slope_index,
        # 'js_data': js_data,
        'js_lables': js_lables,
        'js_price': js_price,
    }
    return render(request, 'front/car.html', context)


@login_required
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

    lables = json.dumps(lables)
    data_price = json.dumps(data_price)
    return lables, data_price


def test(request):
    return HttpResponse('PIPISA')

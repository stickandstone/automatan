from django.shortcuts import render
import sqlite3
from . import graps, slopes_calc
from django.http import HttpResponse
# from front.forms import IndexForm
from django import forms
from . import models

# Create your views here.


# def index(request):
#     return HttpResponse("<h1>Test karatest!</h1>")
# Вот чтобы такую ебобятину не писать, как сверху, существует модуль шорткаты
# Чтобы не писать функцию ХттпРеспонс
#
# Надо чертые листа, list_of_Brands_for_link, list_of_Models_for_link
# list_Of_Brand_Name, list_Of_Model_Name
#

# def get(request):
#     form = IndexForm
# return render HttpResponse("<h1>Test karatest!</h1>")


def get_brands_from_DB():
    conn = sqlite3.connect('MyData.db')
    c = conn.cursor()
    c.execute("SELECT company_name FROM manufactories")
    raw_list = c.fetchall()
    brands_list = []
    for i in raw_list:
        brands_list.append(i[0])
    return brands_list


def query_to_DB(kinde, brand):
    conn = sqlite3.connect('MyData.db')
    c = conn.cursor()
    brands_list = []
    models_list = []

    if kinde == 'brands':
        c.execute("SELECT company_name FROM manufactories")
        raw_list = c.fetchall()
        for i in raw_list:
            temp = i[0]
            # Чтобы линк с пробелом не подавать в рендер
            temp = temp.replace(' ', '_')
            brands_list.append({'name': i[0], 'url': temp})
            # тут у нас на выходе лист со словорями [{'name': Land rover, url: Land_rover}]
        return brands_list

    if kinde == 'models':
        # А это просто оббосться как смешно, такой костыль дичайший.
        brand_link = brand.replace(' ', '_')
        brand_name = brand.replace('_', ' ')
        print('BRAND', brand)
        c.execute(
            "SELECT Model_name FROM car_names WHERE Brand_name=? AND Quantity>10", (brand_name,))
        raw_list = c.fetchall()
        print('RAWLIST', raw_list)
        for i in raw_list:
            temp = i[0]
            temp = temp.replace(' ', '_')
            models_list.append({'name': i[0], 'url': temp})
        return models_list, brand_name, brand_link


def index(request):
    brands_list = list(models.Manufactories.objects.all())
    brands = []

    for i in brands_list:
        brands.append({'name': i, 'link': str(i).replace(' ', '_')})

    context = {
        "brands": brands
    }
    return render(request, 'front/index.html', context)


# def brand(request, brand):
#     models_list, brand_name, brand_link = query_to_DB('models', brand)

#     context = {
#         "brand_name": brand_name,
#         "brand_link": brand_link,
#         "models": models_list
#     }
#     return render(request, 'front/brand.html', context)

def brand(request, brand):
    models_list, brand_name, brand_link = query_to_DB('models', brand)

    context = {
        "brand_name": brand_name,
        "brand_link": brand_link,
        "models": models_list
    }
    return render(request, 'front/brand.html', context)


def model(request, brand, model):
    print('Start Graph Build!')
    graps.build_grap(brand, model)
    slope_index = slopes_calc.slope_starter(brand, model)
    context = {
        "brand_name": brand,
        "model_name": model,
        "slope_index": slope_index
    }
    # return HttpResponse("<h1>Ready!</h1>")
    return render(request, 'front/car.html', context)


def about(request):
    return render(request, 'front/about.html')

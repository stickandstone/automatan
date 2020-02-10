from django.shortcuts import render
import sqlite3
# Create your views here.


# from django.http import HttpResponse
# def index(request):
#     return HttpResponse("<h1>Test karatest!</h1>")
# Вот чтобы такую ебобятину не писать, как сверху, существует модуль шорткаты
# Чтобы не писать функцию ХттпРеспонс

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
    return_list = []
    return_list_url = []

    if kinde == 'brands':
        c.execute("SELECT company_name FROM manufactories")
        raw_list = c.fetchall()
        for i in raw_list:
            temp = i[0]
            # Чтобы линк с пробелом не подавать в рендер
            temp = temp.replace(' ', '_')
            return_list.append({'name': i[0], 'url': temp})
            # return_list_url.append(temp)
        return return_list
    if kinde == 'models':
        # А это просто оббосться как смешно, такой костыль дичайший.
        brand = brand.replace('_', ' ')
        print('OK I AM HERE')
        c.execute("SELECT Model_name FROM car_names WHERE Brand_name=?", (brand,))
        raw_list = c.fetchall()
        for i in raw_list:
            return_list.append(i[0])
        print(return_list)
        return return_list, brand


def index(request):
    print('Нихуя себе!')
    # brands_list = get_brands_from_DB()
    brands_list = query_to_DB('brands', None)
    context = {
        'brands': brands_list
    }
    print(context)
    return render(request, 'front/index.html', context)


def brand(request, brand):
    models_list, brand = query_to_DB('models', brand)
    context = {
        "brand": brand,
        "models": models_list
    }
    return render(request, 'front/brand.html', context)


def about(request):
    return render(request, 'front/about.html')

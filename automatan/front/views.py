from django.shortcuts import render
import sqlite3
# Create your views here.


# from django.http import HttpResponse
# def index(request):
#     return HttpResponse("<h1>Test karatest!</h1>")
# Вот чтобы такую ебобятину не писать, как сверху, существует модуль шорткаты
# Чтобы не писать функцию ХттпРеспонс

conn = sqlite3.connect('MyData.db')
c = conn.cursor()
c.execute("SELECT company_name FROM manufactories")
raw_list = c.fetchall()
test_list = []
for i in raw_list:
    test_list.append(i[0])


def index(request):
    context = {
        'brands': test_list
    }
    return render(request, 'front/index.html', context)


def about(request):
    return render(request, 'front/about.html')

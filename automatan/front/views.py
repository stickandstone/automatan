from django.shortcuts import render, redirect
from . import models, index_logic, brand_logic, graphs_JSON
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import ListView
from .models import Manufactories
from django.contrib.auth.mixins import LoginRequiredMixin


class TestList(LoginRequiredMixin, ListView):
    model = Manufactories

    def get_context_data(self, **kwargs):
        num_visits = 0
        context = super(TestList, self).get_context_data(**kwargs)
        context = index_logic.get_context(num_visits)
        print(context)
        return context


@login_required
def index(request):
    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits+1
    context = index_logic.get_context(num_visits)
    return render(request, 'front/index.html', context)


@login_required
def brand(request, brand):
    context = brand_logic.get_context(brand)
    return render(request, 'front/brand.html', context)


@login_required
def model(request, brand, model):
    session_var = request.session.get('session_var')
    brand = brand.replace('_', ' ')
    model = model.replace('_', ' ')
    go_none = []

    js_lables, js_price = graphs_JSON.make_json_data(brand, model)
    context = {
        'ses_var': session_var,
        'brand_name': brand,
        'model_name': model,
        'js_lables': js_lables,
        'js_price': js_price,
        'go_none': go_none,
    }

    if session_var != None and session_var != '[]':

        brand2 = session_var.split(' ')[0]
        model2 = session_var.split(' ')[1]
        js_lables2, js_price2 = graphs_JSON.make_json_data(brand2, model2)
        can_delete = True
        context2 = {
            'brand_name2': brand2,
            'model_name2': model2,
            'js_lables2': js_lables2,
            'js_price2': js_price2,
            'ses_var': session_var,
            'can_delete': can_delete,
            'go_none': go_none,

        }
        context.update(context2)

    carname_compar = request.POST.getlist('session_var')
    if carname_compar != [] and carname_compar != ['[]']:
        request.session['session_var'] = carname_compar[0]
        messages.success(
            request, f'{carname_compar[0]} добавлена для сравнения!'
            ' Выберете машину из списка с которой хотите сравнить')
        return redirect('front-index')
    elif carname_compar == ['[]']:
        request.session['session_var'] = None
        session_var = None
        messages.warning(request, "Модель для сравнения удалена.")
        can_delete = False
        context = {
            'ses_var': session_var,
            'brand_name': brand,
            'model_name': model,
            'js_lables': js_lables,
            'js_price': js_price,
            'go_none': go_none,
            'can_delete': can_delete,
        }
        return render(request, 'front/car.html', context)
    else:
        return render(request, 'front/car.html', context)


@login_required
def about(request):
    return render(request, 'front/about.html')


'''
че хочу сделать? Нужно создать новый темплейт для сравнения? Как тогда это будет выглядеть?
Я захожу в основной темплейт.
Выбираю марку.
Выбираю модель.
Нажимаю кнопку сравнения.
Попадаю на главную.
Повторяю процесс.
Попадаю на страницу сравнения. brand/name/graph-car -> comparasing/brand/name/graph-car1-car2


'''

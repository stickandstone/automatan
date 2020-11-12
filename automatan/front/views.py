from django.http import request
from django.shortcuts import render, redirect
from . import models, index_logic, brand_logic, model_logic, years_logic
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import ListView
from .models import Manufactories
from django.contrib.auth.mixins import LoginRequiredMixin


class TestList(LoginRequiredMixin, ListView):
    model = Manufactories

    def get_context_data(self, **kwargs):
        num_visits = 1
        # context = super(TestList, self).get_context_data(**kwargs)
        context = index_logic.get_context(num_visits)
        # print(context)
        return context

# class BrandList(LoginRequiredMixin, ListView):
#     def suka_kak_tebya_nazvat(brand):
#         context = brand_logic.get_context(brand)


# @login_required
def index(request):
    request.session.set_test_cookie()
    if request.session.test_cookie_worked():
        request.session.delete_test_cookie()
    else:
        # request.session.set_test_cookie()
        messages.error(
            request, 'Для правильной работы сайта требуются включенные coockies.')

    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits+1
    context = index_logic.get_context(num_visits)
    return render(request, 'front/index.html', context)


# @login_required
def brand(request, brand):
    context = brand_logic.get_context(brand)
    return render(request, 'front/brand.html', context)


def year(request, brand, model):
    all_years = years_logic.get_all_years(brand, model)
    context = {'brand': brand, 'model': model, 'years': all_years}
    return render(request, 'front/year.html', context)


# def model_a(request, brand, model):
#     context = brand_logic.get_context(brand)
#     return render(request, 'front/year.html', context)


# @login_required
def model(request, brand, model, year):
    brand = brand.replace('_', ' ')
    model = model.replace('_', ' ')
    pre_context = request.session.get('prev_context', None)
    is_compar = request.session.get('compar', False)
    print('PRRRE: ', pre_context)
    print('Is?:', is_compar)
    context = model_logic.Grap(brand, model, year).get_context()
    # print(a.get_context())
    # context = model_logic.Grap.get_context(brand, model, year)
    # context = model_logic.get_context(brand, model, year)

    carname_compar = request.POST.getlist('session_var')
    compar = request.POST.get('compar')
    print(f'start def model. {carname_compar}')
    if compar:
        request.session['compar'] = True
        request.session['pre_context'] = context
        messages.success(
            request, f'{carname_compar[0]} года добавлена для сравнения!'
            ' Выберете машину из списка с которой хотите сравнить')
        # return redirect('front-index')

    return render(request, 'front/car.html', context)
#####################################################

    # context = {
    #     'year': year,
    #     'ses_var': session_var,
    #     'brand_name': brand,
    #     'model_name': model,
    #     'js_lables': js_lables,
    #     'js_price': js_price,
    #     'go_none': go_none,
    # }

    # if session_var != None and session_var != '[]':
    #     print('Sesseion var: ', session_var)
    #     brand2 = session_var.split(' ')[0]
    #     model2 = session_var.split(' ')[1]
    #     year2 = session_var.split(' ')[2]
    #     js_lables2, js_price2 = model_logic.make_json_data_years(
    #         brand2, model2, year2)
    #     # can_delete = True
    #     context2 = {
    #         'year2': year2,
    #         'brand_name2': brand2,
    #         'model_name2': model2,
    #         'js_lables2': js_lables2,
    #         'js_price2': js_price2,
    #         'ses_var': session_var,
    #         'can_delete': True,
    #         'go_none': go_none,

    #     }
    #     context.update(context2)

    # carname_compar = request.POST.getlist('session_var')
    # if carname_compar != [] and carname_compar != ['[]']:
    #     request.session['session_var'] = carname_compar[0]
    #     messages.success(
    #         request, f'{carname_compar[0]} добавлена для сравнения!'
    #         ' Выберете машину из списка с которой хотите сравнить')
    #     return redirect('front-index')

    # elif carname_compar == ['[]']:
    #     request.session['session_var'] = None
    #     session_var = None
    #     messages.warning(request, "Модель сравнения удалена.")
    #     can_delete = False
    #     context = {
    #         'ses_var': session_var,
    #         'brand_name': brand,
    #         'model_name': model,
    #         'js_lables': js_lables,
    #         'js_price': js_price,
    #         'go_none': go_none,
    #         'can_delete': can_delete,
    #     }
    #     return render(request, 'front/car.html', context)
    # else:
    #     return render(request, 'front/car.html', context)


# @login_required
def about(request):
    return render(request, 'front/about.html')

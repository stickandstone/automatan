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
        context = index_logic.get_context(num_visits)
        return context

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

# @login_required


def model(request, brand, model, year):
    brand = brand.replace('_', ' ')
    model = model.replace('_', ' ')
    pre_context = request.session.get('prev_context', None)
    is_compar = request.session.get('compar', False)
    context = model_logic.Grap(brand, model, year).get_context()

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

# @login_required


def about(request):
    return render(request, 'front/about.html')

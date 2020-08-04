from django.shortcuts import render, redirect
from . import models, index_logic, brand_logic, graphs_JSON
from django.contrib.auth.decorators import login_required


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
    brand = brand.replace('_', ' ')
    model = model.replace('_', ' ')
    js_lables, js_price = graphs_JSON.make_json_data(brand, model)
    context = {
        'brand_name': brand,
        'model_name': model,
        'js_lables': js_lables,
        'js_price': js_price,
    }
    return render(request, 'front/car.html', context)


@login_required
def about(request):
    return render(request, 'front/about.html')

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
    check = False
    js_lables, js_price = graphs_JSON.make_json_data(brand, model)
    context = {
        'brand_name': brand,
        'model_name': model,
        'js_lables': js_lables,
        'js_price': js_price,
        'comparasing': check,
    }
    check_fist = request.POST.getlist('check_first')
    if check_fist:
        check = True

        print("CHECK_FIRST")
        brand2 = 'Acura'
        model2 = 'MDX'
        js_lables2, js_price2 = graphs_JSON.make_json_data(brand2, model2)
        context2 = {
            'brand_name2': brand2,
            'model_name2': model2,
            'js_lables2': js_lables2,
            'js_price2': js_price2,
            'comparasing': check,
        }
        test_but = request.POST.getlist('test_button')
        context.update(context2)
        print(context)
        return render(request, 'front/car.html', context)

    return render(request, 'front/car.html', context)


@login_required
def about(request):
    return render(request, 'front/about.html')

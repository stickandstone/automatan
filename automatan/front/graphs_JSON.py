import numpy as np
import json
from . import models


def make_json_data(brand, model):
    '''Создает джейсон для построения графика год:цена'''
    lables = []

    selected_cars = models.Cars.objects.filter(
        brand=brand, model=model).order_by('-year')
    try:
        current_year = selected_cars[0].year
    except:
        current_year = '2020'

    price_for_specific_year = []
    lables = []
    data_price = []

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

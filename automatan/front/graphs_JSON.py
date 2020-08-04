import numpy as np
import json
from . import models


def make_json_data(brand, model):
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

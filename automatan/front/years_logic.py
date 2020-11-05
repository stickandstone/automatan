from . import models


def get_all_years(brand, model):
    brand = brand.replace('_', ' ')
    model = model.replace('_', ' ')
    query_list = models.Cars.objects.filter(
        brand=brand, model=model
    ).order_by('-year').values_list('year')

    all_years = set()
    for row in query_list:
        all_years.add(row[0])
    all_years = list(all_years)
    all_years.sort()
    return all_years

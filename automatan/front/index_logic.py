from . import models


def get_context(num_visits):
    '''
    Собирает все бренды из базы, созадает список с заглавными буквами
    и отправляет их в виде контекста для вьюшки.
    '''
    brands_list = list(
        models.Manufactories.objects.all().filter())

    brands = []
    check_letter = []
    super_list = []

    # первая инициализация
    first_init = str(brands_list[0])
    first_letter = first_init[0]
    check_letter.append(first_letter)

    for i in brands_list:
        # print(i)
        temp_list = []
        letter = str(i)[0]
        url = str(i).replace(' ', '_')

        # добавляем заглавную букву для навигации
        if letter not in check_letter:
            # check_letter[-1] - это предыдущая буква
            super_list.append({"letter": check_letter[-1], "brands": brands})
            check_letter.append(letter)
            brands = []

        brands.append({'name': i, 'link': url})
    super_list.append({"letter": check_letter[-1], "brands": brands})

    context = {
        'brands': super_list,
        'iter_list': check_letter,
        'num_visits': num_visits
    }

    return context

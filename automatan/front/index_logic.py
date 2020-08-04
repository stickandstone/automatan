from . import models


def get_context(num_visits):
    brands_list = list(models.Manufactories.objects.all())

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
            # print(letter, i)
            previous_letter = check_letter[-1]
            super_list.append({"letter": previous_letter, "brands": brands})
            check_letter.append(letter)
            brands = []

        brands.append({'name': i, 'link': url})
    # NOT DRY ENOUGH
    # Приходится повторятся, чтобы добавить модель на последнюю букву см issues #12
    previous_letter = check_letter[-1]
    super_list.append({"letter": previous_letter, "brands": brands})

    context = {
        'brands': super_list,
        'iter_list': check_letter,
        'num_visits': num_visits
    }

    return context

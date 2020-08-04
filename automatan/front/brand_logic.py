from . import models


def get_context(brand):
    models_list = []
    super_list = []
    brand_name_with_spaces = brand.replace('_', ' ')
    query_list = models.CarNames.objects.filter(
        brand_name=brand_name_with_spaces, quantity__gt=10).order_by('model_name')
    # Извлечение первой буквы\цифры названия модели
    check_letter_list = []
    try:
        first_letter = query_list[0].model_name[0]
        check_letter_list.append(first_letter)

        for i in query_list:

            letter = i.model_name[0]
            model_name = i.model_name.replace('_', ' ')
            model_url = i.model_name.replace(' ', '_')
            if letter not in check_letter_list:
                previous_letter = check_letter_list[-1]
                super_list.append(
                    {"letter": previous_letter, "models": models_list})
                check_letter_list.append(letter)
                models_list = []

            models_list.append(
                {'name': model_name, 'url': model_url})

        # NOT DRY ENOUGH
        # Приходится повторятся, чтобы добавить модель на последнюю букву см issues #12
        previous_letter = check_letter_list[-1]
        super_list.append(
            {"letter": previous_letter, "models": models_list})

        brand_link = brand.replace(' ', '_')

        context = {
            'brand_name': brand_name_with_spaces,
            'brand_link': brand_link,
            'models': super_list
        }

    except:
        context = {
            "error": True
        }
    return context

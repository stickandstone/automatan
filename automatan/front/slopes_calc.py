import sqlite3
import numpy as np
import matplotlib.pyplot as plt
import matplotlib

# создаем таблицу бренд модель слоуп
# берем таблицу бренд-модель, смотрим на кол-во машин, если меньше 100 -- нах.
# Сортируем по годам? Берем первую строчку и отнимаем от реального года год поста
# находим медиану по цене в точке 0 и в точке 1, вычитаем 0 - 1


# def slope_starter(brand, model):
#     try:
#         conn = sqlite3.connect('MyData.db')
#         c = conn.cursor()
#         # brand = "Mitsubishi"
#         # model = "L200"
#         # brand = "BMW"

#         # model = "7-Series"

#         query = f"SELECT year, price FROM cars WHERE brand='{brand}' AND model='{model}'"
#         c.execute(query)
#         raw_data = c.fetchall()
#         raw_data = sorted(raw_data, key=lambda year: year[0])
#         current_year = raw_data[0][0]
#         prices_for_year = []
#         result = []

#         for item in raw_data:
#             if current_year == item[0]:
#                 prices_for_year.append(item[1])
#             else:
#                 # result.append([current_year, int(np.median(prices_for_year))])
#                 result.append([current_year, int(np.average(prices_for_year))])

#                 prices_for_year = []
#                 current_year = item[0]
#                 prices_for_year.append(item[1])
#         result.append([current_year, int(np.average(prices_for_year))])

#         result.reverse()
#         print(result)
#         data_for_print = []
#         mid_slope = []
#         # for i in range(len(result[:-1])):
#         cut_var = len(result)
#         for i in range(len(result[:cut_var-1])):
#             calc = result[i][1] - result[i+1][1]
#             if calc != 0:
#                 slope = ((1/(calc))*10**5)*(-1)
#                 if slope > 10:
#                     slope = 10
#                 if slope < -10:
#                     slope = -10
#                 data_for_print.append([i, slope])
#                 mid_slope.append(slope)
#                 # print(slope, calc)

#         print(model, int(np.average(mid_slope)))

#         def projet_to_axis(data):
#             x = []
#             y = []
#             for i in data:
#                 x.append(i[0])
#                 y.append(i[1])
#             return x, y

#         graph_x, graph_y = projet_to_axis(data_for_print)

#         plt.style.use('fivethirtyeight')
#         plt.bar(graph_x, graph_y)
#         # plt.show()
#         plt.savefig(
#             'front/static/front/test_slope.png', dpi=200)
#         plt.close()
#     except:
#         print('ERROR IN SLOPE!')


def slope_starter(brand, model):
    model = model.replace('_', ' ')
    brand = brand.replace('_', ' ')

    conn = sqlite3.connect('MyData.db')
    c = conn.cursor()
    # brand = "Mitsubishi"
    # model = "L200"
    # brand = "BMW"

    # model = "7-Series"

    query = f"SELECT year, price FROM cars WHERE brand='{brand}' AND model='{model}'"
    c.execute(query)
    raw_data = c.fetchall()
    raw_data = sorted(raw_data, key=lambda year: year[0])
    current_year = raw_data[0][0]
    prices_for_year = []
    result = []

    for item in raw_data:
        if current_year == item[0]:
            prices_for_year.append(item[1])
        else:
            # result.append([current_year, int(np.median(prices_for_year))])
            result.append([current_year, int(np.average(prices_for_year))])

            prices_for_year = []
            current_year = item[0]
            prices_for_year.append(item[1])
    result.append([current_year, int(np.average(prices_for_year))])

    result.reverse()
    data_for_print = []
    mid_slope = []
    # for i in range(len(result[:-1])):
    cut_var = len(result)
    for i in range(len(result[:cut_var-1])):
        calc = result[i][1] - result[i+1][1]
        if calc != 0:
            slope = ((1/(calc))*10**5)*(-1)
            if slope > 0:
                slope = 0
            if slope < -20:
                slope = -20
            data_for_print.append([i, slope])
            mid_slope.append(slope)
            # print(slope, calc)

    slope_index = np.average(mid_slope)

    print(model, slope_index)

    def projet_to_axis(data):
        x = []
        y = []
        for i in data:
            x.append(i[0])
            y.append(i[1])
        return x, y

    graph_x, graph_y = projet_to_axis(data_for_print)

    plt.style.use('fivethirtyeight')
    plt.bar(graph_x, graph_y)
    # plt.show()
    plt.savefig(
        'front/static/front/test_slope.png', dpi=200)
    plt.close()

    return slope_index

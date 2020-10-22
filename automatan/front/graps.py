# from collections import Counter
# import sqlite3
# import matplotlib.pyplot as plt
# import numpy as np
# # import pandas as pd
# import matplotlib
# matplotlib.use('Agg')
# # import seaborn as sns


# def cooking(raw_data):
#     raw_data = sorted(raw_data, key=lambda year: year[0])
#     # print(raw_data)
#     current_year = raw_data[0][0]
#     prices_for_year = []
#     result = []

#     for item in raw_data:
#         if current_year == item[0]:
#             prices_for_year.append(item[1])
#         else:
#             result.append([current_year, int(np.median(prices_for_year))])
#             prices_for_year = []
#             current_year = item[0]
#             prices_for_year.append(item[1])
#     result.append([current_year, int(np.median(prices_for_year))])

#     return result


# def projet_to_axis(data):
#     x = []
#     y = []
#     for i in data:
#         x.append(i[0])
#         y.append(i[1])
#     return x, y


# def build_grap(brand, model):
#     # brand = brand.replace('_', ' ')
#     # model = model.replace('_', ' ')

#     conn = sqlite3.connect('MyData.db')
#     c = conn.cursor()
#     # brand = "Kia"
#     # model = "Rio"

#     query = f"SELECT year, price FROM cars WHERE brand='{brand}' AND model='{model}' AND year > '1990' "
#     c.execute(query)
#     raw_data_all = c.fetchall()
#     c.execute(query + "AND gearbox='автомат'")
#     raw_data_auto = c.fetchall()
#     c.execute(query + "AND gearbox='механика'")
#     raw_data_man = c.fetchall()

#     plt.style.use('fivethirtyeight')

#     cooked_data_all = cooking(raw_data_all)
#     if len(raw_data_auto) != 0:
#         cooked_data_auto = cooking(raw_data_auto)
#         grap_auto_x, grap_auto_y = projet_to_axis(cooked_data_auto)
#         plt.plot(grap_auto_x, grap_auto_y, label='Автомат')

#     if len(raw_data_man) != 0:
#         cooked_data_manual = cooking(raw_data_man)
#         grap_manual_x, grap_manual_y = projet_to_axis(cooked_data_manual)
#         plt.plot(grap_manual_x, grap_manual_y, label='Механика')

#     # перевернуть график
#     # зарефакторить все под функцию, чтобы вызывалось по переменным
#     grap_all_x, grap_all_y = projet_to_axis(cooked_data_all)

#     # plt.style.use('seaborn')
#     plt.plot(grap_all_x, grap_all_y, label='Все')

#     hi_lim = int(max(grap_all_x))
#     lo_lim = int(min(grap_all_x))
#     plt.xticks(np.arange(lo_lim, hi_lim+1))
#     plt.xlim(hi_lim+1, lo_lim)

#     SMALL_SIZE = 8
#     MEDIUM_SIZE = 10
#     BIGGER_SIZE = 12

#     plt.rc('font', size=SMALL_SIZE)          # controls default text sizes
#     plt.rc('axes', titlesize=SMALL_SIZE)     # fontsize of the axes title
#     plt.rc('axes', labelsize=MEDIUM_SIZE)    # fontsize of the x and y labels
#     plt.rc('xtick', labelsize=4)    # fontsize of the tick labels
#     plt.rc('ytick', labelsize=4)    # fontsize of the tick labels
#     plt.rc('legend', fontsize=SMALL_SIZE)    # legend fontsize
#     plt.rc('figure', titlesize=BIGGER_SIZE)

#     SMALL_SIZE = 8
#     matplotlib.rc('font', size=SMALL_SIZE)
#     matplotlib.rc('axes', titlesize=SMALL_SIZE)

#     plt.xlabel('Год выпуска')
#     plt.ylabel('Цена')
#     plt.title(f'{brand} {model}')

#     plt.legend()
#     # plt.grid(True)
#     plt.tight_layout()
#     plt.savefig(
#         'front/static/front/test.png', dpi=200)
#     plt.close()

#     # plt.show()


# # build_grap("Subaru", "Forester")

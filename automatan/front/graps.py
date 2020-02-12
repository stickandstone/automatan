import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sqlite3
from collections import Counter


def cooking(raw_data):
    raw_data = sorted(raw_data, key=lambda year: year[0])
    current_year = raw_data[0][0]
    prices_for_year = []
    result = []

    for item in raw_data:
        if current_year == item[0]:
            prices_for_year.append(item[1])
        else:
            result.append([current_year, int(np.median(prices_for_year))])
            prices_for_year = []
            current_year = item[0]
            prices_for_year.append(item[1])
    result.append([current_year, int(np.median(prices_for_year))])

    return result


def projet_to_axis(data):
    x = []
    y = []
    for i in data:
        x.append(i[0])
        y.append(i[1])
    return x, y


def build_grap(brand, model):

    conn = sqlite3.connect('MyData.db')
    c = conn.cursor()
    # brand = "Kia"
    # model = "Rio"

    query = f"SELECT year, price FROM cars WHERE brand='{brand}' AND model='{model}'"
    c.execute(query + "AND gearbox='автомат'")
    raw_data_auto = c.fetchall()
    c.execute(query + "AND gearbox='механика'")
    raw_data_man = c.fetchall()

    cooked_data_auto = cooking(raw_data_auto)
    cooked_data_manual = cooking(raw_data_man)

    # перевернуть график
    # зарефакторить все под функцию, чтобы вызывалось по переменным

    grap_auto_x, grap_auto_y = projet_to_axis(cooked_data_auto)
    grap_manual_x, grap_manual_y = projet_to_axis(cooked_data_manual)

    plt.style.use('fivethirtyeight')
    # plt.style.use('seaborn')

    plt.plot(grap_auto_x, grap_auto_y, label='Автомат')
    plt.plot(grap_manual_x, grap_manual_y, label='Механика')

    hi_lim = int(max(grap_auto_x))
    lo_lim = int(min(grap_manual_x))
    plt.xticks(np.arange(lo_lim, hi_lim+1))
    plt.xlim(hi_lim+1, lo_lim)

    plt.xlabel('Год выпуска')
    plt.ylabel('Цена')
    plt.title(f'{brand} {model}')

    plt.legend()
    # plt.grid(True)
    plt.tight_layout()

    plt.show()


# build_grap("Subaru", "Forester")

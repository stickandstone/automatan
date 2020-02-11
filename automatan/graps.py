import numpy as nu
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sqlite3


conn = sqlite3.connect('MyData.db')
c = conn.cursor()
c.execute("SELECT year, price FROM cars WHERE brand='Kia' AND model='Rio'")
raw_data = c.fetchall()
gra_x = []
gra_y = []

for i in raw_data:
    gra_x.append(i[0])
    gra_y.append(i[1])
# sns.set(style='darkgrid')
# cars = sns.load_dataset(raw_data)
# sns.relplot(x="Year", y="Price", data=raw_data)

# plt.plot(gra_x, gra_y)
plt.scatter(gra_x, gra_y, color='#5a7d9a', label='rio')

plt.xlabel('Год выпуска')
plt.ylabel('Цена')
plt.title('Kia Rio')

plt.legend()
plt.show()

# fig = plt.figure()
# fig.suptitle('ПИЗДИИИИЩА ВОТ ТАКАААЯ!')

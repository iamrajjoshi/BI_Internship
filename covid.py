import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
from datetime import datetime as dt


df = pd.read_csv('test.csv')
date = df[df.columns[0]].tolist()
cases = df[df.columns[3]].tolist()
print(cases)

d = []
for i in range(0,len(date)):
	d.append(mdates.date2num(dt.strptime(date[i], '%Y-%m-%d')))

plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=1))

plt.plot(d,cases)
plt.gcf().autofmt_xdate()
plt.show()

if(d[0] == d[2]):
	print("yes")
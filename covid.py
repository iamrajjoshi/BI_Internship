import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
from datetime import datetime as dt

plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=20))

df = pd.read_csv('test.csv')
string_state = list(dict.fromkeys(df[df.columns[1]].tolist()))
data = {}

for i in range (0, len(string_state)):
	data.update({string_state[i]: []})
latestDate = df.at[0,'date']

days = 0
for i in range(0,int(df.size/5)):
	state = str(df.at[i,'state_name'])
	currentDate = df.at[i,'date']
	cases = df.at[i,'confirmed_cases']
	if(latestDate == currentDate):
		data[state].append(cases)
	else:
		latestDate = currentDate
		days +=1
		for j in data:
			if(len(data[j]) < days):
				if(len (data[j]) == 0):
					data[j].append(0)
				else:
					data[j].append(data[j][-1])
		data[state].append(cases)
days +=1
for j in data:
	if(len(data[j]) < days):
		data[j].append(0)		
#print(data)

#Get all Dates
string_date = list(dict.fromkeys(df[df.columns[0]].tolist()))
date = []
for i in range(0,len(string_date)):
	date.append(mdates.date2num(dt.strptime(string_date[i], '%Y-%m-%d')))
#print(date)


for y in data:
	plt.plot(date, data[y], label = str(y))
plt.legend()
plt.gcf().autofmt_xdate()
plt.show()
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
from datetime import datetime as dt

plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=20))

dataFrame = pd.read_csv('test.csv')
uniqueStates = list(dict.fromkeys(dataFrame[dataFrame.columns[1]].tolist()))

data = {}
for i in range (0, len(uniqueStates)):
	data.update({uniqueStates[i]: []})

#Fill data with a list of all the cases of each state
newDate = dataFrame.at[0,'date']
day = 0
for i in range(0,int(dataFrame.size/5)):
	state = str(dataFrame.at[i,'state_name'])
	currentDate = dataFrame.at[i,'date']
	cases = dataFrame.at[i,'confirmed_cases']
	if(newDate == currentDate):
		data[state].append(cases)
	else:
		newDate = currentDate
		day +=1
		for j in data:
			if(len(data[j]) < day):
				if(len (data[j]) == 0):
					data[j].append(0)
				else:
					data[j].append(data[j][-1])
		data[state].append(cases)
day +=1
for j in data:
	if(len(data[j]) < day):
		data[j].append(0)		

#Get all Dates
string_date = list(dict.fromkeys(dataFrame[dataFrame.columns[0]].tolist()))
date = []
for i in range(0,len(string_date)):
	date.append(mdates.date2num(dt.strptime(string_date[i], '%Y-%m-%d')))
#print(date)
sumStates = [0]*(day+1)
for each in data:
	data[each].insert(0,data[each][0])
	data[each] = list(map(int, data[each])) 
	data[each] = [data[each][n]-data[each][n-1] for n in range(1,len(data[each]))]
	sumStates = [sum(x) for x in zip(sumStates, data[each])]

N = 7
cumsum, moving_aves = [0], []
for i, x in enumerate(sumStates, 1):
    cumsum.append(cumsum[i-1] + x)
    if i>=N:
        moving_ave = (cumsum[i] - cumsum[i-N])/N
        #can do stuff with moving_ave here
        moving_aves.append(moving_ave)
for i in range(0,N-1):
	moving_aves.insert(0,0)

clickDataFrame = pd.read_csv('bob.csv')
clicks = clickDataFrame[clickDataFrame.columns[1]].tolist()

N = 7
cumsum, clicksavg = [0], []
for i, x in enumerate(clicks, 1):
    cumsum.append(cumsum[i-1] + x)
    if i>=N:
        moving_ave = ((cumsum[i] - cumsum[i-N])/N)*0.1
        #can do stuff with moving_ave here
        clicksavg.append(moving_ave)
for i in range(0,N-1):
	clicksavg.insert(0,0)

clickDataFrame = pd.read_csv('vaccine.csv')
vaccine = clickDataFrame[clickDataFrame.columns[1]].tolist()

N = 7
cumsum, vaccineavg = [0], []
for i, x in enumerate(vaccine, 1):
    cumsum.append(cumsum[i-1] + x)
    if i>=N:
        moving_ave = ((cumsum[i] - cumsum[i-N])/N)*3
        #can do stuff with moving_ave here
        vaccineavg.append(moving_ave)
for i in range(0,N-1):
	vaccineavg.insert(0,0)

#plt.plot(date, sumStates, label = str('USA'))
plt.plot(date, clicksavg, label = str('clicks'))
plt.plot(date, moving_aves, label = str('USA 7 Day Average'))
plt.plot(date, vaccineavg, label = str('vaccine'))
plt.legend()
plt.gcf().autofmt_xdate()
#print(moving_aves)
plt.show()
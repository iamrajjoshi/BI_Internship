import pandas as pd
from mpl_toolkits.axisartist.parasite_axes import HostAxes, ParasiteAxes
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime as dt

def runningAverage(N, inputList):
	N = 7
	cumsum, moving_aves = [0], []
	for i, x in enumerate(inputList, 1):
		cumsum.append(cumsum[i-1] + x)
		if i>=N:
			moving_ave = (cumsum[i] - cumsum[i-N])/N
			moving_aves.append(moving_ave)
	for i in range(0,N-1):
		moving_aves.insert(0,0)
	return moving_aves

def covidCases(df):
	uniqueStates = list(dict.fromkeys(df[df.columns[1]].tolist()))
	cases = {}
	for i in range (0, len(uniqueStates)):
		cases.update({uniqueStates[i]: []})

	#Fill data with a list of all the cases of each state
	newDate = df.at[0,'date']
	day = 0
	for i in range(0,int(df.size/5)):
		state = str(df.at[i,'state_name'])
		currentDate = df.at[i,'date']
		rawCases = df.at[i,'confirmed_cases']
		if(newDate == currentDate):
			cases[state].append(rawCases)
		else:
			newDate = currentDate
			day +=1
			for j in cases:
				if(len(cases[j]) < day):
					if(len (cases[j]) == 0):
						cases[j].append(0)
					else:
						cases[j].append(cases[j][-1])
			cases[state].append(rawCases)
	day +=1
	for j in cases:
		if(len(cases[j]) < day):
			cases[j].append(0)
	sumCases = [0]*(day+1)
	for each in cases:
		cases[each].insert(0,cases[each][0])
		cases[each] = list(map(int, cases[each]))
		cases[each] = [cases[each][n]-cases[each][n-1] for n in range(1,len(cases[each]))]
		sumCases = [sum(x) for x in zip(sumCases, cases[each])]
	return runningAverage(7, sumCases)

def extractDates(df):
	stringDates = list(dict.fromkeys(df[df.columns[0]].tolist()))
	dates = []
	for i in range(0,len(stringDates)):
		dates.append(mdates.date2num(dt.strptime(stringDates[i], '%Y-%m-%d')))
	return dates
	
def covidClicks(df):
	covid = df[df.columns[1]].tolist()
	return runningAverage(7,covid)

def vaccineClicks(df):
	vaccine = df[df.columns[1]].tolist()
	return runningAverage(7,vaccine)

def display(dates,cases,covid,vaccine):

	fig = plt.figure()
	host = HostAxes(fig, [0.15, 0.1, 0.65, 0.8])
	par1 = ParasiteAxes(host, sharex=host)
	par2 = ParasiteAxes(host, sharex=host)
	host.parasites.append(par1)
	host.parasites.append(par2)

	host.set_ylabel("Cases")

	host.axis["right"].set_visible(False)
	par1.axis["right"].set_visible(True)
	par1.set_ylabel("COVID - 19 Clicks")
	par1.axis["right"].major_ticklabels.set_visible(True)
	par1.axis["right"].label.set_visible(True)

	par2.set_ylabel("Vaccine Clicks")
	offset = (60, 0)
	new_axisline = par2.get_grid_helper().new_fixed_axis
	par2.axis["right2"] = new_axisline(loc="right", axes=par2, offset=offset)

	fig.add_axes(host)


	plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
	plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=7))

	p1, = host.plot(dates,cases, label="USA 7 Day Average")
	p2, = par1.plot(dates,covid, label="COVID Keyword Clicks")
	p3, = par2.plot(dates,vaccine, label="Vaccine Keyword Clicks")

	host.legend()

	host.axis["left"].label.set_color(p1.get_color())
	par1.axis["right"].label.set_color(p2.get_color())
	par2.axis["right2"].label.set_color(p3.get_color())

	plt.setp(host.axis["bottom"].major_ticklabels, rotation=45, ha="right")	
	plt.gcf().canvas.set_window_title('COVID-19 Cases vs. BI Search Queries')
	plt.show()


if __name__ == "__main__":
	df = pd.read_csv('cases.csv')
	dates = extractDates(df)
	cases = covidCases(df)
	
	df = pd.read_csv('covid_keywords.csv')
	covid = covidClicks(df)
	
	df = pd.read_csv('vaccine_keywords.csv')
	vaccine = vaccineClicks(df)
	
	display(dates,cases,covid,vaccine)

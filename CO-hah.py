
from pandas import read_csv
import pandas as pd
from matplotlib import pyplot as plt
import matplotlib.dates as mdates
from matplotlib.dates import DateFormatter
import datetime
import numpy as np

#plot settings
plt.rcParams['figure.figsize'] = [10, 4]

#import the data
data_file = measurement.csv
df = read_csv(data_file, parse_dates=True, header=0, squeeze=True)

#set date
date = df['date']
date_dt = [datetime.datetime.strptime(item, '%Y-%m-%d %H:%M:%S') for item in date]
df['date_dt'] = pd.DataFrame(date_dt)

# set calibration
x = [0.36, 19.20] # CO_concentration in ppm
y = [0, 285] # measurement in volt
beta = (y[1] - y[0]) / (x[1] - x[0])
alpha = y[1]-float(beta)*x[1]

# calculate the conversion
co_ppm = ((beta * df['voltage']) + alpha)
# set in a new raw
df['co_ppm'] = pd.DataFrame(co_ppm)

header = ['date_dt', 'voltage', 'co_ppm']
print(df[header].head())

#---calculate the half an hour mean : hah_mean
df.index= df['date_dt']
hah_mean = df['co_ppm'].resample('30T').mean()
index_of_maximum = np.where(hah_mean == hah_mean.max())[0]
index_of_minimum = np.where(hah_mean == hah_mean.min())[0]

print('highest halb-hour-mean-value for CO: ', np.around(hah_mean.max(),2), '(ppm) on ',hah_mean.index[index_of_maximum][0])
print('lowest halb-hour-mean-value for CO: ', np.around(hah_mean.min(),2), '(ppm) on ',hah_mean.index[index_of_minimum][0])

#plot
df.plot('date_dt', 'co_ppm', style='k.', label= 'CO concentration')

# set x-axis day.month
ax = plt.gca()
myFmt = DateFormatter("%d.%m")
ax.xaxis.set_major_formatter(myFmt)
ax.xaxis.set_major_locator(mdates.WeekdayLocator(interval=1))
ax.xaxis.set_minor_locator(mdates.DayLocator())

#plot mean
mean = df['co_ppm'].mean()
x_min = 0.01; x_max = 0.99
plt.axhline(mean, x_min, x_max, color='red', linestyle='-', linewidth=2, label='mean')

#plot the hah_mean

hah_mean.plot(label='half an hour mean', marker='_',  markersize=10, linestyle="")

#plot settings:
legend = ax.legend(loc='upper right', fontsize='large')
ax.set_ylim([0, 10])
plt.xlabel('date')
plt.ylabel('CO concentration [ppm]')
plt.title('CO Long-term Measurement')

plt.show()




import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
import pandas as pd
import pandas_datareader.data as web



style.use('ggplot')
end = dt.date.today()
years=5
time_period=dt.timedelta(weeks=years*52)
start=end-time_period


"""
for start date from a particular date uncomment this
start = dt.datetime(2000, 1, 1)#for a fixed start date

"""


df = web.DataReader('TSLA', "yahoo", start, end)

print(df.tail())
print(df.head())

"""
to do a combined plot
df.plot()
plt.show()

"""
"""
to plot a single data point
df['Adj Close'].plot()
plt.show()
"""
#multiple data points
df[['High','Low']].plot()
plt.show()

# instead of constantly extracting the Data from Web
df.to_csv('TSLA.csv')
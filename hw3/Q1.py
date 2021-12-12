import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def filterAndSave() -> pd.DataFrame:
    whole = pd.read_csv('SP500_stocks_5yr.csv')
    stockName = 'AAL'
    while True:
        stockName = input('Enter stock name: ')
        filtered = whole[whole['Name'] == stockName]
        if len(filtered) > 0:
            break
        else:
            print('Not found stock code {}'.format(stockName))

    print('The shape of the filtered data is {}'.format(filtered.shape))
    filtered.reset_index(drop=True, inplace=True)
    print('The filtered data for {} starts at {}, and ends at {}.'.format(stockName, filtered['date'][0], filtered['date'][len(filtered) - 1]))
    filtered.to_csv(stockName + '.csv')
    print('The filtered data saved as {}.'.format(stockName + '.csv'))
    return filtered

def movingAverage(values, window):
    weigths = np.repeat(1.0, window)/window
    smas = np.convolve(values, weigths, 'valid')
    return smas

def selectAndPlot(raw):
    raw['date'] = pd.to_datetime(raw['date'])
    startDate, endDate = '2013-02-10', '2013-06-20'
    movingAverageWindow = 15
    while True:
        startDate = input('Enter start date, as \'1949-10-01\': ')
        endDate = input('Enter start date, as \'1991-12-25\': ')
        movingAverageWindow = int(input('Enter the moving average: '))
        filtered = raw[(raw['date'] > startDate) & (raw['date'] < endDate)]
        if len(filtered) > 0:
            break
        else:
            print('Your date is out of range of the filtered stock information!')
    
    filtered.reset_index(drop=True, inplace=True)
    print(filtered.info())
    print(filtered.head(8))
    fig = plt.figure(figsize=(15, 10))
    fig.suptitle('Stock information of {} from {} to {}'.format(filtered['Name'][0], startDate, endDate))
    i = 0
    for priceType in ['open', 'close', 'high', 'low']:
        i += 1
        ax = fig.add_subplot(2, 2, i)
        ax.set_title('{} price'.format(priceType))
        ax.set_xlabel('Date')
        ax.set_ylabel('Price')
        ax.plot(filtered['date'].values, filtered[priceType].values, label='daily')
        movingAveragePrice = movingAverage(filtered[priceType].values, movingAverageWindow)
        ax.plot(filtered['date'].values[(movingAverageWindow - 1) // 2 : (movingAverageWindow - 1) // 2 + len(movingAveragePrice)], movingAveragePrice, label='AVG '+str(movingAverageWindow))
        ax.xaxis.set_major_locator(mdates.MonthLocator(interval=3)) 
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))
        plt.legend()
        for label in ax.xaxis.get_ticklabels():   
            label.set_rotation(45)
    
    focus = plt.figure()
    focus.suptitle('Stock {} daily change'.format(filtered['Name'][0]))
    plt.xlabel('Date')
    plt.ylabel('Price')
    color = []
    for open, close in zip(filtered['open'].values, filtered['close'].values):
        if open < close:
            color.append('r')
        else:
            color.append('g')
    plt.scatter(filtered['date'].values, filtered['open'].values, marker='o', c=color)
    plt.scatter(filtered['date'].values, filtered['close'].values, marker='x', c=color)

    volume = plt.figure(figsize=(15, 5))
    volume.suptitle('Stock {} trade volume'.format(filtered['Name'][0]))
    plt.xlabel('Date')
    plt.ylabel('Amount')
    plt.bar(filtered['date'].values, filtered['volume'].values)

    plt.show()





filtered = filterAndSave()
selectAndPlot(filtered)


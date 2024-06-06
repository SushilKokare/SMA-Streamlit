# finding data of next day of marubozu found day
# but only if next day close is greater than marubozu day close

import pandas as pd
import numpy as np 
from datetime import timedelta
import yfinance as yf

def getsmadf(data,days):
    l = []
    smadf = pd.DataFrame()
    flag = 0
    row_index = 0
    for i in data.index:
        if flag==0:
            if data['Close'][i] >= data[str(days)+' SMA'][i]:
    #         if data[str(days)+' SMA'][i] >= data['Adj Close'][i]:
                l.append(i)
                
                smadf.loc[row_index,'flag'] = flag
                smadf.loc[row_index,'date'] = i
                smadf.loc[row_index,'Close'] = data['Close'][i]
                smadf.loc[row_index,'SMA'] = data[str(days)+' SMA'][i]
                row_index += 1
                
                flag=1
                
        elif flag==1:
            if data['Close'][i] <= data[str(days)+' SMA'][i]:
    #         if data[str(days)+' SMA'][i] <= data['Adj Close'][i]:
                l.append(i)
                
                smadf.loc[row_index,'flag'] = flag
                smadf.loc[row_index,'date'] = i
                smadf.loc[row_index,'Close'] = data['Close'][i]
                smadf.loc[row_index,'SMA'] = data[str(days)+' SMA'][i]
                row_index += 1
                
                flag=0
            
    # l = list(set(l))
    # l.sort(reverse=False)
    # l

    return smadf


def getfinaldf(smadf,data):
    # indexDates = pd.DataFrame()
    start = smadf.loc[smadf['flag']==0]['date']
    end = smadf.loc[smadf['flag']==1]['date']
    indexDates = pd.DataFrame({ 'start' : start.reset_index(drop=True), 'end' :  end.reset_index(drop=True)})
    finaldf = indexDates.copy()
    for i in range(len(indexDates)):
        per = (max(data.loc[indexDates['start'][i] : indexDates['end'][i],'Close']) - data.loc[indexDates['start'][i],'Close'] )/ data.loc[indexDates['start'][i],'Close']*100
        finaldf.loc[i,'max price between the start and end dates'] = max(data.loc[indexDates['start'][i] : indexDates['end'][i],'Close'])
        finaldf.loc[i,'percentage'] = per
        finaldf.loc[i,'max price date'] = data.loc[data['Close']==max(data.loc[indexDates['start'][i] : indexDates['end'][i],'Close'])].index[0]

    return finaldf


def get_count_by_category(fc):
    per = list(fc.loc[fc['percentage']!=0]['percentage'])
    bins = [0,5,10,15,20,25,30,35,40,45,50,55,float('inf')]

    categories = pd.cut(per, bins=bins, labels=['0-5','5-10','10-15','15-20','20-25','25-30','30-35','35-40','40-45','45-50',
                                                '50-55','55+'])

    count_by_category = categories.value_counts().sort_index()

    return count_by_category

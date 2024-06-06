# finding data of next day of marubozu found day
# but only if next day close is greater than marubozu day close

import pandas as pd
import numpy as np 
from datetime import timedelta
import yfinance as yf

def marubozu(df,sym):
    marlist = []
    successlist = []

    for i in df.index:
        if(df['Open'][i]<df['Close'][i]):
            head = df['High'][i] - df['Close'][i]
            tail = df['Open'][i] - df['Low'][i]
            body = df['Close'][i] - df['Open'][i]
            if( (head < ((body/100)*20) ) and (tail < ((body/100)*20))):
#                 print('Marubozu on =',i)
                marlist.append(i)

                df_next = pd.DataFrame()
                one_day = timedelta(days=1)
                new_date_1 = i
                while(len(df_next)==0):
                    new_date_1 = new_date_1 + one_day
                    #print('new_date_1 ',new_date_1)
                    nxt_year_1 = str(new_date_1).split()[0].split('-')[0]
                    nxt_mon_1 = str(new_date_1).split()[0].split('-')[1]
                    nxt_date_1 = str(new_date_1).split()[0].split('-')[2]
                    new_date_2 = new_date_1 + one_day
                    #print('new_date_2 ',new_date_2)
                    nxt_year_2 = str(new_date_2).split()[0].split('-')[0]
                    nxt_mon_2 = str(new_date_2).split()[0].split('-')[1]
                    nxt_date_2 = str(new_date_2).split()[0].split('-')[2]

                    start_date = str(nxt_year_1)+'-'+str(nxt_mon_1)+'-'+str(nxt_date_1)
                    end_date = str(nxt_year_2)+'-'+str(nxt_mon_2)+'-'+str(nxt_date_2)

                    #print('start date ',start_date)
                    #print('end date ',end_date)
                    
                    df_next = yf.download(sym+'.ns',start=start_date,end=end_date,progress=False,show_errors=False)

                    if(len(df_next)==0):
                        continue
                    if(df['Close'][i] < df_next['Close'][0]):
#                         print(df_next.index)
                        successlist.append(df_next.index)

                #print('next of marubozu',df_next.index)
                #print('*'*100)
    return marlist, successlist



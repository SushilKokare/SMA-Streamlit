import streamlit as st
import yfinance as yf
import niftystocks as ns
import pandas as pd
from datetime import datetime as dt
from datetime import timedelta
from dateutil.relativedelta import relativedelta
import cm2 as cm
import chartsma as csma
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


dark = '''
<style>
    .stApp {
    background-color: black;
    }
</style>
'''

light = '''
<style>
    .stApp {
    background-color: white;
    }
</style>
'''

st.markdown(light, unsafe_allow_html=True)

# Create a toggle button
toggle = st.button("Toggle theme")

def get_data(symbol,start=None,end=None,period='max'):
    df = pd.DataFrame()
    if start:
        df = yf.download(symbol,start=str(start) , end=str(end),progress=False)
        st.write(str(len(df))+' Rows')
    else:
            df = yf.download(symbol,period=period,progress=False)
            st.write(str(len(df))+' Rows')
    return df

# Finding dates on which marubozu is formed
def show_marubozu_dates(df):
    st.markdown('### Marubozu Found of following dates : \n')
    for i in df.index:
        if(df['Open'][i]<df['Close'][i]):
            head = df['High'][i] - df['Close'][i]
            tail = df['Open'][i] - df['Low'][i]
            body = df['Close'][i] - df['Open'][i]
            if( (head < ((body/100)*20) ) and (tail < ((body/100)*20))):
                # i = str(i).split('-')
                # st.write(int(i[0]),'-',int(i[1]),'-',int(i[2]))
                st.write(i)

    

st.title('Stock Analyzer ')

sym = st.text_input('Enter stock symbol : ')


st.info('Either select range of date Or Just enter the period',icon=":material/info:")
choice = st.selectbox('Choose any one',['Date Range','Period'],help='choose how you want to download the data !')

if choice=="Period":

    # 1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo
    col1,col2 = st.columns(2)
    with col1:
        num = st.number_input('Enter number',min_value=1)
        
    with col2:
        ymw = st.selectbox('Select any one',['Year','Month','Week'])


option_to_key = {
    'Year' : 'y',
    'Month' : 'mo',
    'Week' : 'wk' } 


if choice=="Date Range":
    col1,col2 = st.columns(2)

    with col1:
        start_date = st.date_input('Select start date')
        
    with col2:
        end_date = st.date_input('Select end date')



    
strategy =  st.selectbox(label='Select Candle ',options=['Bullish Marubozu','SMA'])

if strategy=='SMA':
    smadays = st.number_input('Enter days for SMA : ',min_value=1)
    days_to_show = st.number_input('Enter days to show chart ',min_value=20)


chkbtn = st.button('Check')

marubozu_list = list()
successs_list = list()


def marubozufun():
    df = pd.DataFrame()
    if choice=='Date Range':
        if start_date>end_date:
            st.error('Start date cannot be greater then End date')  
        else:
            df = get_data(sym+'.ns',start=start_date,end=end_date)  
    elif choice=='Period':
        period = str(num)+option_to_key.get(ymw)
        # st.write(period)
        df = get_data(sym+'.ns',period=period)

    df2 = df.copy()
    df2.index = pd.to_datetime(df.index)
    df2.index = df.index.strftime('%Y-%m-%d')

    st.write(df2)   
    #show_marubozu_dates(df)
    #st.header('xxxxxxxxxxxxxxx')
    
    info_placeholder = st.empty()
    info_placeholder.info('Calculation started please wait !')

    marubozu_list, successs_list = cm.marubozu(df,sym)

    info_placeholder.empty()

    successs_list = [str(s).split(",")[0] for s in successs_list]
    successs_list = [s.split("'")[1] for s in successs_list]
    
    if marubozu_list:
        st.header('Check Report')
        col1,col2 = st.columns(2)


        with col1:
            with st.expander('click to see marubozu dates '):
                st.write([x.strftime('%Y-%m-%d') for x in marubozu_list])

        with col2:
            with st.expander('click to see success dates '):
                # st.write([y.strftime('%Y-%m-%d') for y in successs_list])
                st.write(successs_list)



        success_percentage = (len(successs_list) / len(marubozu_list))*100


        rate = pd.DataFrame({ 'Category' : ['success rate','failure rate'],
        'Percentage' : [success_percentage,100-success_percentage]})
        

        system_bg_color = '#ffffff'

        # Create a smaller pie chart with adjusted background color
        fig, ax = plt.subplots(figsize=(1.5,1.5) ) # Adjust the figsize for smaller chart
        ax.pie(rate['Percentage'], labels=rate['Category'], autopct='%1.1f%%', startangle=90,   textprops=dict(color="black"),  # Default text color
        colors=['green', 'red'] )
        ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

        # Set the background color
        fig.patch.set_facecolor(system_bg_color)
        ax.set_facecolor(system_bg_color)

        # Display the pie chart in Streamlit
        st.write("Pie Chart:")
        st.pyplot(fig)
    else:
        st.error('No marubozu found on selected data! ')

def calculate_sma(data, window):
    sma = []

    for i in range(len(data) - window + 1):
        window_data = data[i : i + window]
        sma_value = sum(window_data['Close']) / window
        sma.append(round(sma_value,2))
    padding = [0] * (window -1) 
    new_row = padding + sma
    data[str(window)+' SMA'] = new_row
    return data


def smafun():
    df = pd.DataFrame()
    if choice=='Date Range':
        if start_date>end_date:
            st.error('Start date cannot be greater then End date')  
        else:
            df = get_data(sym+'.ns',start=start_date,end=end_date)  
    elif choice=='Period':
        period = str(num)+option_to_key.get(ymw)
        # st.write(period)
        df = get_data(sym+'.ns',period=period)

    df2 = df.copy()
    df2.index = pd.to_datetime(df2.index)
    df2.index = df2.index.strftime('%Y-%m-%d')

    datatable = st.empty()
    datatable.write(df2)

    data = calculate_sma(df,smadays)

    df2 = data.copy()
    df2.index = pd.to_datetime(df2.index)
    df2.index = df2.index.strftime('%Y-%m-%d')
    datatable.write(df2)
    # Plotting
    st.markdown(f'### Last {days_to_show} Day Data')
    
    fig, ax = plt.subplots(figsize=(12, 5))

    # plt.figure(figsize=(12, 5))
    ax.plot(data[f'{smadays} SMA'][-days_to_show:], label=f'{smadays} SMA')
    ax.plot(data['Close'][-days_to_show:], label='Adj Close')
    ax.legend()
    plt.title(f"{sym} Close Vs {smadays} SMA")
    plt.xticks(rotation=90)
    plt.xlabel('Date')
    plt.ylabel('Price')

    # Display the plot in Streamlit
    st.pyplot(fig)

    smadf = csma.getsmadf(data,smadays)

    smafinaldf = csma.getfinaldf(smadf,data)

    st.markdown('### Data Table of SMA Crossover:')
    st.write('start date,end data, max price, max gain percentage,max price date   ')
    st.write(smafinaldf)

    gain = len(smafinaldf.loc[smafinaldf['percentage']!=0])
    loss = len(smafinaldf.loc[smafinaldf['percentage']!=0])

    success_percentage = (gain / len(smafinaldf))*100

    rate = pd.DataFrame({ 'Category' : ['success rate','failure rate'],
    'Percentage' : [success_percentage,100-success_percentage]})
    
    col1,col2,col3 = st.columns([1,5,1])
    with col2:
        system_bg_color = '#ffffff'

        # Create a smaller pie chart with adjusted background color
        fig, ax = plt.subplots(figsize=(1.5,1.5) ) # Adjust the figsize for smaller chart
        ax.pie(rate['Percentage'], labels=rate['Category'], autopct='%1.1f%%', startangle=90,   textprops=dict(color="black"),  # Default text color
        colors=['green', 'red'] )
        ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

        # Set the background color
        fig.patch.set_facecolor(system_bg_color)
        ax.set_facecolor(system_bg_color)

        # Display the pie chart in Streamlit
        st.write("Pie Chart:")
        st.pyplot(fig)

    count_by_category = csma.get_count_by_category(smafinaldf)
    
    count_by_category = count_by_category[count_by_category.values!=0]

    st.write('Time of percentage returns ')
    cbc = pd.DataFrame({ 'gain in %' : count_by_category.index,
                        'no. of time got those gains' : count_by_category.values})

    st.markdown('## Data Table SMA ')
    st.write(cbc)
    
    # Create the countplot using seaborn
    col1,col2,col3 = st.columns([1,7,1])
    with col2:
        fig, ax = plt.subplots(figsize=(5, 3))  # Adjust figsize for smaller chart

        cmap = plt.get_cmap('viridis')  # You can use any colormap you like
        colors = cmap(np.linspace(0, 1, len(cbc['gain in %'])))

        plt.bar(x=cbc['gain in %'],height=cbc['no. of time got those gains'],color=colors)

        # ax.set_ylim(0,upperlimit)
        ax.set_xlabel('Returns Percentage')
        ax.set_ylabel('Count')
        ax.set_title('Count of percentage returns ')
        # Display the countplot in Streamlit
        st.write("Count of percentage returns Count Plot:")
        st.pyplot(fig)

        # Annotate bars with count values
        for bar in ax.patches:
            yval = bar.get_height()
            ax.text(bar.get_x() + bar.get_width() / 2, yval + 0.2, int(yval), ha='center', va='bottom', fontsize=10)  # Adjust fontsize as needed


 

if chkbtn:
    if strategy== 'Bullish Marubozu':
        #st.header('xxxxxxxxxxxxxxx')
        marubozufun()

    elif strategy == 'SMA':
        smafun()






for i in range(5):
    st.write("")
    
    
def myname():
  footer_text = f""" 
  Developed by Sushil Kokare    
  © 2024 
  """
  st.markdown(footer_text, unsafe_allow_html=True)




myname()  





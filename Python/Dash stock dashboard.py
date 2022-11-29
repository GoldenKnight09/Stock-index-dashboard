# -*- coding: utf-8 -*-
"""
Created on Mon Aug  1 13:22:23 2022

@author: chris
"""

import pandas as pd
import dash
from dash import html, dcc, dash_table
from dash.dash_table.Format import Format, Scheme, Trim
from dash.dependencies import Input, Output
import yfinance as yf
from datetime import date, timedelta
import plotly.graph_objects as go

# Import list of index tickers and descriptions from a .csv file
index_list = pd.read_csv('Index_list.csv', header = None)
index_dict = dict(index_list.values)
index_dropdown_list = list({'label':index_dict[index_key],'value':index_key} for index_key in index_dict.keys())

# Import list of stock tickers and description from a .csv file
stock_list = pd.read_csv('Stock_list.csv', header = None)
stock_dict = dict(stock_list.values)
stock_dropdown_list = list({'label':stock_dict[stock_key],'value':stock_key} for stock_key in stock_dict.keys())

def get_stock_ticker_data(ticker_symbol):
    stock_data = yf.Ticker(ticker_symbol)
    stock_data = stock_data.history(period = 'max')
    stock_data.reset_index(inplace = True)
    return(stock_data)

def stock_chart_title(ticker_symbol):
    # Convert the stock ticker to a descriptive name using stock dictionary
    stock_label = stock_dict.get(ticker_symbol, 'Uh-oh, something went wrong')
    return stock_label
    
def stock_chart_y_label(ticker_symbol):
    # Set stock price chart y-axis (currency) label
    match ticker_symbol:
        case 'BAS.DE' | 'AI.PA' | 'BAYN.DE' | 'EVK.DE' | 'LIN.DE' | 'OR.PA':
            return 'Price (€)'
        case 'BP.L'| 'JMAT.L' | 'SHEL.L':
            return 'Price (£)'
        case '4911.T' | '4042.T' | '4005.T' | '600028.SS' | '601857.SS':
            return 'Price (¥)'
        case 'NESN.SW' | 'ROG.SW':
            return 'Price (CHF)' # Swiss Francs
        case '0386.HK' | '0857.HK':
            return 'Price (HK$)'
        case _:
            return 'Price ($)'

def index_chart_title(ticker_symbol):
    # Convert the index ticker to a descriptive name using index dictionary
    index_label = index_dict.get(ticker_symbol, 'Uh-oh, something went wrong')
    return index_label
        
def index_chart_y_label(ticker_symbol):
    # Set index price chart y-axis (currency) label
    match ticker_symbol:
        case '^GDAXI':
            return 'Price (€)'
        case '^FTSE':
            return 'Price (£)'
        case '^N225' | '000001.SS' | '000300.SS':
            return 'Price (¥)'
        case '^HSI':
            return 'Price (HK$)'
        case _:
            return 'Price ($)'
        
def construct_data_table(summary_data_max_high,summary_data_max_close,summary_data_min_close,summary_data_min_low,y_label):
    for max_high in range(0,len(summary_data_max_high)):
        # iterate through high price maxima
        if max_high == 0:
            # if only one maxima / first maxima
            max_high_data = pd.DataFrame(data = {' ':'Maximum Price',
                                                  'Date':summary_data_max_high.loc[max_high,'Date'].date().strftime("%m-%d-%Y"),
                                                  y_label:summary_data_max_high.loc[max_high,'High']},
                                         index = [max_high])
        else:
            # additional local maxima
            max_high_data_vector = pd.DataFrame(data = {' ':'',
                                                        'Date':summary_data_max_high.loc[max_high,'Date'].date().strftime("%m-%d-%Y"),
                                                        y_label:summary_data_max_high.loc[max_high,'High']},
                                                index = [max_high])
            max_high_data = pd.concat([max_high_data, max_high_data_vector], ignore_index = True)
    for max_close in range(0,len(summary_data_max_close)):
        if max_close == 0:
            max_close_data = pd.DataFrame(data = {' ':'Maximum Closing Price',
                                                  'Date':summary_data_max_close.loc[max_close,'Date'].date().strftime("%m-%d-%Y"),
                                                  y_label:summary_data_max_close.loc[max_close,'Close']},
                                          index = [max_close])
        else:
            max_close_data_vector = pd.DataFrame(data = {' ':'',
                                                         'Date':summary_data_max_close.loc[max_close,'Date'].date().strftime("%m-%d-%Y"),
                                                         y_label:summary_data_max_close.loc[max_close,'Close']},
                                                 index = [max_close])
            max_close_data = pd.concat([max_close_data, max_close_data_vector], ignore_index = True)
    for min_close in range(0,len(summary_data_min_close)):
        if min_close == 0:
            min_close_data = pd.DataFrame(data = {' ':'Minimum Closing Price',
                                                  'Date':summary_data_min_close.loc[min_close,'Date'].date().strftime("%m-%d-%Y"),
                                                  y_label:summary_data_min_close.loc[min_close,'Close']},
                                          index = [min_close])
        else:
            min_close_data_vector = pd.DataFrame(data = {' ':'',
                                                         'Date':summary_data_min_close.loc[min_close,'Date'].date().strftime("%m-%d-%Y"),
                                                         y_label:summary_data_min_close.loc[min_close,'Close']},
                                                 index = [min_close])
            min_close_data = pd.concat([min_close_data, min_close_data_vector], ignore_index = True)
    for min_low in range(0,len(summary_data_min_low)):
        if min_low == 0:
            min_low_data = pd.DataFrame(data = {' ':'Minimum Price',
                                                  'Date':summary_data_min_low.loc[min_low,'Date'].date().strftime("%m-%d-%Y"),
                                                  y_label:summary_data_min_low.loc[min_low,'Low']},
                                        index = [min_low])
        else:
            min_low_data_vector = pd.DataFrame(data = {' ':'',
                                                       'Date':summary_data_min_low.loc[min_low,'Date'].date().strftime("%m-%d-%Y"),
                                                       y_label:summary_data_min_low.loc[min_low,'Low']},
                                               index = [min_low])
            min_low_data = pd.concat([min_low_data, min_low_data_vector], ignore_index = True)
    plot_data_summary = pd.concat([max_high_data, max_close_data, min_close_data, min_low_data], ignore_index = True)
    # combine all dataframes for maxima and minima together into one
    return plot_data_summary

app = dash.Dash(__name__)


app.layout = html.Div(children=[html.H1('Stock/Index Price Dashboard',
                                        style = {'textAlign':'center','font-size':50}),
                                html.Div(children=[
                                    html.Div(children = [html.Label(['Select plot type:'],
                                                                    style = {'font-weight':'bold',
                                                                             'font-size':28}),
                                                         dcc.RadioItems(id='stock_plot_type',options=[{'label':'Candlestick plot','value':'candle'},
                                                                                                     {'label':'Closing data only','value':'closing'}],
                                                                        value = 'candle',
                                                                        inline = True,
                                                                        inputStyle = {'margin-right':'4px',
                                                                                      'margin-left':'15px'},
                                                                        style ={'font-size':24,
                                                                                'margin-top':'10px',
                                                                                'margin-bottom':'20px'}),
                                                         html.Label(['Select a company for stock price information:'],
                                                                    style = {'font-weight':'bold',
                                                                             'font-size':28}),
                                                         dcc.Dropdown(id='stock_ticker',
                                                                      options = stock_dropdown_list,                                                                      
                                                                      placeholder = 'Select a stock',
                                                                      value = 'AAPL',
                                                                      searchable = True,
                                                                      style={'font-size':22,
                                                                             'margin-top':'10px',
                                                                             'margin-bottom':'20px'}),
                                                         html.Label(['Specify date entry type:'],
                                                                    style = {'font-weight':'bold',
                                                                             'font-size':28}),
                                                         dcc.RadioItems(id='stock_plot_date_select',options=[{'label':'Date range','value':'stock_date_range'},
                                                                                                             {'label':'Days back from now','value':'stock_days_back'}],
                                                                        value = 'stock_date_range',
                                                                        inline = True,
                                                                        inputStyle = {'margin-right':'4px',
                                                                                      'margin-left':'15px'},
                                                                        style ={'font-size':24,
                                                                                'margin-top':'10px',
                                                                                'margin-bottom':'20px'}),
                                                         html.Div(children=[html.Label(['# of days to display back from today (min 2):'],
                                                                                       id = 'stock_tail_days_label',
                                                                                       style = {}),
                                                                            dcc.Input(id = 'stock_tail_days',
                                                                                      type='number',
                                                                                      min=2,
                                                                                      step=1,
                                                                                      value = 30,
                                                                                      debounce = True,
                                                                                      style={}),
                                                                            html.Label(['Date range to display:'],
                                                                                       id = 'stock_date_range_label',
                                                                                       style = {}),
                                                                            dcc.DatePickerRange(id = 'stock_date_range',
                                                                                                start_date = date.today() - timedelta(days = 30),
                                                                                                end_date = date.today(),
                                                                                                max_date_allowed = date.today(),
                                                                                                style = {}),
                                                                            html.Button('Reset to default dates',
                                                                                        id = 'stock_date_reset_button',
                                                                                        n_clicks = 0,
                                                                                        style = {})]),
                                                         html.Div(children=[html.Label(['Display closing price moving average?'],
                                                                                       id = 'moving_average_option_label'),
                                                                            dcc.RadioItems(id = 'moving_average_option',
                                                                                           options = [{'label':'Yes','value':'display_MA'},
                                                                                                      {'label':'No','value':'do_not_display_MA'}],
                                                                                           value = 'do_not_display_MA',
                                                                                           labelStyle = {'display':'block'},
                                                                                           inputStyle = {'margin-right':'4px',
                                                                                                         'margin-left':'15px',
                                                                                                         'margin-bottom':'4px'})],
                                                                  style = {}),
                                                         html.Div(children=[html.Label(['# of days to use for moving average (min 2)'],
                                                                                       id = 'moving_average_days_label'),
                                                                            dcc.Input(id = 'moving_average_days',
                                                                                      type = 'number',
                                                                                      min = 2,
                                                                                      step = 1,
                                                                                      value = 7,
                                                                                      debounce = True)],
                                                                  style = {})],
                                             style={'width':'24%',
                                                    'display':'inline-block',
                                                    'verticalAlign':'top',
                                                    'margin-top':'55px'}),
                                    html.Div(children = dcc.Graph(id = 'stock_plot'),
                                             style={'width':'49%',
                                                    'display':'inline-block',
                                                    'margin-left':'10px'}),
                                    html.Div(children = [html.Div(id = 'stock_summary_table_title',
                                                                  style={'font-size':30,
                                                                         'margin-top':'10px',
                                                                         'margin-bottom':'15px'}),
                                                         dash_table.DataTable(id = 'stock_summary_table',
                                                                             columns = [{'name':'Column 1','id':'column1'},
                                                                                        {'name':'Column 2','id':'column2'},
                                                                                        {'name':'Column 3','id':'column3'}],
                                                                             data=[])],
                                             style={'width':'24%',
                                                    'display':'inline-block',
                                                    'verticalAlign':'top',
                                                    'font-size':22})]),
                                html.Div(children=[
                                    html.Div(children=[html.Label(['Select plot type:'],
                                                                  style = {'font-weight':'bold',
                                                                           'font-size':28}),
                                                       dcc.RadioItems(id='index_plot_type',options=[{'label':'Candlestick plot','value':'candle'},
                                                                                                    {'label':'Closing data only','value':'closing'}],
                                                                      value = 'candle',
                                                                      inline = True,
                                                                      inputStyle = {'margin-right':'4px',
                                                                                    'margin-left':'15px'},
                                                                      style ={'font-size':24,
                                                                              'margin-top':'10px',
                                                                              'margin-bottom':'20px'}),
                                                       html.Label(['Select stock exchange index for price information:'],
                                                                  style = {'font-weight':'bold',
                                                                           'font-size':28}),
                                                       dcc.Dropdown(id='index_ticker',
                                                                    options = index_dropdown_list,
                                                                    placeholder = 'Select an index',
                                                                    value = '^GSPC',
                                                                    searchable = True,
                                                                    style = {'font-size':22,
                                                                             'margin-top':'10px',
                                                                             'margin-bottom':'20px'}),
                                                       html.Label(['Specify date entry type:'],
                                                                  style = {'font-weight':'bold',
                                                                           'font-size':28}),
                                                       dcc.RadioItems(id='index_plot_date_select',options=[{'label':'Date range','value':'index_date_range'},
                                                                                                           {'label':'Days back from now','value':'index_days_back'}],
                                                                      value = 'index_date_range',
                                                                      inline = True,
                                                                      inputStyle = {'margin-right':'4px',
                                                                                    'margin-left':'15px'},
                                                                      style ={'font-size':24,
                                                                              'margin-top':'10px',
                                                                              'margin-bottom':'20px'}),
                                                       html.Div(children=[html.Label(['# of days to display back from today (min 2):'],
                                                                                     id = 'index_tail_days_label',
                                                                                     style = {}),
                                                                          dcc.Input(id = 'index_tail_days',
                                                                                    type = 'number',
                                                                                    min = 2,
                                                                                    step = 1,
                                                                                    value = 30,
                                                                                    debounce = True,
                                                                                    style = {}),
                                                                          html.Label(['Date range to display:'],
                                                                                     id = 'index_date_range_label',
                                                                                     style = {}),
                                                                          dcc.DatePickerRange(id = 'index_date_range',
                                                                                              start_date = date.today() - timedelta(days = 30),
                                                                                              end_date = date.today(),
                                                                                              max_date_allowed = date.today(),
                                                                                              style = {}),
                                                                          html.Button('Reset to default dates',
                                                                                      id = 'index_date_reset_button',
                                                                                      n_clicks = 0,
                                                                                      style = {})])],
                                             style = {'width':'24%',
                                                      'display':'inline-block',
                                                      'vertical-align':'top',
                                                      'margin-top':'80px'}),
                                    html.Div(children = dcc.Graph(id = 'index_plot'),
                                             style = {'width':'49%',
                                                      'display':'inline-block',
                                                      'margin-top':'25px',
                                                      'margin-left':'10px'}),
                                    html.Div(children = [html.Div(id = 'index_summary_table_title',
                                                                  style={'font-size':30,
                                                                         'margin-top':'35px',
                                                                         'margin-bottom':'15px'}),
                                                         dash_table.DataTable(id = 'index_summary_table',
                                                                             columns = [{'name':'Column 1','id':'column1'},
                                                                                        {'name':'Column 2','id':'column2'},
                                                                                        {'name':'Column 3','id':'column3'}],
                                                                             data=[])],
                                             style={'width':'24%',
                                                    'display':'inline-block',
                                                    'verticalAlign':'top',
                                                    'font-size':22})])])
                                
@app.callback(Output(component_id='moving_average_option_label',component_property='style'),
              Output(component_id='moving_average_option',component_property='style'),
              Input(component_id='stock_plot_type',component_property='value'))

def show_moving_average_option(stock_plot_type):
    if stock_plot_type == 'candle':
        return ({'font-size':28,'font-weight':'bold','margin-top':'20px','display':'block'},
                {'font-size':24,'margin-top':'10px','display':'block'})
    if stock_plot_type == 'closing':
        return ({'display':'none'},
                {'display':'none'})
    
@app.callback(Output(component_id='moving_average_days_label',component_property='style'),
              Output(component_id='moving_average_days',component_property='style'),
              Input(component_id='moving_average_option',component_property='value'))

def show_moving_average(moving_average_option):
    if moving_average_option == 'display_MA':
        return ({'font-size':28,'font-weight':'bold','margin-top':'20px','display':'block'},
                {'font-size':24,'margin-top':'10px','display':'block'})
    if moving_average_option == 'do_not_display_MA':
        return ({'display':'none'},
                {'display':'none'})
    
@app.callback(Output(component_id='stock_tail_days_label',component_property='style'),
              Output(component_id='stock_tail_days',component_property='style'),
              Output(component_id='stock_date_range_label',component_property='style'),
              Output(component_id='stock_date_range',component_property='style'),
              Output(component_id='stock_date_reset_button',component_property='style'),
              Input(component_id='stock_plot_date_select',component_property='value'))

def select_index_date_input(stock_plot_date_select):
    if stock_plot_date_select == 'stock_days_back':
        return ({'font-size':28,'font-weight':'bold','display':'block'},
                {'font-size':22,'margin-top':'10px','display':'block'},
                {'display':'none'},
                {'display':'none'},
                {'display':'none'})
    if stock_plot_date_select == 'stock_date_range':
        return ({'display':'none'},
                {'display':'none'},
                {'font-size':28,'font-weight':'bold','display':'inline-block'},
                {'font-size':22,'margin-left':'20px','display':'inline-block'},
                {'font-size':24,'margin-top':'10px','margin-left':'15px','display':'block'})

@app.callback(Output(component_id='index_tail_days_label',component_property='style'),
              Output(component_id='index_tail_days',component_property='style'),
              Output(component_id='index_date_range_label',component_property='style'),
              Output(component_id='index_date_range',component_property='style'),
              Output(component_id='index_date_reset_button',component_property='style'),
              Input(component_id='index_plot_date_select',component_property='value'))

def select_index_date_input(index_plot_date_select):
    if index_plot_date_select == 'index_days_back':
        return ({'font-size':28,'font-weight':'bold','display':'block'},
                {'font-size':22,'margin-top':'10px','display':'block'},
                {'display':'none'},
                {'display':'none'},
                {'display':'none'})
    if index_plot_date_select == 'index_date_range':
        return ({'display':'none'},
                {'display':'none'},
                {'font-size':28,'font-weight':'bold','display':'inline-block'},
                {'font-size':22,'margin-left':'20px','display':'inline-block'},
                {'font-size':24,'margin-top':'10px','margin-left':'15px','display':'block'})
                                
@app.callback(Output(component_id='stock_plot',component_property='figure'),
              Output(component_id='stock_summary_table_title',component_property='children'),
              Output(component_id='stock_summary_table',component_property='columns'),
              Output(component_id='stock_summary_table',component_property='data'),
              Input(component_id='stock_plot_type',component_property='value'),
              Input(component_id='stock_ticker',component_property='value'),
              Input(component_id='stock_plot_date_select',component_property='value'),
              Input(component_id='stock_tail_days',component_property='value'),
              Input(component_id='stock_date_range',component_property='start_date'),
              Input(component_id='stock_date_range',component_property='end_date'),
              Input(component_id='moving_average_option',component_property='value'),
              Input(component_id='moving_average_days',component_property='value'))

def stock_plot(stock_plot_type,stock_ticker,stock_plot_date_select,stock_tail_days,start_date,end_date,moving_average_option,moving_average_days):
    stock_data = get_stock_ticker_data(stock_ticker)
    if stock_plot_date_select == 'stock_days_back':
        today = date.today()
        begin_date = today - timedelta(days = stock_tail_days)
        # stock_data 'Date' column is (pandas) datetime64[ns] where datetime objects are either (usually) datetime or date
        # convert datetime objects to pandas datetime objects to allow for comparison:
        stock_data_date_masked = stock_data.loc[stock_data['Date'] >= pd.Timestamp(begin_date)]
    if stock_plot_date_select == 'stock_date_range':
        stock_data_date_masked = stock_data.loc[((stock_data['Date'] >= pd.Timestamp(start_date)) & (stock_data['Date'] <= pd.Timestamp(end_date)))]
    y_label = stock_chart_y_label(stock_ticker)
    if (y_label == 'Price (£)'):
        # Stock prices on London Stock Exchange are reported in pence (£0.01), not pounds.
        # Need to divide by 100 to convert to pounds.
        pound_mask = ['Open', 'High','Low','Close']
        stock_plot_data = stock_data_date_masked.copy()
        stock_plot_data.loc[:,pound_mask] = stock_data_date_masked.loc[:,pound_mask] / 100
        stock_summary_data = stock_plot_data
    else:
        stock_plot_data = stock_data_date_masked
        stock_summary_data = stock_plot_data
    if (stock_plot_type == 'candle'):
        if (moving_average_option == 'display_MA'):
            MA_stock_data = stock_data.tail(len(stock_plot_data) + moving_average_days)
            moving_average = MA_stock_data['Close'].rolling(moving_average_days).mean()
            fig = go.Figure(data=[go.Candlestick(x=stock_plot_data['Date'],
                                                 open=stock_plot_data['Open'],
                                                 high=stock_plot_data['High'],
                                                 low=stock_plot_data['Low'],
                                                 close=stock_plot_data['Close'],
                                                 increasing_line_color = 'darkseagreen',
                                                 decreasing_line_color = 'red'),
                                  go.Scatter(x=stock_plot_data['Date'],
                                             y=moving_average[-len(stock_plot_data):],
                                             mode = 'lines',
                                             line_color = 'orange',
                                             line_width = 2)])
        else:
            fig = go.Figure(data=[go.Candlestick(x=stock_plot_data['Date'],
                                                 open=stock_plot_data['Open'],
                                                 high=stock_plot_data['High'],
                                                 low=stock_plot_data['Low'],
                                                 close=stock_plot_data['Close'],
                                                 increasing_line_color = 'darkseagreen',
                                                 decreasing_line_color = 'red')])
    else:
        fig = go.Figure(data=go.Scatter(x=stock_plot_data['Date'],
                               y=stock_plot_data['Close'],
                               mode = 'lines',
                               line_color = 'black',
                               line_width = 2))
    fig.update_layout(title = f'<b>{stock_chart_title(stock_ticker)}</b>',
                      title_font_size = 30,
                      title_x=0.5,
                      xaxis_title = '<b>Date</b>',
                      yaxis_title = f'<b>{y_label}</b>',
                      xaxis_rangeslider_visible=False,
                      height = 600,
                      margin = dict(
                          b = 60,
                          l = 80,
                          r = 80,
                          t = 60),
                      showlegend = False,
                      plot_bgcolor = 'white')
    fig.update_xaxes(title_font_size = 22,
                     tickfont_size = 18,
                     showline = True, # plot area border line
                     linecolor = 'black', # plot area border line color
                     mirror = False, # mirror to both parallel axes (otherwise just axis with tickmarks)
                     gridcolor = 'lightgray')
    fig.update_yaxes(title_font_size = 22,
                     tickfont_size = 18,
                     showline = True, # plot area border line
                     linecolor = 'black', # plot area border line color
                     mirror = False, # mirror to both parallel axes (otherwise just axis with tickmarks)
                     gridcolor = 'lightgray')
    if (max(stock_summary_data['High']) - min(stock_summary_data['Low']) < 5):
        fig.update_yaxes(tickformat = '.2f')
    summary_title = html.Label([f'{stock_chart_title(stock_ticker)}'+' summary table'])
    stock_summary_data_max_high = stock_summary_data.loc[(stock_summary_data['High'] == max(stock_summary_data['High']))].reset_index(drop = True)
    stock_summary_data_max_close = stock_summary_data.loc[(stock_summary_data['Close'] == max(stock_summary_data['Close']))].reset_index(drop = True)
    stock_summary_data_min_close = stock_summary_data.loc[(stock_summary_data['Close'] == min(stock_summary_data['Close']))].reset_index(drop = True)
    stock_summary_data_min_low = stock_summary_data.loc[(stock_summary_data['Low'] == min(stock_summary_data['Low']))].reset_index(drop = True)
    # get rows corresponding to maxima and minima stock values
    stock_plot_data_summary = construct_data_table(stock_summary_data_max_high,stock_summary_data_max_close,stock_summary_data_min_close,stock_summary_data_min_low,y_label)
    columns = [{'name':' ', 'id':' '},
               {'name':'Date','id':'Date'},
               {'name':y_label,'id':y_label,'type':'numeric','format':Format(precision=2, scheme = Scheme.fixed)}]
    data = stock_plot_data_summary.to_dict(orient = 'records')
    return fig, summary_title, columns, data

@app.callback(Output(component_id='stock_date_range',component_property='start_date'),
              Output(component_id='stock_date_range',component_property='end_date'),
              Input(component_id='stock_date_reset_button',component_property='n_clicks'))

def stock_date_reset(n_clicks):
    start_date = date.today() - timedelta(days = 30)
    end_date = date.today()
    return start_date,end_date

@app.callback(Output(component_id='index_plot',component_property='figure'),
              Output(component_id='index_summary_table_title',component_property='children'),
              Output(component_id='index_summary_table',component_property='columns'),
              Output(component_id='index_summary_table',component_property='data'),
              Input(component_id='index_plot_type',component_property='value'),
              Input(component_id='index_ticker',component_property='value'),
              Input(component_id='index_plot_date_select',component_property='value'),
              Input(component_id='index_tail_days',component_property='value'),
              Input(component_id='index_date_range',component_property='start_date'),
              Input(component_id='index_date_range',component_property='end_date'))

def index_plot(index_plot_type,index_ticker,index_plot_date_select,index_tail_days,start_date,end_date):
    index_data = get_stock_ticker_data(index_ticker)
    if index_plot_date_select == 'index_days_back':
        today = date.today()
        begin_date = today - timedelta(days = index_tail_days)
        index_data_date_masked = index_data.loc[index_data['Date'] >= pd.Timestamp(begin_date)]
    if index_plot_date_select == 'index_date_range':
        index_data_date_masked = index_data.loc[((index_data['Date'] >= pd.Timestamp(start_date)) & (index_data['Date'] <= pd.Timestamp(end_date)))]
    y_label = index_chart_y_label(index_ticker)
    index_plot_data = index_data_date_masked
    if (index_plot_type == 'candle'):
        fig = go.Figure(data=[go.Candlestick(x=index_plot_data['Date'],
                                             open=index_plot_data['Open'],
                                             high=index_plot_data['High'],
                                             low=index_plot_data['Low'],
                                             close=index_plot_data['Close'],
                                             increasing_line_color = 'darkseagreen',
                                             decreasing_line_color = 'red')])
    else:
       fig = go.Figure(data=go.Scatter(x=index_plot_data['Date'],
                                       y=index_plot_data['Close'],
                                       mode = 'lines',
                                       line_color = 'black',
                                       line_width = 2)) 
    fig.update_layout(title = f'<b>{index_chart_title(index_ticker)}</b>',
                      title_font_size = 30,
                      title_x=0.5,
                      xaxis_title = '<b>Date</b>',
                      yaxis_title = f'<b>{y_label}</b>',
                      xaxis_rangeslider_visible=False,
                      height = 600,
                      margin = dict(
                          b = 60,
                          l = 80,
                          r = 80,
                          t = 60),
                      plot_bgcolor = 'white')
    fig.update_xaxes(title_font_size = 22,
                     tickfont_size = 18,
                     showline = True, # plot area border line
                     linecolor = 'black', # plot area border line color
                     mirror = False, # mirror to both parallel axes (otherwise just axis with tickmarks)
                     gridcolor = 'lightgray')
    fig.update_yaxes(title_font_size = 22,
                     tickfont_size = 18,
                     showline = True, # plot area border line
                     linecolor = 'black', # plot area border line color
                     mirror = False, # mirror to both parallel axes (otherwise just axis with tickmarks)
                     gridcolor = 'lightgray')
    if max(index_plot_data['High'] > 10000):
        fig.update_yaxes(tickformat = '000')
    summary_title = html.Label([f'{index_chart_title(index_ticker)}'+' summary table'])
    # Relax volume > 0 restriction on extrema, since Python yfinance package can download current day's data (volume may be 0)
    index_summary_data_max_high = index_plot_data.loc[(index_plot_data['High'] == max(index_plot_data['High']))].reset_index(drop = True)
    index_summary_data_max_close = index_plot_data.loc[(index_plot_data['Close'] == max(index_plot_data['Close']))].reset_index(drop = True)
    index_summary_data_min_close = index_plot_data.loc[(index_plot_data['Close'] == min(index_plot_data['Close']))].reset_index(drop = True)
    index_summary_data_min_low = index_plot_data.loc[(index_plot_data['Low'] == min(index_plot_data['Low']))].reset_index(drop = True)
    # get rows corresponding to maxima and minima index values
    index_plot_data_summary = construct_data_table(index_summary_data_max_high,index_summary_data_max_close,index_summary_data_min_close,index_summary_data_min_low,y_label)
    columns = [{'name':' ', 'id':' '},
               {'name':'Date','id':'Date'},
               {'name':y_label,'id':y_label,'type':'numeric','format':Format(precision=2, scheme = Scheme.fixed)}]
    data = index_plot_data_summary.to_dict(orient = 'records')
    return fig, summary_title, columns, data

@app.callback(Output(component_id='index_date_range',component_property='start_date'),
              Output(component_id='index_date_range',component_property='end_date'),
              Input(component_id='index_date_reset_button',component_property='n_clicks'))

def index_date_reset(n_clicks):
    start_date = date.today() - timedelta(days = 30)
    end_date = date.today()
    return start_date,end_date

if __name__ == '__main__':
    app.run_server()
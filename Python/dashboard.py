import pandas as pd
import dash
from dash import html, dcc, dash_table
from dash.dash_table.Format import Format, Scheme, Trim
from dash.dependencies import Input, Output
import yfinance as yf
from datetime import date, timedelta
import plotly.graph_objects as go

def get_stock_ticker_data(ticker_symbol):
    stock_data = yf.Ticker(ticker_symbol)
    stock_data = stock_data.history(period = 'max')
    stock_data.reset_index(inplace = True)
    return(stock_data)

def stock_chart_title(ticker_symbol):
    match ticker_symbol:
        case 'AI.PA':
            return 'Air Liquide (Euronext Paris)'
        case 'APD':
            return 'Air Products'
        case 'AMZN':
            return 'Amazon'
        case 'AMGN':
            return 'Amgen'
        case 'AAPL':
            return 'Apple'
        case 'BAS.DE':
            return 'BASF SE (Frankfurt Stock Exchange)'
        case 'BAYN.DE':
            return 'Bayer AG (Frankfurt Stock Exchange)'
        case 'BDX':
            return 'Becton, Dickinson and Company (BD)'
        case 'BMY':
            return 'Bristol Myers Squibb'
        case 'BP':
            return 'BP (NY Stock Exchange)'
        case 'BP.L':
            return 'BP (London Stock Exchange)'
        case 'CVX':
            return 'Chevron'
        # case 'SNP':
        #     return 'China Pretroleum & Chemical (Sinopec) (NY Stock Exchange)'
        case '0386.HK':
            return 'China Pretroleum & Chemical (Sinopec) (Hong Kong Stock Exchange)'
        case '600028.SS':
            return 'China Pretroleum & Chemical (Sinopec) (Shanghai Stock Exchange)'
        case 'CHD':
            return 'Church & Dwight'
        case 'CL':
            return 'Colgate-Palmolive'
        case 'COP':
            return 'ConocoPhillips'
        case 'DOW':
            return 'Dow'
        case 'DD':
            return 'DuPont'
        case 'EMN':
            return 'Eastman Chemical Company'
        case 'ECL':
            return 'Ecolab'        
        case 'EVK.DE':
            return 'Evonik Industries'
        case 'XOM':
            return 'ExxonMobil'
        case 'HUN':
            return 'Huntsman Corporation'
        case 'IFF':
            return 'IFF'
        case 'JNJ':
            return 'Johnson & Johnson'
        case 'JMAT.L':
            return 'Johnson Matthey (London Stock Exchange)'
        case 'K':
            return 'Kellogg Company'
        case 'KHC':
            return 'The Kraft Heinz Company'
        case 'LIN.DE':
            return 'Linde (Frankfurt Stock Exchange)'
        case 'LIN':
            return 'Linde (NY Stock Exchange)'
        case 'OR.PA':
            return 'L_Oreal S.A. (Euronext Paris)'
        case 'LYB':
            return 'LyondellBasell'
        case 'MMM':
            return '3M'
        case 'MPC':
            return 'Marthon Petroleum'
        case 'MRK':
            return 'Merck'
        case 'NESN.SW':
            return 'Nestle S.A (SIX Swiss Exchange)'
        # case 'PTC':
        #     return 'PetroChina (NY Stock Exchange)'
        case '0857.HK':
            return 'PetroChina (Hong Kong Stock Exchange)'
        case '601857.SS':
            return 'PetroChina (Shanghai Stock Exchange)'
        case 'PFF':
            return 'Pfizer'
        case 'PG':
            return 'Proctor & Gamble'
        case 'ROG.SW':
            return 'Roche (SIX Swiss Exchange)'
        case 'SHEL':
            return 'Shell (NY Stock Exchange)'
        case 'SHEL.L':
            return 'Shell (London Stock Exchange)'
        case '4911.T':
            return 'Shiseido (Tokyo Stock Exchange)'
        case '4005.T':
            return 'Sumitomo Chemical (Tokyo Stock Exchange)'
        case 'TGT':
            return 'Target'
        case 'TSLA':
            return 'Tesla'
        case '4042.T':
            return 'Tosoh (Tokyo Stock Exchange)'
        case 'UL':
            return 'Unilever'
        case 'WMT':
            return 'Walmart'
        case _:
            return 'Uh-oh, something went wrong'
    
def stock_chart_y_label(ticker_symbol):
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
    match ticker_symbol:
        case '^GSPC':
            return 'S&P500 (NY Stock Exchange)'
        case '^DJI':
            return 'Dow Jones (NY Stock Exchange)'
        case '^IXIC':
            return 'NASDAQ (NY Stock Exchange)'
        case '^NYA':
            return 'NYSE Composite (NY Stock Exchange)'
        case '^GDAXI':
            return 'Dax Performance Index (Frankfurt Stock Exchange)'
        case '^FTSE':
            return 'FTSE 100 (London Stock Exchange)'
        case '^N225':
            return 'Nikkei 225 (Tokyo Stock Exchange)'
        case '000001.SS':
            return 'Shanghai SE Composite Index (Shanghai Stock Exchange)'
        case '000300.SS':
            return 'CSI 300 (Shanghai Stock Exchange)'
        case '^HSI':
            return 'Hang Seng Index (Hong Kong Stock Exchange)'
        
def index_chart_y_label(ticker_symbol):
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
        if max_high == 0:
            max_high_data = pd.DataFrame(data = {' ':'Maximum Price',
                                                  'Date':summary_data_max_high.loc[max_high,'Date'].date().strftime("%m-%d-%Y"),
                                                  y_label:summary_data_max_high.loc[max_high,'High']},
                                         index = [max_high])
        else:
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
                                                         dcc.Dropdown(id='stock_ticker',options=[{'label':'Air Liquide (Euronext Paris)','value':'AI.PA'},
                                                                                                 {'label':'Air Products','value':'APD'},
                                                                                                 {'label':'Amazon','value':'AMZN'},
                                                                                                 {'label':'Amgen','value':'AMGN'},
                                                                                                 {'label':'Apple','value':'AAPL'},
                                                                                                 {'label':'BASF SE (Frankfurt Stock Exchange)','value':'BAS.DE'},
                                                                                                 {'label':'Bayer AG (Frankfurt Stock Exchange)','value':'BAYN.DE'},
                                                                                                 {'label':'Becton, Dickinson and Company (BD)','value':'BDX'},
                                                                                                 {'label':'Bristol Myers Squibb','value':'BMY'},
                                                                                                 {'label':'BP (NY Stock Exchange)','value':'BP'},
                                                                                                 {'label':'BP (London Stock Exchange)','value':'BP.L'},
                                                                                                 {'label':'Chevron','value':'CVX'},
                                                                                                 # {'label':'China Pretroleum & Chemical (Sinopec) (NY Stock Exchange)','value':'SNP'},
                                                                                                 {'label':'China Pretroleum & Chemical (Sinopec) (Hong Kong Stock Exchange)','value':'0386.HK'},
                                                                                                 {'label':'China Pretroleum & Chemical (Sinopec) (Shanghai Stock Exchange)','value':'600028.SS'},
                                                                                                 {'label':'Church & Dwight','value':'CHD'},
                                                                                                 {'label':'Colgate-Palmolive','value':'CL'},
                                                                                                 {'label':'ConocoPhillips','value':'COP'},
                                                                                                 {'label':'Dow','value':'DOW'},
                                                                                                 {'label':'DuPont','value':'DD'},
                                                                                                 {'label':'Eastman Chemical Company','value':'EMN'},
                                                                                                 {'label':'Ecolab','value':'ECL'},
                                                                                                 {'label':'Evonik Industries AG (Frankfurt Stock Exchange)','value':'EVK.DE'},
                                                                                                 {'label':'ExxonMobil','value':'XOM'},
                                                                                                 {'label':'Huntsman Corporation','value':'HUN'},
                                                                                                 {'label':'IFF','value':'IFF'},
                                                                                                 {'label':'Johnson & Johnson','value':'JNJ'},
                                                                                                 {'label':'Johnson Matthey (London Stock Exchange)','value':'JMAT.L'},
                                                                                                 {'label':'Kellogg Company','value':'K'},
                                                                                                 {'label':'The Kraft Heinz Company','value':'KHC'},
                                                                                                 {'label':'Linde (Frankfurt Stock Exchange)','value':'LIN.DE'},
                                                                                                 {'label':'Linde (NY Stock Exchange)','value':'LIN'},
                                                                                                 {'label':'L_Oreal S.A. (Euronext Paris)','value':'OR.PA'},
                                                                                                 {'label':'LyondellBasell','value':'LYB'},
                                                                                                 {'label':'3M','value':'MMM'},
                                                                                                 {'label':'Marathon Petroleum','value':'MPC'},
                                                                                                 {'label':'Merck','value':'MRK'},
                                                                                                 {'label':'Nestle S.A. (SIX Swiss Exchange)','value':'NESN.SW'},
                                                                                                 # {'label':'PetroChina (NY Stock Exchange)','value':'PTC'},
                                                                                                 {'label':'PetroChina (Hong Kong Stock Exchange)','value':'0857.HK'},
                                                                                                 {'label':'PetroChina (Shanghai Stock Exchange)','value':'601857.SS'},
                                                                                                 {'label':'Pfizer','value':'PFE'},
                                                                                                 {'label':'Proctor & Gamble','value':'PG'},
                                                                                                 {'label':'Roche (SIX Swiss Exchange)','value':'ROG.SW'},
                                                                                                 {'label':'Shell (NY Stock Exchange)','value':'SHEL'},
                                                                                                 {'label':'Shell (London Stock Exchange)','value':'SHEL.L'},
                                                                                                 {'label':'Shiseido (Tokyo Stock Exchange)','value':'4911.T'},
                                                                                                 {'label':'Sumitomo Chemical (Tokyo Stock Exchange)','value':'4005.T'},
                                                                                                 {'label':'Target','value':'TGT'},
                                                                                                 {'label':'Tesla','value':'TSLA'},
                                                                                                 {'label':'Tosoh (Tokyo Stock Exchange)','value':'4042.T'},
                                                                                                 {'label':'Unilever','value':'UL'},
                                                                                                 {'label':'Walmart','value':'WMT'}],
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
                                                       dcc.Dropdown(id='index_ticker',options=[{'label':'S&P500 (NY Stock Exchange)','value':'^GSPC'},
                                                                                               {'label':'Dow Jones (NY Stock Exchange)','value':'^DJI'},
                                                                                               {'label':'NASDAQ (NY Stock Exchange','value':'^IXIC'},
                                                                                               {'label':'NYSE Composite (NY Stock Exchange)','value':'^NYA'},
                                                                                               {'label':'Dax Performance Index (Frankfurt Stock Exchange)','value':'^GDAXI'},
                                                                                               {'label':'FTSE 100 (London Stock Exchange)','value':'^FTSE'},
                                                                                               {'label':'Nikkei 225 (Tokyo Stock Exchange)','value':'^N225'},
                                                                                               {'label':'Shanghai SE Composite Index (Shanghai Stock Exchange)','value':'000001.SS'},
                                                                                               {'label':'CSI 300 (Shanghai Stock Exchange)','value':'000300.SS'},
                                                                                               {'label':'Hang Seng Index (Hong Kong Stock Exchange)','value':'^HSI'}],
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
                      showlegend = False)
    fig.update_xaxes(title_font_size = 22,
                     tickfont_size = 18)
    fig.update_yaxes(title_font_size = 22,
                     tickfont_size = 18)
    if (max(stock_summary_data['High']) - min(stock_summary_data['Low']) < 5):
        fig.update_yaxes(tickformat = '.2f')
    summary_title = html.Label([f'{stock_chart_title(stock_ticker)}'+' summary table'])
    stock_summary_data_max_high = stock_summary_data.loc[((stock_summary_data['High'] == max(stock_summary_data['High'])) & (stock_summary_data['Volume']>0))].reset_index(drop = True)
    stock_summary_data_max_close = stock_summary_data.loc[((stock_summary_data['Close'] == max(stock_summary_data['Close'])) & (stock_summary_data['Volume']>0))].reset_index(drop = True)
    stock_summary_data_min_close = stock_summary_data.loc[((stock_summary_data['Close'] == min(stock_summary_data['Close'])) & (stock_summary_data['Volume']>0))].reset_index(drop = True)
    stock_summary_data_min_low = stock_summary_data.loc[((stock_summary_data['Low'] == min(stock_summary_data['Low'])) & (stock_summary_data['Volume']>0))].reset_index(drop = True)
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
                          t = 60))
    fig.update_xaxes(title_font_size = 22,
                     tickfont_size = 18)
    fig.update_yaxes(title_font_size = 22,
                     tickfont_size = 18)
    if max(index_plot_data['High'] > 10000):
        fig.update_yaxes(tickformat = '000')
    summary_title = html.Label([f'{index_chart_title(index_ticker)}'+' summary table'])
    index_summary_data_max_high = index_plot_data.loc[((index_plot_data['High'] == max(index_plot_data['High'])) & (index_plot_data['Volume']>0))].reset_index(drop = True)
    index_summary_data_max_close = index_plot_data.loc[((index_plot_data['Close'] == max(index_plot_data['Close'])) & (index_plot_data['Volume']>0))].reset_index(drop = True)
    index_summary_data_min_close = index_plot_data.loc[((index_plot_data['Close'] == min(index_plot_data['Close'])) & (index_plot_data['Volume']>0))].reset_index(drop = True)
    index_summary_data_min_low = index_plot_data.loc[((index_plot_data['Low'] == min(index_plot_data['Low'])) & (index_plot_data['Volume']>0))].reset_index(drop = True)
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

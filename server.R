require(shiny)
require(quantmod)
require(tidyquant)
require(dplyr)
require(tidyr)
require(ggplot2)
require(scales)

get_stock_ticker_data <- function (ticker_symbol) {
  raw_data <- suppressWarnings(getSymbols(ticker_symbol,env=NULL))
  # the quantmod version of this function seems to only update with yesterday's data, whereas Python's yfinance can fetch today's data
  data_framed_data <- data.frame(Date = index(raw_data),coredata(raw_data)) %>%
    drop_na()
  return(data_framed_data)
}

stock_chart_title <- function(ticker_symbol) {
  company_name <- switch(ticker_symbol,
                         'AI.PA' = 'Air Liquide (Euronext Paris)',
                         'APD' = 'Air Products',
                         'AMZN' = 'Amazon',
                         'AMGN' = 'Amgen',
                         'AAPL' = 'Apple',
                         'BAS.DE' = 'BASF SE (Frankfurt Stock Exchange)',
                         'BAYN.DE' = 'Bayer AG (Frankfurt Stock Exchange)',
                         'BDX' = 'Becton, Dickinson and Company (BD)',
                         'BP' = 'BP (NY Stock Exchange)',
                         'BP.L' = 'BP (London Stock Exchange)',
                         'BMY' = 'Bristol Myers Squibb',
                         'CVX' = 'Chevron',
                         # 'SNP' = 'China Petroleum & Chemical (Sinopec) (NY Stock Exchange)',
                         '0386.HK' = 'China Petroleum & Chemical (Sinopec) (Hong Kong Stock Exchange)',
                         '600028.SS' = 'China Petroleum & Chemical (Sinopec) (Shanghai Stock Exchange)',
                         'CHD' = 'Church & Dwight',
                         'CL' = 'Colgate-Palmolive',
                         'COP' = 'ConocoPhillips',
                         'DOW' = 'Dow',
                         'DD' = 'DuPont',
                         'EMN' = 'Eastman Chemical Company',
                         'ECL' = 'Ecolab',
                         'EVK.DE' = 'Evonik Industries AG (Frankfurt Stock Exchange)',
                         'XOM' = 'ExxonMobil',
                         'HUN' = 'Huntsman Corporation',
                         'IFF' = 'IFF',
                         'JNJ' = 'Johnson & Johnson',
                         'JMAT.L' = 'Johnson Matthey (London Stock Exchange)',
                         'K' = 'Kellogg Company',
                         'KHC' = 'The Kraft Heinz Company',
                         'LIN.DE' = 'Linde (Frankfurt Stock Exchange)',
                         'LIN' = 'Linde (NY Stock Exchange)',
                         'OR.PA' = "L'Oreal S.A (Euronext Paris)",
                         'LYB' = 'LyondellBasell',
                         'MPC' = 'Marathon Petroleum',
                         'MRK' = 'Merck',
                         'MMM' = '3M',
                         'MDLZ' = 'Mondelez International',
                         'NESN.SW' = 'Nestle S.A. (SIX Swiss Exchange)',
                         # 'PTC' = 'PetroChina (NY Stock Exchange)',
                         '0857.HK' = 'PetroChina (Hong Kong Stock Exchange)',
                         '601857.SS' = 'PetroChina (Shanghai Stock Exchange)',
                         'PFE' = 'Pfizer',
                         'PG' = 'Proctor & Gamble',
                         'ROG.SW' = 'Roche (SIX Swiss Exchange)',
                         'SHEL' = 'Shell (NY Stock Exchange)',
                         'SHEL.L' = 'Shell (London Stock Exchange)',
                         '4991.T' = 'Shiseido (Tokyo Stock Exchange)',
                         '4005.T' = 'Sumitomo Chemical (Tokyo Stock Exchange)',
                         'TGT' = 'Target',
                         'TSLA' = 'Tesla',
                         '4042.T' = 'Tosoh (Tokyo Stock Exchange)',
                         'UL' = 'Unilever',
                         'WMT' = 'Walmart')
  return(company_name)
}

index_chart_title <- function(selected_index) {
  index_name <- switch(selected_index,
                       '^GSPC' = 'S&P500 (NY Stock Exchange)',
                       '^DJI' = 'Dow Jones (NY Stock Exchange)',
                       '^IXIC' = 'NASDAQ (NY Stock Exchange)',
                       '^NYA' = 'NYSE Composite (NY Stock Exchange)',
                       '^GDAXI' = 'Dax Performance Index (Frankfurt Stock Exchange)',
                       '^FTSE' = 'FTSE 100 (London Stock Exchange)',
                       '^N225' = 'Nikkei 225 (Tokyo Stock Exchange)',
                       '000001.SS' = 'Shanghai SE Composite Index (Shanghai Stock Exchange)',
                       '000300.SS' = 'CSI 300 (Shanghai Stock Exchange)',
                       '^HSI' = 'Hang Seng Index (Hong Kong Stock Exchange)')
  return(index_name)
}

shinyServer(function(input, output, session) {
  stock_to_listen <- reactive({
    list(input$stock_plot_type,
         input$stock_ticker,
         input$stock_tail_days,
         input$stock_plot_date_select,
         input$stock_date_range,
         input$moving_average_days,
         input$moving_average_check)
  })
  observeEvent(stock_to_listen(), {
    stock_data <- get_stock_ticker_data(input$stock_ticker)
    stock_column_names <- c('Date','Open','High','Low','Close','Volume','Adjusted')
    colnames(stock_data) <- stock_column_names
    moving_average_days <- input$moving_average_days
    if (input$stock_plot_date_select == 'stock_date_range') {
      stock_plot_data <- stock_data %>%
        filter(Date >= input$stock_date_range[1]) %>%
        filter(Date <= input$stock_date_range[2])
      stock_summary_data <- stock_data %>%
        filter(Date >= input$stock_date_range[1]) %>%
        filter(Date <= input$stock_date_range[2])
      stock_moving_average_data <- stock_data %>%
        tail(dim(stock_plot_data)[1] + moving_average_days)
    } else {
      stock_tail_days <- input$stock_tail_days
      stock_plot_data <- stock_data %>%
        filter(Date >= Sys.Date()-stock_tail_days)
      stock_summary_data <- stock_data %>%
        filter(Date >= Sys.Date()-stock_tail_days)
      stock_moving_average_data <- stock_data %>%
        tail(dim(stock_plot_data)[1] + moving_average_days)
    }
    format_digits <- 0
    if (input$stock_ticker == 'BAS.DE' ||
        input$stock_ticker == 'AI.PA' ||
        input$stock_ticker == 'BAYN.DE' ||
        input$stock_ticker == 'EVK.DE' ||
        input$stock_ticker == 'LIN.DE' ||
        input$stock_ticker == 'OR.PA') {
      y_label <- 'Price (€)'
    } else {
      if (input$stock_ticker == 'BP.L' ||
          input$stock_ticker == 'JMAT.L' ||
          input$stock_ticker == 'SHEL.L') {
        y_label <- 'Price (£)'
        format_digits <- 2
        for (column_name in colnames(stock_plot_data)) {
          if (column_name == 'Open' ||
              column_name == 'High' ||
              column_name == 'Low' ||
              column_name == 'Close') {
            stock_plot_data[[column_name]] <- stock_plot_data[[column_name]] / 100
          }
        }
        for (column_name in colnames(stock_summary_data)) {
          if (column_name == 'Open' ||
              column_name == 'High' ||
              column_name == 'Low' ||
              column_name == 'Close') {
            stock_summary_data[[column_name]] <- stock_summary_data[[column_name]] / 100
          }
        }
        for (column_name in colnames(stock_moving_average_data)) {
          if (column_name == 'Open' ||
              column_name == 'High' ||
              column_name == 'Low' ||
              column_name == 'Close') {
            stock_moving_average_data[[column_name]] <- stock_moving_average_data[[column_name]] / 100
          }
        }
      } else {
        if (input$stock_ticker == '4911.T' ||
            input$stock_ticker == '4042.T' ||
            input$stock_ticker == '4005.T' ||
            input$stock_ticker == '600028.SS' ||
            input$stock_ticker == '601857.SS') {
          y_label <- 'Price (¥)'
          } else {
            if (input$stock_ticker == 'NESN.SW' ||
                input$stock_ticker == 'ROG.SW') {
              y_label <- 'Price (CHF)'
              } else {
                if (input$stock_ticker == '0386.HK' ||
                    input$stock_ticker == '0857.HK') {
                  y_label <- 'Price (HK$)'
                  format_digits <- 2
                } else {
                  y_label <- 'Price ($)'
                }
              }
          }
      }
    }
    output$stock_plot <- renderPlot({
      stock_plot <- ggplot(data = stock_plot_data, aes(x=Date, y = Close)) +
        labs(title = stock_chart_title(input$stock_ticker), y = y_label) +
        coord_x_date(xlim = c(stock_plot_data$Date[1],stock_plot_data$Date[length(stock_plot_data$Date)]),expand = TRUE) +
        scale_y_continuous(labels = function(x) formatC(x, digits = format_digits, width = 7, format = 'f')) +
        theme(title = element_text(size = 18),
              plot.title = element_text(hjust = 0.5),
              axis.title = element_text(size = 18),
              axis.text = element_text(size = 14))
      if (input$stock_plot_type == 'candle') {
        if (input$moving_average_check == TRUE) {
          stock_plot + geom_candlestick(aes(open = Open, high = High, low = Low, close = Close), colour_up = 'darkseagreen', fill_up = 'darkseagreen') +
            geom_ma(data = stock_moving_average_data, aes(x = Date, y = Close), ma_fun = SMA, n = moving_average_days, color = 'orange', size = 1)
        } else {
          stock_plot + geom_candlestick(aes(open = Open, high = High, low = Low, close = Close), colour_up = 'darkseagreen', fill_up = 'darkseagreen')
        }
      } else {
        stock_plot + geom_line(size = 0.7)
      }
    })
    stock_summary_data_max_high <- stock_summary_data %>%
      filter(High == max(High)) %>%
      filter(Volume > 0)
    stock_summary_data_max_close <- stock_summary_data %>%
      filter(Close == max(Close)) %>%
      filter(Volume > 0)
    stock_summary_data_min_close <- stock_summary_data %>%
      filter(Close == min(Close)) %>%
      filter(Volume > 0)
    stock_summary_data_min_Low <- stock_summary_data %>%
      filter(Low == min(Low)) %>%
      filter(Volume > 0)
    for (max_high in 1:dim(stock_summary_data_max_high)[1]) {
      if (max_high == 1) {
        stock_max_high_data <- data.frame(label = 'Maximum Price',
                                          Date = stock_summary_data_max_high$Date[max_high],
                                          price_placeholder = stock_summary_data_max_high$High[max_high])
      } else {
        stock_max_high_data_vector <- data.frame(label = '',
                                                 Date = stock_summary_data_max_high$Date[max_high],
                                                 price_placeholder = stock_summary_data_max_high$High[max_high])
        stock_max_high_data <- rbind(stock_max_high_data,stock_max_high_data_vector)
      }
    }
    for (max_close in 1:dim(stock_summary_data_max_close)[1]) {
      if (max_close == 1) {
        stock_max_close_data <- data.frame(label = 'Maximum Closing Price',
                                           Date = stock_summary_data_max_close$Date[max_close],
                                           price_placeholder = stock_summary_data_max_close$Close[max_close])
      } else {
        stock_max_close_data_vector <- data.frame(label = '',
                                                  Date = stock_summary_data_max_close$Date[max_close],
                                                  price_placeholder = stock_summary_data_max_close$Close[max_close])
        stock_max_close_data <- rbind(stock_max_close_data,stock_max_close_data_vector)
      }
    }
    for (min_close in 1:dim(stock_summary_data_min_close)[1]) {
      if (min_close == 1) {
        stock_min_close_data <- data.frame(label = 'Minimum Closing Price',
                                           Date = stock_summary_data_min_close$Date[min_close],
                                           price_placeholder = stock_summary_data_min_close$Close[min_close])
      } else {
        stock_min_close_data_vector <- data.frame(label = '',
                                                  Date = stock_summary_data_min_close$Date[min_close],
                                                  price_placeholder = stock_summary_data_min_close$Close[min_close])
        stock_min_close_data <- rbind(stock_min_close_data,stock_min_close_data_vector)
      }
    }
    for (min_low in 1:dim(stock_summary_data_min_Low)[1]) {
      if (min_low == 1) {
        stock_min_low_data <- data.frame(label = 'Miniumum Price',
                                         Date = stock_summary_data_min_Low$Date[min_low],
                                         price_placeholder = stock_summary_data_min_Low$Low[min_low])
      } else {
        stock_min_low_data_vector <- data.frame(label = '',
                                                Date = stock_summary_data_min_Low$Date[min_low],
                                                price_placeholder = stock_summary_data_min_Low$Low[min_low])
        stock_min_low_data <- rbind(stock_min_low_data,stock_min_low_data_vector)
      }
    }
    stock_plot_data_summary <- rbind(stock_max_high_data, stock_max_close_data, stock_min_close_data, stock_min_low_data)
    Price_column_new_name <- c(' ',y_label)
    stock_plot_data_summary <- stock_plot_data_summary %>%
      rename_with(~Price_column_new_name,.cols = c('label','price_placeholder'))
    # stock_plot_data_summary$Date <- format(stock_plot_data_summary$Date, '%Y-%m-%d')
    stock_plot_data_summary$Date <- format(stock_plot_data_summary$Date, '%m-%d-%y')
    output$stock_summary_table_title <- renderText(paste0(stock_chart_title(input$stock_ticker),' summary table'))
    output$stock_summary_table <- renderTable(stock_plot_data_summary)
  })
  observeEvent(input$stock_date_reset_button, ignoreInit = TRUE, {
    updateDateRangeInput(session,
                         inputId = 'stock_date_range',
                         label = 'Date range input: yyyy-mm-dd',
                         start = Sys.Date() - 30,
                         end = Sys.Date(),
                         max = Sys.Date())
  })
  index_to_listen <- reactive({
    list(input$index_plot_type,
         input$selected_index,
         input$index_tail_days,
         input$index_plot_date_select,
         input$index_date_range)
  })
  observeEvent(index_to_listen(),{
    index_data <- get_stock_ticker_data(input$selected_index)
    index_column_names <- c('Date','Open','High','Low','Close','Volume','Adjusted')
    colnames(index_data) <- index_column_names
    if (input$index_plot_date_select == 'index_date_range') {
      index_plot_data <- index_data %>%
        filter(Date >= input$index_date_range[1]) %>%
        filter(Date <= input$index_date_range[2])
    } else {
      index_tail_days <- input$index_tail_days
      index_plot_data <- index_data %>%
        filter(Date >= Sys.Date()-index_tail_days)
    }
    if (input$selected_index == '^GDAXI') {
      y_label <- 'Price (€)'
    } else {
      if (input$selected_index == '^FTSE') {
        y_label <- 'Price (£)'
      } else {
        if (input$selected_index == '^N225' ||
            input$selected_index == '000001.SS' ||
            input$selected_index == '000300.SS') {
          y_label <- 'Price (¥)'
        } else {
          if(input$selected_index == '^HSI') {
            y_label <- 'Price (HK$)'
          } else {
            y_label <- 'Price ($)'
          }
          
        }
      }
    }
    output$index_plot <- renderPlot({
      index_plot <- ggplot(data = index_plot_data,aes(x=Date,y=Close)) +
        labs(title = index_chart_title(input$selected_index), y = y_label) +
        coord_x_date(xlim = c(index_plot_data$Date[1],index_plot_data$Date[length(index_plot_data$Date)]),expand = TRUE) +
        scale_y_continuous(labels = function(x) formatC(x, digits = 0, width = 6, format = 'f')) +
        theme(title = element_text(size = 18),
              plot.title = element_text(hjust = 0.5),
              axis.title = element_text(size = 18),
              axis.text = element_text(size = 14))
      if (input$index_plot_type == 'candle') {
        index_plot + geom_candlestick(aes(open = Open, high = High, low = Low, close = Close), colour_up = 'darkseagreen', fill_up = 'darkseagreen')  
      } else {
        index_plot + geom_line(size = 0.7)
      }
    })
    index_summary_data_max_high <- index_plot_data %>%
      filter(High == max(High)) %>%
      filter(Volume > 0)
    index_summary_data_max_close <- index_plot_data %>%
      filter(Close == max(Close)) %>%
      filter(Volume > 0)
    index_summary_data_min_close <- index_plot_data %>%
      filter(Close == min(Close)) %>%
      filter(Volume > 0)
    index_summary_data_min_low <- index_plot_data %>%
      filter(Low == min(Low)) %>%
      filter(Volume >0)
    for (max_high in 1:dim(index_summary_data_max_high)[1]) {
      if (max_high == 1) {
        index_max_high_data <- data.frame(label = 'Maximum Price',
                                          Date = index_summary_data_max_high$Date[max_high],
                                          price_placeholder = index_summary_data_max_high$High[max_high])
      } else {
        index_max_high_data_vector <- data.frame(label = '',
                                                 Date = index_summary_data_max_high$Date[max_high],
                                                 price_placeholder = index_summary_data_max_high$High[max_high])
        index_max_high_data <- rbind(index_max_high_data,index_max_high_data_vector)
      }
    }
    for (max_close in 1:dim(index_summary_data_max_close)[1]) {
      if (max_close == 1) {
        index_max_close_data <- data.frame(label = 'Maximum Closing Price',
                                           Date = index_summary_data_max_close$Date[max_close],
                                           price_placeholder = index_summary_data_max_close$Close[max_close])
      } else {
        index_max_close_data_vector <- data.frame(label = '',
                                                  Date = index_summary_data_max_close$Date[max_close],
                                                  price_placeholder = index_summary_data_max_close$Close[max_close])
        index_max_close_data <- rbind(index_max_close_data,index_max_close_data_vector)
      }
    }
    for (min_close in 1:dim(index_summary_data_min_close)[1]) {
      if (min_close == 1) {
        index_min_close_data <- data.frame(label = 'Minimum Closing Price',
                                           Date = index_summary_data_min_close$Date[min_close],
                                           price_placeholder = index_summary_data_min_close$Close[min_close])
      } else {
        index_min_close_data_vector <- data.frame(label = '',
                                                  Date = index_summary_data_min_close$Date[min_close],
                                                  price_placeholder = index_summary_data_min_close$Close[min_close])
        index_min_close_data <- rbind(index_min_close_data,index_min_close_data_vector)
      }
    }
    for (min_low in 1:dim(index_summary_data_min_low)[1]) {
      if (min_low == 1) {
        index_min_low_data <- data.frame(label = 'Miniumum Price',
                                         Date = index_summary_data_min_low$Date[min_low],
                                         price_placeholder = index_summary_data_min_low$Low[min_low])
      } else {
        index_min_low_data_vector <- data.frame(label = '',
                                                Date = index_summary_data_min_low$Date[min_low],
                                                price_placeholder = index_summary_data_min_low$Low[min_low])
        index_min_low_data <- rbind(index_min_low_data,index_min_low_data_vector)
      }
    }
    index_plot_data_summary <- rbind(index_max_high_data, index_max_close_data, index_min_close_data, index_min_low_data)
    Price_column_new_name <- c(' ',y_label)
    index_plot_data_summary <- index_plot_data_summary %>%
      rename_with(~Price_column_new_name,.cols = c('label','price_placeholder'))
    index_plot_data_summary$Date <- format(index_plot_data_summary$Date, '%m-%d-%y')
    output$index_summary_table_title <- renderText(paste0(index_chart_title(input$selected_index),' summary table'))
    output$index_summary_table <- renderTable(index_plot_data_summary)
  })
  observeEvent(input$index_date_reset_button, ignoreInit = TRUE, {
    updateDateRangeInput(session,
                         inputId = 'index_date_range',
                         label = 'Date range input: yyyy-mm-dd',
                         start = Sys.Date() - 30,
                         end = Sys.Date(),
                         max = Sys.Date())
  })
})

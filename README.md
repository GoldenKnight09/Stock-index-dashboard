# Stock & index dashboard
This is a simple dashboard designed to visualize various stock & index prices. There are two versions of it: one is written in R (Shiny) and the other is written in Python (Dash). The two versions are designed to present the information in the same manner as much as possible, with the only difference being the language used to write the code.

## Key features:
- Consolidates several stocks & indices onto a single dashboard, displaying each on separate graphs (limited to one stock and index at a time).
- Pricing information is displayed using either candlestick (full pricing information) or line (closing price only) visualizations.
  - A visualization of the moving average of the closing price (with a user defined period) can also be added to the candlestick visualization.
- User specified time period for the visualizations.
- Dynamic user interface that updates based on user inputs.

## Live demonstrations of the dashboard:
R: hosted on shinyapps.io located [here](https://goldenknight09.shinyapps.io/stock_price_dashboard/).

Python: hosted on Render located [here](https://stock-index-dashboard.onrender.com).

## Future plans:
Utilize predictive modeling and  machine learning to attempt to predict future stock / index prices from historical data and include this prediction in the dashboard.

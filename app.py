#Import some modules so we can do some work
from flask import Flask, render_template, request, redirect

import pandas as pd
import numpy as np
import requests
from datetime import date

from bokeh.layouts import gridplot
from bokeh.plotting import figure, show, output_file
from bokeh.io import output_notebook

def datetime(t):
    return np.array(t, dtype=np.datetime64)

def getStock(stock, start_date, end_date):
    base_url = 'https://www.quandl.com/api/v3/datasets/EOD/'
    api_key = 'qxekeyFpUrqsvbjijqCF'
    query=base_url + stock + '?start_date=' + start_date + '&end_date=' + end_date + '&api_key=' + api_key

    r = requests.get(query).json()
    cols = r['dataset']['column_names']
    rows = r['dataset']['data']
    
    df = pd.DataFrame.from_records(rows, columns=cols)
    df.set_index('Date',inplace=True)
    df.sort_index(inplace=True)

    return df

def drawGraph(df, stock, open_price=False, close_price=True, adj_open=False, adj_close=False):
    p = figure(x_axis_type="datetime", title="Quandl WIKI EOD Stock Prices") 
    p.grid.grid_line_alpha = 0.3
    p.xaxis.axis_label = 'Date'
    p.yaxis.axis_label = 'Price'
    
    if open_price:
        p.line(datetime(df.index),df['Open'], color="darkorange", legend=stock + ': Open')
    if close_price:
        p.line(datetime(df.index),df['Close'], color="blue", legend=stock + ': Close')
    if adj_open:
        p.line(datetime(df.index),df['Adj_Open'], color="red", legend=stock + ': Adj_Open')
    if adj_close:
        p.line(datetime(df.index),df['Adj_Close'], color="green", legend=stock + ': Adj_Close')
    p.legend.location='top_right'
    show(p)


app = Flask(__name__)

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/about')
def about():
  return render_template('about.html')

@app.route('/graph/'i,methods=['GET','POST'])
def graph():
  stock = request.form['ticker']
  return render_template('graph.html')

if __name__ == '__main__':
  app.run(port=33507)

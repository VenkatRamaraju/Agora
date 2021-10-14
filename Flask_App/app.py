from flask import Flask, render_template, request, redirect
import sqlite3
from sqlite3 import Error
import os.path
from fetch_top_stocks_yf import get_trending_stocks

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
print(BASE_DIR)
db_path = os.path.join(BASE_DIR, "database.db")


def get_db_connection():
    conn = None
    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
    except Error as e:
        print(e)

    return conn


app = Flask(__name__)


@app.route('/')
def index():
    trending_stocks = get_trending_stocks()
    conn = get_db_connection()
    all_tickers_sql = conn.execute(
        "select ticker from TickerStockMetrics;"
    ).fetchall()

    all_tickers = []
    for i in all_tickers_sql:
        all_tickers.append(i[0])

    trending_tickers = []
    for i in trending_stocks:
        trending_tickers.append(i['ticker'])

    filtered_tickers = [x for x in trending_tickers if x in all_tickers]

    return render_template('index.html',
                           trending_stocks=filtered_tickers[:5])


@app.route('/data/', methods=['GET', 'POST'])
def data():
    conn = get_db_connection()
    ticker_name = ""
    if request.method == 'GET':
        # return f"The URL '/data' is accessed directly"
        ticker_name = request.args["Searched Ticker"]
    if request.method == 'POST':
        form_data = request.form
        ticker_name = form_data["Searched Ticker"]

    all_tickers_sql = conn.execute(
        "select ticker from TickerStockMetrics;"
    ).fetchall()

    all_tickers = []
    for i in all_tickers_sql:
        all_tickers.append(i[0])

    if ticker_name not in all_tickers:
        return redirect("/")

    predictions_sql = f"""
            Select * from TickerPredictions where ticker="{ticker_name}";
            """
    ticker_preds = conn.execute(predictions_sql).fetchall()

    info_sql = f"""
          Select * from TickerStockMetrics where ticker="{ticker_name}";
          """
    ticker_info = conn.execute(info_sql).fetchall()

    if ticker_info == [] or ticker_preds == []:     # Enter a valid ticker
        return render_template('index.html')

    headlines_sql = f"""
                Select headlines from TickerHeadlines where ticker="{ticker_name}" limit 3
                """
    ticker_headlines = conn.execute(headlines_sql).fetchall()

    conn.close()

    return render_template('data.html',
                           ticker_name=ticker_name,
                           ticker_info=ticker_info,
                           ticker_headlines=ticker_headlines,
                           ticker_predictions=ticker_preds)

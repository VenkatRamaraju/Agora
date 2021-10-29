from flask import Flask, render_template, request, redirect
import sqlite3
from sqlite3 import Error
import os.path
from fetch_top_stocks_yf import get_trending_stocks
from price import get_last_price

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

    all_tickers_sql_preds = conn.execute(
        "select ticker, agora_pred from TickerPredictions;"
    ).fetchall()

    all_tickers = []

    for i in all_tickers_sql_preds:
        all_tickers.append(
            {
                "ticker": i[0],
                "agora_pred": i[1]
            }
        )

    trending_tickers = []
    for i in trending_stocks:
        trending_tickers.append(
            {
                "ticker": i['ticker'],
                "price": i['current_price']
            }
        )

    filtered_tickers = []

    for trending_dict in trending_tickers:
        for ticker_dict in all_tickers:
            if trending_dict['ticker'] == ticker_dict['ticker'] and ticker_dict['agora_pred'] is not None:
                filtered_tickers.append(
                    {
                        "ticker": trending_dict['ticker'],
                        "price": trending_dict['price'],
                        "pred": ticker_dict['agora_pred']
                    }
                )

    # filtered_tickers = [x for x in trending_tickers if x in all_tickers]

    # print(filtered_tickers)

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

    stock_price_dict = get_last_price(ticker_name)

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

    predictions_sql = f"""
            Select ticker, company_name, analyst_pred, agora_pred, 
                   Round(headline_polarity, 2) as headline_polarity,
                   Round(conversation_polarity, 2) as conversation_polarity 
                   from TickerPredictions where ticker="{ticker_name}";
            """
    ticker_preds = conn.execute(predictions_sql).fetchall()

    # info_sql = f"""
    #       Select ticker, Round(beta, 2) as beta,
    #       	     Round(profit_margins, 2) as profit_margins,
    #       	     Round(forward_eps, 2) as forward_eps,
    #       	     Round(book_value, 2) as book_value,
    #       	     Round(held_percent_institutions, 2) as held_percent_institutions,
    #       	     Round(short_ratio, 2) as short_ratio,
    #       	     Round(short_percent_of_float, 2) as short_percent_of_float
    #       	     from TickerStockMetrics where ticker="{ticker_name}";
    #       """

    info_sql = f"""
        Select * from TickerStockMetrics where ticker="{ticker_name}";
    """

    ticker_info = conn.execute(info_sql).fetchall()

    headlines_sql = f"""
                SELECT headline, url, publisher FROM 'TickerHeadlines' where ticker='{ticker_name}' group by publisher;
                """
    ticker_headlines = conn.execute(headlines_sql).fetchall()

    conn.close()

    return render_template('ticker-details.html',
                           ticker_name=ticker_name,
                           ticker_info=ticker_info,
                           ticker_headlines=ticker_headlines,
                           ticker_predictions=ticker_preds,
                           stock_price_dict=stock_price_dict)


@app.route('/about', methods=['GET', 'POST'])
def about():
    return render_template("about.html")

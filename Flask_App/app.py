from flask import Flask, render_template, request
import sqlite3
from sqlite3 import Error
import os.path

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
    return render_template('index.html')


@app.route('/data', methods=['POST', 'GET'])
def data():
    if request.method == 'GET':
        return f"The URL '/data' is accessed directly"
    if request.method == 'POST':
        form_data = request.form
        conn = get_db_connection()
        ticker_name = form_data["Searched Ticker"]

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
                               form_data=form_data,
                               ticker_info=ticker_info,
                               ticker_headlines=ticker_headlines,
                               ticker_predictions=ticker_preds)

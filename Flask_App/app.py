from flask import Flask, render_template, request
import sqlite3
from sqlite3 import Error
import os.path

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "database.db")


def get_db_connection():
    conn = None
    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
    except Error as e:
        print(e)

    return conn


def select_all(conn):
    cursor = conn.cursor()
    cursor.execute("Select * from TickerInfo")
    rows = cursor.fetchall()

    for row in rows:
        print(row)


# select_all(get_db_connection())

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
        info_sql = f"""
              Select * from TickerInfo where ticker="{ticker_name}";
              """
        ticker_info = conn.execute(info_sql).fetchall()

        headlines_sql = f"""
                    Select headlines from TickerHeadlines where ticker="{ticker_name}" limit 3
                    """
        ticker_headlines = conn.execute(headlines_sql).fetchall()

        conn.close()

        return render_template('data.html', form_data=form_data,
                               ticker_info=ticker_info, ticker_headlines=ticker_headlines)

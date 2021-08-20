from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/data', methods=['POST', 'GET'])
def data():
    if request.method == 'GET':
        return f"The URL '/data' is accessed directly. Try going to '/form' to submit a form."
    if request.method == 'POST':
        form_data = request.form
        return render_template('data.html', form_data=form_data)

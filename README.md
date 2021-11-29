# Agora

#### Sentiment Analysis Stock Predictor

![Homepage](/Interface/homepage.png?raw=true)

![Ticker Search Page](/Interface/ticker_page.png?raw=true)

## Usage

1. Clone this repository to your local machine.

2. Install requirements with `pip install -r requirements.txt`.

3. Run `flask run` in the Flask_App directory.

4. Go to `http://localhost:5000/` in a web browser.

### Containerized

1. Clone this repository to your local machine.

2. Build the container with `docker build . -t agora`.

3. Run the container with `docker run -p5000:5000 agora`.

4. Go to `http://localhost:5000/` in a web browser.

## Technical Information

This application uses
- Python 3
- Flask web application framework
- Selenium web drivers
- NTLK VADER sentiment analysis model
- yfinance API queries
- Logistic Regression machine learning models
- GitHub actions for workflow automation

## Disclaimer
This application does not offer investment advice. Do not invest what you cannot lose. You should
carry out your own independent research before making any investment decision.

## License

MIT

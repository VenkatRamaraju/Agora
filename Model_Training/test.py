import yfinance as yf

amzn = yf.Ticker("AMZN")

print(amzn.info)

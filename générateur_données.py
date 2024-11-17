import yfinance as yf
import sqlite3


tickers = ["AAPL", "NVDA", "TSLA"]

connexion = sqlite3.connect("stocks.db")
curseur = connexion.cursor()

for ticker in tickers:
    data = yf.download(ticker, period="1y", interval="1d")

    data['Ticker'] = ticker

    data.to_sql(ticker, connexion, if_exists='replace', index=True)
    print("Succès!")

connexion.close()

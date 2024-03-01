import requests
import time
import json

def fetch_trade_history_page(pageNumber, portfolioId, pageSize=10):
    url = "https://www.binance.com/bapi/futures/v1/public/future/copy-trade/lead-portfolio/trade-history"
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "pageNumber": pageNumber,
        "pageSize": pageSize,
        "portfolioId": portfolioId
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    return response.json()

def write_trade_history_to_file(history):
    with open('trade_history.json', 'w') as f:
        json.dump(history, f)

def fetch_trade_history(portfolioId):
    pageNumber = 1
    pageSize = 10
    history = []
    while True:
        data = fetch_trade_history_page(pageNumber, portfolioId, pageSize)
        if (data['data']['list'] == []):
            break
        history += data['data']['list']
        write_trade_history_to_file(history)
        print(data, pageNumber)
        pageNumber += 1
        time.sleep(1)


fetch_trade_history("3865423691884344576")
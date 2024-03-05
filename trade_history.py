import requests
import time
import json
import sys

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

def write_trade_history_to_file(history, portfolioId):
    with open(f'data_trade_history/trade_history_{portfolioId}.json', 'w') as f:
        json.dump(history, f)

def read_trade_history_from_file(portfolioId):
    try:
        with open(f'data_trade_history/trade_history_{portfolioId}.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []
    
def toJsonStr(obj):
    return json.dumps(obj, sort_keys=True)
def fetch_trade_history(portfolioId):
    storedHistory = read_trade_history_from_file(portfolioId)
    storedHistoryStrSet = set(map(lambda x: toJsonStr(x), storedHistory))
    print(storedHistoryStrSet)
    fetchedHistory = []
    pageNumber = 1
    pageSize = 10
    history = []
    while True:
        data = fetch_trade_history_page(pageNumber, portfolioId, pageSize)
        if (data['data']['list'] == []):
            break
        fetchedHistory += data['data']['list']
        crossed = False
        while len(fetchedHistory) > 0 and toJsonStr(fetchedHistory[-1]) in storedHistoryStrSet:
            fetchedHistory.pop()
            crossed = True
        if crossed:
            print("crossed")
            break
        print(pageNumber)
        pageNumber += 1
        
    history = fetchedHistory + storedHistory
    write_trade_history_to_file(history, portfolioId)

# read id from args
# portfolioId = sys.argv[1]
# if portfolioId == '':
#     print("portfolioId is empty")
#     sys.exit(1)
# fetch_trade_history(portfolioId)
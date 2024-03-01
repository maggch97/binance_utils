import requests
import json
import time

def fetch_detail(id):
    url = f"https://www.binance.com/bapi/futures/v1/friendly/future/copy-trade/lead-portfolio/detail?portfolioId={id}"
    response = requests.get(url, timeout=5)
    data = response.json()
    return data

# https://www.binance.com/bapi/futures/v1/public/future/copy-trade/lead-portfolio/performance?portfolioId=3851722353025479937&timeRange=7D
def fetch_7d_performance(id):
    url = f"https://www.binance.com/bapi/futures/v1/public/future/copy-trade/lead-portfolio/performance?portfolioId={id}&timeRange=7D"
    response = requests.get(url, timeout=5)
    data = response.json()
    return data

def fetch_API_trader_list(pageNumber):
    pageSize = 18
    # https://www.binance.com/bapi/futures/v1/friendly/future/copy-trade/home-page/query-list
    # {"pageNumber":1,"pageSize":18,"timeRange":"7D","dataType":"PNL","favoriteOnly":false,"hideFull":true,"nickname":"","order":"DESC","userAsset":0,"apiKeyOnly":true}
    url = "https://www.binance.com/bapi/futures/v1/friendly/future/copy-trade/home-page/query-list"
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "pageNumber": pageNumber,
        "pageSize": pageSize,
        "timeRange": "7D",
        "dataType": "PNL",
        "favoriteOnly": False,
        "hideFull": True,
        "nickname": "",
        "order": "DESC",
        "userAsset": 0,
        "apiKeyOnly": True
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    return response.json()

def check_super_trader(id):
    try:
        detail = fetch_detail(id)
        startTime = int(detail['data']['startTime'])
        performance = fetch_7d_performance(id)
        mdd = performance['data']['mdd']
        roi = performance['data']['roi']
        totalOrder = performance['data']['totalOrder']
        # cal running day
        runningDay = (int(time.time()) - startTime / 1000) / 86400

        if (runningDay > 12):
            # an old trader is not a super trader
            return False
        # TODO check trade history, if all action are same direction, then it is not a super trader

        if (mdd > 15):
            return False
        if (roi < 20):
            return False
        if (totalOrder < 10):
            return False
        return True
    except Exception as e:
        return False

def check_super_trader_list(pageNumber):
    try:
        data = fetch_API_trader_list(pageNumber)
        result = []
        for trader in data['data']['list']:
            roi = trader['roi']
            # print("trader:", trader['nickname'], "roi:", roi, "leadPortfolioId:", trader['leadPortfolioId'])
            if (check_super_trader(trader['leadPortfolioId'])):
                result.append(trader)
                print("Super trader:", trader['nickname'], "leadPortfolioId:", trader['leadPortfolioId'])
        return result
    except Exception as e:
        print(e, "pageNumber:", pageNumber)
        return []


# 100 to 1
for i in range(1,20):
    check_super_trader_list(i)
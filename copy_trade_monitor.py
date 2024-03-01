import requests
import time

# https://www.binance.com/bapi/futures/v1/friendly/future/copy-trade/lead-portfolio/detail?portfolioId=3845446112579238400
def fetch_detail(id):
    url = f"https://www.binance.com/bapi/futures/v1/friendly/future/copy-trade/lead-portfolio/detail?portfolioId={id}"
    response = requests.get(url, timeout=5)
    data = response.json()
    return data

def schedule():
    # 3845446112579238400
    while True:
        try:
            data = fetch_detail(3845446112579238400)
            # currentCopyCount
            if (data['data']['currentCopyCount'] != data['data']['maxCopyCount']):
                print("Copy count is not equal")

                requests.get("https://api.day.app/xxxxxxxx/True-Miracle-can-copy", timeout=5)
                time.sleep(600)
            else:
                print("Copy count is equal time:", time.time() , "currentCopyCount:", data['data']['currentCopyCount'], "maxCopyCount:", data['data']['maxCopyCount'])
        except Exception as e:
            print(e)
        time.sleep(3)

schedule()
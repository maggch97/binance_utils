# https://www.binance.com/bapi/futures/v1/friendly/future/copy-trade/lead-data/positions?portfolioId=3699951837954445568

# {
#     "code": "000000",
#     "message": null,
#     "messageDetail": null,
#     "data": [
#         {
#             "id": "0_SNTUSDT_BOTH",
#             "symbol": "SNTUSDT",
#             "collateral": "USDT",
#             "positionAmount": "0",
#             "entryPrice": "0.0",
#             "unrealizedProfit": "0.00000000",
#             "cumRealized": "0",
#             "askNotional": "0",
#             "bidNotional": "0",
#             "notionalValue": "0",
#             "markPrice": "0.00000000",
#             "leverage": 5,
#             "isolated": false,
#             "isolatedWallet": "0",
#             "adl": 0,
#             "positionSide": "BOTH",
#             "breakEvenPrice": "0.0"
#         },
#         {
#             "id": "0_SNTUSDT_LONG",
#             "symbol": "SNTUSDT",
#             "collateral": "USDT",
#             "positionAmount": "0",
#             "entryPrice": "0.0",
#             "unrealizedProfit": "0.00000000",
#             "cumRealized": "0",
#             "askNotional": "0",
#             "bidNotional": "0",
#             "notionalValue": "0",
#             "markPrice": "0.00000000",
#             "leverage": 5,
#             "isolated": false,
#             "isolatedWallet": "0",
#             "adl": 0,
#             "positionSide": "LONG",
#             "breakEvenPrice": "0.0"
#         },
#         {
#             "id": "0_SNTUSDT_SHORT",
#             "symbol": "SNTUSDT",
#             "collateral": "USDT",
#             "positionAmount": "0",
#             "entryPrice": "0.0",
#             "unrealizedProfit": "0.00000000",
#             "cumRealized": "0",
#             "askNotional": "0",
#             "bidNotional": "0",
#             "notionalValue": "0",
#             "markPrice": "0.00000000",
#             "leverage": 5,
#             "isolated": false,
#             "isolatedWallet": "0",
#             "adl": 0,
#             "positionSide": "SHORT",
#             "breakEvenPrice": "0.0"
#         },
#         {
#             "id": "0_SUSHIUSDT_BOTH",
#             "symbol": "SUSHIUSDT",
#             "collateral": "USDT",
#             "positionAmount": "0",
#             "entryPrice": "0.0",
#             "unrealizedProfit": "0.00000000",
#             "cumRealized": "0",
#             "askNotional": "0",
#             "bidNotional": "0",
#             "notionalValue": "0",
#             "markPrice": "1.56896047",
#             "leverage": 5,
#             "isolated": false,

import requests
import json

def fetch_trader_position(portfolioId):
    url = f"https://www.binance.com/bapi/futures/v1/friendly/future/copy-trade/lead-data/positions?portfolioId={portfolioId}"
    response = requests.get(url, timeout=5)
    data = response.json()
    return data

def calculate_position_total_value(positions):
    total = 0
    for position in positions:
        total += float(position['notionalValue'])
    return total

positions = fetch_trader_position("3699951837954445568")
print(calculate_position_total_value(positions))


Array.from(document.querySelectorAll(".bn-table-row-level-0")).map(r=>r.children[4]?.innerText.split(' USDT')[0]).reduce((partialSum, a) => partialSum + (a? parseInt(a):0), 0);

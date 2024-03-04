import json
import time

portfolioId = "3865423691884344576"
coinCode = "WLDUSDT"

def read_trade_history_from_file():
    with open(f'trade_history_{portfolioId}.json', 'r') as f:
        return json.load(f)
    
def filter_trade_history_by_coin(history, coin):
    coin_history = list(filter(lambda x: x['symbol'] == coin, history))
    # merge all record with same second time and side and positionSide, and calculate the qty and realizedProfit and weighted avg price
    merged = {}
    for item in coin_history:
        key = f"{int(item['time']/1000/60)}_{item['side']}_{item['positionSide']}"

        if key in merged:
            merged[key]['qty'] += item['qty']
            merged[key]['realizedProfit'] += item['realizedProfit']
            merged[key]['price'] = (merged[key]['price'] * merged[key]['qty'] + item['price'] * item['qty']) / (merged[key]['qty'] + item['qty'])
        else:
            merged[key] = item
    return list(merged.values())
def get_all_coins(history):
    # coins with operation times
    coins = {}
    for item in history:
        if item['symbol'] in coins:
            coins[item['symbol']] += 1
        else:
            coins[item['symbol']] = 1
    # pretty print and sort by operation times
    coins = sorted(coins.items(), key=lambda x: x[1], reverse=True)
    return coins

history = read_trade_history_from_file()
print(get_all_coins(history))
filtered = filter_trade_history_by_coin(history, coinCode)

print(f"\033[35m{'时间':<19}\t{'操作':<4}\t{'数量':<4}\t{'价格':<4}\t{'盈亏':<4}\t{'总价':<4}\033[0m")
for item in filtered:
    # cal the  开多/开空/平多/平空  from side and positionSide

    action = ''
    if item['side'] == 'BUY':
        if item['positionSide'] == 'LONG':
            action = '开多'
        elif item['positionSide'] == 'BOTH':
            action = '开多/平空'
        else:
            action = '平空'
    else:
        if item['positionSide'] == 'LONG':
            action = '平多'
        elif item['positionSide'] == 'BOTH':
            action = '开空/平多'
        else:
            action = '开空'
    # YYYY-MM-DD HH:MM:SS
    date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(item['time'] / 1000))

    # print with \t
    # print(date, action, item['qty'], item['price'], item['realizedProfit'], total price)
    # print  '开空' as red color
    # print  '开多' as green color
    # print  '平空' as red color
    # print  '平多' as green color

    # keep 2 decimal
    totalPrice = round(item['price'] * item['qty'], 2)
    item['price'] = round(item['price'], 3)
    item['realizedProfit'] = round(item['realizedProfit'], 2)
    item['qty'] = round(item['qty'], 2)

    if action == '开空' or (action == '开空/平多' and item['realizedProfit'] == 0):
        action = '开空'
        print(f"\033[31m{date}\t{action}\t{item['qty']}\t{item['price']}\t{item['realizedProfit']}\t{totalPrice}\033[0m")
    elif action == '平空' or (action == '开多/平空' and item['realizedProfit'] != 0):
        action = '平空'
        print(f"\033[33m{date}\t{action}\t{item['qty']}\t{item['price']}\t{item['realizedProfit']}\t{totalPrice}\033[0m")
    elif action == '开多' or (action == '开多/平空' and item['realizedProfit'] == 0):
        action = '开多'
        print(f"\033[32m{date}\t{action}\t{item['qty']}\t{item['price']}\t{item['realizedProfit']}\t{totalPrice}\033[0m")
    else:
        action = '平多'
        print(f"\033[30m{date}\t{action}\t{item['qty']}\t{item['price']}\t{item['realizedProfit']}\t{totalPrice}\033[0m")
import json
import time

portfolioId = "3761161442588992512"
coinCode = "ARBUSDT"

def read_trade_history_from_file(portfolioId):
    with open(f'./data_trade_history/trade_history_{portfolioId}.json', 'r') as f:
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
    # to list and sort by time
    sorted_coin_history = sorted(list(merged.values()), key=lambda x: x['time'])
    return sorted_coin_history

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

def cal_coin_switch_order_count(history, coin):
    filtered = filter_trade_history_by_coin(history, coin)
    switchList = []
    i = 0
    while i < len(filtered):
        if filtered[i]['realizedProfit'] == 0:
            j = i
            while j < len(filtered) and filtered[j]['realizedProfit'] == 0:
                j += 1
            switchList.append(j-i)
            i = j+1
        else:
            i += 1
    return switchList


def cal_score(profileId):
    history = read_trade_history_from_file(profileId)
    coinCodes = get_all_coins(history)

    swtichList = []
    for coinCode in coinCodes:
        swtichList += cal_coin_switch_order_count(history, coinCode[0])
    avgScore = sum(swtichList) / len(swtichList)
    maxScore = max(swtichList)
    # id  score
    print(f"{profileId} {avgScore} {maxScore} {len(history)}")
    # return id score
    return profileId, avgScore, maxScore, len(history)

# list all files /data_trade_history/trade_history_{portfolioId}.json and extract portfolioIds
# for each portfolioId, call cal_score
# code start 
import os
rank = []
for filename in os.listdir('./data_trade_history'):
    if filename.startswith('trade_history_'):
        profileId = filename.split('_')[2].split('.')[0]
        score = cal_score(profileId)
        rank.append(score)
# sort by avg
rank = sorted(rank, key=lambda x: x[1], reverse=True)
# filter len(history) < 500
rank = list(filter(lambda x: x[3] > 1500, rank))
# print rank 1 by 1
for r in rank:
    print(r)
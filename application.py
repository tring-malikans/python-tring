import os
# import asyncio
from binance.client import Client
from binance.websockets import BinanceSocketManager
# from twisted.internet import reactor
import pymongo
import time
# from multiprocessing import Pool
# import multiprocessing
import threading
import io
import datetime
from flask import Flask , render_template
from flask_socketio import SocketIO
application =  Flask(__name__)
async_mode=None
socket_=SocketIO(application,async_mode=async_mode)



mongo1=pymongo.MongoClient('mongodb+srv://sufiyan:sufiyan1@tring1.vef4g.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')


db = mongo1['test-database']
# # coins=["BTC","SUSHI","DOGE",'ADA','EOS','XRP','VET','TRX','LINK','THETA']
# coins=["BTC","XRP","DOGE",'ADA','THETA','']

coins=["BTC","XRP","DOGE"]
pairs=["BUSD"]





client = Client("gyHLoFuT1VKWwtWM8djg7lshfeHGkiADh6lkPsma0HBHIYAhqqZe2grzK7ZIywT0", "AUZge7ylUu48BSTONuEv8zOsWcFiHOX6hli2pHMWVQI3BHSyAii9hBiLzHzUApr3")
bm = BinanceSocketManager(client)
bm.start()


def process_messageC(msg):
    information=db["coins"]
    Event_type=msg['e']
    s = msg['E'] / 1000
    year=datetime.datetime.fromtimestamp(s).strftime('%Y')[-2:]
    Event_time=datetime.datetime.fromtimestamp(s).strftime(f'%a %m-%d-{year} %H:%M:%S.%f')[:-3]
    Event_times=msg['E']
    Symbol=msg['s']
    Aggregate_trade_ID=msg['a']
    Price=msg['p']
    Quantity=msg['q']
    if msg['m']:
        tradeType="Sell"
    else:
        tradeType="Buy"
    scrape_data=str(Event_type)+','+str(Event_time)+','+str(Event_times)+','+str(Symbol)+','+str(Aggregate_trade_ID)+','+str(Price)+','+str(Quantity)+','+str(tradeType)
    # with io.open('coins.csv','a',encoding="utf8") as f2:
    #     f2.write(scrape_data+'\n')
    #     f2.close()
    record={
        "Event_type":Event_type,
        "Event_time":Event_time,
        "Event_times":Event_times,
        "Symbol":Symbol,
        "Aggregate_trade_ID":Aggregate_trade_ID,
        "Price":Price,
        "Quantity":Quantity,
        "tradeType":tradeType
    }
    information.insert_one(record)

def process_messageT(msg):
    information=db["trades"]
    print("message type: {}".format(msg['e']))
    Event_type=msg['e']
    s = msg['E'] / 1000
    Event_time=datetime.datetime.fromtimestamp(s).strftime('%a %b %d %Y %H:%M:%S:%MS')
    Symbol=msg['s']
    Trade_ID=msg['a']
    Price=msg['p']
    Quantity=msg['q']
    scrape_data=str(Event_type)+','+str(Event_time)+','+str(Symbol)+','+str(Trade_ID)+','+str(Price)+','+str(Quantity)
    # with io.open('trades.csv','a',encoding="utf8") as f2:
    #     f2.write(scrape_data+'\n')
    #     f2.close()
    record={
        "Event_type":Event_type,
        "Event_time":Event_time,
        "Symbol":Symbol,
        "Trade_ID":Trade_ID,
        "Price":Price,
        "Quantity":Quantity
    }
    information.insert_one(record)
def process_messageO(msg):
    information=db["orders"]
    print("message type: {}".format(msg['u']))
    updateId=msg['u']
    Symbol=msg['s']
    Bids=msg['b']
    Bids_quan=msg['B']
    Asks=msg['a']
    Asks_quan1=msg['A']
    scrape_data=str(updateId)+','+str(Symbol)+','+str(Bids)+','+str(Bids_quan)+','+str(Asks)+','+str(Asks_quan1)
    # with io.open('orders.csv','a',encoding="utf8") as f2:
    #     f2.write(scrape_data+'\n')
    #     f2.close()
    record={
        "Event_type":Event_type,
        "Event_time":Event_time,
        "Symbol":Symbol,
        "Trade_ID":Trade_ID,
        "Price":Price,
        "Quantity":Quantity
    }
    information.insert_one(record)
def start_extract_coins(coin):   
    print(coin,'xx') 
    # conn_key = bm.start_multiplex_socket(['bnbbtc@aggTrade', 'neobtc@ticker'], process_m_message)
    # time.sleep(1)
    trades = bm.start_trade_socket(coin, process_messageT)
    prices= bm.start_aggtrade_socket(coin, process_messageC)
    

process=[]
# print(bm)
# import requests\
def main():
    # for proxie in proxies:
    print("222")
    for coin in coins:
        for pair in pairs:
            # proxy={
            #     "https":f"{proxie}",
            #     "http":f"{proxie}"
            # }
            # print(proxy)
            # client = Client("gyHLoFuT1VKWwtWM8djg7lshfeHGkiADh6lkPsma0HBHIYAhqqZe2grzK7ZIywT0", "AUZge7ylUu48BSTONuEv8zOsWcFiHOX6hli2pHMWVQI3BHSyAii9hBiLzHzUApr3",{"proxies":proxy})
            
            newCoin=coin+pair
            # new1=newCoin.lower()+'@aggTrade'
            # start_extract_coins(1,newCoin)
            # response=requests.get('https://httpbin.org/ip', proxies=proxy)
            # print(response)
            # print(new1)
            # streams=[new1]
            # print(streams)
            # p=threading.Thread(target=bm.start_multiplex_socket,args=[streams,process_messageC])
            # p=multiprocessing.Process(target=bm.start_multiplex_socket,args=[streams,process_messageC])
            # print(newCoin)
            # coins1=[newCoin]
            # pool=multiprocessing.Pool()
            # p=pool.map(start_extract_coins(newCoin),coins,5)
            # p=pool.map(bm.start_multiplex_socket(streams,process_messageC),pairs)
            process.append(newCoin)

@application.route('/')
def hello():
    # application.run(host='0.0.0.0', port=81)
    
    return render_template('index.html',sync_mode=socket_.async_mode)
    # return 'Sup'

if __name__ == '__main__':
    application.run(host="0.0.0.0",port=8080)
    # application.run(debug=true)
    main()
    print("1")
    threads = [ threading.Thread(target = start_extract_coins, args=(p,)) for p in process ]
    [ t.start() for t in threads ]
    [ t.join() for t in threads ]
    print("yes")














# # headers='Event_type'+','+'Event_time'+','+'Symbol'+','+'Trade_ID'+','+'Price'+','+'Quantity'
# # with io.open('trades.csv','w',encoding="utf8") as f2:
# #     f2.write(headers+'\n')
# #     f2.close()

# # headers2='updateId'+','+'Symbol'+','+'Bids'+'bid quantity'+','+'Asks'+','+'Asks quan'
# # with io.open('orders.csv','w',encoding="utf8") as f2:
# #     f2.write(headers2+'\n')
# #     f2.close()

# # headers3='Event_type'+','+'Event_time'+','+'Event_times'+','+'Symbol'+','+'Aggregate_trade_ID'+','+'Price'+','+'Quantity'+','+'TradeType'
# # with io.open('coins.csv','w',encoding="utf8") as f2:
# #     f2.write(headers3+'\n')
# #     f2.close()

# def process_message(msg):
#     # information=db["coins"]
#     print("message type: {}".format(msg['e']))
#     print(msg)


# # conn_key = bm.start_aggtrade_socket('BNBBTC', process_message)




# proxies=[
#     # 'http://movais:QA3arTsD@23.106.192.79:29842',
#     # 'http://movais:QA3arTsD@45.147.63.31:29842',
#     # 'http://movais:QA3arTsD@23.106.192.189:29842',
#     # 'http://movais:QA3arTsD@45.147.63.94:29842',
#     'http://movais:QA3arTsD@23.106.192.64:29842'
# ]
# # if __name__=="__main__":
# #     # print(process)
#     # return 'Sup'
# # if __name__=="__main__":
    
#     # with Pool(len(process)) as pool:
#     #     # for p in process:
#     #     pool.map(start_extract_coins, process)


# # for p in process:
# #     p.start()

# # with Pool(processes=len(process)) as pool:
# #     result = pool.map(p)
# # for p in process:
# #     p.join()     

# #     print('1')
# # def process_messageT(msg):
# #     print("message type: {}".format(msg['e']))
# #     print(msg)
# #     informationT.insert_one(msg)
# #     # do something

#     # informationO.insert_one(msg)

# # # conn_key = bm.start_aggtrade_socket('BNBBTC', handle_message)
# # conn_key = bm.start_aggtrade_socket('BNBBTC', process_messageT)
# # conn_key = bm.start_depth_socket('BNBBTC', process_messageD)

# # # # then start the socket manager


# # # # let some data flow..
# # time.sleep(10)

# # # stop the socket manager
# # bm.stop_socket(conn_key)
















# # place a test market buy order, to place an actual order use the create_order˓→function

# # order=client.create_test_order(
# #     symbol='BNBBTC',
# #     side=Client.SIDE_BUY,
# #     type=Client.ORDER_TYPE_MARKET,
# #     quantity=100
# # )


# # get all symbol prices
# # prices = client.get_all_tickers()

# # print(prices)
# # print(client.get_account())

# # get Balance
# # print(client.get_asset_balance(asset='DOGE'))

# # get balances for futures account
# # print(client.futures_account_balance())


# # get balances for margin account
# # print(client.get_margin_account())


# # get latest price from Binance API
# # btc_price = client.get_symbol_ticker(symbol="BTCUSDT") 
# # print full output (dictionary)
# # print(btc_price)
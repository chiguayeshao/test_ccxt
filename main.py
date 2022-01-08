import ccxt
import pandas as pd

from configparser import ConfigParser

#从配置文件中读取私人api
cp = ConfigParser()
cp.read('user.conf')
section = cp.sections()[0]
apiKey = cp.get(section, "apiKey")
secret = cp.get(section, "secret")

def main():
    #exchanges

    #获取所有的交易所id
    exchange_list = ccxt.exchanges
    # print(exchange_list)

    #初始化交易所
    binance_exchange = ccxt.binance({
        'apiKey': apiKey,
        'secret': secret,
        'timeout': 15000,
        'enableRateLimit': True
    })

    #交易所结构数据
    # print('交易所id', binance_exchange.id)
    # print('交易所名称', binance_exchange.name)
    # print('是否支持共有api', binance_exchange.has['publicAPI'])
    # print('是否支持私有api', binance_exchange.has['privateAPI'])
    # print('支持的时间频率', binance_exchange.timeframes)
    # print('最长等待时间s', binance_exchange.timeout / 1000)
    # print('访问频率s', binance_exchange.rateLimit / 1000)
    # print('交易所当前时间', binance_exchange.iso8601(binance_exchange.milliseconds()))


    #markets
    #加载市场数据
    binance_markets = binance_exchange.load_markets()
    # print(binance_market.keys())

    #根据key获取指定交易对市场信息
    symbol = 'BTC/USDT'
    btc_usdt_market = binance_markets[symbol]
    # print(btc_usdt_market)


    #获取单个交易对ticker数据
    ticker_data = binance_exchange.fetch_ticker(symbol)
    # print(ticker_data)
    #获取多个交易对ticker数据
    ticker_datas = binance_exchange.fetch_tickers(['BTC/USDT', 'ETH/USDT'])
    # print(ticker_datas)

    #获取交易委托账本
    order_book = binance_exchange.fetch_order_book(symbol)
    # print(order_book)

    #计算委托账本价差，得出市场流动性
    #最高买价
    bid = order_book['bids'][0][0] if len(order_book['bids']) > 0 else None
    #最低卖价
    ask = order_book['asks'][0][0] if len(order_book['asks']) > 0 else None
    #价差
    spread = (ask-bid) if (bid and ask) else None
    #市场行情
    # print('买价:{:.4f}, 卖价:{:.4f}, 价差:{:.4f}'.format(bid,ask,spread))


    #k线数据的获取
    k_line = binance_exchange.fetch_ohlcv(symbol, '1m')
    kline_data = pd.DataFrame(k_line)
    kline_data.columns = ['Datetime', 'Open', 'High', 'Low', 'Close', 'Vol']
    kline_data['Datetime'] = kline_data['Datetime'].apply(binance_exchange.iso8601)
    # print(kline_data.head())


    #交易

    #查询账户余额
    # binance_exchange.fetch_balance()

    # print('DOGE一共：',binance_exchange.fetch_balance()['total']['DOGE'])
    # print('DOGE可用：',binance_exchange.fetch_balance()['free']['DOGE'])
    # print('DOGE冻结：',binance_exchange.fetch_balance()['used']['DOGE'])
    #
    #
    # print('USDT一共：',binance_exchange.fetch_balance()['total']['USDT'])
    # print('USDT可用：',binance_exchange.fetch_balance()['free']['USDT'])
    # print('USDT冻结：',binance_exchange.fetch_balance()['used']['USDT'])

    #创建买单
    # 创建一个现价单，用1usdt买入1btc
    # binance_exchange.create_order(symbol = 'BTC/USDT', side='buy', type='limit', price=1, amount=1)

    #查询订单
    open_orders = binance_exchange.fetch_open_orders('BTC/USDT')
    # print(open_orders)

    #取消订单
    #获取订单id
    # open_order_id = open_orders[0]['info']['orderId']
    # binance_exchange.cancel_order(open_order_id)

    #获取交易完的order
    closed_orders = binance_exchange.fetch_closed_orders('BTC/USDT')
    print(closed_orders)

if __name__ == '__main__':
    main()
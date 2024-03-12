# import ssi_fc_trading
from ssi_fc_data import fc_md_client, model
from datetime import datetime
import config


client = fc_md_client.MarketDataClient(config)
timenow = datetime.today().date().strftime("%d/%m/%Y")

def md_access_token():
    print(client.access_token(model.accessToken(
        config.consumerID, config.consumerSecret)))


def md_get_securities_list():
    req = model.securities('Der', 1, 10)
    print(client.securities(config, req))


def md_get_securities_details():
    req = model.securities_details('Hose', 'hvn', 1, 10)
    print(client.securities_details(config, req))


def md_get_index_components():
    print(client.index_components(config, model.index_components('vn30', 1, 30)))


def md_get_index_list():
    print(client.index_list(config, model.index_list('hose', 1, 10)))


def md_get_daily_OHLC():
    print(client.daily_ohlc(config, model.daily_ohlc(
        'ssi', '01/03/2024', '01/03/2024', 1, 10, True)))


def md_get_intraday_OHLC():
    print(client.intraday_ohlc(config, model.intraday_ohlc(
        'fpt', '01/03/2024', '01/03/2024', 1, 10, True, 1)))


def md_get_daily_index():
    print(client.daily_index(config, model.daily_index(
        '123', 'VN100', '01/03/2024', '01/03/2024', 1, 100, '', '')))


def md_get_stock_price():
    # print(client.daily_stock_price(config, model.daily_stock_price(
    #     'ssi', '28/02/2024', '01/03/2024', 1, 10, 'hose')))
    data = client.daily_stock_price(config, model.daily_stock_price(
        'ssi', timenow, timenow, 1, 10, 'hose'))
    for i in range(len(data["data"])):
        if data["data"][i]["Symbol"] == "SSI":
            print(data["data"][i])


def main():

    while True:
        print('11  - Securities List')
        print('12  - Securities Details')
        print('13  - Index Components')
        print('14  - Index List')
        print('15  - Daily OHLC')
        print('16  - Intraday OHLC')
        print('17  - Daily index')
        print('18  - Stock price')
        value = input('Enter your choice: ')

        if value == '11':
            md_get_securities_list()
        elif value == '12':
            md_get_securities_details()
        elif value == '13':
            md_get_index_components()
        elif value == '14':
            md_get_index_list()
        elif value == '15':
            md_get_daily_OHLC()
        elif value == '16':
            md_get_intraday_OHLC()
        elif value == '17':
            md_get_daily_index()
        elif value == '18':
            md_get_stock_price()


if __name__ == '__main__':
    main()

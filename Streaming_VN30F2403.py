# import ssi_fc_data
import re
import config
import json
import platform
from datetime import datetime, time
from ssi_fc_data.fc_md_stream import MarketDataStream
from ssi_fc_data.fc_md_client import MarketDataClient
from inputimeout import inputimeout

# Example Data
# {'DataType': 'B', 'Content': '{"RType":"B","TradingDate":"04/03/2024","Time":"10:51:24",
# "Symbol":"VN30F2403","Open":1265.6,"High":1265.6,"Low":1265.6,"Close":1265.6,"Volume":9.0,"Value":0.0}'}

# get time exit


def _isReady():
    year = datetime.now().year
    month = datetime.now().month
    day = datetime.now().day
    atTime = datetime.now()
    timeRelax = datetime(year, month, day, 12, 0, 0, 0)
    if atTime < timeRelax:
        timeExit = datetime(year, month, day, 11, 31, 0, 0)
    else:
        timeExit = datetime(year, month, day, 14, 47, 0, 0)
    diffTime = (timeExit - atTime).total_seconds()
    if diffTime < 0:
        return False
    else:
        return diffTime

# get name data


def name_json():
    name_data = "DataVN30F2403_" + datetime.now().strftime("%d-%m-%H-%M-%S")
    type_data = ".json"
    if platform.system() == 'Windows':
        path_data = 'Data\Auto Data\VN30F2403\\'
    else:
        path_data = 'Data/Auto Data/VN30F2403/'
    path = path_data + name_data + type_data
    return path

# get market data message


def get_market_data(lst, message):
    result_dict = json.loads(message)
    lst_pop = ['High', 'Low', 'Close', 'Value']
    for x in lst_pop:
        result_dict.pop(x)
    print("Open: {}, Volume: {}, Time: {}".format(
        result_dict["Open"], result_dict["Volume"], result_dict["Time"]))
    lst.append(result_dict)


# get error
def getError(error):
    print(error)


# main function

def main():
    result_lst = []
    # selected_channel = input("Please select channel: ")
    selected_channel = "B:VN30F2403"
    mm = MarketDataStream(result_lst, config, MarketDataClient(config))
    mm.start(get_market_data, getError, selected_channel)
    message = None
    workTime = _isReady()
    while workTime != False and message != 'exit':
        print("Time for crawling: ", workTime)
        try:
            message = inputimeout(
                prompt=">> type 'exit' or choose different channel:\n", timeout=workTime)
        except:
            message = 'exit'
        if message is not None and message != "" and message != "exit":
            mm.swith_channel(message)
        workTime = _isReady()
    path = name_json()
    with open(path, 'w', encoding='utf8') as json_file:
        json.dump(result_lst, json_file, indent=4)


main()

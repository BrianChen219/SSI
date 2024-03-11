# import ssi_fc_data
import re
import config
import json
import platform
from time import sleep
from threading import Timer
from datetime import datetime
from ssi_fc_data.fc_md_stream import MarketDataStream
from ssi_fc_data.fc_md_client import MarketDataClient
from inputimeout import inputimeout

# Example Data
# {"IndexId":"VN30","IndexValue":1268.94,"PriorIndexValue":1267.07,"TradingDate":"04/03/2024",
# "Time":"13:18:15","TotalTrade":0.0,"TotalQtty":150536100.0,"TotalValue":4895659000000.0,
# "IndexName":"VN30","Advances":18,"NoChanges":1,"Declines":11,"Ceilings":0,"Floors":0,"Change":1.87,
# "RatioChange":0.15,"TotalQttyPt":25445037.0,"TotalValuePt":728271000000.0,"Exchange":"HOSE",
# "AllQty":175981137.0,"AllValue":5623930000000.0,"IndexType":"","TradingSession":"LO","MarketId":null,
# "RType":"MI","TotalQttyOd":0.0,"TotalValueOd":0.0}


# get time exit


def _isReady():
    year = datetime.now().year
    month = datetime.now().month
    day = datetime.now().day
    atTime = datetime.now()
    beginTime = datetime(year, month, day, 9, 25, 0, 0)
    beginBreak = datetime(year, month, day, 11, 32, 0, 0)
    endBreak = datetime(year, month, day, 12, 58, 0, 0)
    endTime = datetime(year, month, day, 14, 47, 0, 0)
    if atTime < beginTime:
        relaxTime = (beginTime - atTime).total_seconds()
        workTime = (beginBreak - beginTime).total_seconds()
        return (relaxTime, workTime)
    elif atTime < beginBreak:
        relaxTime = 0
        workTime = (beginBreak - atTime).total_seconds()
        return (relaxTime, workTime)
    elif atTime >= beginBreak and atTime <= endBreak:
        relaxTime = (endBreak - atTime).total_seconds()
        workTime = 0
        return (relaxTime, workTime)
    elif atTime > endBreak and atTime < endTime:
        relaxTime = 0
        workTime = (endTime - atTime).total_seconds()
        return (relaxTime, workTime)
    else:
        return (False, False)

# get name data


def name_json():
    name_data = "DataVN30_" + datetime.now().strftime("%d-%m-%H-%M-%S")
    type_data = ".json"
    if platform.system() == 'Windows':
        path_data = 'Data\Auto Data\VN30\\'
    else:
        path_data = 'Data/Auto Data/VN30/'
    path = path_data + name_data + type_data
    return path

# get market data message


def get_market_data(lst, message):
    result_dict = json.loads(message)
    print('Change: {}, Time: {}'.format(
        result_dict['Change'], result_dict['Time']))
    lst.append(result_dict)

# get error


def getError(error):
    print(error)


# main function

def main():
    result_lst = []
    # selected_channel = input("Please select channel: ")
    selected_channel = "MI:VN30"
    mm = MarketDataStream(result_lst, config, MarketDataClient(config))
    mm.start(get_market_data, getError, selected_channel)
    message = None
    (relaxTime, workTime) = _isReady()
    
    while (relaxTime or workTime) and message != 'exit':
        print("Time for relax: ", relaxTime)
        print("Time for crawling: ", workTime)
        sleep(relaxTime)
        try:
            message = inputimeout(
                prompt=">> type 'exit' or choose different channel:\n", timeout=workTime)
        except:
            message = 'exit'
        if message is not None and message != "" and message != "exit":
            mm.swith_channel(message)

    path = name_json()
    with open(path, 'w', encoding='utf8') as json_file:
        json.dump(result_lst, json_file, indent=4)


main()
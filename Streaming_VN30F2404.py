import config
import json
import platform
from time import sleep
from datetime import datetime
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
    beginTime = datetime(year, month, day, 8, 59, 50, 0)
    beginBreak = datetime(year, month, day, 11, 30, 20, 0)
    endBreak = datetime(year, month, day, 12, 59, 50, 0)
    endTime = datetime(year, month, day, 14, 45, 5, 0)
    if atTime < beginTime:
        relaxTime = (beginTime - atTime).total_seconds()
        workTime = 0
    elif atTime < beginBreak:
        relaxTime = 0
        workTime = (beginBreak - atTime).total_seconds()
    elif atTime >= beginBreak and atTime <= endBreak:
        relaxTime = (endBreak - atTime).total_seconds()
        workTime = 0
    elif atTime > endBreak and atTime < endTime:
        relaxTime = 0
        workTime = (endTime - atTime).total_seconds()
    else:
        return (False, False)
    return (relaxTime, workTime)

# get name data


def name_json():
    name_data = "DataVN30F2404_" + datetime.now().strftime("%d-%m-%H-%M-%S")
    type_data = ".json"
    if platform.system() == 'Windows':
        path_data = 'L:\OneDrive\Learning Process\Project\Data\\vn30f2404\\'
    else:
        path_data = '/Users/baobao/Library/CloudStorage/OneDrive-Personal/Learning Process/Project/Data/vn30f2404/'
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
    # selected_channel = input("Please select channel: ")
    selected_channel = "B:VN30F2404"
    message = None
    (relaxTime, workTime) = _isReady()
    while (relaxTime or workTime) and message != 'exit':
        message = None
        result_lst = []
        if relaxTime > 0:
            print("Time for relax: ", relaxTime)
            sleep(relaxTime)
        (relaxTime, workTime) = _isReady()
        if workTime > 0:
            mm = MarketDataStream(result_lst, config, MarketDataClient(config))
            mm.start(get_market_data, getError, selected_channel)
        # Check work time, if work time is False so exit
        # Clients could exit by message
        while workTime and message != 'timeout' and message != 'exit':
            print("Time for crawling: ", workTime)
            try:
                message = inputimeout(
                    prompt=">> Type 'exit' or choose different channel:\n", timeout=workTime)
            except:
                message = 'timeout'
            if message is not None and message != "" and message != "exit":
                mm.swith_channel(message)
            (relaxTime, workTime) = _isReady()
        # Store data into json file
        if len(result_lst) != 0:
            result_lst.pop(0)
            path = name_json()
            with open(path, 'w', encoding='utf8') as json_file:
                json.dump(result_lst, json_file, indent=4)


main()

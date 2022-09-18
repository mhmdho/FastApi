from typing import Union
from fastapi import FastAPI

from utils import binanceDataTime
from arctic import Arctic
import calendar
import time


# Connect to Local MONGODB
store = Arctic('localhost')

app = FastAPI()


@app.get("/{symbol}/{interval}/{startTime}")
def read_data(symbol: str, interval: str, startTime: str, endTime: Union[str, None] = None):
    data = binanceDataTime(symbol, interval, '2010-01-01-01:00').get_data()

    start = calendar.timegm(time.strptime(startTime, '%Y-%m-%d-%H:%M'))*1000
    if endTime == None:
        end = time.time()*1000
    else:
        end = calendar.timegm(time.strptime(endTime, '%Y-%m-%d-%H:%M'))*1000

    store.initialize_library(symbol)
    library = store[symbol]
    library.write(interval, data, prune_previous_version=True)
    lib_data = library.read(interval).data

    return [obj for obj in lib_data if(obj['openTime'] >= start and obj['openTime'] <= end)]

import binance
import time
import math
import calendar
from arctic import Arctic


class binanceDataTime:
    """
    Get every symbol crypto data in binance from start time to end time.
    Interval, symbol and start time are necessary, but end time is optional.
    """
    def __init__(self, symbol, interval, startTime, endTime=None):
        self.symbol = symbol
        self.interval = interval
        self.startTime = startTime
        self.endTime = endTime    
        self.dataBatch = 0

    @property
    def lastprice(self):
        return binance.prices()[self.symbol]

    @property
    def time_to_epotch(self):
        startTimeEpoch = calendar.timegm(time.strptime(self.startTime, '%Y-%m-%d-%H:%M'))
        if self.endTime == None:
            endTimeEpoch = int(time.time())
        else:
            endTimeEpoch = calendar.timegm(time.strptime(self.endTime, '%Y-%m-%d-%H:%M'))
        numCandles = (endTimeEpoch - startTimeEpoch) / (self.get_interval() * 60)
        self.dataBatch = math.ceil(numCandles/1000)
        return startTimeEpoch*1000, endTimeEpoch*1000
        
    def get_interval(self):
        interval = {'5m': 5, '15m': 15, '1h': 60, '2h': 120, '4h': 240, '12h': 720, '1d': 1440, '1w': 10080, '1M': 43800}
        return interval[self.interval]

    def get_data(self):
        data = binance.klines(self.symbol, self.interval, startTime=self.time_to_epotch[0], endTime=self.time_to_epotch[1], limit=1000)
        for i in range(1, self.dataBatch):
            startTime = self.time_to_epotch[0] + (i*1000*self.get_interval()*60*1000)
            data = data + binance.klines(self.symbol, self.interval, startTime=startTime, endTime=self.time_to_epotch[1], limit=1000)
        return data


# Connect to Local MONGODB
store = Arctic('localhost')

def ArcTicDB(symbol, interval, startTime, endTime=None):
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

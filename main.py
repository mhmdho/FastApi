from typing import Union
from fastapi import FastAPI

from utils import binanceDataTime
from arctic import Arctic


# Connect to Local MONGODB
store = Arctic('localhost')

app = FastAPI()


@app.get("/{symbol}/{interval}/{startTime}")
def read_data(symbol: str, interval: str, startTime: str, endTime: Union[str, None] = None):
    data = binanceDataTime(symbol, interval, startTime, endTime).get_data()
    
    store.initialize_library(symbol)
    library = store[symbol]
    library.write(interval, data, prune_previous_version=True)

    print('------all lib----',library.list_symbols())
    return library.read(interval).data


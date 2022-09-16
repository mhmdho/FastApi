from typing import Union
from fastapi import FastAPI

from utils import binanceDataTime


app = FastAPI()


@app.get("/{symbol}/{interval}/{startTime}")
def read_data(symbol: str, interval: str, startTime: str, endTime: Union[str, None] = None):
    data = binanceDataTime(symbol, interval, startTime, endTime).get_data()
    return data

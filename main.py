from typing import Union
from fastapi import FastAPI

from utils import ArcTicDB


app = FastAPI()


@app.get("/{symbol}/{interval}/{startTime}")
def read_data(symbol: str, interval: str, startTime: str, endTime: Union[str, None] = None):
    return ArcTicDB(symbol, interval, startTime, endTime)

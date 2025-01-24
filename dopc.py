# curl http://localhost:8000/api/v1/delivery-order-price?venue_slug=home-assignment-venue-helsinki&cart_value=1000&user_lat=60.17094&user_lon=24.93087

import uvicorn
import requests
import json
import sys
from fastapi import FastAPI, Query, HTTPException
import logging

# CUSTOM MODULES
from data import Data

# GLOBALS
app = FastAPI()
data: Data

logging.basicConfig(
    level=1,
    handlers=[
        logging.FileHandler("logger"),
        logging.StreamHandler()
    ]
)

def fetchDynamicData():
    pass

class ServerState:
    def __init__(self):
        self.status_code = 200
        self.error: Optional[str] = None
    def update(self, _status_code, _error):
        self.status_code = _status_code
        self.error = _error

def main():
    logging.info("app started")
    server_state = ServerState()
    try:
        data = Data()
    except Exception as e:
        server_state.update(503, "Service unavailable, failure to retrieve venue data")
    print(data)
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    main()

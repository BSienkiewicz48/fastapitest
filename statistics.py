from fastapi import Query
from fastapi.responses import JSONResponse
from fastapi import FastAPI, Query, Response, HTTPException
import yfinance as yf
import matplotlib.pyplot as plt
import io

app = FastAPI()

@app.get("/stats")
def get_stock_stats(ticker: str = Query(...)):
    try:
        data = yf.download(ticker, period='3y')
        if data.empty:
            raise HTTPException(status_code=404, detail="Brak danych dla tego tickera")
        current_price = data["Close"][-1]
        return JSONResponse({
            "min": float(data["Close"].min()),
            "max": float(data["Close"].max()),
            "current": float(current_price)
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

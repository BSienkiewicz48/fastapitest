from fastapi import FastAPI, Query, HTTPException
from fastapi.responses import JSONResponse
import yfinance as yf
import pandas as pd
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()



app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # lub podaj konkretną domenę np. ["https://mojastrona.pl"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/stats")
def get_stock_stats(ticker: str = Query(...)):
    try:
        data = yf.download(ticker, period='3y')

        if data.empty or "Close" not in data:
            raise HTTPException(status_code=404, detail="Brak danych dla tego tickera")

        close = data["Close"].dropna()

        if close.empty:
            raise HTTPException(status_code=404, detail="Brak danych cen zamknięcia")

        current_price = close.iloc[-1]
        return JSONResponse({
            "min": float(close.min()),
            "max": float(close.max()),
            "current": float(current_price)
        })

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Błąd wewnętrzny: {str(e)}")

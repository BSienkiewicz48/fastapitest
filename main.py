from fastapi import FastAPI, Query, Response, HTTPException
import yfinance as yf
import matplotlib.pyplot as plt
import io

app = FastAPI()

@app.get("/stock")
def get_stock_chart(ticker: str = Query(..., description="Ticker giełdowy, np. AAPL")):
    try:
        # Pobierz dane
        data = yf.download(ticker, period='1y')
        if data.empty:
            raise HTTPException(status_code=404, detail="Brak danych dla podanego tickera")

        # Tworzenie wykresu
        plt.figure(figsize=(10, 5))
        plt.plot(data['Close'], label='Cena zamknięcia')
        plt.title(f'Cena zamknięcia {ticker.upper()} (ostatni rok)')
        plt.xlabel('Data')
        plt.ylabel('Cena (USD)')
        plt.legend()
        plt.grid(True)

        # Zapis wykresu do bufora jako PNG
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        plt.close()
        buf.seek(0)

        return Response(content=buf.read(), media_type="image/png")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

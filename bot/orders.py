from fastapi import FastAPI, HTTPException

from .validators import OrderRequest
from .client import BinanceFuturesClient
from .logging_config import logger

app = FastAPI(title="Trading Bot API", description="Internal API for Binance Futures Trading Bot")

binance_client = BinanceFuturesClient()

@app.post("/api/v1/order")
def create_order(request: OrderRequest):
    logger.info(f"Received order request: {request.dict()}")
    try:
        req_dict = request.dict() if hasattr(request, "dict") else request.model_dump()
        
        result = binance_client.place_order(
            symbol=req_dict['symbol'],
            side=req_dict['side'],
            order_type=req_dict['order_type'],
            quantity=req_dict['quantity'],
            price=req_dict.get('price')
        )
        logger.info(f"Order successfully placed: {result.get('orderId')}")
        return result

    except RuntimeError as api_err:
        logger.error(f"Binance API request failed: {str(api_err)}")
        raise HTTPException(status_code=400, detail=str(api_err))
    except Exception as e:
        logger.exception("Unexpected error placing order.")
        raise HTTPException(status_code=500, detail=str(e))

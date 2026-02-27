from pydantic import BaseModel, Field, root_validator
from typing import Optional, Literal

class OrderRequest(BaseModel):
    symbol: str = Field(..., description="Trading pair symbol, e.g. BTCUSDT", min_length=1)
    side: Literal["BUY", "SELL"] = Field(..., description="Trade side")
    order_type: Literal["MARKET", "LIMIT"] = Field(..., description="Order type")
    quantity: float = Field(..., description="Order quantity", gt=0)
    price: Optional[float] = Field(None, description="Order price, required if LIMIT", gt=0)

    @root_validator(pre=False, skip_on_failure=True)
    def check_price_for_limit(cls, values):
        order_type = values.get('order_type')
        price = values.get('price')
        
        if order_type == "LIMIT" and price is None:
            raise ValueError("Price is required for LIMIT orders.")
        
        if order_type == "MARKET" and price is not None:
             raise ValueError("Price should not be provided for MARKET orders.")
             
        return values

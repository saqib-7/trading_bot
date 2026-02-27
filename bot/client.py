import os
import hmac
import hashlib
import time
from urllib.parse import urlencode
import requests
from typing import Dict, Any, Optional
from dotenv import load_dotenv, find_dotenv

from .logging_config import logger

load_dotenv(find_dotenv())

BASE_URL = "https://testnet.binancefuture.com"

class BinanceFuturesClient:
    def __init__(self, api_key: str = None, api_secret: str = None):
        self.api_key = api_key or os.getenv("BINANCE_API_KEY")
        self.api_secret = api_secret or os.getenv("BINANCE_API_SECRET") or os.getenv("BINANCE_SECRET_KEY")
        self.base_url = BASE_URL
        self.session = requests.Session()
        
        if self.api_key:
            self.session.headers.update({"X-MBX-APIKEY": self.api_key})

    def _generate_signature(self, query_string: str) -> str:
        if not self.api_secret:
            raise ValueError("API Secret is required for signing requests.")
            
        return hmac.new(
            self.api_secret.encode('utf-8'),
            query_string.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()

    def _send_signed_request(self, method: str, endpoint: str, payload: dict = None) -> Dict[str, Any]:
        if not payload:
            payload = {}
            
        payload['timestamp'] = int(time.time() * 1000)
        query_string = urlencode(payload)
        signature = self._generate_signature(query_string)
        
        url = f"{self.base_url}{endpoint}?{query_string}&signature={signature}"
        
        logger.info(f"Sending {method} request to {endpoint}")
        
        try:
            response = self.session.request(method, url)
            response.raise_for_status()
            logger.info(f"Response received from {endpoint} - Status: {response.status_code}")
            return response.json()
        except requests.exceptions.HTTPError as err:
            logger.error(f"HTTPError: {err.response.text}")
            raise RuntimeError(f"API Error: {err.response.text}")
        except Exception as e:
            logger.error(f"Network Error: {str(e)}")
            raise e

    def place_order(
        self,
        symbol: str,
        side: str,
        order_type: str,
        quantity: float,
        price: Optional[float] = None
    ) -> Dict[str, Any]:
        """Places a MARKET or LIMIT order on Binance Futures Testnet."""
        endpoint = "/fapi/v1/order"
        payload = {
            "symbol": symbol,
            "side": side,
            "type": order_type,
            "quantity": quantity
        }
        
        if order_type == "LIMIT":
            if price is None:
                raise ValueError("Price must be specified for LIMIT orders.")
            payload["price"] = price
            payload["timeInForce"] = "GTC"
            
        return self._send_signed_request("POST", endpoint, payload)

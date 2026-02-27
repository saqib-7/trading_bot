import typer
from rich.console import Console
from rich.panel import Panel
from fastapi.testclient import TestClient

from bot.orders import app
from bot.logging_config import logger


cli = typer.Typer(help="Binance Futures CLI Trading Bot")
console = Console()
client = TestClient(app)

@cli.command("order")
def place_order(
    symbol: str = typer.Option(..., prompt="Enter Trading Pair (e.g., BTCUSDT)", help="Trading pair, e.g. BTCUSDT"),
    side: str = typer.Option(..., prompt="Enter Side [BUY/SELL]", help="BUY or SELL"),
    order_type: str = typer.Option(..., prompt="Enter Order Type [MARKET/LIMIT]", help="MARKET or LIMIT"),
    quantity: float = typer.Option(..., prompt="Enter Order Quantity", help="Order quantity"),
    price: float = typer.Option(None, "--price", "-p", help="Order price (required for LIMIT)")
):
    """
    Place an order interactively or via flags.
    Options: MARKET or LIMIT. 
    If LIMIT, you will be prompted for price.
    """
    # Interactive follow-up prompts for conditional arguments
    if order_type.upper() == "LIMIT" and price is None:
        price = typer.prompt("Enter Target Price", type=float)

    console.print(Panel(f"Order Request:\nSymbol: {symbol}\nSide: {side}\nType: {order_type}\nQty: {quantity}\nPrice: {price}", title="Placing Order..."))
    logger.info(f"CLI init order: {symbol} {side} {order_type} {quantity} {price}")
    
    payload = {
        "symbol": symbol,
        "side": side,
        "order_type": order_type,
        "quantity": quantity,
        "price": price
    }
    
    try:
        response = client.post("/api/v1/order", json=payload)
        
        if response.status_code == 200:
            data = response.json()
            success_msg = (
                f"[green]Order Successfully Placed![/green]\n"
                f"Order ID: {data.get('orderId')}\n"
                f"Status: {data.get('status')}\n"
                f"Executed Qty: {data.get('executedQty')}\n"
                f"Avg Price: {data.get('avgPrice')}"
            )
            console.print(Panel(success_msg, title="Success", border_style="green"))
        else:
            err_msg = response.json()
            console.print(Panel(f"[red]Order Failed![/red]\nStatus Code: {response.status_code}\nDetails: {err_msg}", title="Error", border_style="red"))
            
    except Exception as e:
        logger.exception("CLI encountered an error.")
        console.print(f"[red]Fatal CLI Error: {str(e)}[/red]")

@cli.command("serve")
def start_server(port: int = 8000):
    """Start the FastAPI backend server (optional, not strictly required for CLI)."""
    import uvicorn
    console.print(f"Starting server on port {port}...")
    uvicorn.run("bot.orders:app", host="0.0.0.0", port=port)

if __name__ == "__main__":
    cli()

import typer
from rich.console import Console
from rich.table import Table
from typing import Optional

# Importing custom modules
from bot.client import get_binance_client, verify_connection
from bot.validators import validate_symbol, validate_side, validate_order_type, validate_quantity, validate_price, validate_stop_price
from bot.orders import place_market_order, place_limit_order, place_stop_limit_order, check_order_status, get_usdt_balance
from bot.logging_config import bot_logger

app = typer.Typer(help="Binance Futures Testnet Trading Bot", no_args_is_help=True)
console = Console()

@app.callback()
def main():
    pass

@app.command()
def trade(
    symbol: str = typer.Option(..., "--symbol", "-s", help="Trading pair, e.g., BTCUSDT"),
    side: str = typer.Option(..., "--side", help="BUY or SELL"),
    order_type: str = typer.Option(..., "--type", "-t", help="MARKET, LIMIT, or STOP_LIMIT"),
    quantity: float = typer.Option(..., "--qty", "-q", help="Amount to trade"),
    price: Optional[float] = typer.Option(None, "--price", "-p", help="Required if type is LIMIT or STOP_LIMIT"),
    stop_price: Optional[float] = typer.Option(None, "--stop-price", "-sp", help="Trigger price for STOP_LIMIT")
):
    try:
        # validating inputs
        clean_symbol = validate_symbol(symbol)
        clean_side = validate_side(side)
        clean_type = validate_order_type(order_type)
        clean_qty = validate_quantity(quantity)
        clean_price = validate_price(price, clean_type)
        clean_stop = validate_stop_price(stop_price, clean_type)

        console.print("[bold cyan]Connecting to Testnet...[/bold cyan]")
        client = get_binance_client()

        if not verify_connection(client):
            console.print("[bold red]Connection failed. Check your network or API keys.[/bold red]")
            raise typer.Exit(code=1)

        response = None
        if clean_type == "MARKET":
            response = place_market_order(client, clean_symbol, clean_side, clean_qty)
        elif clean_type == "LIMIT":
            assert clean_price is not None
            response = place_limit_order(client, clean_symbol, clean_side, clean_qty, clean_price)
        elif clean_type == "STOP_LIMIT":
            assert clean_price is not None
            assert clean_stop is not None
            response = place_stop_limit_order(client, clean_symbol, clean_side, clean_qty, clean_price, clean_stop)

        # Displaying result
        if response:
            _render_success_table(response, clean_symbol, clean_side, clean_type, clean_price, clean_stop)
        else:
            console.print("[bold red]Order failed. Check the logs (trading_bot.log) for details.[/bold red]")

    except ValueError as e:
        # Catching validation errors
        console.print(f"[bold red]Input Error:[/bold red] {e}")
        bot_logger.warning(f"User provided invalid input: {e}")
        raise typer.Exit(code=1)
    except Exception as e:
        # Catching unexpected crashes
        console.print("[bold red]Critical system error occurred.[/bold red] See logs.")
        bot_logger.error(f"CLI crash: {e}")
        raise typer.Exit(code=1)


def _render_success_table(response: dict, symbol: str, side: str, order_type: str, price: float | None, stop_price: float | None = None):
    table = Table(title="🚀 Trade Executed Successfully", show_header=True, header_style="bold green")

    # Defining columns
    table.add_column("Order ID", style="cyan")
    table.add_column("Symbol", style="magenta")
    table.add_column("Side")
    table.add_column("Type")
    table.add_column("Status")
    table.add_column("Executed Qty", justify="right")

    side_fmt = f"[bold green]{side}[/bold green]" if side == "BUY" else f"[bold red]{side}[/bold red]"

    table.add_row(
        str(response.get("orderId", "N/A")),
        symbol,
        side_fmt,
        order_type,
        str(response.get("status", "N/A")),
        str(response.get("executedQty", "0"))
    )

    console.print(table)
    if price:
        console.print(f"[dim]Target Price set at: {price}[/dim]")
    if stop_price:
        console.print(f"[dim]Stop Trigger set at: {stop_price}[/dim]")

@app.command()
def status(
    symbol: str = typer.Option(..., "--symbol", "-s", help="Trading pair, e.g., BTCUSDT"),
    order_id: int = typer.Option(..., "--order-id", "-id", help="The Binance Order ID to check")
):
    """Check the real-time status and filled quantity of an existing order."""
    try:
        clean_symbol = validate_symbol(symbol)

        console.print(f"[bold cyan]Querying Binance for Order {order_id}...[/bold cyan]")
        client = get_binance_client()

        if not verify_connection(client):
            raise typer.Exit(code=1)

        response = check_order_status(client, clean_symbol, order_id)

        if response:
            table = Table(title=f"🔍 Status Update: {order_id}", show_header=True)
            table.add_column("Symbol", style="magenta")
            table.add_column("Type")
            table.add_column("Status", style="bold yellow")
            table.add_column("Filled Qty", style="bold green")

            table.add_row(
                clean_symbol,
                str(response.get("type", "N/A")),
                str(response.get("status", "N/A")),
                str(response.get("executedQty", "0"))
            )
            console.print(table)
        else:
            console.print("[bold red]Failed to retrieve status. Ensure the Order ID is correct.[/bold red]")

    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
        raise typer.Exit(code=1)

@app.command()
def balance():
    """Check your current Testnet USDT balance."""
    console.print("[bold cyan]Fetching account balance...[/bold cyan]")
    try:
        client = get_binance_client()
        if not verify_connection(client):
            raise typer.Exit(code=1)

        usdt_bal = get_usdt_balance(client)
        if usdt_bal:
            console.print(f"\n💰 [bold white]Available USDT Balance:[/bold white] [bold green]${usdt_bal}[/bold green]\n")
        else:
            console.print("[bold red]Failed to retrieve balance. Check logs.[/bold red]")

    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
        raise typer.Exit(code=1)

if __name__ == "__main__":
    app()

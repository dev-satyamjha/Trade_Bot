from binance.client import Client
from binance.exceptions import BinanceAPIException
from bot.logging_config import bot_logger

def place_market_order(client: Client, symbol: str, side: str, quantity: float) -> dict | None:
    bot_logger.info(f"Attempting MARKET {side} | {quantity} {symbol}")

    try:
        response = client.futures_create_order(
            symbol=symbol,
            side=side,
            type='MARKET',
            quantity=quantity
        )

        # Details grabbing from the response
        order_id = response.get('orderId')
        status = response.get('status')
        exec_qty = response.get('executedQty')

        bot_logger.info(f"Success -> ID: {order_id} | Status: {status} | Filled: {exec_qty}")
        return response

    except BinanceAPIException as api_err:
        # Handle rejections
        bot_logger.error(f"API Rejected MARKET Order: {api_err.message}")
        return None
    except Exception as e:
        bot_logger.error(f"Unexpected crash during MARKET order: {str(e)}")
        return None


def place_limit_order(client: Client, symbol: str, side: str, quantity: float, price: float) -> dict | None:
    bot_logger.info(f"Attempting LIMIT {side} | {quantity} {symbol} @ {price}")

    try:
        # Limit orders
        response = client.futures_create_order(
            symbol=symbol,
            side=side,
            type='LIMIT',
            timeInForce='GTC',
            quantity=quantity,
            price=price
        )

        order_id = response.get('orderId')
        status = response.get('status')

        bot_logger.info(f"Success -> ID: {order_id} | Status: {status} | Target Price: {price}")
        return response

    except BinanceAPIException as api_err:
        bot_logger.error(f"API Rejected LIMIT Order: {api_err.message}")
        return None
    except Exception as e:
        bot_logger.error(f"Unexpected crash during LIMIT order: {str(e)}")
        return None


def place_stop_limit_order(client: Client, symbol: str, side: str, quantity: float, price: float, stop_price: float) -> dict | None:
    bot_logger.info(f"Attempting STOP_LIMIT {side} | {quantity} {symbol} @ Price: {price} | Trigger: {stop_price}")

    try:
        # Stop-limit orders
        response = client.futures_create_order(
            symbol=symbol,
            side=side,
            type='STOP',
            timeInForce='GTC',
            quantity=quantity,
            price=price,
            stopPrice=stop_price
        )

        order_id = response.get('orderId')
        status = response.get('status')

        bot_logger.info(f"Success -> ID: {order_id} | Status: {status} | Target: {price} | Stop: {stop_price}")
        return response

    except BinanceAPIException as api_err:
        bot_logger.error(f"API Rejected STOP_LIMIT Order: {api_err.message}")
        return None
    except Exception as e:
        bot_logger.error(f"Unexpected crash during STOP_LIMIT order: {str(e)}")
        return None

def check_order_status(client: Client, symbol: str, order_id: int) -> dict | None:
    bot_logger.info(f"Checking status for {symbol} Order ID: {order_id}")
    try:
        response = client.futures_get_order(symbol=symbol, orderId=order_id)

        status = response.get('status')
        exec_qty = response.get('executedQty')

        bot_logger.info(f"Status retrieved -> ID: {order_id} | Status: {status} | Filled: {exec_qty}")
        return response

    except BinanceAPIException as api_err:
        bot_logger.error(f"API Error checking status: {api_err.message}")
        return None
    except Exception as e:
        bot_logger.error(f"Unexpected error checking status: {str(e)}")
        return None

def get_usdt_balance(client: Client) -> str | None:
    bot_logger.info("Fetching USDT balance...")
    try:
        # Get asset balances
        balances = client.futures_account_balance()
        for asset in balances:
            if asset['asset'] == 'USDT':
                bot_logger.info(f"Balance retrieved: {asset['balance']} USDT")
                return asset['balance']

        return "0.0000"

    except BinanceAPIException as api_err:
        bot_logger.error(f"API Error fetching balance: {api_err.message}")
        return None
    except Exception as e:
        bot_logger.error(f"Unexpected error fetching balance: {str(e)}")
        return None

import os
from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceRequestException
from dotenv import load_dotenv
from bot.logging_config import bot_logger

load_dotenv()

def get_binance_client() -> Client:
    """
    Initializes and returns the Binance client using Testnet credentials.
    """
    api_key = os.getenv("BINANCE_TESTNET_API_KEY")
    api_secret = os.getenv("BINANCE_TESTNET_API_SECRET")

    # Fast-fail if the keys are missing
    if not api_key or not api_secret:
        bot_logger.error("API keys are missing! Make sure your .env file is set up.")
        raise ValueError("Missing Binance API credentials. Check .env file.")

    try:
        client = Client(api_key, api_secret, testnet=True)
        return client

    except Exception as e:
        bot_logger.error(f"Failed to boot up the Binance client: {e}")
        raise

def verify_connection(client: Client) -> bool:
    """
    Pings the Futures API to ensure credentials and network are working
    before placing orders.
    """
    try:
        client.futures_ping()
        bot_logger.info("Successfully connected to Binance Futures Testnet.")
        return True

    except BinanceAPIException as api_error:
        bot_logger.error(f"Binance API rejected us: {api_error.message} (Code: {api_error.code})")
        return False

    except BinanceRequestException as req_error:
        bot_logger.error(f"Network error while connecting to Binance: {req_error}")
        return False

    except Exception as e:
        bot_logger.error(f"Unexpected error during connection test: {e}")
        return False

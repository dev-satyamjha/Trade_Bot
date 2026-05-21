import logging
from logging.handlers import RotatingFileHandler

def setup_logger():
    """
    Sets up a robust logging system.
    Logs go to both the terminal and a rotating file for audit.
    """
    logger = logging.getLogger("TradingBot")
    logger.setLevel(logging.INFO)

    # Prevent duplicate logs if this function gets called more than once
    if logger.handlers:
        return logger

    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # Keeps the last 5 logs, max 2MB each
    file_handler = RotatingFileHandler(
        filename="trading_bot.log",
        maxBytes=2 * 1024 * 1024,
        backupCount=5
    )
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger

bot_logger = setup_logger()

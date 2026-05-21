def validate_symbol(symbol: str) -> str:
    clean_symbol = symbol.strip().upper()

    if not clean_symbol.isalnum():
        raise ValueError("Symbol must be alphanumeric without spaces.")

    return clean_symbol

def validate_side(side: str) -> str:
    # Lock down the side to only exact matches
    clean_side = side.strip().upper()
    if clean_side not in ["BUY", "SELL"]:
        raise ValueError("Order side must be strictly 'BUY' or 'SELL'.")

    return clean_side

def validate_order_type(order_type: str) -> str:
    # Lock down order types
    clean_type = order_type.strip().upper()
    if clean_type not in ["MARKET", "LIMIT", "STOP_LIMIT"]:
        raise ValueError("Order type must be strictly 'MARKET', 'LIMIT', or 'STOP_LIMIT'.")

    return clean_type

def validate_quantity(qty: float) -> float:
    # Prevent zero or negative trades
    if qty <= 0:
        raise ValueError("Quantity must be a positive number.")

    return qty

def validate_price(price: float | None, order_type: str) -> float | None:
    if order_type == "MARKET":
        return None

    # Limit and Stop-Limit orders requires a positive price
    if price is None or price <= 0:
        raise ValueError(f"A positive price is mandatory for {order_type} orders.")

    return price

def validate_stop_price(stop_price: float | None, order_type: str) -> float | None:
    if order_type == "STOP_LIMIT":
        if stop_price is None or stop_price <= 0:
            raise ValueError("A trigger stop-price is mandatory for STOP_LIMIT orders.")
        return stop_price
    return None

# 🚀 Binance Futures Testnet Trading Bot

A robust, CLI-based Python application for executing and managing trades on the Binance Futures Testnet . Built with modern Python tooling, it features a sleek Terminal User Interface (TUI), input validation, and rotating logs.

## ✨ Features
- **Multiple Order Types:** Supports `MARKET`, `LIMIT`, and the bonus `STOP_LIMIT` orders.
- **Enhanced CLI UX:** Built with `Typer` and `Rich` for a beautifully formatted, color-coded terminal experience.
- **Robust Validation:** Prevents bad API calls by sanitizing symbols, enforcing positive quantities, and validating required price fields locally.
- **Production Logging:** Implements a rotating file handler (max 2MB per file, 5 backups) alongside clean console output.
- **Modern Tooling:** Uses `uv` for lightning-fast dependency management.

---

## ⚙️ Setup & Installation

This project uses [uv](https://docs.astral.sh/uv/) for dependency management instead of a legacy `requirements.txt`. The `pyproject.toml` file contains all necessary metadata and dependencies.

### 1. Clone the repository
```bash
git clone https://github.com/dev-satyamjha/Trade_Bot.git
cd Trade_Bot
```

## 📂 Project Structure

```text
├── bot/
│   ├── __init__.py
│   ├── client.py         
│   ├── logging_config.py 
│   ├── orders.py         
│   └── validators.py     
├── cli.py                
├── pyproject.toml        
├── trading_bot.log       
├── uv.lock               
└── README.md
```
---

### 2. Configure Environment Variables

You must provide your Binance Testnet API credentials.

```bash
cp .env.example .env
```

Edit the `.env` file and insert your keys:

```env
BINANCE_TESTNET_API_KEY=your_actual_api_key
BINANCE_TESTNET_API_SECRET=your_actual_api_secret
```

### 3. Run the Bot

Since `uv` manages the virtual environment automatically, you can run the CLI directly. `uv` will automatically download the dependencies listed in `pyproject.toml` on the first run.

```bash
uv run cli.py --help
```

---

## 🏗 Architectural Decisions & Assumptions

* **UI Framework:** Chose a CLI TUI (Typer/Rich) over a lightweight web UI. For a trading bot, a fast, keyboard-driven interface with structured table outputs is vastly superior for developers and power users.
* **Separation of Concerns:** The logic is strictly decoupled. `cli.py` handles user interaction, `validators.py` handles input sanitization, and `orders.py` interfaces with the Binance API.
* **Limit Order Behavior:** All `LIMIT` and `STOP_LIMIT` orders are submitted with `timeInForce='GTC'` (Good Till Cancelled) as standard practice.
* **Stop-Limit Implementation:** Binance Futures utilizes `type='STOP'` for stop-limit orders on the backend, which was handled accordingly in the API wrapper.

---

## ❓ FAQ: Why does my executed quantity show 0?

**Q: I placed an order, but the success table shows `Status: NEW` and `Executed Qty: 0.0000`. Did it fail?**

**A:** No, your order was successful! This is the intended behavior of the Binance REST API.

1. **The Receipt:** When you send an order via the REST API, Binance instantly replies with an acknowledgment receipt. This receipt says, "I have received your order, it is now placed on the order book (`NEW`), and at this exact millisecond, 0 quantities have been filled."
2. **The Execution:** A few milliseconds *after* that receipt is sent, the Binance Matching Engine actually executes the trade.
3. **How to verify:** To see the updated status (e.g., `FILLED` and `0.01` executed), wait a few seconds and run the **Status Check Command** (see examples below) using your Order ID.

---

## 💻 Usage & Command Examples

The bot utilizes a subcommand structure. Use `uv run cli.py <command> [OPTIONS]`.

### System Commands

**1. View the main help menu**

```bash
uv run cli.py --help
```

**2. View the trade command options and required arguments**

```bash
uv run cli.py trade --help
```

**3. Check your current Testnet USDT balance**

```bash
uv run cli.py balance
```

**4. Check the real-time status of a specific order** *(Replace with your actual Order ID)*

```bash
uv run cli.py status -s BTCUSDT --order-id 13172640126
```

### Market Orders (Executes Immediately)

**5. Place a Market BUY order**

```bash
uv run cli.py trade -s BTCUSDT --side BUY -t MARKET -q 0.01
```

**6. Place a Market SELL order**

```bash
uv run cli.py trade -s ETHUSDT --side SELL -t MARKET -q 0.1
```

### Limit Orders (Waits for specific price)

**7. Place a Limit BUY**

```bash
uv run cli.py trade -s BTCUSDT --side BUY -t LIMIT -q 0.01 -p 40000.0
```

**8. Place a Limit SELL**

```bash
uv run cli.py trade -s SOLUSDT --side SELL -t LIMIT -q 2.5 -p 200.0
```

### Stop-Limit Orders (Bonus Feature)

**9. Place a Stop-Limit SELL**

```bash
uv run cli.py trade -s BTCUSDT --side SELL -t STOP_LIMIT -q 0.01 -p 39000.0 --stop-price 39500.0
```

**10. Place a Stop-Limit BUY**

```bash
uv run cli.py trade -s BTCUSDT --side BUY -t STOP_LIMIT -q 0.01 -p 71000.0 --stop-price 70500.0
```

### Error Handling & Validation Examples

**11. Invalid Symbol Format** 

```bash
uv run cli.py trade -s BTC-USDT --side BUY -t MARKET -q 0.01
```

**12. Invalid Side** 

```bash
uv run cli.py trade -s BTCUSDT --side HOLD -t MARKET -q 0.01
```

**13. Invalid Quantity** 

```bash
uv run cli.py trade -s ETHUSDT --side BUY -t MARKET -q -1.5
```

**14. Missing Required Price** 

```bash
uv run cli.py trade -s BTCUSDT --side BUY -t LIMIT -q 0.01
```

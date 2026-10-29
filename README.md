# STRATUM

STRATUM is a full-stack trading simulator and algorithmic trading dashboard. It combines a Django REST/ASGI backend with a React dashboard for paper trading, market data, portfolios, strategies, backtests, and automated bots.

> **Development status:** This project is intended for development and paper-trading environments. Do not use it with real funds without completing an independent security, reliability, and compliance review.

## Features

- JWT authentication and user portfolios
- Market quotes and historical price data
- Market, limit, and stop-loss orders
- Simulated broker adapter with optional Alpaca paper-trading support
- Portfolio, order, and transaction history
- Strategy configuration and backtesting
- Bot management and scheduled background jobs
- Live market and portfolio updates over WebSockets
- OpenAPI schema and Swagger UI
- PostgreSQL, Redis, and InfluxDB integrations

## Architecture

| Component | Purpose |
| --- | --- |
| Django + Django REST Framework | API, authentication, trading, strategy, and backtest services |
| Django Channels + Daphne | ASGI server and WebSocket updates |
| Celery + Redis | Background tasks and scheduled jobs |
| PostgreSQL | Application data |
| InfluxDB | Time-series market data |
| React + Vite | Dashboard frontend |

## Requirements

- Docker and Docker Compose
- Node.js 18+ and npm for frontend development outside Docker
- Python 3.11+ for running the backend directly

## Quick start with Docker

1. Copy the example environment file and replace development values or API credentials as needed:

   ```bash
   cp .env.example .env
   ```

2. Start the backend, worker, scheduler, and supporting services:

   ```bash
   docker compose up --build
   ```

3. In a separate terminal, install and start the frontend:

   ```bash
   cd frontend
   npm install
   npm run dev
   ```

4. Open <http://localhost:3000>. The Vite development server proxies API and WebSocket requests to the backend at <http://localhost:8000>.

Seed the default symbols in another terminal:

```bash
docker compose exec web python manage.py seed_stocks
```

The default seed includes AAPL, MSFT, GOOGL, TSLA, NVDA, AMZN, META, BTC-USD, and ETH-USD.

## Useful URLs

- Dashboard: <http://localhost:3000>
- API root: <http://localhost:8000/api/v1/>
- Swagger UI: <http://localhost:8000/api/docs/>
- OpenAPI schema: <http://localhost:8000/api/schema/>
- Health check: <http://localhost:8000/health/>
- Readiness check: <http://localhost:8000/ready/>
- InfluxDB: <http://localhost:8086>

The API also exposes the same versioned routes under `/api/`.

## Local backend development

Create a virtual environment and install the Python dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

For a lightweight local setup, use SQLite and Django's in-memory channel layer:

```bash
export USE_SQLITE=true
python manage.py migrate
python manage.py seed_stocks
python manage.py runserver
```

Celery tasks and external market-data services require Redis and the corresponding environment variables. Docker Compose provides the complete development service stack.

## Frontend development

```bash
cd frontend
npm install
npm run dev
```

To create a production frontend bundle:

```bash
npm run build
```

The Vite server accepts `VITE_BACKEND_URL` and `VITE_BACKEND_WS_URL` when the backend is not running on the default local addresses.

## Configuration

Copy `.env.example` to `.env` and configure values for your environment. Optional integrations include:

- `FINNHUB_API_KEY` for market data
- `ALPACA_API_KEY`, `ALPACA_SECRET_KEY`, and `ALPACA_BASE_URL` for Alpaca paper trading
- `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID` for notifications
- `INFLUX_*` variables for time-series storage

Never commit `.env` files, API keys, broker secrets, or production credentials.

## API overview

All protected API endpoints use a JWT access token. Main route groups include:

- `/api/v1/auth/` - registration, login, token refresh, and user portfolio
- `/api/v1/market/` - stocks, quotes, and historical data
- `/api/v1/trading/` - orders, cancellations, transactions, and portfolios
- `/api/v1/strategy/` - strategy configuration and signals
- `/api/v1/backtest/` - backtest execution and results
- `/api/v1/bot/` - bot management

Use the Swagger UI for request schemas and interactive API exploration.

## Testing

Run the test suite in the Docker web container:

```bash
docker compose exec web pytest
```

Or run it locally after installing the requirements:

```bash
pytest
```

The repository's CI workflow runs the Python test suite with PostgreSQL and Redis services.

## Project layout

```text
accounts/       Authentication and user portfolios
backtest/       Backtesting API and services
bot/            Automated trading bots and Celery tasks
config/         Django settings, ASGI, URLs, and Celery configuration
core/           Shared middleware, health checks, permissions, and utilities
market/         Symbols, quotes, market data, and WebSockets
strategy/       Trading strategy models and APIs
trading/        Orders, portfolios, broker adapters, and WebSockets
frontend/       React/Vite dashboard
k8s/            Kubernetes deployment examples
```

## License

No license has been specified for this repository yet.
This Project is under Maintenance. anyone have interested to contribute please DM  

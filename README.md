# 📈 Crypto Price Tracker — Airflow ETL Pipeline

A production-ready data pipeline that fetches live cryptocurrency prices from the CoinGecko API, stores them in PostgreSQL, and orchestrates the entire workflow with Apache Airflow — all containerized with Docker Compose.

---

## 🗂️ Project Structure

```
.
├── dags/
│   └── market_data_dag.py        # Airflow DAG definition
├── scripts/
│   ├── extract_load.py           # ETL logic (fetch & store)
│   ├── sql_create_table          # Table initialization SQL
│   ├── __init__.py
│   └── .env_example
├── Dockerfile                    # Custom Airflow image
├── docker-compose.yml            # Full stack orchestration
├── requirements.txt
└── .gitignore
```

---

## ⚙️ How It Works

The pipeline runs on an **hourly schedule** and consists of three tasks chained in sequence:

```
check_api_availability  ──►  run_etl_script  ──►  validate_database_count
```

| Task | Type | Description |
|------|------|-------------|
| `check_api_availability` | `HttpSensor` | Pings CoinGecko's `/api/v3/ping` before pulling data |
| `run_etl_script` | `PythonOperator` | Fetches BTC, ETH, SOL prices and inserts into PostgreSQL |
| `validate_database_count` | `PostgresOperator` | Asserts that new rows landed within the last hour |

---

## 🛠️ Tech Stack

- **Apache Airflow 2.8.1** — workflow orchestration
- **PostgreSQL 15** — price data storage
- **Python 3.8** — ETL scripting (`requests`, `psycopg2`)
- **CoinGecko API** — free public crypto price feed
- **Docker Compose** — local multi-container deployment

---

## 🚀 Getting Started

### Prerequisites

- [Docker](https://docs.docker.com/get-docker/) & Docker Compose installed
- No API key required (CoinGecko free tier)

### 1. Clone the repository

```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
```

### 2. Configure environment variables

```bash
cp scripts/.env_example scripts/.env
```

Edit `scripts/.env` with your target database credentials:

```env
DB_HOST=postgres
DB_NAME=your_db_name
DB_USER=your_db_user
DB_PASS=your_db_password
```

### 3. Start the stack

```bash
docker compose up --build
```

This will spin up:
- **PostgreSQL** (port `5432`) — initializes the `coin_prices` table automatically
- **Airflow Webserver** (port `8080`) — UI at `http://localhost:8080`
- **Airflow Scheduler** — picks up and runs the DAG

Default Airflow login: `admin` / `admin`

### 4. Configure Airflow Connections

In the Airflow UI (**Admin → Connections**), create two connections:

**HTTP connection** (for the API health check):
| Field | Value |
|-------|-------|
| Conn Id | `http_default` |
| Conn Type | `HTTP` |
| Host | `https://api.coingecko.com` |

**Postgres connection** (for the validation task):
| Field | Value |
|-------|-------|
| Conn Id | `my_postgres_conn` |
| Conn Type | `Postgres` |
| Host | `postgres` |
| Schema | your DB name |
| Login | your DB user |
| Password | your DB password |
| Port | `5432` |

### 5. Enable and trigger the DAG

In the Airflow UI, toggle **`market_data_etl_v1`** to active. It will run on the next hourly boundary, or you can trigger it manually.

---

## 🗄️ Database Schema

```sql
CREATE TABLE IF NOT EXISTS coin_prices (
    id               SERIAL PRIMARY KEY,
    coin_name        TEXT,
    price_usd        NUMERIC,
    last_updated_at  TIMESTAMP,
    fetched_at       TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

Coins tracked: **Bitcoin**, **Ethereum**, **Solana**

---

## 📦 Dependencies

```
psycopg2-binary
requests
python-dotenv
apache-airflow-providers-postgres
apache-airflow-providers-http
```

---

## 🐛 Troubleshooting

not done yet

MIT

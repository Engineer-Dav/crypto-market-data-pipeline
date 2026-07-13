# 🚀 Crypto Market Data Pipeline

An end-to-end Data Engineering project that extracts live cryptocurrency market data from the CoinGecko API, stores historical records in PostgreSQL using the Medallion Architecture, transforms the data into analytics-ready datasets, and prepares them for visualization in Microsoft Power BI.

---

# 📌 Project Overview

This project demonstrates the complete lifecycle of a modern data engineering pipeline.

The pipeline automatically extracts live cryptocurrency market data, validates and transforms it, stores historical records in PostgreSQL, and organizes the data into Bronze, Silver, and Gold layers following the Medallion Architecture.

The final Gold layer contains business-ready datasets optimized for reporting and dashboard development.

---

# 🎯 Objectives

* Extract live cryptocurrency market data automatically.
* Preserve raw historical data.
* Build a dimensional model using Fact and Dimension tables.
* Produce analytics-ready Gold tables.
* Demonstrate an end-to-end ETL workflow.
* Implement logging for monitoring and debugging.
* Prepare the data warehouse for Microsoft Power BI.

---

# 🏗 Architecture

```text
                         CoinGecko API
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Bronze Layer      │
                    │ crypto_market_raw   │
                    └─────────────────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │    Silver Layer     │
                    ├─────────────────────┤
                    │ dim_crypto_asset    │
                    │ fact_crypto_market  │
                    └─────────────────────┘
                               │
              ┌────────────────┴────────────────┐
              │                                 │
              ▼                                 ▼
 ┌─────────────────────────┐       ┌─────────────────────────┐
 │ gold_market_overview    │       │ gold_market_statistics  │
 └─────────────────────────┘       └─────────────────────────┘
              │                                 │
              └────────────────┬────────────────┘
                               ▼
                    Microsoft Power BI
```

---

# 🥉 Bronze Layer

## Table

`crypto_market_raw`

### Purpose

Stores raw cryptocurrency market data exactly as received from the CoinGecko API.

### Characteristics

* Historical data is preserved.
* No transformations are applied.
* Acts as the source of truth.
* Supports auditing and historical replay.

---

# 🥈 Silver Layer

The Silver layer cleans, validates, and structures the Bronze data.

## Dimension Table

`dim_crypto_asset`

Contains one unique record for every cryptocurrency.

Columns include:

* coin_id
* symbol
* name

---

## Fact Table

`fact_crypto_market`

Stores historical market observations.

Columns include:

* prices
* market_cap
* market_cap_rank
* total_volume
* price_change_percentage_24h
* last_updated
* ingestion_time
* dim_id

The Fact table continuously grows as new market snapshots are collected.

---

# 🥇 Gold Layer

The Gold layer contains analytics-ready datasets designed for reporting.

## gold_market_overview

Provides the most recent market snapshot for every cryptocurrency.

Contains:

* Coin ID
* Symbol
* Name
* Current Price
* Market Capitalization
* Market Rank
* Trading Volume
* Price Change (24 Hours)
* Last Updated
* Refresh Time

One row is maintained for each cryptocurrency through PostgreSQL UPSERT operations.

---

## gold_market_statistics

Provides historical analytical metrics.

Contains:

* Average Price
* Average Volume
* Highest Price
* Lowest Price
* Average Market Capitalization
* Price Volatility
* Refresh Time

These statistics are recalculated every pipeline execution.

---

# ⚙ ETL Workflow

## Extract

* Retrieve live cryptocurrency market data from the CoinGecko API.

## Transform

* Read Bronze data.
* Convert data types.
* Remove duplicate records.
* Validate numeric ranges.
* Prepare clean datasets.

## Load

* Load transformed data into the Silver layer.
* Populate the Fact and Dimension tables.
* Refresh the Gold reporting tables.
* Update existing records using PostgreSQL UPSERT (`ON CONFLICT`).

---

# 📂 Project Structure

```text
market-data-pipeline/

├── api.py
├── database.py
├── transform.py
├── logger.py
├── main.py
├── database.sql
├── requirements.txt
├── README.md
├── .gitignore
├── logs/
└── .env
```

---

# 🛠 Technologies Used

## Programming

* Python

## Database

* PostgreSQL

## Python Libraries

* pandas
* requests
* psycopg2-binary
* python-dotenv

## Data Engineering Concepts

* ETL Pipeline
* Medallion Architecture
* Star Schema
* Fact & Dimension Modeling
* Incremental Loading
* Logging

## Visualization

* Microsoft Power BI

---

# 📋 Requirements

## Software Requirements

Before running this project, ensure the following software is installed:

* Python 3.10 or later
* PostgreSQL 14 or later
* Git

---

## Python Dependencies

Install the required Python packages:

```bash
pip install -r requirements.txt
```

---

# ⚙ Configuration

Create a `.env` file in the project root.

```env
DB_NAME=market_data_db
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
```

---

# 🚀 Running the Pipeline

Run the project with:

```bash
python main.py
```

Each execution will:

* Extract live cryptocurrency data
* Store raw data in Bronze
* Transform and load data into Silver
* Refresh the Gold reporting tables
* Record execution logs

---

# 📊 Features

* Live API ingestion
* Historical data storage
* Data validation
* Duplicate handling
* PostgreSQL UPSERT operations
* Star Schema implementation
* Gold reporting layer
* Modular Python architecture
* Logging and monitoring
* Power BI ready

---

# 📈 Future Improvements

* Apache Airflow orchestration
* Docker containerization
* Microsoft Fabric integration
* Azure deployment
* Automated scheduling
* Power BI dashboard
* CI/CD pipeline
* Unit testing

---

# 📚 Concepts Demonstrated

* ETL
* PostgreSQL
* SQL
* Python
* Data Warehousing
* Medallion Architecture
* Star Schema
* Fact Tables
* Dimension Tables
* Incremental Loading
* Data Validation
* Logging
* Analytics Engineering

---

# 👨‍💻 Author

**David Mike**
**Engineer-Dav**

This project demonstrates the design and implementation of an end-to-end data pipeline using Python and PostgreSQL. It showcases data ingestion from a live API, ETL processing, dimensional data modeling with a star schema, Medallion Architecture, and the creation of analytics-ready datasets for business intelligence applications such as Microsoft Power BI.
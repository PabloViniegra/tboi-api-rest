# The Binding of Isaac Platinum Remake API

Welcome to the REST API for **The Binding of Isaac Platinum Remake**! This API provides endpoints to retrieve and manage data scraped from the game's items and resources. Built using modern technologies like **FastAPI**, **SQLAlchemy**, and **Python**, this API ensures high performance and maintainability.

## Technologies Used

- **Python**: The core programming language for the API.
- **FastAPI**: A modern, fast (high-performance) web framework for building APIs with Python.
- **SQLAlchemy**: Used for ORM (Object Relational Mapping) to manage database operations.
- **BeautifulSoup**: For web scraping game data from external sources.

## Features

- Scrapes data from external sources to populate the database.
- Provides endpoints to retrieve and manipulate items data.
- Utilizes SQLAlchemy for seamless database interactions.
- FastAPI ensures a clean, auto-documented API using Swagger UI.

## Prerequisites

- **Python 3.9+**
- **Git**
- **PostgreSQL** (or a compatible database)

## Installation

### Clone the Repository

```bash
git clone https://github.com/your-username/tboi-platinum-remake-api.git
cd tboi-platinum-remake-api
```

## Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate # On Windows: venv\Scripts\activate
```

## Install dependencies

```bash
pip install -r requirements.txt
```

## Set up environment variables

Create a ```.env``` file in the project root and configure the following variables:

```bash
DATABASE_URL=postgresql://username:password@localhost:5432/database_name
SCRAPING_URL=https://tboi.com/all-items
```
Replace ```username```, ```password```, and ```database_name``` with your PostgreSQL credentials.

## Run the Application

Start the FastAPI server:
```bash
fastapi dev main.py
```
The API will be available at http://127.0.0.1:8000.

[docs](http://127.0.0.1:8000/docs)

# Stockmood

Stockmood is a Flask application that visualizes stock sentiment using heat map, word cloud, bar charts, and emotional dot 
graphs etc. 

## Description

We are building our application using a Flask Dashboard boilerplate called Flask Dashboard Black (https://appseed.us/admin-dashboards/flask-dashboard-black).

## Installation & Execution

```bash
docker compose up -d
[+] Running 1/0
 ✔ Container stockmood-appseed-app-1  Created                                                                                                                                                                 0.0s
Attaching to appseed-app-1
appseed-app-1  |  * Serving Flask app 'run.py' (lazy loading)
appseed-app-1  |  * Environment: production
appseed-app-1  |    WARNING: This is a development server. Do not use it in a production deployment.
appseed-app-1  |    Use a production WSGI server instead.
appseed-app-1  |  * Debug mode: off
appseed-app-1  | [2024-04-25 06:25:40,523] INFO in run: DEBUG       = True
appseed-app-1  | [2024-04-25 06:25:40,523] INFO in run: Environment = Debug
appseed-app-1  | [2024-04-25 06:25:40,523] INFO in run: DBMS        = sqlite:////apps/db.sqlite3
appseed-app-1  |  * Running on all addresses.
appseed-app-1  |    WARNING: This is a development server. Do not use it in a production deployment.
appseed-app-1  |  * Running on <generated_link> (Press CTRL+C to quit)
```
## Data

Data is attaching via volume. Need to create datascalp sqlite file

```yaml
    volumes:
      - ./datascalp:/apps/datascalp
```

```bash
sqlite3 datascalp
```

### Tables

```sql
CREATE TABLE stock_list (
    stockID INTEGER PRIMARY KEY AUTOINCREMENT,
    Name TEXT
);
CREATE TABLE twitter_raw (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date DATE,
    tweet TEXT,
    stockID INTEGER,
    FOREIGN KEY(stockID) REFERENCES stock_list(stockID)
);
CREATE TABLE twitter_score (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    message_id INTEGER,
    stock_id INTEGER,
    nltk_score REAL,
    textblob_score REAL,
    flair_score REAL,
    bert_score REAL,
    FOREIGN KEY(message_id) REFERENCES twitter_raw(id),
    FOREIGN KEY(stock_id) REFERENCES stock_list(stockID)
);
CREATE TABLE yahoo_finance_with_trend (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    stock_id INTEGER,
    CLOSING_DATE DATE,
    Next_day_Trend TEXT,
    FOREIGN KEY(stock_id) REFERENCES stock_list(stockID)
);
CREATE TABLE Users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(64) UNIQUE,
    email VARCHAR(64) UNIQUE,
    password BLOB
);
```


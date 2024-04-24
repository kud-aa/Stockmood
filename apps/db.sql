PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
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
DELETE FROM sqlite_sequence;
COMMIT;

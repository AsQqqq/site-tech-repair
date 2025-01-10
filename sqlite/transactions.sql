CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    transaction_type TEXT NOT NULL,  -- 'income' или 'expense'
    amount REAL NOT NULL,  -- сумма операции
    receipt_filename TEXT,  -- ссылка на чек
    transaction_date TEXT NOT NULL,  -- дата операции
    uuid BIGINT NOT NULL
);

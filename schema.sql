CREATE TABLE IF NOT EXISTS transactions(
    id INTEGER PRIMARY KEY,
    transaction_name TEXT,
    transaction_type TEXT CHECK (transaction_type IN ('income', 'expense')),
    amount REAL,
    transaction_date TEXT DEFAULT CURRENT_DATE
);
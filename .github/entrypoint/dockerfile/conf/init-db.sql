CREATE TABLE IF NOT EXISTS ledger (
    id INTEGER PRIMARY KEY,
    date DATE NOT NULL,
    account VARCHAR(255) NOT NULL,
    debit FLOAT,
    credit FLOAT,
    description VARCHAR(255)
);

INSERT INTO ledger (id, date, account, debit, credit, description) VALUES
    (0, '2024-05-10', 'Sales', '5000.00', NULL, 'Sale of product A'),
    (1, '2024-05-10', 'Cash', NULL, '5000.00', 'Sale of product A'),
    (2, '2024-05-12', 'Expenses', NULL, '1500.00', 'Office supplies purchase'),
    (3, '2024-05-12', 'Accounts Payable', '1500.00', NULL, 'Office supplies purchase'), 
    (4, '2024-05-15', 'Accounts Receivable', '10000.00', NULL, 'Invoice payment received'),
    (5, '2024-05-15', 'Sales', NULL, '10000.00', 'Sale of product A');


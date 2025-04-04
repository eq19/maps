# SELECT timeframe, AVG(total_trades) AS avg_total_trades
# FROM backtest_results
# GROUP BY timeframe;

import sqlite3
from config import *

# ================================================================================================================


def trade_perc_deviation_punishment():
    # Connect to the SQLite database
    conn = sqlite3.connect(db_path + db_name)
    c = conn.cursor()
    # Check if the table exists and create it if it doesn't
    c.execute(
        "SELECT count(name) FROM sqlite_master WHERE type='table' AND name='trade_perc_deviation_punishment'"
    )
    if c.fetchone()[0] == 0:
        print("Table 'trade_perc_deviation_punishment' does not exist. Creating...")
        c.execute(
            """CREATE TABLE IF NOT EXISTS trade_perc_deviation_punishment
                    (score INTEGER PRIMARY KEY, metric_low REAL, metric_high REAL)"""
        )

        # Check if the table is empty and insert rows if it is
        c.execute("""SELECT COUNT(*) FROM trade_perc_deviation_punishment""")
        if c.fetchone()[0] == 0:
            scores = [
                (0, 0, 60),
                (-12, 61, 100),
                (-23, 101, 150),
                (-34, 151, 200),
                (-45, 201, 2000),
            ]
            c.executemany(
                "INSERT INTO trade_perc_deviation_punishment VALUES (?, ?, ?)", scores
            )

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

# trade_perc_deviation_punishment()

# ================================================================================================================


def modify_stragety_scores_table_structure():
    # Connect to the SQLite database
    conn = sqlite3.connect(db_path + db_name)
    cursor = conn.cursor()

    try:
        # Create a temporary table without the ID column
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS strategy_scores_temp (
                strategy_name TEXT,
                timeframe TEXT,
                results_filename TEXT PRIMARY KEY,
                profit_score REAL,
                winrate_score REAL,
                cagr_score REAL,
                drawdown_score REAL,
                calmar_ratio_score REAL,
                sortino_score REAL,
                sharpe_score REAL,
                profit_factor_score REAL,
                profitable_pairs_ratio_score REAL,
                expectancy_score REAL,
                trade_perc_punishment_score REAL ,
                total_score REAL,
                u_timestamp INTEGER
            )
        ''')

        # Copy the data from the original table to the temporary table
        cursor.execute('''
            INSERT INTO strategy_scores_temp
            SELECT
                strategy_name,
                timeframe,
                results_filename,
                profit_score,
                winrate_score,
                cagr_score,
                drawdown_score,
                calmar_ratio_score,
                sortino_score,
                sharpe_score,
                profit_factor_score,
                profitable_pairs_ratio_score,
                expectancy_score,
                trade_perc_punishment_score,
                total_score,
                u_timestamp
            FROM strategy_scores
        ''')

        # Drop the original table
        cursor.execute('DROP TABLE strategy_scores')

        # Rename the temporary table to the original table name
        cursor.execute(
            'ALTER TABLE strategy_scores_temp RENAME TO strategy_scores')

        # Commit the changes
        conn.commit()

        print("Table modified successfully!")
    except Exception as e:
        print("An error occurred:", str(e))

    # Close the database connection
    conn.close()


# Call the function to modify the table structure
# modify_stragety_scores_table_structure()
# ================================================================================================================

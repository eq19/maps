#!/usr/bin/python3
# coding=utf-8
import logging
import sqlite3
import os
from config import *

import sqlite3

# Initial strategy backtests database functions


def check_strategy_backtest_existence(strategy_name, strategy_filename):
    conn = sqlite3.connect(db_path + db_name)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM strategies_tested WHERE strategy_name = ? AND strategy_filename = ?",
        (strategy_name, strategy_filename),
    )
    # cursor.execute("SELECT * FROM backtest_results WHERE strategy_name = ? AND timeframe = ?", (strategy_name, timeframe))
    result = cursor.fetchone()
    conn.close()

    if result:
        print(
            f"Checking if the '{strategy_name}' and '{strategy_filename}' already exists in the result backtest database."
        )
        return True
    else:
        print(
            f"The combination of strategy_name '{strategy_name}' and timeframe '{strategy_filename}' does not exists in the database. Proceeding...")
        return False


def insert_backtest_results(
    strategy_name,
    strategy_filename,
    results_filename,
    exchange,
    strategy_type,
    bt_start_date,
    bt_start_date_ts,
    bt_end_date,
    bt_end_date_ts,
    timerange,
    start_balance,
    total_pairs,
    stake_type,
    stake_amount,
    timeframe,
    end_balance,
    net_profit,
    profit_perc,
    cagr,
    sortino,
    sharpe,
    profit_factor,
    expectancy,
    drawdown,
    calmar_ratio,
    wins,
    draws,
    losses,
    total_trades,
    win_perc,
    draws_perc,
    loss_perc,
    risk_per_trade,
    pairs_with_profit,
    pairs_with_profit_perc,
    trade_count_long,
    trade_count_short,
    profit_mean,
    profit_median,
    profit_total,
    profit_total_long,
    profit_total_short,
    profit_total_abs,
    profit_total_long_abs,
    profit_total_short_abs,
    calmar,
    stoploss,
    total_volume,
    trades_per_day,
    market_change,
    stake_currency,
    rejected_signals,
    max_open_trades,
    trailing_stop,
    trailing_stop_positive,
    trailing_stop_positive_offset,
    trailing_only_offset_is_reached,
    use_custom_stoploss,
    use_exit_signal,
    exit_profit_only,
    exit_profit_offset,
    ignore_roi_if_entry_signal,
    backtest_best_day,
    backtest_worst_day,
    backtest_best_day_abs,
    backtest_worst_day_abs,
    winning_days,
    draw_days,
    losing_days,
    holding_avg,
    holding_avg_s,
    winner_holding_avg,
    winner_holding_avg_s,
    loser_holding_avg,
    loser_holding_avg_s,
    max_drawdown,
    max_relative_drawdown,
    max_drawdown_abs,
    drawdown_start,
    drawdown_start_ts,
    drawdown_end,
    drawdown_end_ts,
    max_drawdown_low,
    max_drawdown_high,
    csum_min,
    csum_max,
    h_timestamp,
    u_timestamp,
    strategy_remark,
    hyperopt,
    positive_streaks_high,
    positive_streaks_average,
    negative_streaks_high,
    negative_streaks_average,
    tf_trades_avg,
    percentage_difference
):
    conn = sqlite3.connect(db_path + db_name)
    c = conn.cursor()

    c.execute(
        "INSERT INTO backtest_results (strategy_name, strategy_filename, results_filename, exchange, strategy_type, bt_start_date, bt_start_date_ts, bt_end_date, bt_end_date_ts, timerange, start_balance, total_pairs, stake_type, stake_amount, timeframe, end_balance, net_profit, profit_perc, cagr, sortino, sharpe, profit_factor, expectancy, drawdown, calmar_ratio, wins, draws, losses, total_trades, win_perc, draws_perc, loss_perc, risk_per_trade, pairs_with_profit, pairs_with_profit_perc, trade_count_long, trade_count_short, profit_mean, profit_median, profit_total, profit_total_long, profit_total_short, profit_total_abs, profit_total_long_abs, profit_total_short_abs, calmar, stoploss, total_volume, trades_per_day, market_change, stake_currency, rejected_signals, max_open_trades, trailing_stop, trailing_stop_positive, trailing_stop_positive_offset, trailing_only_offset_is_reached, use_custom_stoploss, use_exit_signal, exit_profit_only, exit_profit_offset, ignore_roi_if_entry_signal, backtest_best_day, backtest_worst_day, backtest_best_day_abs, backtest_worst_day_abs, winning_days, draw_days, losing_days, holding_avg, holding_avg_s, winner_holding_avg, winner_holding_avg_s, loser_holding_avg, loser_holding_avg_s, max_drawdown, max_relative_drawdown, max_drawdown_abs, drawdown_start, drawdown_start_ts, drawdown_end, drawdown_end_ts, max_drawdown_low, max_drawdown_high, csum_min, csum_max, h_timestamp, u_timestamp, strategy_remark, hyperopt, positive_streaks_high, positive_streaks_average, negative_streaks_high, negative_streaks_average, tf_trades_avg, percentage_difference) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (
            strategy_name,
            strategy_filename,
            results_filename,
            exchange,
            strategy_type,
            bt_start_date,
            bt_start_date_ts,
            bt_end_date,
            bt_end_date_ts,
            timerange,
            start_balance,
            total_pairs,
            stake_type,
            stake_amount,
            timeframe,
            end_balance,
            net_profit,
            profit_perc,
            cagr,
            sortino,
            sharpe,
            profit_factor,
            expectancy,
            drawdown,
            calmar_ratio,
            wins,
            draws,
            losses,
            total_trades,
            win_perc,
            draws_perc,
            loss_perc,
            risk_per_trade,
            pairs_with_profit,
            pairs_with_profit_perc,
            trade_count_long,
            trade_count_short,
            profit_mean,
            profit_median,
            profit_total,
            profit_total_long,
            profit_total_short,
            profit_total_abs,
            profit_total_long_abs,
            profit_total_short_abs,
            calmar,
            stoploss,
            total_volume,
            trades_per_day,
            market_change,
            stake_currency,
            rejected_signals,
            max_open_trades,
            trailing_stop,
            trailing_stop_positive,
            trailing_stop_positive_offset,
            trailing_only_offset_is_reached,
            use_custom_stoploss,
            use_exit_signal,
            exit_profit_only,
            exit_profit_offset,
            ignore_roi_if_entry_signal,
            backtest_best_day,
            backtest_worst_day,
            backtest_best_day_abs,
            backtest_worst_day_abs,
            winning_days,
            draw_days,
            losing_days,
            holding_avg,
            holding_avg_s,
            winner_holding_avg,
            winner_holding_avg_s,
            loser_holding_avg,
            loser_holding_avg_s,
            max_drawdown,
            max_relative_drawdown,
            max_drawdown_abs,
            drawdown_start,
            drawdown_start_ts,
            drawdown_end,
            drawdown_end_ts,
            max_drawdown_low,
            max_drawdown_high,
            csum_min,
            csum_max,
            h_timestamp,
            u_timestamp,
            strategy_remark,
            hyperopt,
            positive_streaks_high,
            positive_streaks_average,
            negative_streaks_high,
            negative_streaks_average,
            tf_trades_avg,
            percentage_difference
        ),
    )

    conn.commit()
    conn.close()


def insert_strategy_name_and_filename(strategy_name, strategy_filename):
    conn = sqlite3.connect(db_path + db_name)
    c = conn.cursor()

    c.execute(
        "INSERT INTO strategies_tested (strategy_name, strategy_filename) VALUES (?, ?)",
        (strategy_name, strategy_filename),
    )

    conn.commit()
    conn.close()

# Initial database and tables creation section


def check_tables_exist_and_have_data():
    """
    please provide python function script to check if all tables exists and contain any information .
    """
    # Connect to the database
    conn = sqlite3.connect(db_path + db_name)
    c = conn.cursor()

    # Get a list of all tables in the database
    c.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = c.fetchall()

    # Check each table for data
    for table in tables:
        c.execute(f"SELECT COUNT(*) FROM {table[0]}")
        count = c.fetchone()[0]
        if count == 0:
            print(f"Table '{table[0]}' exists but has no data.")
        else:
            print(f"Table '{table[0]}' exists and has {count} rows of data.")

    # Close the database connection
    conn.close()


def initial_create_database_and_tables():
    """
    This function checks for the existence of database and tables and, if non existend,
    will create these.
    """
    if os.path.isdir(db_path):
        print(
            f"\nThe directory {db_path} already exists."
        )
    else:
        os.makedirs(db_path)
        print(f"Created directory for {db_path} for the database")

    if not os.path.exists(db_path + db_name):
        # create a connection to the database
        # logging.warning("Database '/db/stratscorer.db' does not exist. Creating...")
        logging.warning(
            f"Database {db_path}{db_name} does not exist. Creating...")
        conn = sqlite3.connect(db_path + db_name)
        c = conn.cursor()

        # ===========================================================
        # backtest_results table where backtest results are inserted
        # ===========================================================

        # check if the table exists
        c.execute(
            "SELECT count(name) FROM sqlite_master WHERE type='table' AND name='backtest_results'"
        )
        if c.fetchone()[0] == 0:
            # create a table called "backtest_results" with the specified columns (87) and data types
            logging.warning(
                "Table 'backtest_results' does not exist. Creating...")
            c.execute(
                """CREATE TABLE IF NOT EXISTS backtest_results (
                            strategy_name TEXT,
                            strategy_filename TEXT,
                            results_filename TEXT NOT NULL PRIMARY KEY,
                            exchange TEXT,
                            strategy_type TEXT,
                            bt_start_date TEXT,
                            bt_start_date_ts REAL,
                            bt_end_date TEXT,
                            bt_end_date_ts REAL,
                            timerange TEXT,
                            start_balance INTEGER,
                            total_pairs INTEGER,
                            stake_type TEXT,
                            stake_amount TEXT,
                            timeframe TEXT,
                            end_balance REAL,
                            net_profit REAL,
                            profit_perc REAL,
                            cagr REAL,
                            sortino REAL,
                            sharpe REAL,
                            profit_factor REAL,
                            expectancy REAL,
                            drawdown REAL,
                            calmar_ratio REAL,
                            wins INTEGER,
                            draws INTEGER,
                            losses INTEGER,
                            total_trades INTEGER,
                            win_perc REAL,
                            draws_perc REAL,
                            loss_perc REAL,
                            risk_per_trade REAL,
                            pairs_with_profit INTEGER,
                            pairs_with_profit_perc REAL,
                            trade_count_long INTEGER,
                            trade_count_short INTEGER,
                            profit_mean REAL,
                            profit_median REAL,
                            profit_total REAL,
                            profit_total_long REAL,
                            profit_total_short REAL,
                            profit_total_abs REAL,
                            profit_total_long_abs REAL,
                            profit_total_short_abs REAL,
                            calmar REAL,
                            stoploss REAL,
                            total_volume REAL,
                            trades_per_day REAL,
                            market_change REAL,
                            stake_currency TEXT,
                            rejected_signals INTEGER,
                            max_open_trades INTEGER,
                            trailing_stop TEXT,
                            trailing_stop_positive REAL,
                            trailing_stop_positive_offset REAL,
                            trailing_only_offset_is_reached TEXT,
                            use_custom_stoploss TEXT,
                            use_exit_signal TEXT,
                            exit_profit_only TEXT,
                            exit_profit_offset REAL,
                            ignore_roi_if_entry_signal TEXT,
                            backtest_best_day REAL,
                            backtest_worst_day REAL,
                            backtest_best_day_abs REAL,
                            backtest_worst_day_abs REAL,
                            winning_days INTEGER,
                            draw_days INTEGER,
                            losing_days INTEGER,
                            holding_avg TEXT,
                            holding_avg_s INTEGER,
                            winner_holding_avg TEXT,
                            winner_holding_avg_s INTEGER,
                            loser_holding_avg TEXT,
                            loser_holding_avg_s INTEGER,
                            max_drawdown REAL,
                            max_relative_drawdown REAL,
                            max_drawdown_abs REAL,
                            drawdown_start TEXT,
                            drawdown_start_ts REAL,
                            drawdown_end TEXT,
                            drawdown_end_ts REAL,
                            max_drawdown_low REAL,
                            max_drawdown_high REAL,
                            csum_min REAL,
                            csum_max REAL,
                            h_timestamp TEXT,
                            u_timestamp INTEGER,
                            strategy_remark TEXT,
                            hyperopt TEXT,
                            positive_streaks_high INTEGER,
                            positive_streaks_average INTEGER,
                            negative_streaks_high INTEGER,
                            negative_streaks_average INTEGER,
                            tf_trades_avg REAL,
                            percentage_difference REAL
                            )"""
            )

        # =============================
        # strategy scoring table
        # =============================

        # check if the table exists
        c.execute(
            "SELECT count(name) FROM sqlite_master WHERE type='table' AND name='strategy_scores'"
        )
        if c.fetchone()[0] == 0:
            logging.warning(
                "Table 'strategy_scores' does not exist. Creating...")
            c.execute(
                """CREATE TABLE IF NOT EXISTS strategy_scores
                        (strategy_name TEXT ,
                        timeframe TEXT ,
                        results_filename TEXT NOT NULL PRIMARY KEY,
                        profit_score REAL ,
                        winrate_score REAL ,
                        cagr_score REAL ,
                        drawdown_score REAL ,
                        calmar_ratio_score REAL ,
                        sortino_score REAL ,
                        sharpe_score REAL ,
                        profit_factor_score REAL ,
                        profitable_pairs_ratio_score REAL ,
                        expectancy_score REAL ,
                        trade_perc_punishment_score REAL ,
                        total_score REAL ,
                        u_timestamp INTEGER)"""
            )

        # =============================
        # strategies tested table
        # =============================

        # check if the table exists
        c.execute(
            "SELECT count(name) FROM sqlite_master WHERE type='table' AND name='strategies_tested'"
        )
        if c.fetchone()[0] == 0:
            logging.warning(
                "Table 'strategies_tested' does not exist. Creating...")
            c.execute(
                """CREATE TABLE IF NOT EXISTS strategies_tested
                            (strategy_name TEXT, strategy_filename TEXT)"""
            )

        # ============================
        # profit_score table & values
        # ============================

        # check if the table exists
        c.execute(
            "SELECT count(name) FROM sqlite_master WHERE type='table' AND name='profit_score'"
        )
        if c.fetchone()[0] == 0:
            logging.warning("Table 'profit_score' does not exist. Creating...")
            c.execute(
                """CREATE TABLE IF NOT EXISTS profit_score
                        (score INTEGER PRIMARY KEY, metric_low REAL, metric_high REAL)"""
            )

            # Check if the table is empty and insert rows if it is
            c.execute("""SELECT COUNT(*) FROM profit_score""")
            if c.fetchone()[0] == 0:
                scores = [
                    (-100, -110, 0),
                    (5, 0, 1),
                    (7, 1, 2),
                    (10, 2, 3),
                    (15, 3, 4),
                    (23, 4, 5),
                    (20, 5, 7),
                    (25, 7, 10),
                    (27, 10, 15),
                    (30, 15, 20),
                    (33, 20, 25),
                    (35, 25, 30),
                    (37, 30, 35),
                    (40, 35, 40),
                    (43, 40, 45),
                    (45, 45, 50),
                    (47, 50, 55),
                    (50, 55, 60),
                    (53, 60, 65),
                    (56, 65, 70),
                    (60, 70, 1000),
                ]
                c.executemany(
                    "INSERT INTO profit_score VALUES (?, ?, ?)", scores)

        # =============================
        # drawdown_score table & values
        # =============================

        # check if the table exists
        c.execute(
            "SELECT count(name) FROM sqlite_master WHERE type='table' AND name='drawdown_score'"
        )
        if c.fetchone()[0] == 0:
            logging.warning(
                "Table 'drawdown_score' does not exist. Creating...")
            c.execute(
                """CREATE TABLE IF NOT EXISTS drawdown_score
                        (score INTEGER PRIMARY KEY, metric_low REAL, metric_high REAL)"""
            )

            # Check if the table is empty and insert rows if it is
            c.execute("""SELECT COUNT(*) FROM drawdown_score""")
            if c.fetchone()[0] == 0:
                scores = [
                    (55, 0.00, 0.05),
                    (50, 0.05, 0.10),
                    (45, 0.10, 0.15),
                    (40, 0.15, 0.20),
                    (30, 0.20, 0.25),
                    (25, 0.25, 0.30),
                    (20, 0.30, 0.35),
                    (17, 0.35, 0.37),
                    (15, 0.37, 0.40),
                    (13, 0.40, 0.43),
                    (10, 0.43, 0.45),
                    (5, 0.45, 0.50),
                    (2, 0.50, 0.57),
                    (0, 0.57, 1.10),
                ]
                c.executemany(
                    "INSERT INTO drawdown_score VALUES (?, ?, ?)", scores)

        # =================================
        # risk_of_ruin_score table & values
        # =================================

        # check if the table exists
        c.execute(
            "SELECT count(name) FROM sqlite_master WHERE type='table' AND name='risk_of_ruin_score'"
        )
        if c.fetchone()[0] == 0:
            logging.warning(
                "Table 'risk_of_ruin_score' does not exist. Creating...")
            c.execute(
                """CREATE TABLE IF NOT EXISTS risk_of_ruin_score
                        (score INTEGER PRIMARY KEY, metric_low REAL, metric_high REAL)"""
            )

            # Check if the table is empty and insert rows if it is
            c.execute("""SELECT COUNT(*) FROM risk_of_ruin_score""")
            if c.fetchone()[0] == 0:
                scores = [
                    (9, 0, 3),
                    (8, 3, 5),
                    (7, 5, 15),
                    (6, 15, 25),
                    (5, 25, 50),
                    (4, 50, 100),
                    (3, 100, 125),
                    (2, 125, 150),
                    (1, 150, 200),
                    (0, 200, 1000),
                ]
                c.executemany(
                    "INSERT INTO risk_of_ruin_score VALUES (?, ?, ?)", scores)

        # ===========================================
        # profitable_pairs_ratio_score table & values
        # ===========================================

        # check if the table exists
        c.execute(
            "SELECT count(name) FROM sqlite_master WHERE type='table' AND name='profitable_pairs_ratio_score'"
        )
        if c.fetchone()[0] == 0:
            logging.warning(
                "Table 'profitable_pairs_ratio_score' does not exist. Creating..."
            )
            c.execute(
                """CREATE TABLE IF NOT EXISTS profitable_pairs_ratio_score
                        (score INTEGER PRIMARY KEY, metric_low REAL, metric_high REAL)"""
            )

            # Check if the table is empty and insert rows if it is
            c.execute("""SELECT COUNT(*) FROM profitable_pairs_ratio_score""")
            if c.fetchone()[0] == 0:
                scores = [
                    (-25, 0.00, 0.20),
                    (-20, 0.20, 0.30),
                    (-15, 0.30, 0.40),
                    (-10, 0.40, 0.50),
                    (-5, 0.50, 0.55),
                    (10, 0.55, 0.60),
                    (20, 0.60, 0.65),
                    (30, 0.65, 0.70),
                    (40, 0.70, 0.75),
                    (50, 0.75, 0.80),
                    (60, 0.80, 0.85),
                    (70, 0.85, 1.10),
                ]
                c.executemany(
                    "INSERT INTO profitable_pairs_ratio_score VALUES (?, ?, ?)", scores
                )

        # ============================
        # winrate_score table & values
        # ============================

        # check if the table exists
        c.execute(
            "SELECT count(name) FROM sqlite_master WHERE type='table' AND name='winrate_score'"
        )
        if c.fetchone()[0] == 0:
            logging.warning(
                "Table 'winrate_score' does not exist. Creating...")
            c.execute(
                """CREATE TABLE IF NOT EXISTS winrate_score
                        (score INTEGER PRIMARY KEY, metric_low REAL, metric_high REAL)"""
            )

            # Check if the table is empty and insert rows if it is
            c.execute("""SELECT COUNT(*) FROM winrate_score""")
            if c.fetchone()[0] == 0:
                scores = [
                    (-5, -2.00, 0.00),
                    (5, 0.00, 0.10),
                    (7, 0.10, 0.15),
                    (10, 0.15, 0.20),
                    (13, 0.20, 0.25),
                    (15, 0.25, 0.30),
                    (17, 0.30, 0.35),
                    (20, 0.35, 0.40),
                    (23, 0.40, 0.45),
                    (25, 0.45, 0.50),
                    (27, 0.50, 0.55),
                    (30, 0.55, 0.60),
                    (33, 0.60, 0.65),
                    (35, 0.65, 0.70),
                    (37, 0.70, 0.75),
                    (40, 0.75, 0.80),
                    (43, 0.80, 0.85),
                    (45, 0.85, 0.90),
                    (47, 0.90, 0.95),
                    (50, 0.95, 1.00),
                    (0, 1.50, 2.00),
                ]
                c.executemany(
                    "INSERT INTO winrate_score VALUES (?, ?, ?)", scores)

        # =========================
        # cagr_score table & values
        # =========================

        # check if the table exists
        c.execute(
            "SELECT count(name) FROM sqlite_master WHERE type='table' AND name='cagr_score'"
        )
        if c.fetchone()[0] == 0:
            logging.warning("Table 'cagr_score' does not exist. Creating...")
            c.execute(
                """CREATE TABLE IF NOT EXISTS cagr_score
                        (score INTEGER PRIMARY KEY, metric_low REAL, metric_high REAL)"""
            )

            # Check if the table is empty and insert rows if it is
            c.execute("""SELECT COUNT(*) FROM cagr_score""")
            if c.fetchone()[0] == 0:
                scores = [
                    (5, -2.00, 0.10),
                    (10, 0.10, 0.20),
                    (15, 0.20, 0.30),
                    (20, 0.30, 0.40),
                    (25, 0.40, 0.50),
                    (30, 0.50, 0.60),
                    (35, 0.60, 0.70),
                    (40, 0.70, 0.80),
                    (45, 0.80, 0.90),
                    (50, 0.90, 1.00),
                    (55, 1.00, 2.00),
                ]
                c.executemany(
                    "INSERT INTO cagr_score VALUES (?, ?, ?)", scores)

        # ===========================
        # calmar_score table & values
        # ===========================

        # check if the table exists
        c.execute(
            "SELECT count(name) FROM sqlite_master WHERE type='table' AND name='calmar_score'"
        )
        if c.fetchone()[0] == 0:
            logging.warning("Table 'calmar_score' does not exist. Creating...")
            c.execute(
                """CREATE TABLE IF NOT EXISTS calmar_score
                        (score INTEGER PRIMARY KEY, metric_low REAL, metric_high REAL)"""
            )

            # Check if the table is empty and insert rows if it is
            c.execute("""SELECT COUNT(*) FROM calmar_score""")
            if c.fetchone()[0] == 0:
                scores = [
                    (-10, -10000, -50),
                    (-5, -50, 0),
                    (10, 0, 1),
                    (20, 1, 2),
                    (30, 2, 3),
                    (35, 3, 100),
                ]
                c.executemany(
                    "INSERT INTO calmar_score VALUES (?, ?, ?)", scores)

        # =================================
        # calmar_ratio_score table & values
        # =================================

        # check if the table exists
        c.execute(
            "SELECT count(name) FROM sqlite_master WHERE type='table' AND name='calmar_ratio_score'"
        )
        if c.fetchone()[0] == 0:
            logging.warning(
                "Table 'calmar_ratio_score' does not exist. Creating...")
            c.execute(
                """CREATE TABLE IF NOT EXISTS calmar_ratio_score
                        (score INTEGER PRIMARY KEY, metric_low REAL, metric_high REAL)"""
            )

            # Check if the table is empty and insert rows if it is
            c.execute("""SELECT COUNT(*) FROM calmar_ratio_score""")
            if c.fetchone()[0] == 0:
                scores = [
                    (-10, -10000, -50),
                    (-5, -50, 0),
                    (10, 0, 1),
                    (20, 1, 2),
                    (30, 2, 3),
                    (35, 3, 100),
                ]
                c.executemany(
                    "INSERT INTO calmar_ratio_score VALUES (?, ?, ?)", scores)

        # ============================
        # sortino_score table & values
        # ============================

        # check if the table exists
        c.execute(
            "SELECT count(name) FROM sqlite_master WHERE type='table' AND name='sortino_score'"
        )
        if c.fetchone()[0] == 0:
            logging.warning(
                "Table 'sortino_score' does not exist. Creating...")
            c.execute(
                """CREATE TABLE IF NOT EXISTS sortino_score
                        (score INTEGER PRIMARY KEY, metric_low REAL, metric_high REAL)"""
            )

            # Check if the table is empty and insert rows if it is
            c.execute("""SELECT COUNT(*) FROM sortino_score""")
            if c.fetchone()[0] == 0:
                scores = [
                    (-10, -10000, -50),
                    (-5, -50, 0),
                    (10, 0, 1),
                    (20, 1, 2),
                    (30, 2, 3),
                    (35, 3, 100),
                ]
                c.executemany(
                    "INSERT INTO sortino_score VALUES (?, ?, ?)", scores)

        # ===========================
        # sharpe_score table & values
        # ===========================

        # check if the table exists
        c.execute(
            "SELECT count(name) FROM sqlite_master WHERE type='table' AND name='sharpe_score'"
        )
        if c.fetchone()[0] == 0:
            logging.warning("Table 'sharpe_score' does not exist. Creating...")
            c.execute(
                """CREATE TABLE IF NOT EXISTS sharpe_score
                        (score INTEGER PRIMARY KEY, metric_low REAL, metric_high REAL)"""
            )

            # Check if the table is empty and insert rows if it is
            c.execute("""SELECT COUNT(*) FROM sharpe_score""")
            if c.fetchone()[0] == 0:
                scores = [
                    (-10, -10000, -50),
                    (-5, -50, 0),
                    (10, 0, 1),
                    (15, 1, 2),
                    (20, 2, 3),
                    (25, 3, 100),
                ]
                c.executemany(
                    "INSERT INTO sharpe_score VALUES (?, ?, ?)", scores)

        # ==================================
        # profit_factor_score table & values
        # ==================================

        # check if the table exists
        c.execute(
            "SELECT count(name) FROM sqlite_master WHERE type='table' AND name='profit_factor_score'"
        )
        if c.fetchone()[0] == 0:
            logging.warning(
                "Table 'profit_factor_score' does not exist. Creating...")
            c.execute(
                """CREATE TABLE IF NOT EXISTS profit_factor_score
                        (score INTEGER PRIMARY KEY, metric_low REAL, metric_high REAL)"""
            )

            # Check if the table is empty and insert rows if it is
            c.execute("""SELECT COUNT(*) FROM profit_factor_score""")
            if c.fetchone()[0] == 0:
                scores = [
                    (-7, -20, 0),
                    (-5, 0, 1),
                    (10, 1, 1.2),
                    (15, 1.2, 1.4),
                    (20, 1.4, 20),
                ]
                c.executemany(
                    "INSERT INTO profit_factor_score VALUES (?, ?, ?)", scores
                )

        # ======================
        # expectancy_score table
        # ======================

        # check if the table exists
        c.execute(
            "SELECT count(name) FROM sqlite_master WHERE type='table' AND name='expectancy_score'"
        )
        if c.fetchone()[0] == 0:
            logging.warning(
                "Table 'expectancy_score' does not exist. Creating...")
            c.execute(
                """CREATE TABLE IF NOT EXISTS expectancy_score
                        (score INTEGER PRIMARY KEY, metric_low REAL, metric_high REAL)"""
            )

            # Check if the table is empty and insert rows if it is
            c.execute("""SELECT COUNT(*) FROM expectancy_score""")
            if c.fetchone()[0] == 0:
                scores = [
                    (-5, -2.0, -0.1),
                    (10, -0.1, 0),
                    (15, 0, 0.1),
                    (20, 0.1, 0.2),
                    (25, 0.2, 0.5),
                    (30, 0.5, 2.0),
                ]
                c.executemany(
                    "INSERT INTO expectancy_score VALUES (?, ?, ?)", scores)

        # ======================
        # PUNISHMENTS: trade_perc_deviation_punishment table
        # ======================
        # Punishes strategies that deviate negatively from the average amount of trades on that timeframe

        # check if the table exists
        c.execute(
            "SELECT count(name) FROM sqlite_master WHERE type='table' AND name='trade_perc_deviation_punishment'"
        )
        if c.fetchone()[0] == 0:
            logging.warning(
                "Table 'trade_perc_deviation_punishment' does not exist. Creating...")
            c.execute(
                """CREATE TABLE IF NOT EXISTS trade_perc_deviation_punishment
                        (score INTEGER PRIMARY KEY, metric_low REAL, metric_high REAL)"""
            )

            # Check if the table is empty and insert rows if it is
            c.execute(
                """SELECT COUNT(*) FROM trade_perc_deviation_punishment""")
            if c.fetchone()[0] == 0:
                scores = [
                    (0, 0, 60),
                    (-12, 61, 100),
                    (-23, 101, 150),
                    (-34, 151, 200),
                    (-45, 201, 2000),
                ]
                c.executemany(
                    "INSERT INTO trade_perc_deviation_punishment VALUES (?, ?, ?)", scores)

        # commit the changes and close the connection
        conn.commit()
        conn.close()
    else:
        print(f"Database {db_name} and tables exist.")


def initial_create_league_database_and_tables():
    """
    This function checks for the existence of the strategy league database and tables and,
    if non existend, will create these.
    """
    if not os.path.exists(db_path + league_db_name):
        # create a connection to the database
        logging.warning(
            f"Database {db_path}{league_db_name} does not exist. Creating..."
        )
        conn = sqlite3.connect(db_path + league_db_name)
        c = conn.cursor()

        # ===========================================================
        # strategy_league table where backtest results are inserted
        # ===========================================================

        # check if the table exists
        c.execute(
            "SELECT count(name) FROM sqlite_master WHERE type='table' AND name='strategy_league'"
        )
        if c.fetchone()[0] == 0:
            # create a table called "strategy_league" with the specified columns (87) and data types
            logging.warning(
                "Table 'strategy_league' does not exist. Creating...")
            c.execute(
                """CREATE TABLE IF NOT EXISTS strategy_league (
                            strategy_name TEXT,
                            strategy_filename TEXT,
                            timeframe TEXT,
                            profit_perc REAL,
                            win_perc REAL,
                            cagr REAL,
                            drawdown REAL,
                            calmar_ratio REAL,
                            sortino REAL,
                            sharpe REAL,
                            profit_factor REAL,
                            pairs_with_profit_perc REAL,
                            total_score REAL,
                            u_timestamp INTEGER,
                            results_filename TEXT NOT NULL PRIMARY KEY,
                            hyperopt TEXT,
                            strategy_remark TEXT
                            )"""
            )

        # commit the changes and close the connection
        conn.commit()
        conn.close()
    else:
        print(f"Database {league_db_name} and tables exist.")

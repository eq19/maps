#!/usr/bin/python3
# coding=utf-8

import json
import logging
import sqlite3
import os
from config import *

# =========== Creation of dababase and tables ===========


def initial_create_pair_results_database_and_tables():
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

    if not os.path.exists(db_path + pair_results_db_name):
        # create a connection to the database
        logging.warning(
            f"Database {db_path}{pair_results_db_name} does not exist. Creating...")
        conn = sqlite3.connect(db_path + pair_results_db_name)
        c = conn.cursor()

        # ===========================================================
        # Best pair table
        # ===========================================================

        # check if the table exists
        c.execute(
            "SELECT count(name) FROM sqlite_master WHERE type='table' AND name='best_pair'"
        )
        if c.fetchone()[0] == 0:
            logging.warning("Table 'best pair' does not exist. Creating...")
            c.execute(
                """CREATE TABLE IF NOT EXISTS best_pair (
                            key TEXT,
                            trades INTEGER,
                            profit_mean REAL,
                            profit_mean_pct REAL,
                            profit_sum REAL,
                            profit_sum_pct REAL,
                            profit_total_abs REAL,
                            profit_total REAL,
                            profit_total_pct REAL,
                            duration_avg TEXT,
                            wins INTEGER,
                            draws INTEGER,
                            losses INTEGER,
                            strategy_name TEXT,
                            results_filename TEXT NOT NULL PRIMARY KEY,
                            timeframe TEXT,
                            timerange TEXT
                            )"""
            )

        # ===========================================================
        # worst pair table
        # ===========================================================

        # check if the table exists
        c.execute(
            "SELECT count(name) FROM sqlite_master WHERE type='table' AND name='worst_pair'"
        )
        if c.fetchone()[0] == 0:
            logging.warning(
                "Table 'worst pair' does not exist. Creating...")
            c.execute(
                """CREATE TABLE IF NOT EXISTS worst_pair (
                            key TEXT,
                            trades INTEGER,
                            profit_mean REAL,
                            profit_mean_pct REAL,
                            profit_sum REAL,
                            profit_sum_pct REAL,
                            profit_total_abs REAL,
                            profit_total REAL,
                            profit_total_pct REAL,
                            duration_avg TEXT,
                            wins INTEGER,
                            draws INTEGER,
                            losses INTEGER,
                            strategy_name TEXT,
                            results_filename TEXT NOT NULL PRIMARY KEY,
                            timeframe TEXT,
                            timerange TEXT
                            )"""
            )

        # commit the changes and close the connection
        conn.commit()
        conn.close()
    else:
        print(f"Database {pair_results_db_name} and tables exist.")


def import_best_pair_data():
    """
    This function reads the contents of all JSON files in the specified import directory.
    """
    # Connect to the SQLite database
    conn = sqlite3.connect(db_path + pair_results_db_name)
    c = conn.cursor()

    json_files = [file for file in os.listdir(
        import_dir) if file.endswith('.json')]
    json_data = []

    for file_name in json_files:
        with open(os.path.join(import_dir, file_name)) as of:
            data = json.load(of)

            # Strategy data
            strategy_name = data["strategy_comparison"][0].get("key")
            results_filename = file_name  # Index value for the database
            timeframe = data["strategy"][strategy_name]["timeframe"]
            timerange = data["strategy"][strategy_name]["timerange"]

            # Best pair data
            key = data["strategy"][strategy_name]["best_pair"]["key"]
            trades = data["strategy"][strategy_name]["best_pair"]["trades"]
            profit_mean = data["strategy"][strategy_name]["best_pair"]["profit_mean"]
            profit_mean_pct = data["strategy"][strategy_name]["best_pair"]["profit_mean_pct"]
            profit_sum = data["strategy"][strategy_name]["best_pair"]["profit_sum"]
            profit_sum_pct = data["strategy"][strategy_name]["best_pair"]["profit_sum_pct"]
            profit_total_abs = data["strategy"][strategy_name]["best_pair"]["profit_total_abs"]
            profit_total = data["strategy"][strategy_name]["best_pair"]["profit_total"]
            profit_total_pct = data["strategy"][strategy_name]["best_pair"]["profit_total_pct"]
            duration_avg = data["strategy"][strategy_name]["best_pair"]["duration_avg"]
            wins = data["strategy"][strategy_name]["best_pair"]["wins"]
            draws = data["strategy"][strategy_name]["best_pair"]["draws"]
            losses = data["strategy"][strategy_name]["best_pair"]["losses"]

            # Check if the results_filename already exists in the table
            c.execute(
                "SELECT results_filename FROM best_pair WHERE results_filename = ?", (results_filename,))
            existing_file = c.fetchone()

            if existing_file:
                print(
                    f"Skipping file '{results_filename}' as it already exists in the best pair table.")
                continue

            # Insert the data into the SQLite table
            try:
                c.execute("""
                    INSERT INTO best_pair (
                        key, trades, profit_mean, profit_mean_pct, profit_sum, profit_sum_pct,
                        profit_total_abs, profit_total, profit_total_pct, duration_avg,
                        wins, draws, losses, strategy_name, results_filename, timeframe, timerange
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    key, trades, profit_mean, profit_mean_pct, profit_sum, profit_sum_pct,
                    profit_total_abs, profit_total, profit_total_pct, duration_avg,
                    wins, draws, losses, strategy_name, results_filename, timeframe, timerange
                ))
            except sqlite3.IntegrityError:
                print(
                    f"Error: File '{results_filename}' already exists in the best pair table. Skipping insertion.")

    conn.commit()
    conn.close()


def import_worst_pair_data():
    """
    This function reads the contents of all JSON files in the specified import directory.
    """
    # Connect to the SQLite database
    conn = sqlite3.connect(db_path + pair_results_db_name)
    c = conn.cursor()

    json_files = [file for file in os.listdir(
        import_dir) if file.endswith('.json')]
    json_data = []

    for file_name in json_files:
        with open(os.path.join(import_dir, file_name)) as of:
            data = json.load(of)

            # Strategy data
            strategy_name = data["strategy_comparison"][0].get("key")
            results_filename = file_name  # Index value for the database
            timeframe = data["strategy"][strategy_name]["timeframe"]
            timerange = data["strategy"][strategy_name]["timerange"]

            # worst pair data
            key = data["strategy"][strategy_name]["worst_pair"]["key"]
            trades = data["strategy"][strategy_name]["worst_pair"]["trades"]
            profit_mean = data["strategy"][strategy_name]["worst_pair"]["profit_mean"]
            profit_mean_pct = data["strategy"][strategy_name]["worst_pair"]["profit_mean_pct"]
            profit_sum = data["strategy"][strategy_name]["worst_pair"]["profit_sum"]
            profit_sum_pct = data["strategy"][strategy_name]["worst_pair"]["profit_sum_pct"]
            profit_total_abs = data["strategy"][strategy_name]["worst_pair"]["profit_total_abs"]
            profit_total = data["strategy"][strategy_name]["worst_pair"]["profit_total"]
            profit_total_pct = data["strategy"][strategy_name]["worst_pair"]["profit_total_pct"]
            duration_avg = data["strategy"][strategy_name]["worst_pair"]["duration_avg"]
            wins = data["strategy"][strategy_name]["worst_pair"]["wins"]
            draws = data["strategy"][strategy_name]["worst_pair"]["draws"]
            losses = data["strategy"][strategy_name]["worst_pair"]["losses"]

            # Check if the results_filename already exists in the table
            c.execute(
                "SELECT results_filename FROM worst_pair WHERE results_filename = ?", (results_filename,))
            existing_file = c.fetchone()

            if existing_file:
                print(
                    f"Skipping file '{results_filename}' as it already exists in the worst pair table.")
                continue

            # Insert the data into the SQLite table
            try:
                c.execute("""
                    INSERT INTO worst_pair (
                        key, trades, profit_mean, profit_mean_pct, profit_sum, profit_sum_pct,
                        profit_total_abs, profit_total, profit_total_pct, duration_avg,
                        wins, draws, losses, strategy_name, results_filename, timeframe, timerange
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    key, trades, profit_mean, profit_mean_pct, profit_sum, profit_sum_pct,
                    profit_total_abs, profit_total, profit_total_pct, duration_avg,
                    wins, draws, losses, strategy_name, results_filename, timeframe, timerange
                ))
            except sqlite3.IntegrityError:
                print(
                    f"Error: File '{results_filename}' already exists in the worst pair table. Skipping insertion.")

    conn.commit()
    conn.close()


def import_pair_data():
    """
    This function reads the contents of all JSON files in the specified import directory.
    """
    # Connect to the SQLite database
    conn = sqlite3.connect(db_path + pair_results_db_name)
    c = conn.cursor()

    json_files = [file for file in os.listdir(
        import_dir) if file.endswith('.json')]
    json_data = []

    for file_name in json_files:
        with open(os.path.join(import_dir, file_name)) as of:
            data = json.load(of)

            # Strategy data
            strategy_name = data["strategy_comparison"][0].get("key")
            results_filename = file_name  # Index value for the database
            timeframe = data["strategy"][strategy_name]["timeframe"]
            timerange = data["strategy"][strategy_name]["timerange"]

            # Get all results per pair for this strategy
            pairs = data["strategy"][strategy_name]["results_per_pair"]

            # all rows but the last one (TOTAL)
            # for pair in pairs[:-1]:
            for pair in pairs:
                # strategy_name = strategy_name
                # results_filename = results_filename
                key = pair["key"]
                trades = pair["trades"]
                profit_mean = pair["profit_mean"]
                profit_mean_pct = pair["profit_mean_pct"]
                profit_sum = pair["profit_sum"]
                profit_sum_pct = pair["profit_sum_pct"]
                profit_total_abs = pair["profit_total_abs"]
                profit_total = pair["profit_total"]
                profit_total_pct = pair["profit_total_pct"]
                duration_avg = pair["duration_avg"]
                wins = pair["wins"]
                draws = pair["draws"]
                losses = pair["losses"]

                # print(key, trades, profit_mean, profit_mean_pct, profit_sum, profit_sum_pct,
                #       profit_total_abs, profit_total, profit_total_pct, duration_avg,
                #       wins, draws, losses, strategy_name, results_filename, timeframe, timerange)

                # check if the table exists
                c.execute(
                    f"SELECT count(name) FROM sqlite_master WHERE type='table' AND name='results_per_pair_{key}'"
                )
                if c.fetchone()[0] == 0:
                    logging.warning(
                        f"Table 'results per pair' for pair {key} does not exist. Creating...")
                    c.execute(
                        f"""CREATE TABLE IF NOT EXISTS "results_per_pair_{key}" (
                                    key TEXT,
                                    trades INTEGER,
                                    profit_mean REAL,
                                    profit_mean_pct REAL,
                                    profit_sum REAL,
                                    profit_sum_pct REAL,
                                    profit_total_abs REAL,
                                    profit_total REAL,
                                    profit_total_pct REAL,
                                    duration_avg TEXT,
                                    wins INTEGER,
                                    draws INTEGER,
                                    losses INTEGER,
                                    strategy_name TEXT,
                                    results_filename TEXT NOT NULL PRIMARY KEY,
                                    timeframe TEXT,
                                    timerange TEXT
                                    )"""
                    )

                # Check if the results_filename already exists in the table
                c.execute(
                    f"SELECT results_filename FROM 'results_per_pair_{key}' WHERE results_filename = ?", (results_filename,))
                existing_file = c.fetchone()

                if existing_file:
                    print(
                        f"Skipping file '{results_filename}' as it already exists in the pair table.")
                    continue

                # Insert the data into the SQLite table
                try:
                    c.execute(f"""
                        INSERT INTO "results_per_pair_{key}" (
                            key, trades, profit_mean, profit_mean_pct, profit_sum, profit_sum_pct,
                            profit_total_abs, profit_total, profit_total_pct, duration_avg,
                            wins, draws, losses, strategy_name, results_filename, timeframe, timerange
                        )
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        key, trades, profit_mean, profit_mean_pct, profit_sum, profit_sum_pct,
                        profit_total_abs, profit_total, profit_total_pct, duration_avg,
                        wins, draws, losses, strategy_name, results_filename, timeframe, timerange
                    ))
                except sqlite3.IntegrityError:
                    print(
                        f"Error: File '{results_filename}' already exists in the pair table. Skipping insertion.")

    conn.commit()
    conn.close()


initial_create_pair_results_database_and_tables()
import_best_pair_data()
import_worst_pair_data()
import_pair_data()

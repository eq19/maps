#!/usr/bin/python3
# coding=utf-8
import csv
import subprocess
import os
import ftplib
import time
import data_output
from datetime import datetime
import sqlite3
from prettytable import PrettyTable
from config import *
from private import *
from start import create_strategy_logdir, main

# Global variables here
h_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
u_timestamp = datetime.now().strftime("%s")
timestr = time.strftime("%Y%m%d-%H%M%S")
cust_epochs = 500
cust_workers = -4


def ftp_upload():
    """
    In this script, you would need to replace the values for ftp_server, ftp_user, ftp_password, ftp_directory,
    and local_directory with the appropriate values for your specific use case. This script assumes that the files
    in the local directory are to be uploaded to the root directory of the remote FTP server directory, so you
    may need to modify the ftp_directory variable to include the subdirectory you wish to upload the files to.
    """
    from getpass import getpass

    # FTP connection details in private.py
    FTP_USERNAME = input("\nEnter the FTP user name: ")
    # FTP_PASSWORD = input("Enter the FTP password: ")
    FTP_PASSWORD = getpass()

    # Connect to FTP server
    ftp = ftplib.FTP(ftp_server)
    ftp.login(user=FTP_USERNAME, passwd=FTP_PASSWORD)

    # Change to the remote directory where files will be uploaded
    ftp.cwd(remote_path)

    # Loop through files in local directory and upload each file to the remote directory
    for filename in os.listdir(league_dir):
        local_path = os.path.join(league_dir, filename)
        if os.path.isfile(local_path):
            with open(local_path, "rb") as f:
                ftp.storbinary(f"STOR {filename}", f)

    # Close FTP connection
    ftp.quit()


def create_strategy_logdir(strategy_name):
    strategy_dir = logs_dir + strategy_name

    # Check if directory already exists
    if os.path.isdir(strategy_dir):
        print(
            f"\nThe directory {strategy_name} already exists. \nFiles will be added to this directory."
        )
    else:
        # Create directory for strategy
        os.makedirs(strategy_dir)
        print(f"Created directory for {strategy_name} for the Freqtrade files")

    return strategy_dir


def hyperopt():
    """Function that contains the full Freqtrade backtest command

    Args:
        strategy (str): The strategy that will be tested
        strategy_type (str): The type of strategy (spot/futures)
        timeframe (str): The timeframe where the strategy will be tested
    """
    # Ask for the filename and timeframe
    strategy_filename = input(
        "\nEnter the strategy FILENAME (e.g. AverageStrategy.py): "
    )
    strategy_timeframe = input(
        "Enter the strategy TIMEFRAME (e.g. 1d, 4h, 1h, 30m, 15m, 5m): "
    )
    strategy_spaces = input(
        "Using additional spaces, then add them here \n(USE: 'all', 'buy', 'sell', 'roi', 'stoploss', 'trailing', 'protection', 'trades', 'default'): "
    )

    # Open the file and read its contents
    file_path = ft_dir + strategy_dir + strategy_filename
    with open(file_path, "r") as file:
        contents = file.read()

    # Search for the variable/phrase
    if "can_short = True" in contents:
        # strategy = "futures_strategy"
        strategy_type = "futures"
    else:
        # strategy = "spot_strategy"
        strategy_type = "spot"

    # Search for the first class defined in the file
    strategy_name = None
    for line in contents.split("\n"):
        if line.startswith("class"):
            strategy_name = line.split()[1]
            strategy_name = strategy_name.replace("(IStrategy):", "").strip()
            break

    # Select the right config based on selected strategy type (spot/futures)
    if strategy_type == "spot":
        trade_config = spot_cfg
    elif strategy_type == "futures":
        trade_config = futures_cfg

    # # Filename for export trades to backtest_results directory
    # trades_output = strategy_name + "-" + strategy_type + "-" + timeframe + ".json"

    # Determine the correct timerange for the timeframes
    def multi_tf(strategy_timeframe):
        if strategy_timeframe == "30m":
            tr = ho_tr_30m
        elif strategy_timeframe == "15m":
            tr = ho_tr_15m
        elif strategy_timeframe == "5m":
            tr = ho_tr_5m
        elif strategy_timeframe == "1m":
            tr = ho_tr_1m
        else:
            tr = ho_tr

        return tr

    tr = multi_tf(strategy_timeframe)

    # Determine the correct loss function for the timeframes
    def multi_loss(strategy_timeframe):
        if strategy_timeframe == "1d":
            # loss = "SortinoHyperOptLossDaily"
            loss = "SharpeHyperOptLossDaily"
        else:
            # loss = "SortinoHyperOptLoss"
            loss = "SharpeHyperOptLoss"

        return loss

    loss = multi_loss(strategy_timeframe)

    # Determine the spaces to optimize
    def multi_spaces(strategy_spaces):
        if strategy_spaces:
            spaces = strategy_spaces
        else:
            spaces = ""

        return spaces

    spaces = multi_spaces(strategy_spaces)

    logs_dir = create_strategy_logdir(strategy_name)

    # print(
    #     f"=== Hyperparameter optimization by DUTCHCRYPTODAD of {strategy_type} strategy {strategy_name}"
    # )
    # print(
    #     f"=== Used parameters >> Timeframe: {strategy_timeframe}; Lossfunction: {loss}; Spaces: {spaces}."
    # )

    # Execute the backtest with this command
    # Experience has shown that best results are usually not improving much after 500-1000 epochs.
    program = f"{ft_dir}/.env/bin/freqtrade hyperopt --config {ft_dir}{trade_config} \
        --epochs {cust_epochs} --random-state 12345 --job-workers {cust_workers} \
        --timeframe {strategy_timeframe} \
        --spaces {spaces} \
        --hyperopt-loss {loss} \
        --strategy  {strategy_name} \
        --timerange {tr}"

    # --epochs 500 --random-state 12345 --job-workers -4 \

    # output to logfile in logs dir
    def log_output(program):
        # logs_dir = "./logs"
        # os.makedirs(logs_dir, exist_ok=True)

        logfile_path = os.path.join(
            logs_dir,
            f"hyperopt-output-{strategy_name}-{strategy_timeframe}-{h_timestamp}-{u_timestamp}.log",
        )

        with open(logfile_path, "w") as logfile:
            # Custom log line
            logfile.write(
                f"=== Hyperparameter optimization by DUTCHCRYPTODAD of {strategy_type} strategy {strategy_name}\n"
            )
            logfile.write(
                f"=== Used parameters >> Timeframe: {strategy_timeframe}; Lossfunction: {loss}; Spaces: {spaces}.\n"
            )
            logfile.write(
                f"=== Visit my website: https://www.dutchalgotrading.com for more information\n"
            )
            logfile.write(
                f"=== or become a Patreon supporter on: https://www.patreon.com/dutchalgotrading\n"
            )
            process = subprocess.Popen(
                program, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True
            )
            for line in process.stdout:
                line = line.decode().strip()
                print(line)
                logfile.write(line + "\n")
            process.wait()

        return logfile_path

    log_output(program)


def manual_backtest():
    strategy_filename = input(
        "\nEnter the filename (e.g. AverageStrategy.py) of the strategy to manually test: "
    )
    timeframe = input(
        "Specify timeframe for the backtest (e.g. 1d, 4h, 1h, 30m, 15m, 5m): "
    )
    remark = input("Add an additional remark to add to the log output: ")

    # Open the file and read its contents
    file_path = ft_dir + strategy_dir + strategy_filename
    with open(file_path, "r") as file:
        contents = file.read()

    # Search for the variable/phrase
    if "can_short = True" in contents:
        # strategy = "futures_strategy"
        strategy_type = "futures"
        trade_config = futures_cfg
    elif "can_short: bool = True" in contents:
        # strategy = "futures_strategy"
        strategy_type = "futures"
        trade_config = futures_cfg
    else:
        # strategy = "spot_strategy"
        strategy_type = "spot"
        trade_config = spot_cfg

    # Determine the correct timerange for the timeframes
    def multi_tf(timeframe):
        if timeframe == "30m":
            tr = bt_tr_30m
        elif timeframe == "15m":
            tr = bt_tr_15m
        elif timeframe == "5m":
            tr = bt_tr_5m
        elif timeframe == "1m":
            tr = bt_tr_1m
        else:
            tr = bt_tr

        return tr

    tr = multi_tf(timeframe)

    # Search for the first class defined in the file
    strategy_name = None
    for line in contents.split("\n"):
        if line.startswith("class"):
            strategy_name = line.split()[1]
            strategy_name = strategy_name.replace("(IStrategy):", "").strip()
            break
    print(
        f'The  {strategy_type} with name  {strategy_name} and remark "{remark}", will be tested!'
    )

    # Filename for export trades to backtest_results directory
    trades_output = strategy_name + "-" + strategy_type + "-" + timeframe + ".json"

    create_strategy_logdir(strategy_name)

    # Execute the backtest with this command
    program = f"{ft_dir}/.env/bin/freqtrade backtesting --config {ft_dir}{trade_config} \
        --strategy {strategy_name} --timeframe {timeframe} --timerange={tr} \
        --export trades --export-filename {ft_dir}/user_data/backtest_results/{trades_output} \
        --datadir {ft_dir}/user_data/data/{crypto_exch}"

    # output to logfile in logs dir
    def log_output(program):
        # logs_dir = "./logs"
        # os.makedirs(logs_dir, exist_ok=True)

        logfile_path = os.path.join(
            logs_dir,
            strategy_name,
            # strategy_dir,
            f"backtest-output-{strategy_name}-{timeframe}-{remark}-{h_timestamp}-{u_timestamp}.log",
        )

        with open(logfile_path, "w") as logfile:
            # Custom log line
            logfile.write(
                f"=== Backtest by DUTCHCRYPTODAD of {strategy_name}-{timeframe} on {h_timestamp}\n"
            )
            logfile.write(
                f"=== Visit my website: https://www.dutchalgotrading.com for more information\n"
            )
            logfile.write(
                f"=== or become a Patreon supporter on: https://www.patreon.com/dutchalgotrading\n"
            )
            process = subprocess.Popen(
                program, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True
            )
            for line in process.stdout:
                line = line.decode().strip()
                print(line)
                logfile.write(line + "\n")
            process.wait()

        return logfile_path

    log_output(program)


def list_strategies():
    directory = '/opt/freqtrade/user_data/strategies'
    for filename in os.listdir(directory):
        print(filename)


def open_file_in_nano():
    directory = '/opt/freqtrade/user_data/strategies'
    """Opens a file in the nano text editor in a specified directory."""
    filename = input(
        "\nPlease enter the strategy filename to edit: ")  # Get user input for the filename
    file_path = os.path.join(directory, filename)  # Create the full file path
    if os.path.isfile(file_path):  # Check if the file exists
        os.system(f'nano {file_path}')  # Open the file in nano
    else:
        # Display error message if file not found
        print(f'Error: {filename} not found in {directory}')


def add_column_to_table():
    # Connect to the SQLite database
    conn = sqlite3.connect(db_path + db_name)
    cursor = conn.cursor()
    your_table = "backtest_results"

    # Prompt the user for column name and type
    column_name = input("\nEnter the column name: ")

    column_type = None
    while column_type not in ['T', 'I', 'R']:
        column_type = input(
            "Enter the column type (T for TEXT, I for INTEGER, R for REAL): ").upper()

    if column_type == 'T':
        column_type = 'TEXT'
    elif column_type == 'I':
        column_type = 'INTEGER'
    elif column_type == 'R':
        column_type = 'REAL'

    # Alter the table to add the new column
    alter_query = f"ALTER TABLE {your_table} ADD COLUMN {column_name} {column_type};"
    cursor.execute(alter_query)
    conn.commit()

    # Close the connection
    conn.close()


def export_strategy_data_to_csv():
    # Prompt the user for the strategy name
    strategy_name = input(
        "\nEnter the strategy name to export (CASE SENSITIVE): ")

    # Connect to the databases
    stratscorer_db = sqlite3.connect(db_path + db_name)
    strategy_league_db = sqlite3.connect(db_path + league_db_name)

    # Create a cursor for each database
    stratscorer_cursor = stratscorer_db.cursor()
    strategy_league_cursor = strategy_league_db.cursor()

    # Check if the strategy exists in the tables
    stratscorer_cursor.execute(
        "SELECT strategy_name FROM backtest_results WHERE strategy_name=?", (strategy_name,))
    strategy_exists_in_backtest_results = bool(stratscorer_cursor.fetchone())

    # Check if the strategy exists in the tables
    stratscorer_cursor.execute(
        "SELECT strategy_name FROM strategy_scores WHERE strategy_name=?", (strategy_name,))
    strategy_exists_in_strategy_scores = bool(stratscorer_cursor.fetchone())

    strategy_league_cursor.execute(
        "SELECT strategy_name FROM strategy_league WHERE strategy_name=?", (strategy_name,))
    strategy_exists_in_strategy_league = bool(
        strategy_league_cursor.fetchone())

    stratscorer_cursor.execute(
        "SELECT strategy_name FROM strategies_tested WHERE strategy_name=?", (strategy_name,))
    strategy_exists_in_strategies_tested = bool(stratscorer_cursor.fetchone())

    if not (strategy_exists_in_backtest_results or strategy_exists_in_strategy_scores or strategy_exists_in_strategy_league or strategy_exists_in_strategies_tested):
        print("Strategy does not exist in the database.")
        return

    # Create the export directory if it doesn't exist
    export_directory = './export/'
    if not os.path.exists(export_directory):
        os.makedirs(export_directory)

    # Export data from the backtest_results table
    backtest_results_csv_filename = f"./export/backtest_results_{strategy_name}.csv"
    stratscorer_cursor.execute(
        "SELECT * FROM backtest_results WHERE strategy_name=?", (strategy_name,))
    backtest_results_data = stratscorer_cursor.fetchall()

    with open(backtest_results_csv_filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(backtest_results_data)

    print(f"Data exported to {backtest_results_csv_filename}.")

    # Export data from the strategy_scores table
    strategy_scores_csv_filename = f"./export/strategy_scores_{strategy_name}.csv"
    stratscorer_cursor.execute(
        "SELECT * FROM strategy_scores WHERE strategy_name=?", (strategy_name,))
    strategy_scores_data = stratscorer_cursor.fetchall()

    with open(strategy_scores_csv_filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(strategy_scores_data)

    print(f"Data exported to {strategy_scores_csv_filename}.")

    # Export data from the strategy_league table
    strategy_league_csv_filename = f"./export/strategy_league_{strategy_name}.csv"
    strategy_league_cursor.execute(
        "SELECT * FROM strategy_league WHERE strategy_name=?", (strategy_name,))
    strategy_league_data = strategy_league_cursor.fetchall()

    with open(strategy_league_csv_filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(strategy_league_data)

    print(f"Data exported to {strategy_league_csv_filename}.")

    # Export data from the strategies_tested table
    strategies_tested_csv_filename = f"./export/strategies_tested_{strategy_name}.csv"
    stratscorer_cursor.execute(
        "SELECT * FROM strategies_tested WHERE strategy_name=?", (strategy_name,))
    strategies_tested_data = stratscorer_cursor.fetchall()

    with open(strategies_tested_csv_filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(strategies_tested_data)

    print(f"Data exported to {strategies_tested_csv_filename}.")

    # Close the database connections
    stratscorer_db.close()
    strategy_league_db.close()

    print(
        f"Data exported successfully. Files saved in the '{export_directory}' directory.")


def import_strategy_data_from_csv():
    # Prompt the user for the strategy name
    strategy_name = input(
        "\nEnter the strategy name to import (CASE SENSITIVE): ")

    # Derive the CSV filenames based on the strategy name
    backtest_results_csv_filename = f"./export/backtest_results_{strategy_name}.csv"
    strategy_scores_csv_filename = f"./export/strategy_scores_{strategy_name}.csv"
    strategy_league_csv_filename = f"./export/strategy_league_{strategy_name}.csv"
    strategies_tested_csv_filename = f"./export/strategies_tested_{strategy_name}.csv"

    # Connect to the databases
    stratscorer_db = sqlite3.connect(db_path + db_name)
    # stratscorer_db = sqlite3.connect('stratscorer.db')
    strategy_league_db = sqlite3.connect(db_path + league_db_name)
    # strategy_league_db = sqlite3.connect('strategy_league.db')

    # Create a cursor for each database
    stratscorer_cursor = stratscorer_db.cursor()
    strategy_league_cursor = strategy_league_db.cursor()

    # Check if strategy name already exists in all tables
    stratscorer_cursor.execute(
        "SELECT strategy_name FROM backtest_results WHERE strategy_name=?", (strategy_name,))
    strategy_name_exists_in_backtest_results = bool(
        stratscorer_cursor.fetchone())

    stratscorer_cursor.execute(
        "SELECT strategy_name FROM strategy_scores WHERE strategy_name=?", (strategy_name,))
    strategy_name_exists_in_strategy_scores = bool(
        stratscorer_cursor.fetchone())

    stratscorer_cursor.execute(
        "SELECT strategy_name FROM strategies_tested WHERE strategy_name=?", (strategy_name,))
    strategy_name_exists_in_strategies_tested = bool(
        stratscorer_cursor.fetchone())

    strategy_league_cursor.execute(
        "SELECT strategy_name FROM strategy_league WHERE strategy_name=?", (strategy_name,))
    strategy_name_exists_in_strategy_league = bool(
        strategy_league_cursor.fetchone())

    # Check if results_filename already exists in the strategy_league and backtest_results tables
    try:
        # Import data into the backtest_results table
        if strategy_name_exists_in_backtest_results and os.path.isfile(backtest_results_csv_filename):
            print(
                "Data for the strategy name already exists in the backtest_results table. Skipping import.")
        else:
            with open(backtest_results_csv_filename, 'r') as csvfile:
                print(f"Importing {backtest_results_csv_filename}.")
                reader = csv.reader(csvfile)
                # next(reader)  # Skip the header row

                for row in reader:
                    stratscorer_cursor.execute(
                        # "INSERT INTO backtest_results (column1, column2, column3, column4) VALUES (?, ?, ?, ?)", row)
                        "INSERT INTO backtest_results (strategy_name, strategy_filename, results_filename, exchange, strategy_type, bt_start_date, bt_start_date_ts, bt_end_date, bt_end_date_ts, timerange, start_balance, total_pairs, stake_type, stake_amount, timeframe, end_balance, net_profit, profit_perc, cagr, sortino, sharpe, profit_factor, expectancy, drawdown, calmar_ratio, wins, draws, losses, total_trades, win_perc, draws_perc, loss_perc, risk_per_trade, pairs_with_profit, pairs_with_profit_perc, trade_count_long, trade_count_short, profit_mean, profit_median, profit_total, profit_total_long, profit_total_short, profit_total_abs, profit_total_long_abs, profit_total_short_abs, calmar, stoploss, total_volume, trades_per_day, market_change, stake_currency, rejected_signals, max_open_trades, trailing_stop, trailing_stop_positive, trailing_stop_positive_offset, trailing_only_offset_is_reached, use_custom_stoploss, use_exit_signal, exit_profit_only, exit_profit_offset, ignore_roi_if_entry_signal, backtest_best_day, backtest_worst_day, backtest_best_day_abs, backtest_worst_day_abs, winning_days, draw_days, losing_days, holding_avg, holding_avg_s, winner_holding_avg, winner_holding_avg_s, loser_holding_avg, loser_holding_avg_s, max_drawdown, max_relative_drawdown, max_drawdown_abs, drawdown_start, drawdown_start_ts, drawdown_end, drawdown_end_ts, max_drawdown_low, max_drawdown_high, csum_min, csum_max, h_timestamp, u_timestamp, strategy_remark, hyperopt, positive_streaks_high, positive_streaks_average, negative_streaks_high, negative_streaks_average, tf_trades_avg, percentage_difference) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", row)

        # Import data into the strategy_scores table
        if strategy_name_exists_in_strategy_scores and os.path.isfile(strategy_scores_csv_filename):
            print(
                "Data for the strategy name already exists in the strategy_scores table. Skipping import.")
        else:
            with open(strategy_scores_csv_filename, 'r') as csvfile:
                print(f"Importing {strategy_scores_csv_filename}.")
                reader = csv.reader(csvfile)
                # next(reader)  # Skip the header row

                for row in reader:
                    stratscorer_cursor.execute(
                        # "INSERT INTO strategy_scores (column1, column2, column3, column4) VALUES (?, ?, ?, ?)", row)
                        "INSERT INTO strategy_scores (strategy_name,timeframe,results_filename,profit_score,winrate_score,cagr_score,drawdown_score,calmar_ratio_score,sortino_score,sharpe_score,profit_factor_score,profitable_pairs_ratio_score,expectancy_score,trade_perc_punishment_score,total_score,u_timestamp) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", row)

        # Import data into the strategy_league table
        if strategy_name_exists_in_strategy_league and os.path.isfile(strategy_league_csv_filename):
            print(
                "Data for the strategy name already exists in the strategy_league table. Skipping import.")
        else:
            with open(strategy_league_csv_filename, 'r') as csvfile:
                print(f"Importing {strategy_league_csv_filename}.")
                reader = csv.reader(csvfile)
                # next(reader)  # Skip the header row

                for row in reader:
                    strategy_league_cursor.execute(
                        # "INSERT INTO strategy_league (column1, column2, column3) VALUES (?, ?, ?)", row)
                        "INSERT INTO strategy_league (strategy_name, strategy_filename, timeframe, profit_perc, win_perc, cagr, drawdown, calmar_ratio, sortino, sharpe, profit_factor, pairs_with_profit_perc, total_score, u_timestamp, results_filename, hyperopt, strategy_remark) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", row)

        # Import data into the strategies_tested table
        if strategy_name_exists_in_strategies_tested and os.path.isfile(strategies_tested_csv_filename):
            print(
                "Data for the strategy name already exists in the strategies_tested table. Skipping import.")
        else:
            with open(strategies_tested_csv_filename, 'r') as csvfile:
                print(f"Importing {strategies_tested_csv_filename}.")
                reader = csv.reader(csvfile)
                # next(reader)  # Skip the header row

                for row in reader:
                    stratscorer_cursor.execute(
                        # "INSERT INTO strategies_tested (column1, column2, column3) VALUES (?, ?, ?)", row)
                        "INSERT INTO strategies_tested (strategy_name, strategy_filename) VALUES (?, ?)", row)

        # Commit the changes to the databases
        stratscorer_db.commit()
        strategy_league_db.commit()

        print("Data imported successfully.")
    except Exception as e:
        print(f"An error occurred during import: {str(e)}")

    # Close the database connections
    stratscorer_db.close()
    strategy_league_db.close()


def delete_strategy():
    # Prompt the user to enter the strategy name
    strategy_name = input(
        "\nEnter the strategy name to DELETE (CASE SENSITIVE): ")

    # Connect to the 'stratscorer.db' database
    conn_stratscorer = sqlite3.connect(db_path + db_name)
    cursor_stratscorer = conn_stratscorer.cursor()

    # Connect to the 'strategy_league.db' database
    conn_strategy_league = sqlite3.connect(db_path + league_db_name)
    cursor_strategy_league = conn_strategy_league.cursor()

    try:
        # Check if the strategy name exists in 'strategies_tested' table in 'stratscorer.db'
        cursor_stratscorer.execute(
            "SELECT strategy_name FROM strategies_tested WHERE strategy_name = ?", (strategy_name,))
        result_stratscorer = cursor_stratscorer.fetchone()

        # Check if the strategy name exists in 'backtest_results' table in 'stratscorer.db'
        cursor_stratscorer.execute(
            "SELECT strategy_name FROM backtest_results WHERE strategy_name = ?", (strategy_name,))
        result_stratscorer_backtest = cursor_stratscorer.fetchone()

        # Check if the strategy name exists in 'strategy_scores' table in 'stratscorer.db'
        cursor_stratscorer.execute(
            "SELECT strategy_name FROM strategy_scores WHERE strategy_name = ?", (strategy_name,))
        result_stratscorer_score = cursor_stratscorer.fetchone()

        # Check if the strategy name exists in 'strategy_league' table in 'strategy_league.db'
        cursor_strategy_league.execute(
            "SELECT strategy_name FROM strategy_league WHERE strategy_name = ?", (strategy_name,))
        result_strategy_league = cursor_strategy_league.fetchone()

        if result_stratscorer or result_stratscorer_backtest or result_stratscorer_score or result_strategy_league:
            # Delete entries from 'strategies_tested' table in 'stratscorer.db'
            cursor_stratscorer.execute(
                "DELETE FROM strategies_tested WHERE strategy_name = ?", (strategy_name,))
            conn_stratscorer.commit()

            # Delete entries from 'backtest_results' table in 'stratscorer.db'
            cursor_stratscorer.execute(
                "DELETE FROM backtest_results WHERE strategy_name = ?", (strategy_name,))
            conn_stratscorer.commit()

            # Delete entries from 'strategy_scores' table in 'stratscorer.db'
            cursor_stratscorer.execute(
                "DELETE FROM strategy_scores WHERE strategy_name = ?", (strategy_name,))
            conn_stratscorer.commit()

            # Delete entries from 'strategy_league' table in 'strategy_league.db'
            cursor_strategy_league.execute(
                "DELETE FROM strategy_league WHERE strategy_name = ?", (strategy_name,))
            conn_strategy_league.commit()

            print(
                f"Deletion of strategy {strategy_name} completed successfully.")

        else:
            print("")
            print(
                f"Strategy name {strategy_name} does not exist in the tables. \nUse case sensitive strategy name here!")

    except sqlite3.Error as e:
        print("Error occurred during deletion:", e)

    finally:
        # Close the database connections
        cursor_stratscorer.close()
        conn_stratscorer.close()
        cursor_strategy_league.close()
        conn_strategy_league.close()


def menu():
    while True:
        print("\nMenu:")
        print("===== OUTPUT SECTION =====")
        print("1. SHOW STRATEGY LEAGUE")
        print("2. SHOW STRATEGY DB ENTRY")
        print("3. SHOW WINNNING TIMEFRAME OVERVIEW")
        print("")
        print("===== BACKTEST SECTION =====")
        print("4. LIST OF AVAILABLE STRATEGY FILES")
        print("5. RUN MANUAL BACKTEST (test if strategy works)")
        print("6. START MAIN STRATSCORER PROGRAM")
        print("7. HYPEROPT STRATEGY")
        print("8. UPLOAD LEAGUE FILE TO DAT WEBSITE")
        print("9. OPEN A STRATEGY FILE IN NANO")
        print("")
        print("===== !!! DANGER SECTION !!! =====")
        print("10.ADD COLUMN TO STRATSCORER.DB, DATABASE_RESULTS TABLE")
        print("11.EXPORT STRATEGY ENTRY TO CSV FILE")
        print("12.IMPORT STRATEGY ENTRY TO DATABASES")
        print("13.REMOVE STRATEGY ENTRY FROM DATABASE")
        print("E. EXIT")
        choice = input("Enter your choice: ").lower()

        if choice == "1":
            data_output.show_strategy_league_table()
        elif choice == "2":
            strat = input("Enter strategy name: ")
            data_output.print_backtest_results(strat)
        elif choice == "3":
            data_output.get_winner_overview()
        elif choice == "4":
            list_strategies()
        elif choice == "5":
            manual_backtest()
        elif choice == "6":
            main()
        elif choice == "7":
            hyperopt()
        elif choice == "8":
            ftp_upload()
        elif choice == "9":
            open_file_in_nano()
        elif choice == "10":
            add_column_to_table()
        elif choice == "11":
            export_strategy_data_to_csv()
        elif choice == "12":
            import_strategy_data_from_csv()
        elif choice == "13":
            delete_strategy()
        elif choice == "E".casefold():
            break
        else:
            print("Invalid choice. Please try again.")


menu()

#!/usr/bin/python3
# coding=utf-8
from prettytable import PrettyTable
from config import *
from decorators import *
import os
import csv
import subprocess
import shutil
from datetime import datetime
from functools import wraps


@db_league_connection
def print_terminal_league_entry(conn):
    """
    This function prints the specific best league entry at the end of the backtests on the 
    terminal screen in table format. This will be shown after the backtest results overview.
    """
    c = conn.cursor()

    c.execute(
        """SELECT strategy_name, timeframe,
                   ROUND(profit_perc * 100, 2), ROUND(win_perc * 100, 2),
                   ROUND(cagr, 2), ROUND(drawdown * 100, 2),
                   ROUND(calmar_ratio, 2), ROUND(sortino, 2), ROUND(sharpe, 2),
                   ROUND(profit_factor, 2), ROUND(pairs_with_profit_perc * 100, 2),
                   ROUND(total_score, 2), u_timestamp, hyperopt
            FROM strategy_league
            ORDER BY u_timestamp DESC
            LIMIT 1"""
    )

    rows = c.fetchall()

    if not rows:
        print("No results found in backtest_results table.")
        return

    headers = [
        "Strategy",
        "TF",
        "Profit % ",
        "Winrate %",
        "CAGR",
        "Drawdown %",
        "Calmar",
        "Sortino",
        "Sharpe",
        "Profit fact.",
        "Pairs %",
        "Best Score",
        "Timestamp",
        "HO",
    ]
    max_lengths = [len(header) for header in headers]
    for row in rows:
        for i, value in enumerate(row):
            max_lengths[i] = max(max_lengths[i], len(str(value)))

    row_format = " | ".join(["{{:<{}}}".format(length)
                            for length in max_lengths])
    print("")
    print(
        f"               =============== BEST SCORED TIMEFRAME FOR STRATEGY: {row[0]} is {row[1]} timeframe =============== "
    )
    print("-" * (sum(max_lengths) + len(max_lengths) * 3 - 1))
    print(row_format.format(*headers))
    print("-" * (sum(max_lengths) + len(max_lengths) * 3 - 1))
    for row in rows:
        # Convert percentage values to human-readable format
        row = list(row)
        row[2] = "{:.2%}".format(float(row[2]) / 100)  # profit
        row[3] = "{:.2%}".format(float(row[3]) / 100)  # winrate
        row[5] = "{:.2%}".format(float(row[5]) / 100)  # drawdown
        row[10] = "{:.0%}".format(float(row[10]) / 100)  # pairs
        row[11] = "{:}".format(int(row[11]))  # score

        print(row_format.format(*row))
    print("-" * (sum(max_lengths) + len(max_lengths) * 3 - 1))
    print("")


@db_connection
def print_backtest_results(conn, strategy_name=None):
    """
    This function prints the backtest results at the end of the backtests on the
    terminal screen in table format.
    """
    strategy_name = strategy_name.lower()
    c = conn.cursor()

    c.execute(
        """SELECT 
                    strategy_scores.timeframe AS "TF",
                    round(backtest_results.end_balance, 2) AS "End Balance",
                    round(backtest_results.profit_perc, 2) AS "Profit %",
                    round(backtest_results.win_perc, 2) AS "Win %",
                    round(backtest_results.cagr, 2) AS "CAGR",
                    round(backtest_results.drawdown, 2) AS "Drawdown",
                    round(backtest_results.calmar_ratio, 2) AS "Calmar Ratio",
                    round(backtest_results.sortino, 2) AS "Sortino",
                    round(backtest_results.sharpe, 2) AS "Sharpe",
                    round(backtest_results.profit_factor, 2) AS "Profit Factor",
                    round(backtest_results.pairs_with_profit_perc, 2) AS "Pairs %",
                    round(strategy_scores.total_score, 2) AS "Total Score",
                    backtest_results.hyperopt AS "Hyperopt",
                    backtest_results.positive_streaks_high AS "W.str.Max", 
                    backtest_results.positive_streaks_average AS "W.str.Avg",
                    backtest_results.negative_streaks_high AS "L.str.Max",
                    backtest_results.negative_streaks_average AS "L.str.Avg",
                    backtest_results.total_trades AS "Trades"
                FROM backtest_results
                JOIN strategy_scores ON backtest_results.results_filename = strategy_scores.results_filename
                WHERE lower(backtest_results.strategy_name) = ?
                ORDER BY backtest_results.u_timestamp DESC, strategy_scores.total_score DESC, backtest_results.sharpe DESC, backtest_results.sortino DESC""",
        (strategy_name,),
    )

    # get the column names and the results
    # col_names = [desc[0] for desc in c.description]
    col_names = [
        "TF",
        "Endbalance",
        "Profit%",
        "Trades",
        "Win%",
        "W.str.M/A",
        "L.str.M/A",
        "CAGR",
        "Drawdown",
        "Calmar",
        "Sortino",
        "Sharpe",
        "Profit F",
        "Pairs%",
        "Score",
        "HO"
    ]

    rows = c.fetchall()

    # create a prettytable and add the column names
    table = PrettyTable(col_names)

    # add the results to the table
    for row in rows:
        # Format the profit percentage and win percentage columns as percentages with 2 decimal places
        profit_perc = "{:.0f}%".format(float(row[2]) * 100)
        win_perc = "{:.0f}%".format(float(row[3]) * 100)

        # Format the CAGR, drawdown, Calmar, Sortino, Sharpe, and profit factor columns as decimals with 2 decimal places
        cagr = "{:.2f}".format(row[4])
        drawdown = "{:.0f}%".format(float(row[5]) * 100)
        calmar_ratio = "{:.2f}".format(row[6])
        sortino = "{:.2f}".format(row[7])
        sharpe = "{:.2f}".format(row[8])
        profit_factor = "{:.2f}".format(row[9])

        # Format the pairs with profit percentage column as a percentage with 2 decimal places, or as "N/A" if the value is NULL
        pairs_with_profit_perc = (
            "{:.0f}%".format(float(row[10]) *
                             100) if row[10] is not None else "N/A"
        )
        score = "{:.0f}".format(float(row[11]))

        winstreak = "{}/{}".format(row[13], row[14])  # Winstr.M/A
        losestreak = "{}/{}".format(row[15], row[16])  # Losestr.M/A

        # Add the formatted row to the table
        table.add_row(
            [
                row[0],
                row[1],
                profit_perc,
                row[17],
                win_perc,
                winstreak,
                losestreak,
                cagr,
                drawdown,
                calmar_ratio,
                sortino,
                sharpe,
                profit_factor,
                pairs_with_profit_perc,
                score,
                row[12],
            ]
        )

    # set the column names as the table headers
    table.field_names = col_names

    # print the table to the terminal
    print()
    print(table.get_string(
        title=f"Strategy: {strategy_name.upper()}. Timerange: 201801-202301. Pairs: ~50.  === WARNING: Backtest results give absolutely no guarantees for future performance!! ==="))


@db_connection
def export_backtest_to_csv(conn, strategy_name=None, u_timestamp=None):
    """
    This function will take the complete backtest results table and exports it to CSV
    format for backup purposes.
    """
    print(
        f"\nExporting csv data for {strategy_name} on timestamp {u_timestamp}.")
    c = conn.cursor()

    c.execute(
        """
        SELECT 
            backtest_results.strategy_name,
            strategy_scores.timeframe,
            backtest_results.start_balance, 
            backtest_results.end_balance,
            backtest_results.profit_perc,
            backtest_results.win_perc,
            backtest_results.cagr,
            backtest_results.drawdown,
            backtest_results.calmar_ratio,
            backtest_results.sortino,
            backtest_results.sharpe,
            backtest_results.profit_factor,
            backtest_results.pairs_with_profit_perc,
            strategy_scores.total_score,
            backtest_results.u_timestamp,
            backtest_results.hyperopt,
            backtest_results.strategy_remark
        FROM backtest_results
        JOIN strategy_scores ON backtest_results.results_filename = strategy_scores.results_filename
        WHERE backtest_results.strategy_name = ?
        AND backtest_results.u_timestamp = ?
        ORDER BY
        strategy_scores.u_timestamp DESC, strategy_scores.total_score
    """,
        (strategy_name, u_timestamp),
    )

    rows = c.fetchall()

    if not rows:
        print("No results found in backtest_results table.")
        return

    headers = [
        "Strategy Name",
        "Start balance",
        "End balance",
        "Timeframe",
        "Profit %",
        "Winrate %",
        "CAGR",
        "Drawdown %",
        "Calmar Ratio",
        "Sortino",
        "Sharpe",
        "Profit Factor",
        "Pairs w Profit %",
        "Total Score",
        "Timestamp",
        "Hyperopt",
        "Remark",
    ]

    # Check if CSV file already exists and if backtest_results.hyperopt value is True
    strategy_name = rows[0][0]
    timeframe = rows[0][3]
    u_timestamp = rows[0][14]
    csv_filename = f"{strategy_name}-{u_timestamp}.csv"
    csv_filepath = os.path.join(logs_dir, strategy_name, csv_filename)
    if os.path.exists(csv_filepath) and rows[0][15]:
        with open(csv_filepath, "a", newline="") as f:
            csv_writer = csv.writer(f)
            for row in rows:
                csv_writer.writerow(row)
        print(f"CSV data added to existing file {csv_filepath}.")
    else:
        with open(csv_filepath, "w", newline="") as f:
            csv_writer = csv.writer(f)
            csv_writer.writerow(headers)
            for row in rows:
                csv_writer.writerow(row)
        print(f"CSV exported to {csv_filepath}.")


@db_league_connection
def export_league_to_csv(conn):
    """
    This function exports the strategy league to CSV. This CSV will be used for the strategy
    league overview on the dutchalgotrading.com website!
    """
    print("\nExporting strategy league table to CSV.")
    c = conn.cursor()

    c.execute(
        """SELECT strategy_name, timeframe, 
                   ROUND(profit_perc * 100, 2), ROUND(win_perc * 100, 2),
                   ROUND(cagr, 2), ROUND(drawdown * 100, 2),
                   ROUND(calmar_ratio, 2), ROUND(sortino, 2), ROUND(sharpe, 2),
                   ROUND(profit_factor, 2), ROUND(pairs_with_profit_perc * 100, 2),
                   ROUND(total_score, 2), u_timestamp, hyperopt
            FROM strategy_league
            ORDER BY total_score DESC
            """
    )

    rows = c.fetchall()

    if not rows:
        print("No results found in backtest_results table.")
        return

    headers = [
        "Strategy",
        "TF",
        "Profit % ",
        "Winrate %",
        "CAGR",
        "Drawdown %",
        "Calmar",
        "Sortino",
        "Sharpe",
        "Profit fact.",
        "Pairs %",
        "Best Score",
        "Timestamp",
        "HO",
    ]

    folder = f"{logs_dir}strategy_league/"
    if not os.path.exists(folder):
        os.makedirs(folder)

    file_path = folder + "strategy_league.csv"

    with open(file_path, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        writer.writerows(rows)

    print(f"Exported strategy league to {file_path}")


@db_connection
def export_all_backtest_results_to_csv(conn):
    print("\nExporting backtest_results table to CSV.")

    c = conn.cursor()

    c.execute(
        """
        SELECT
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

        FROM backtest_results
    """
    )

    rows = c.fetchall()

    if not rows:
        print("No results found in backtest_results table.")
        return

    headers = [
        "Strategy Name",
        "Strategy Filename",
        "Results Filename",
        "Exchange",
        "Strategy Type",
        "BT Start Date",
        "BT Start Date TS",
        "BT End Date",
        "BT End Date TS",
        "Timerange",
        "Start Balance",
        "Total Pairs",
        "Stake Type",
        "Stake Amount",
        "Timeframe",
        "End Balance",
        "Net Profit",
        "Profit %",
        "CAGR",
        "Sortino",
        "Sharpe",
        "Profit Factor",
        "Expectancy",
        "Drawdown %",
        "Calmar Ratio",
        "Wins",
        "Draws",
        "Losses",
        "Total Trades",
        "Winrate %",
        "Draws %",
        "Loss %",
        "Risk per Trade",
        "Pairs with Profit",
        "Pairs with Profit %",
        "Trade Count Long",
        "Trade Count Short",
        "Profit Mean",
        "Profit Median",
        "Profit Total",
        "Profit Total Long",
        "Profit Total Short",
        "Profit Total Abs",
        "Profit Total Long Abs",
        "Profit Total Short Abs",
        "Calmar",
        "Stoploss",
        "Total Volume",
        "Trades per Day",
        "Market Change",
        "Stake Currency",
        "Rejected Signals",
        "Max Open Trades",
        "Trailing Stop",
        "Trailing Stop Positive",
        "Trailing Stop Positive Offset",
        "Trailing Only Offset is Reached",
        "Use Custom Stoploss",
        "Use Exit Signal",
        "Exit Profit Only",
        "Exit Profit Offset",
        "Ignore ROI if Entry Signal",
        "Backtest Best Day",
        "Backtest Worst Day",
        "Backtest Best Day Abs",
        "Backtest Worst Day Abs",
        "Winning Days",
        "Draw Days",
        "Losing Days",
        "Holding Avg",
        "Holding Avg S",
        "Winner Holding Avg",
        "Winner Holding Avg S",
        "Loser Holding Avg",
        "Loser Holding Avg S",
        "Max Drawdown",
        "Max Relative Drawdown",
        "Max Drawdown Abs",
        "Drawdown Start",
        "Drawdown Start Ts",
        "Drawdown End",
        "Drawdown End Ts",
        "Max Drawdown Low",
        "Max Drawdown High",
        "Csum Min",
        "Csum Max",
        "H Timestamp",
        "U Timestamp",
        "Strategy Remark",
        "Hyperopt",
        "Highest win streak",
        "Average win streak",
        "Highest lose streak",
        "Average lose streak",
        "Timeframe average trades amount",
        "Difference perc. from trades",

    ]

    folder = f"{logs_dir}backtest_results/"
    if not os.path.exists(folder):
        os.makedirs(folder)

    file_path = folder + "backtest_results.csv"

    with open(file_path, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        writer.writerows(rows)

    print(f"Exported backtest results to {file_path}")


def move_profit_plot(strategy_name, hyperopt, results_filename):
    print(f"Moving the plot for {strategy_name}")
    # move profit plot to strategy directory and rename it
    strategy_dir = os.path.join(logs_dir, strategy_name)

    plot_file = f"freqtrade-profit-plot.html"
    if hyperopt == "1":
        new_plot_file = f"{results_filename}_hyperopt_profit-plot.html"
    elif hyperopt == "0":
        new_plot_file = f"{results_filename}_initial_profit-plot.html"
    else:
        new_plot_file = f"{results_filename}_HO_profit-plot.html"

    plot_src_path = os.path.join(ft_dir, "user_data", "plot", plot_file)
    plot_dest_path = os.path.join(strategy_dir, new_plot_file)

    try:
        # Attempt to move the file
        shutil.move(plot_src_path, plot_dest_path)
        print(f"Backtest profit plot moved to {plot_dest_path}")
    except FileNotFoundError as e:
        print(f"Error: {e}")
        print(
            f"Failed to move the profit plot for {strategy_name}. The source file does not exist.")
    except Exception as e:
        print(f"Error: {e}")
        print(
            f"Failed to move the profit plot for {strategy_name} due to an unexpected error.")

# def move_profit_plot(strategy_name, hyperopt, results_filename):
#     print(f"Moving the plot for {strategy_name}")
#     # move profit plot to strategy directory and rename it
#     strategy_dir = os.path.join(logs_dir, strategy_name)

#     plot_file = f"freqtrade-profit-plot.html"
#     if hyperopt == "1":
#         new_plot_file = f"{results_filename}_hyperopt_profit-plot.html"
#     if hyperopt == "0":
#         new_plot_file = f"{results_filename}_initial_profit-plot.html"
#     else:
#         new_plot_file = f"{results_filename}_HO_profit-plot.html"
#     plot_src_path = os.path.join(ft_dir, "user_data", "plot", plot_file)
#     plot_dest_path = os.path.join(strategy_dir, new_plot_file)
#     # shutil.copy(plot_src_path, plot_dest_path)
#     shutil.move(plot_src_path, plot_dest_path)

#     print(f"Backtest profit plot moved to {plot_dest_path}")


def create_profit_plot(strategy_name, u_timestamp):
    """This function collects the best backtest result data for the strategy tested on the current
    results_filename. And returns these values to that these can be added to the strategy league in another function.
    """
    # # Connect to the database
    conn = sqlite3.connect(db_path + db_name)
    c = conn.cursor()

    c.execute(
        """
        SELECT 
            backtest_results.timeframe,
            backtest_results.u_timestamp,
            backtest_results.results_filename,
            backtest_results.hyperopt,
            strategy_scores.total_score,
            strategy_scores.results_filename
        FROM backtest_results
        JOIN strategy_scores ON backtest_results.results_filename = strategy_scores.results_filename
        WHERE backtest_results.strategy_name = ?
        AND backtest_results.u_timestamp = ?
        ORDER BY
        strategy_scores.u_timestamp DESC, strategy_scores.total_score DESC, backtest_results.sharpe DESC, backtest_results.sortino DESC
        LIMIT
        1;
    """,
        (strategy_name, u_timestamp),
    )

    # Get the column names and data
    data = c.fetchall()

    timeframe = data[0][0]
    results_filename = data[0][2]

    if "spot" in results_filename:
        value = "spot"
        trade_config = spot_cfg
    elif "futures" in results_filename:
        value = "futures"
        trade_config = futures_cfg
    else:
        value = "Not found. Reverting to default config."
        trade_config = spot_cfg

    hyperopt = data[0][3]

    # try:
    # Make a plot
    print(
        f"\n Now creating a profit plot chart for the {timeframe} timeframe.")
    program = f"{ft_dir}/.env/bin/freqtrade plot-profit --config {ft_dir}{trade_config} --timeframe {timeframe} --export-filename {ft_dir}/user_data/backtest_results/{results_filename}"

    # Run the program using subprocess.Popen()
    process = subprocess.Popen(program, stdout=subprocess.PIPE, shell=True)

    # Wait for the program to finish executing
    output, error = process.communicate()

    # Strip the newlines from the output
    output = output.decode().strip()

    # Print the output of the program
    print(output)

    # Move the plot after create_profit_plot()
    move_profit_plot(strategy_name, hyperopt, results_filename)


def show_strategy_league_table():
    conn = sqlite3.connect(db_path + league_db_name)
    cur = conn.cursor()

    # Select the columns you want and order by the "Best Score" column in descending order
    cur.execute(
        """SELECT strategy_name, 
        timeframe, 
        profit_perc, 
        win_perc, 
        cagr, 
        drawdown, 
        calmar_ratio, 
        sortino, 
        sharpe, 
        profit_factor, 
        pairs_with_profit_perc, 
        total_score 
        FROM strategy_league 
        ORDER BY total_score DESC"""
    )
    rows = cur.fetchall()

    # Create the table headers
    table = PrettyTable()
    table.field_names = [
        "Strategy",
        "TF",
        "Profit %",
        "Winrate %",
        "CAGR",
        "Drawdown %",
        "Calmar",
        "Sortino",
        "Sharpe",
        "Profit fact.",
        "Pairs %",
        "Best Score",
    ]

    # Add each row to the table
    for row in rows:
        # Format the profit percentage and win percentage columns as percentages with 2 decimal places
        # profit_perc = "{:.2f}%".format(row[2])
        profit_perc = "{:.0f}%".format(float(row[2]) * 100)
        win_perc = "{:.0f}%".format(float(row[3]) * 100)

        # Format the CAGR, drawdown, Calmar, Sortino, Sharpe, and profit factor columns as decimals with 2 decimal places
        cagr = "{:.2f}".format(row[4])
        drawdown = "{:.0f}%".format(float(row[5]) * 100)
        calmar_ratio = "{:.2f}".format(row[6])
        sortino = "{:.2f}".format(row[7])
        sharpe = "{:.2f}".format(row[8])
        profit_factor = "{:.2f}".format(row[9])

        # Format the pairs with profit percentage column as a percentage with 2 decimal places, or as "N/A" if the value is NULL
        pairs_with_profit_perc = (
            "{:.0f}%".format(float(row[10]) *
                             100) if row[10] is not None else "N/A"
        )
        score = "{:.0f}".format(float(row[11]))

        # Add the formatted row to the table
        table.add_row(
            [
                row[0],
                row[1],
                profit_perc,
                win_perc,
                cagr,
                drawdown,
                calmar_ratio,
                sortino,
                sharpe,
                profit_factor,
                pairs_with_profit_perc,
                score,
            ]
        )

    # Print the table with a horizontal line separating the headers from the data
    print(table.get_string(title="Strategy League Table"))
    conn.commit()
    conn.close()


def get_winner_overview():
    # Prompt the user to enter a strategy name or a partial name
    strategy_name = input("Enter strategy name or part of the name: ")

    # Convert the strategy name to lowercase for case-insensitive matching
    strategy_name = strategy_name.lower()

    # Connect to the database
    conn = sqlite3.connect(db_path + db_name)
    c = conn.cursor()

    # Execute the SELECT statement with placeholders for strategy_name and current timestamp
    c.execute(
        """
        SELECT 
            backtest_results.strategy_name AS "Strategy name",
            strategy_scores.timeframe AS "Best timeframe",
            backtest_results.strategy_type AS "Strategy type",
            round(strategy_scores.total_score, 2) AS "Strategy league Score",
            backtest_results.bt_start_date AS "Backtest start date",
            backtest_results.bt_end_date AS "Backtest end date",
            backtest_results.timerange AS "Timerange configured",
            backtest_results.start_balance AS "Starting balance",
            round(backtest_results.end_balance, 2) AS "End Balance",
            backtest_results.total_pairs AS "Total pairs in backtest",
            round(backtest_results.pairs_with_profit_perc, 2) AS "Pairs with Profit %",
            backtest_results.stake_amount AS "Stake amount set",
            round(backtest_results.net_profit, 2) AS "Net Profit",
            round(backtest_results.profit_perc, 2) AS "Profit %",
            round(backtest_results.cagr, 2) AS "CAGR",
            round(backtest_results.sortino, 2) AS "Sortino",
            round(backtest_results.sharpe, 2) AS "Sharpe",
            round(backtest_results.calmar_ratio, 2) AS "Calmar Ratio",
            round(backtest_results.profit_factor, 2) AS "Profit Factor",
            round(backtest_results.expectancy, 2) AS "Expectancy",
            round(backtest_results.drawdown, 2) AS "Drawdown",
            backtest_results.wins AS "Winning trades",
            backtest_results.draws AS "Draw trades",
            backtest_results.losses AS "Losing trades",
            backtest_results.total_trades AS "Total trades",
            round(backtest_results.win_perc, 2) AS "Percentage of winning trades %",
            backtest_results.trade_count_long AS "Number of long trades",
            backtest_results.trade_count_short AS "number of short trades",
            round(backtest_results.profit_total_long, 2) AS "Profits by long trades",
            round(backtest_results.profit_total_short, 2) AS "Profits by short trades",
            round(backtest_results.profit_total, 2) AS "Profits Total",
            round(backtest_results.risk_per_trade, 2) AS "Risk per trade",
            round(backtest_results.trades_per_day, 2) AS "Trades per Day",
            backtest_results.winning_days AS "Winning days",
            backtest_results.draw_days AS "Draw days",
            backtest_results.losing_days AS "Losing days",
            round(backtest_results.holding_avg, 2) AS "Holding Avg",
            backtest_results.winner_holding_avg AS "Winner Holding Avg",
            backtest_results.loser_holding_avg AS "Loser Holding Avg",
            backtest_results.positive_streaks_high AS "Maximum winning streak", 
            backtest_results.positive_streaks_average AS "Average winning streak",
            backtest_results.negative_streaks_high AS "Maximum losing streak",
            backtest_results.negative_streaks_average AS "Average losing trades",
            backtest_results.hyperopt AS "Is optimized (1 = yes)"
        FROM backtest_results
        JOIN strategy_scores ON backtest_results.results_filename = strategy_scores.results_filename
        WHERE lower(backtest_results.strategy_name) LIKE ?
        ORDER BY
            strategy_scores.total_score DESC
        LIMIT 1
        """,
        ('%' + strategy_name + '%',),
    )

    # Get the column names and the results
    col_names = [desc[0] for desc in c.description]
    row = c.fetchone()

    # Create a PrettyTable and add the column names
    table = PrettyTable(col_names)

    import numpy as np

    # ...
    # Define a list of specific fields where a emtpy line should be added after
    specific_fields = ["Strategy league Score", "Timerange configured", "Drawdown",
                       "Short trade count", "Risk per trade", "Average losing trades"]  # Add more specific field values as needed

    if row:
        # Format the columns as needed
        formatted_row = []
        for i, value in enumerate(row):
            if isinstance(value, float):
                if i == 7:  # Format the starting balance column
                    value = "$ {:.0f}".format(float(value))
                if i == 8:  # Format the end balance column
                    value = "$ {:.0f}".format(float(value))
                if i == 10:  # Format the profit_pairs column
                    value = "{:.0f} %".format(float(value) * 100)
                if i == 12:  # Format the starting balance column
                    value = "$ {:.0f}".format(float(value))
                if i == 13:  # Format the profit_perc column
                    value = "{:.0f} %".format(float(value) * 100)
                if i == 20:  # Format the drawdown column
                    value = "{:.0f} %".format(float(value) * 100)
                if i == 25:  # Format the win_perc column
                    value = "{:.0f} %".format(float(value) * 100)
                if i == 28:  # Format the  Profits by long trades column
                    value = "{:.0f} %".format(float(value) * 100)
                if i == 29:  # Format the  Profits by short trades column
                    value = "{:.0f} %".format(float(value) * 100)
                if i == 30:  # Format the  Profits total column
                    value = "{:.0f} %".format(float(value) * 100)
                if i == 31:  # Format the Risk per trade column
                    value = "$ {:.0f}".format(float(value))

                # formatted_row.append("{:.2f}".format(value))

            formatted_row.append(str(value))

        # Transpose the formatted row
        transposed_row = np.array([formatted_row]).T

        # Create a PrettyTable and add the column names
        table = PrettyTable(["Field", "Value"])

        # Set alignment of cells to the left
        table.align["Field"] = "l"
        table.align["Value"] = "l"

        # Add the transposed row to the table
        for field, value in zip(col_names, transposed_row):
            table.add_row([field, value[0]])
            # Check if the current row is a specific row after which you want to insert an empty row
            if field in specific_fields:
                # Insert an empty row after the specific row
                table.add_row(["", ""])

        # Print the table to the terminal
        print()
        print(table)
    else:
        print("No results found for the given strategy name.")

    # Close the database connection
    conn.close()

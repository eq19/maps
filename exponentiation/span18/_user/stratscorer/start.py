#!/usr/bin/python3
# coding=utf-8
import subprocess
import os
import time
import datetime
from config import *
from data_collection import *
from decorators import *
from data_processing import *
from strat_league import *
from file_actions import *
from data_output import *
from db_functions import initial_create_database_and_tables

# Global variables here
h_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
u_timestamp = datetime.now().strftime("%s")
timestr = time.strftime("%Y%m%d-%H%M%S")


def ask_hyperopt():
    try:
        optimized = input("Is your strategy optimized with hyperopt (Y/N)?: ")

        if optimized.lower() == "y":
            hyperopt = True
            timeframe = input(
                "On which timeframe is the strategy optimized (e.g. 1d, 4h, 1h, 30m, 15m, 5m): "
            )
        elif optimized.lower() == "n":
            hyperopt = False
            timeframe = None
        else:
            raise ValueError("Invalid input.")

        print("Your strategy is optimized:", hyperopt)

        return hyperopt, timeframe

    except (ValueError, UnboundLocalError) as error:
        print("An error occurred:", str(error))
        print("Exiting the script.")
        exit(1)


def ask_strategy():
    """
    Reads a Python file located at `file_path`, searches for the variable/phrase "can_short = True",
    and returns the appropriate strategy ("futures_strategy" or "spot_strategy") and the name of
    the first class defined in the file.
    """

    # Ask for the filename
    strategy_filename = input(
        "\nEnter the strategy FILENAME (e.g. AverageStrategy.py) to test: "
    )

    # Ask if this an optimized strategy backtest
    hyperopt, timeframe = ask_hyperopt()

    # Ask for a remark
    strategy_remark = input("\nEnter a remark for this strategy if needed: ")

    # Open the file and read its contents
    file_path = ft_dir + strategy_dir + strategy_filename
    with open(file_path, "r") as file:
        contents = file.read()

    # # Search for the variable/phrase
    # if "can_short = True" in contents:
    #     # strategy = "futures_strategy"
    #     strategy_type = "futures"
    # else:
    #     # strategy = "spot_strategy"
    #     strategy_type = "spot"

    # Search for the variable/phrase
    if "can_short = True" in contents:
        # strategy = "futures_strategy"
        strategy_type = "futures"
        # trade_config = futures_cfg
    elif "can_short: bool = True" in contents:
        # strategy = "futures_strategy"
        strategy_type = "futures"
        # trade_config = futures_cfg
    else:
        # strategy = "spot_strategy"
        strategy_type = "spot"
        # trade_config = spot_cfg

    # Search for the first class defined in the file
    strategy_name = None
    for line in contents.split("\n"):
        if line.startswith("class"):
            strategy_name = line.split()[1]
            strategy_name = strategy_name.replace("(IStrategy):", "").strip()
            break
    print(
        f'The  {strategy_type} with name  {strategy_name} and remark "{strategy_remark}", will be tested!'
    )

    # return strategy, strategy_type, strategy_name, strategy_filename, strategy_remark
    return (
        strategy_type,
        strategy_name,
        strategy_filename,
        strategy_remark,
        hyperopt,
        timeframe,
    )


def backtest(strategy_type, strategy_name, timeframe):
    """Function that contains the full Freqtrade backtest command

    Args:
        strategy (str): The strategy that will be tested
        strategy_type (str): The type of strategy (spot/futures)
        timeframe (str): The timeframe where the strategy will be tested
    """
    # Select the right config based on selected strategy type (spot/futures)
    if strategy_type == "spot":
        trade_config = spot_cfg
    elif strategy_type == "futures":
        trade_config = futures_cfg

    # Filename for export trades to backtest_results directory
    trades_output = strategy_name + "-" + strategy_type + "-" + timeframe + ".json"

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
            f"backtest-output-{strategy_name}-{timeframe}-{h_timestamp}-{u_timestamp}.log",
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


def add_single_backtest(
    strategy_type,
    strategy_name,
    strategy_filename,
    strategy_remark,
    hyperopt,
    timeframe,
):
    print()
    print(
        ">>> Timeframe "
        + timeframe
        + " of strategy "
        + strategy_name
        + " will be tested next..."
    )
    print()
    # add_backtest(strategy_type, strategy_name, timeframe, strategy_filename)
    backtest(strategy_type, strategy_name, timeframe)

    # Get the output file name for each run and add this to the get_trade_results function.
    output_file = get_last_result()

    # Get the trade results from the JSON output file and
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
        positive_streaks_high,
        positive_streaks_average,
        negative_streaks_high,
        negative_streaks_average,
        tf_trades_avg,
        percentage_difference
    ) = get_trade_results(output_file, strategy_type, strategy_filename)

    # For each result received, enter the data into the stratscorer.db table 'backtest_results' (data_processing.py function)
    try:
        # Insert all the backtest results into the stratscorer.db table
        insert_backtest_results(
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
        )

    except sqlite3.IntegrityError as e:
        if "UNIQUE constraint failed: backtest_results.results_filename" in str(e):
            print("Backtest result already exists.")
        else:
            # Handle other types of IntegrityErrors
            print("An IntegrityError occurred:", e)
    else:
        print("Backtest result successfully inserted.")


def add_backtest(
    strategy_type, strategy_name, strategy_filename, strategy_remark, hyperopt
):
    # h_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # u_timestamp = datetime.now().strftime("%s")
    for timeframe in bt_tf:
        print()
        print(
            ">>> Timeframe "
            + timeframe
            + " of strategy "
            + strategy_name
            + " will be tested next..."
        )
        print()
        # add_backtest(strategy_type, strategy_name, timeframe, strategy_filename)
        backtest(strategy_type, strategy_name, timeframe)

        # Get the output file name for each run and add this to the get_trade_results function.
        output_file = get_last_result()

        # Get the trade results from the JSON output file and
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
            positive_streaks_high,
            positive_streaks_average,
            negative_streaks_high,
            negative_streaks_average,
            tf_trades_avg,
            percentage_difference
        ) = get_trade_results(output_file, strategy_type, strategy_filename)

        # For each result received, enter the data into the stratscorer.db table 'backtest_results' (data_processing.py function)
        try:
            # Insert all the backtest results into the stratscorer.db table
            insert_backtest_results(
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
            )

        except sqlite3.IntegrityError as e:
            if "UNIQUE constraint failed: backtest_results.results_filename" in str(e):
                print("Backtest result already exists.")
            else:
                # Handle other types of IntegrityErrors
                print("An IntegrityError occurred:", e)
        else:
            print("Backtest result successfully inserted.")


@timer
def timeframeRunover(
    strategy_type, strategy_name, strategy_filename, strategy_remark, hyperopt
):
    """Loops over all configured timeframes and backtests the strategy

    Args:
        strategy (str): The strategy that will be tested
        strategy_type (str): The type of strategy (spot/futures)
    """

    backtest_existence = check_strategy_backtest_existence(
        strategy_name, strategy_filename
    )

    if backtest_existence:
        print(
            f"\n!!! - WARNING: THE '{strategy_name}', WITH FILENAME: '{strategy_filename}' ALREADY EXISTS IN THE STRATEGY RESULTS DATABASE - !!!"
        )
        while True:
            try:
                strategy_addition = input(
                    "\nAre you sure you want to continue? [Y/N]: "
                )
                if strategy_addition.upper() == "Y":
                    print("You answered yes. Continuing the backtest.")
                    add_backtest(
                        strategy_type,
                        strategy_name,
                        strategy_filename,
                        strategy_remark,
                        hyperopt,
                    )
                    break
                elif strategy_addition.upper() == "N":
                    print("You answered no. Terminating the backtest.")
                    break
                else:
                    print("Please enter Y or N to quit.")
            except:
                print(
                    "\nAn error occured while backtesting. Please correct error and try again."
                )
                break
    else:
        print(
            f"The combination of strategy_name '{strategy_name}' and filename '{strategy_filename}' does not exists in the database. Proceeding..."
        )
        # Add the strategy name and filename to the strategies_tested table so that I can check if I already
        # tested this strategy
        insert_strategy_name_and_filename(strategy_name, strategy_filename)

        # Add backtest name and filename to the strategies_tested table so that I can check if it was already tested earlier.
        add_backtest(
            strategy_type, strategy_name, strategy_filename, strategy_remark, hyperopt
        )


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


def main():
    """Main function. Starts all subsequent functions to backtest the algorithmic strategies."""

    # Some introductory text
    print()
    print(
        "This script will backtest multiple timeframes of the same strategy and add all the results to a database for further analysis and ranking."
    )
    print(
        'See "freqtrade list-strategies" column "location" for the algo strategies filename that are available.'
    )
    print()

    # Determine datapath of script
    data_path = (os.path.dirname(os.path.realpath(__file__))) + (bt_data)
    # print('data lives in ' + data_path)

    # Check if the database and tables already exist
    initial_create_database_and_tables()
    initial_create_league_database_and_tables()

    # Backup the database with each run
    backup_db()

    # Ask the strategy to test
    (
        strategy_type,
        strategy_name,
        strategy_filename,
        strategy_remark,
        hyperopt,
        timeframe,
    ) = ask_strategy()

    # Create directory for storing logging and strategy files
    strategy_dir = create_strategy_logdir(strategy_name)

    # Run over all timeframes to backtest
    # In that function the strategy asked will be tested
    # and all results will be added to the database.
    if hyperopt == True:
        add_single_backtest(
            strategy_type,
            strategy_name,
            strategy_filename,
            strategy_remark,
            hyperopt,
            timeframe,
        )
    else:
        timeframeRunover(
            strategy_type, strategy_name, strategy_filename, strategy_remark, hyperopt
        )

    # Determine the scores of the timeframes of the strategy that has just ran
    print("\nStart scoring the backtest results...")
    determine_strategy_scores(strategy_name)

    # Add best score of the current backtests to the strategy league for publishing
    strategy_league_insertion(strategy_name, strategy_filename)

    # Export the individual backtest run of the strategy to the strategy folder
    export_backtest_to_csv(strategy_name, u_timestamp)

    # Export all the backtests and their results to a csv
    export_all_backtest_results_to_csv()

    # Export the strategy league to a csv file for publishing
    export_league_to_csv()

    # Create a profit plot for the best scoring timeframe
    create_profit_plot(strategy_name, u_timestamp)

    # After creating the plot move all the freqtrade backtest results to the log directory
    move_results(strategy_name, strategy_dir)

    # Copy strategy file and json if available to log dir for the strategy
    copy_strategy(strategy_name, strategy_filename, strategy_dir)

    # Copy the strategy .PY and .JSON file to my own strategies collection
    collect_strategy(strategy_filename)

    # Show the initial backtest results
    # print_initial_backtest_results(strategy_name, u_timestamp)
    print_backtest_results(strategy_name)

    # Show the output of the best timeframe to the screen
    print_terminal_league_entry()


if __name__ == "__main__":
    main()

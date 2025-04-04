#!/usr/bin/python3
# coding=utf-8
import json
import statistics
from config import *
from db_functions import *

last_result = ft_dir + "/user_data/backtest_results/.last_result.json"
# last_result = "/opt/stratscorer/temp/" + ".last_result.json"


def get_last_result():
    """This function opens the Freqtrade last_result.json file and gets the
    actual filename where all the trades data is stored.
    """
    with open(last_result) as f:
        data = json.load(f)

        for item in data.items():
            output_file = item[1]

    return output_file


def positive_pairs_counter(output_file):
    with open(ft_dir + "/user_data/backtest_results/" + output_file) as of:
        data = json.load(of)

        strategy_name = data["strategy_comparison"][0].get("key")

        results_per_pair = data["strategy"][strategy_name]["results_per_pair"]

        pairs_with_profit = 0
        for pair in results_per_pair:
            if pair["profit_total_abs"] > 0:
                pairs_with_profit = pairs_with_profit + 1

        return pairs_with_profit


def streak(output_file):
    """The streak function takes an output_file as input, reads the data from the specified file, 
    and computes various statistics related to positive and negative streaks in the trades. 
    It calculates the highest value, average, median, and mode for both positive and negative streaks. 
    Finally, it returns these computed values as a tuple.
    """
    # Open the specified output file
    with open(ft_dir + "/user_data/backtest_results/" + output_file) as of:
        # Load the data from the file
        data = json.load(of)

        # Get the strategy name from the data
        strategy_name = data["strategy_comparison"][0].get("key")

        # Get the list of trades for the strategy
        trades = data["strategy"][strategy_name]["trades"]

        # Create an array to store the absolute profits of trades
        trade_profit_abs_array = []

        # Iterate over each trade and append its absolute profit to the array
        for trade in trades:
            trade_profit_abs_array.append(trade["profit_abs"])

        # Create separate arrays to store positive and negative streaks
        positive_streaks = []
        negative_streaks = []

        # Initialize variables to keep track of current streaks
        current_positive_streak = 0
        current_negative_streak = 0

        # Iterate over each profit value in the array
        for num in trade_profit_abs_array:
            if num > 0:
                # Increment the positive streak and reset the negative streak
                current_positive_streak += 1
                current_negative_streak = 0
            elif num < 0:
                # Increment the negative streak and reset the positive streak
                current_negative_streak += 1
                current_positive_streak = 0
            else:
                # Reset both streaks to zero if the profit is zero
                current_positive_streak = 0
                current_negative_streak = 0

            # Append the current positive and negative streaks to their respective arrays
            if current_positive_streak > 0:
                positive_streaks.append(current_positive_streak)
            if current_negative_streak > 0:
                negative_streaks.append(current_negative_streak)

        # Calculate the highest, average, median, and mode of positive streaks
        positive_streaks_high = max(positive_streaks)
        positive_streaks_average = round(
            sum(positive_streaks) / len(positive_streaks))
        positive_streaks_median = statistics.median(positive_streaks)
        positive_streaks_mode = statistics.mode(positive_streaks)

        # Calculate the highest, average, median, and mode of negative streaks
        negative_streaks_high = max(negative_streaks)
        negative_streaks_average = round(
            sum(negative_streaks) / len(negative_streaks))
        negative_streaks_median = statistics.median(negative_streaks)
        negative_streaks_mode = statistics.mode(negative_streaks)

        # Return the computed values for positive and negative streaks
        return positive_streaks_high, positive_streaks_average, positive_streaks_median, positive_streaks_mode, negative_streaks_high, negative_streaks_average, negative_streaks_median, negative_streaks_mode


def calculate_average_total_trades():
    # Establish the database connection
    conn = sqlite3.connect(db_path + db_name)
    c = conn.cursor()

    # Query the database to get average total_trades for each timeframe
    c.execute(
        "SELECT timeframe, ROUND(AVG(total_trades), 2) FROM backtest_results GROUP BY timeframe")
    results = c.fetchall()

    # Create a dictionary to store the results
    average_total_trades = {}
    for row in results:
        timeframe, avg_total_trades = row
        average_total_trades[timeframe] = avg_total_trades

    # Close the database connection
    conn.close()
    # print(average_total_trades)
    return average_total_trades


def get_trade_results(output_file, strategy_type, strategy_filename):
    with open(ft_dir + "/user_data/backtest_results/" + output_file) as of:
        data = json.load(of)

        # Determine the name of the strategy in the .last_result.json file.
        # Tip: everything between {} is dict and should be called with ['name'].
        # everything between [] is list and can be called with [0].
        strategy_name = data["strategy_comparison"][0].get("key")
        strategy_filename = strategy_filename
        results_filename = output_file  # Index value for the database
        exchange = crypto_exch
        strategy_type = strategy_type
        bt_start_date = data["strategy"][strategy_name]["backtest_start"]
        bt_start_date_ts = data["strategy"][strategy_name]["backtest_start_ts"]
        bt_end_date = data["strategy"][strategy_name]["backtest_end"]
        bt_end_date_ts = data["strategy"][strategy_name]["backtest_end_ts"]
        timerange = data["strategy"][strategy_name]["timerange"]
        start_balance = data["strategy"][strategy_name]["starting_balance"]
        pairslist = data["strategy"][strategy_name]["pairlist"]
        total_pairs = len(pairslist)
        stake_type = "compounding"
        stake_amount = data["strategy"][strategy_name]["stake_amount"]
        timeframe = data["strategy"][strategy_name]["timeframe"]
        end_balance = data["strategy"][strategy_name]["final_balance"]
        net_profit = data["strategy"][strategy_name]["profit_total_abs"]
        profit_perc = data["strategy"][strategy_name]["profit_total"]
        cagr = data["strategy"][strategy_name]["cagr"]
        sortino = data["strategy"][strategy_name]["sortino"]
        sharpe = data["strategy"][strategy_name]["sharpe"]
        profit_factor = data["strategy"][strategy_name]["profit_factor"]
        expectancy = data["strategy"][strategy_name]["expectancy"]
        drawdown = data["strategy"][strategy_name]["max_drawdown_account"]
        try:
            calmar_ratio = cagr / drawdown
        except ZeroDivisionError:
            print("Error: division by zero occurred while calculating the Calmar ratio")
            calmar_ratio = 0
        # # else:
        #     # This code block will be executed if no exception is raised
        #     # You can add any additional code here that should be executed if calmar_ratio is successfully calculated
        #     pass
        # calmar_ratio = cagr / drawdown
        wins = data["strategy"][strategy_name]["wins"]
        draws = data["strategy"][strategy_name]["draws"]
        losses = data["strategy"][strategy_name]["losses"]
        total_trades = data["strategy"][strategy_name]["total_trades"]
        try:
            win_perc = wins / total_trades
        except ZeroDivisionError:
            print(
                "Error: division by zero occurred while calculating the win percentage"
            )
            win_perc = 0
        # win_perc = wins / total_trades
        try:
            draws_perc = draws / total_trades
        except ZeroDivisionError:
            print(
                "Error: division by zero occurred while calculating the draw percentage"
            )
            draws_perc = 0
        # draws_perc = draws / total_trades
        try:
            loss_perc = losses / total_trades
        except ZeroDivisionError:
            print(
                "Error: division by zero occurred while calculating the loss percentage"
            )
            loss_perc = 0
        # loss_perc = losses / total_trades
        risk_per_trade = data["strategy"][strategy_name]["avg_stake_amount"]
        pairs_with_profit = positive_pairs_counter(output_file)
        pairs_with_profit_perc = pairs_with_profit / total_pairs
        trade_count_long = data["strategy"][strategy_name]["trade_count_long"]
        trade_count_short = data["strategy"][strategy_name]["trade_count_short"]
        profit_mean = data["strategy"][strategy_name]["profit_mean"]
        profit_median = data["strategy"][strategy_name]["profit_median"]
        profit_total = data["strategy"][strategy_name]["profit_total"]
        profit_total_long = data["strategy"][strategy_name]["profit_total_long"]
        profit_total_short = data["strategy"][strategy_name]["profit_total_short"]
        profit_total_abs = data["strategy"][strategy_name]["profit_total_abs"]
        profit_total_long_abs = data["strategy"][strategy_name]["profit_total_long_abs"]
        profit_total_short_abs = data["strategy"][strategy_name][
            "profit_total_short_abs"
        ]
        calmar = data["strategy"][strategy_name]["calmar"]
        stoploss = data["strategy"][strategy_name]["stoploss"]
        total_volume = data["strategy"][strategy_name]["total_volume"]
        trades_per_day = data["strategy"][strategy_name]["trades_per_day"]
        market_change = data["strategy"][strategy_name]["market_change"]
        stake_currency = data["strategy"][strategy_name]["stake_currency"]
        rejected_signals = data["strategy"][strategy_name]["rejected_signals"]
        max_open_trades = data["strategy"][strategy_name]["max_open_trades"]
        trailing_stop = data["strategy"][strategy_name]["trailing_stop"]
        trailing_stop_positive = data["strategy"][strategy_name][
            "trailing_stop_positive"
        ]
        trailing_stop_positive_offset = data["strategy"][strategy_name][
            "trailing_stop_positive_offset"
        ]
        trailing_only_offset_is_reached = data["strategy"][strategy_name][
            "trailing_only_offset_is_reached"
        ]
        use_custom_stoploss = data["strategy"][strategy_name]["use_custom_stoploss"]
        use_exit_signal = data["strategy"][strategy_name]["use_exit_signal"]
        exit_profit_only = data["strategy"][strategy_name]["exit_profit_only"]
        exit_profit_offset = data["strategy"][strategy_name]["exit_profit_offset"]
        ignore_roi_if_entry_signal = data["strategy"][strategy_name][
            "ignore_roi_if_entry_signal"
        ]
        backtest_best_day = data["strategy"][strategy_name]["backtest_best_day"]
        backtest_worst_day = data["strategy"][strategy_name]["backtest_worst_day"]
        backtest_best_day_abs = data["strategy"][strategy_name]["backtest_best_day_abs"]
        backtest_worst_day_abs = data["strategy"][strategy_name][
            "backtest_worst_day_abs"
        ]
        winning_days = data["strategy"][strategy_name]["winning_days"]
        draw_days = data["strategy"][strategy_name]["draw_days"]
        losing_days = data["strategy"][strategy_name]["losing_days"]
        holding_avg = data["strategy"][strategy_name]["holding_avg"]
        winner_holding_avg = data["strategy"][strategy_name]["winner_holding_avg"]
        loser_holding_avg = data["strategy"][strategy_name]["loser_holding_avg"]
        max_drawdown = data["strategy"][strategy_name]["max_drawdown"]
        max_relative_drawdown = data["strategy"][strategy_name]["max_relative_drawdown"]
        max_drawdown_abs = data["strategy"][strategy_name]["max_drawdown_abs"]
        drawdown_start = data["strategy"][strategy_name]["drawdown_start"]
        drawdown_start_ts = data["strategy"][strategy_name]["drawdown_start_ts"]
        drawdown_end = data["strategy"][strategy_name]["drawdown_end"]
        drawdown_end_ts = data["strategy"][strategy_name]["drawdown_end_ts"]
        max_drawdown_low = data["strategy"][strategy_name]["max_drawdown_low"]
        max_drawdown_high = data["strategy"][strategy_name]["max_drawdown_high"]
        csum_min = data["strategy"][strategy_name]["csum_min"]
        csum_max = data["strategy"][strategy_name]["csum_max"]

        # Handle some variables that are not created if backtests prove not to give any results.
        holding_avg_s = 0  # Initialize key to 0
        if (
            "strategy" in data
            and strategy_name in data["strategy"]
            and "holding_avg_s" in data["strategy"][strategy_name]
        ):
            holding_avg_s = data["strategy"][strategy_name]["holding_avg_s"]

        winner_holding_avg_s = 0  # Initialize key to 0
        if (
            "strategy" in data
            and strategy_name in data["strategy"]
            and "winner_holding_avg_s" in data["strategy"][strategy_name]
        ):
            winner_holding_avg_s = data["strategy"][strategy_name][
                "winner_holding_avg_s"
            ]

        loser_holding_avg_s = 0  # Initialize key to 0
        if (
            "strategy" in data
            and strategy_name in data["strategy"]
            and "loser_holding_avg_s" in data["strategy"][strategy_name]
        ):
            loser_holding_avg_s = data["strategy"][strategy_name]["loser_holding_avg_s"]

        positive_streaks_high, positive_streaks_average, positive_streaks_median, positive_streaks_mode, negative_streaks_high, negative_streaks_average, negative_streaks_median, negative_streaks_mode = streak(
            output_file)

        # Determine average total trades for the timeframe of this strategies backtest.
        # Call the calculate_average_total_trades() function to get the average total trades
        average_total_trades = calculate_average_total_trades()
        # Check if the timeframe exists in the average_total_trades dictionary
        # if timeframe in average_total_trades:
        #     tf_trades_avg = average_total_trades[timeframe]

        #     # Calculate the standard deviation
        #     # Create a list with the average total trades value repeated
        #     trades_list = [tf_trades_avg] * total_trades
        #     trades_std_deviation = statistics.stdev(trades_list)
        # else:
        #     tf_trades_avg = None
        #     trades_std_deviation = None
        if timeframe in average_total_trades:
            tf_trades_avg = average_total_trades[timeframe]

        # Calculate the percentage difference
            if tf_trades_avg != 0:
                percentage_difference = round(
                    abs(total_trades - tf_trades_avg) / ((total_trades + tf_trades_avg) / 2) * 100, 2)
            else:
                percentage_difference = None
        else:
            tf_trades_avg = None
            percentage_difference = None

        # print("===============")
        # print(f"average trades of {timeframe} timeframe is {tf_trades_avg}.")
        # print(
        #     f"percentage difference for {total_trades} is {percentage_difference}.")
        # print("===============")

        # All values should be returned so that they can be processed and inserted into the database
        return (
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
        )


# print(streak(get_last_result()))

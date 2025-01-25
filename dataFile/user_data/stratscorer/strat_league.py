#!/usr/bin/python3
# coding=utf-8
import sqlite3
from config import *

# Strategy league database functions


def get_league_scores(strategy_name, strategy_filename):
    """This function collects the best backtest result data for the strategy tested on the current
    results_filename. And returns these values to that these can be added to the strategy league in another function.
    """
    # # Connect to the database
    conn = sqlite3.connect(db_path + db_name)
    c = conn.cursor()

    c.execute(
        """
        SELECT 
            strategies_tested.strategy_name,
            strategies_tested.strategy_filename,
            strategy_scores.timeframe,
            backtest_results.profit_perc,
            backtest_results.win_perc,
            backtest_results.cagr,
            backtest_results.drawdown,
            backtest_results.calmar_ratio,
            backtest_results.sortino,
            backtest_results.sharpe,
            backtest_results.profit_factor,
            backtest_results.pairs_with_profit_perc,
            backtest_results.u_timestamp,
            backtest_results.results_filename,
            backtest_results.hyperopt,
            backtest_results.strategy_remark,
            strategy_scores.total_score,
            strategy_scores.results_filename
        FROM strategies_tested
        JOIN backtest_results ON strategies_tested.strategy_name = backtest_results.strategy_name
        JOIN strategy_scores ON backtest_results.results_filename = strategy_scores.results_filename
        WHERE strategies_tested.strategy_name = ?
        AND strategies_tested.strategy_filename = ?
        ORDER BY
        strategy_scores.u_timestamp DESC, strategy_scores.total_score DESC, backtest_results.sharpe DESC, backtest_results.sortino DESC
        LIMIT
        1;
    """,
        (strategy_name, strategy_filename),
    )

    # Get the column names and data
    columns = [desc[0] for desc in c.description]
    data = c.fetchall()

    # If no data is found, return None
    if len(data) == 0:
        return None

    # Create a list of dictionaries for the results
    best_result = []
    for row in data:
        results_dict = {columns[i]: row[i] for i in range(len(columns))}
        best_result.append(results_dict)

    # Close the database connection and return the results
    conn.close()
    return best_result


def get_current_league_score(strategy_name):
    conn = sqlite3.connect(db_path + league_db_name)
    c = conn.cursor()

    c.execute(
        "SELECT * FROM strategy_league WHERE strategy_name = ?",
        [strategy_name],
    )

    # Get the column names and data
    columns = [desc[0] for desc in c.description]
    data = c.fetchall()

    # If no data is found, return None
    if len(data) == 0:
        return None

    # Create a list of dictionaries for the results
    current_result = []
    for row in data:
        results_dict = {columns[i]: row[i] for i in range(len(columns))}
        current_result.append(results_dict)

    # Close the database connection and return the results

    current_strategy_name = current_result[0]["strategy_name"]
    current_results_filename = current_result[0]["results_filename"]
    current_total_score = current_result[0]["total_score"]

    # print(current_strategy_name, current_results_filename, current_total_score)

    conn.close()
    return current_strategy_name, current_results_filename, current_total_score


def check_strategy_league_existence(strategy_name, strategy_filename):
    conn = sqlite3.connect(db_path + league_db_name)
    c = conn.cursor()

    c.execute(
        "SELECT * FROM strategy_league WHERE strategy_name = ?",
        [strategy_name],
    )

    result = c.fetchone()
    conn.close()

    if result:
        # print(
        #     f"It seems that the '{strategy_name}' already exists in the Strategy League DB."
        # )
        return True
    else:
        # print(f"The combination of strategy_name '{strategy_name}' and timeframe '{timeframe}' does not exists in the database. Proceeding...")
        return False


def remove_old_score_from_league(strategy_name, strategy_filename):
    conn = sqlite3.connect(db_path + league_db_name)
    c = conn.cursor()

    c.execute(
        """DELETE FROM strategy_league
        WHERE strategy_name = ? 
        AND strategy_filename = ?;
        """,
        (strategy_name, strategy_filename),
    )
    conn.commit()
    conn.close()

    print(f"Removed values for previous result {strategy_name} from {league_db_name}.")


def add_best_score_to_league(result):
    conn = sqlite3.connect(db_path + league_db_name)
    c = conn.cursor()

    c.execute(
        """INSERT INTO strategy_league (
                    strategy_name,
                    strategy_filename,
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
                    total_score,
                    u_timestamp,
                    results_filename,
                    hyperopt,
                    strategy_remark
                ) VALUES (
                    :strategy_name,
                    :strategy_filename,
                    :timeframe,
                    :profit_perc,
                    :win_perc,
                    :cagr,
                    :drawdown,
                    :calmar_ratio,
                    :sortino,
                    :sharpe,
                    :profit_factor,
                    :pairs_with_profit_perc,
                    :total_score,
                    :u_timestamp,
                    :results_filename,
                    :hyperopt,
                    :strategy_remark
                    )""",
        result,
    )

    conn.commit()
    conn.close()
    results_filename = result["results_filename"]

    print(
        f"Inserted {len(result)} values for best result {results_filename} into {league_db_name}."
    )


def insert_into_strategy_league(strategy_name, strategy_filename):
    conn = sqlite3.connect(db_path + league_db_name)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM strategy_league WHERE strategy_name = ?",
        [strategy_name],
    )

    entry_exists = cursor.fetchone()
    conn.close()
    best_result = get_league_scores(strategy_name, strategy_filename)
    for result in best_result:
        add_best_score_to_league(result)


def strategy_league_insertion(strategy_name, strategy_filename):
    league_existence = check_strategy_league_existence(strategy_name, strategy_filename)

    if league_existence:
        (
            current_strategy_name,
            current_results_filename,
            current_total_score,
        ) = get_current_league_score(strategy_name)
        new_best_strategy_score = get_league_scores(strategy_name, strategy_filename)
        new_results_filename = new_best_strategy_score[0]["results_filename"]
        new_total_score = new_best_strategy_score[0]["total_score"]
        print(
            f"\nWARNING: The '{strategy_name}', filename '{strategy_filename}' already exists in the strategy league!"
        )
        print(
            f"The current strategy {current_results_filename} has a score of {current_total_score}, \nwhile the new best backtest result of {new_results_filename} has a score of {new_total_score}."
        )

        while True:
            try:
                strategy_addition = input(
                    "\nDo you want to remove the old score and add the current best one? [Y/N]: "
                )
                if strategy_addition.upper() == "Y":
                    print("You answered yes. Continuing the backtest.")
                    remove_old_score_from_league(strategy_name, strategy_filename)
                    insert_into_strategy_league(strategy_name, strategy_filename)
                    break
                elif strategy_addition.upper() == "N":
                    print(
                        "You answered no. Will not add the best result to strategy league. Terminating the backtest."
                    )
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
            f"The combination of strategy_name '{strategy_name}' and filename '{strategy_filename}' does not exists in the strategy league. Proceeding..."
        )
        # Add the best strategy backtest scores to the strategy league database
        insert_into_strategy_league(strategy_name, strategy_filename)


# strategy_league_insertion("AverageStrategy", "AverageStrategy.py")

# check_and_insert_best_result(
#     "ReinforcedAverageStrategy",
#     "ReinforcedAverageStrategy-spot-1h-2023-03-09_11-04-52.json",
# )

# current = get_league_scores("AverageStrategy", "AverageStrategy.py")
# print(current[0]["strategy_name"])

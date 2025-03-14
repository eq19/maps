#!/usr/bin/python3
# coding=utf-8
import sqlite3
from config import *


def get_backtest_results(strategy_name):
    """This function runs first and collects all the necessary data for further analysis of the current backtest
    for a given strategy and returns a list of dictionaries. The secund function to be adjusted is the 'determine_scores()'
    function. There the actual scoring happens.
    """
    # Connect to the database
    conn = sqlite3.connect(db_path + db_name)
    c = conn.cursor()

    c.execute(
        """
        SELECT strategies_tested.strategy_name, strategies_tested.strategy_filename, backtest_results.results_filename,backtest_results.timeframe,
            backtest_results.profit_perc, backtest_results.drawdown, backtest_results.pairs_with_profit_perc,
            backtest_results.win_perc, backtest_results.cagr, backtest_results.calmar_ratio, backtest_results.sortino,
            backtest_results.sharpe, backtest_results.profit_factor, backtest_results.expectancy, backtest_results.percentage_difference,
            backtest_results.h_timestamp,backtest_results.u_timestamp
        FROM strategies_tested
        INNER JOIN backtest_results ON strategies_tested.strategy_name = backtest_results.strategy_name
        WHERE backtest_results.u_timestamp = (
            SELECT MAX(u_timestamp)
            FROM backtest_results
            WHERE strategy_name = ?
        )
        AND strategies_tested.strategy_name = ?
    """,
        (strategy_name, strategy_name),
    )

    # Get the column names and data
    columns = [desc[0] for desc in c.description]
    data = c.fetchall()

    # If no data is found, return None
    if len(data) == 0:
        return None

    # Create a list of dictionaries for the results
    results_list = []
    for row in data:
        results_dict = {columns[i]: row[i] for i in range(len(columns))}
        results_list.append(results_dict)

    # Close the database connection and return the results
    conn.close()
    return results_list


def insert_scores(scores_dict):
    """
    This third and final function in this scoring system inserts the output of the scoring function into the
    scoring database table strategy_scores. After this, the run is final.
    """
    conn = sqlite3.connect(db_path + db_name)
    c = conn.cursor()
    c.execute(
        """INSERT INTO strategy_scores (
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
                ) VALUES (
                    :strategy_name,
                    :timeframe,
                    :results_filename,
                    :profit_score,
                    :winrate_score,
                    :cagr_score,
                    :drawdown_score,
                    :calmar_ratio_score,
                    :sortino_score,
                    :sharpe_score,
                    :profit_factor_score,
                    :profitable_pairs_ratio_score,
                    :expectancy_score,
                    :trade_perc_punishment_score,
                    :total_score,
                    :u_timestamp
                )""",
        scores_dict,
    )

    conn.commit()
    conn.close()
    results_filename = scores_dict["results_filename"]

    print(
        f"Inserted {len(scores_dict)} scores for {results_filename} into the database."
    )


def determine_scores(result):
    """
    In this second function the values are actually scored against a scoring list (made separately)
    The score will be added to the total score and also returned for the third and final function that
    inserts the score back into the stracegy_scoring table
    """
    # print("Result ==================================")
    # print(result)
    # Get the generic data for the strategy and timeframe from the backtest_result table
    results_filename = result["results_filename"]
    strategy_name = result["strategy_name"]
    timeframe = result["timeframe"]
    u_timestamp = result["u_timestamp"]
    profit_perc = result["profit_perc"]
    win_perc = result["win_perc"]
    cagr = result["cagr"]
    drawdown = result["drawdown"]
    calmar_ratio = result["calmar_ratio"]
    sortino = result["sortino"]
    sharpe = result["sharpe"]
    profit_factor = result["profit_factor"]
    profitable_pairs = result["pairs_with_profit_perc"]
    expectancy = result["expectancy"]
    percentage_difference = result["percentage_difference"]

    # Open a connection to the database and retreive the data
    conn = sqlite3.connect(db_path + db_name)
    c = conn.cursor()

    # ========================
    # Determine profit score
    # profit_perc = result["profit_perc"]
    # print(type(profit_perc), profit_perc)
    c.execute(
        "SELECT score FROM profit_score WHERE :profit_perc BETWEEN metric_low AND metric_high",
        {"profit_perc": profit_perc},
    )
    result = c.fetchone()
    profit_score = result[0]
    # print(profit_score)
    # ========================
    # Determine winrate score
    # print(type(win_perc), win_perc)
    c.execute(
        "SELECT score FROM winrate_score WHERE :win_perc BETWEEN metric_low AND metric_high",
        {"win_perc": win_perc},
    )
    result = c.fetchone()
    winrate_score = result[0]
    # print(winrate_score)
    # ========================
    # Determine cagr score
    # print(type(cagr), cagr)
    c.execute(
        "SELECT score FROM cagr_score WHERE :cagr BETWEEN metric_low AND metric_high",
        {"cagr": cagr},
    )
    result = c.fetchone()
    cagr_score = result[0]
    # print(cagr_score)
    # ========================
    # Determine drawdown score
    # print(type(drawdown), drawdown)
    c.execute(
        "SELECT score FROM drawdown_score WHERE :drawdown BETWEEN metric_low AND metric_high",
        {"drawdown": drawdown},
    )
    result = c.fetchone()
    drawdown_score = result[0]
    # print(drawdown_score)
    # ========================
    # Determine calmar_ratio score
    # print(type(calmar_ratio), calmar_ratio)
    c.execute(
        "SELECT score FROM calmar_ratio_score WHERE :calmar_ratio BETWEEN metric_low AND metric_high",
        {"calmar_ratio": calmar_ratio},
    )
    result = c.fetchone()
    calmar_ratio_score = result[0]
    # print(calmar_ratio_score)
    # ========================
    # Determine sortino score
    # print(type(sortino), sortino)
    c.execute(
        "SELECT score FROM sortino_score WHERE :sortino BETWEEN metric_low AND metric_high",
        {"sortino": sortino},
    )
    result = c.fetchone()
    sortino_score = result[0]
    # print(sortino_score)
    # ========================
    # Determine sharpe score
    # print(type(sharpe), sharpe)
    c.execute(
        "SELECT score FROM sharpe_score WHERE :sharpe BETWEEN metric_low AND metric_high",
        {"sharpe": sharpe},
    )
    result = c.fetchone()
    sharpe_score = result[0]
    # print(sharpe_score)
    # ========================
    # Determine profit_factor score
    # print(type(profit_factor), profit_factor)
    c.execute(
        "SELECT score FROM profit_factor_score WHERE :profit_factor BETWEEN metric_low AND metric_high",
        {"profit_factor": profit_factor},
    )
    result = c.fetchone()
    profit_factor_score = result[0]
    # print(profit_factor_score)
    # ========================
    # Determine profitable_pairs_ratio score
    # print(type(profitable_pairs), profitable_pairs)
    c.execute(
        "SELECT score FROM profitable_pairs_ratio_score WHERE :profitable_pairs BETWEEN metric_low AND metric_high",
        {"profitable_pairs": profitable_pairs},
    )
    result = c.fetchone()
    profitable_pairs_ratio_score = result[0]
    # print(profitable_pairs_ratio_score)
    # ========================
    # Determine expectancy score
    # print(type(expectancy), expectancy)
    c.execute(
        "SELECT score FROM expectancy_score WHERE :expectancy BETWEEN metric_low AND metric_high",
        {"expectancy": expectancy},
    )
    result = c.fetchone()
    expectancy_score = result[0]

    # ========================
    # Determine trade amount deviation punishment
    # print(type(percentage_difference), percentage_difference)
    c.execute(
        "SELECT score FROM trade_perc_deviation_punishment WHERE :percentage_difference BETWEEN metric_low AND metric_high",
        {"percentage_difference": percentage_difference},
    )
    result = c.fetchone()
    trade_perc_punishment_score = result[0]
    # print(profitable_pairs_ratio_score)
   # ========================
    # Determine TOTAL score
    total_score = (
        drawdown_score
        + profit_score
        + profitable_pairs_ratio_score
        + winrate_score
        + cagr_score
        + calmar_ratio_score
        + sortino_score
        + sharpe_score
        + profit_factor_score
        + expectancy_score
        + trade_perc_punishment_score
    )

    conn.commit()
    conn.close()

    scores_dict = {
        "strategy_name": strategy_name,
        "timeframe": timeframe,
        "results_filename": results_filename,
        "profit_score": profit_score,
        "winrate_score": winrate_score,
        "cagr_score": cagr_score,
        "drawdown_score": drawdown_score,
        "calmar_ratio_score": calmar_ratio_score,
        "sortino_score": sortino_score,
        "sharpe_score": sharpe_score,
        "profit_factor_score": profit_factor_score,
        "profitable_pairs_ratio_score": profitable_pairs_ratio_score,
        "expectancy_score": expectancy_score,
        "trade_perc_punishment_score": trade_perc_punishment_score,
        "total_score": total_score,
        "u_timestamp": u_timestamp,
    }

    # print("Scores ==================================")
    # print(scores_dict)
    return scores_dict


def check_and_insert_scores(scores_dict):
    # Connect to the SQLite database
    conn = sqlite3.connect(db_path + db_name)
    c = conn.cursor()

    # Check if the combination of results_filename value and u_timestamp value already exists in the table
    c.execute(
        "SELECT COUNT(*) FROM strategy_scores WHERE results_filename = ? AND u_timestamp = ?",
        (scores_dict["results_filename"], scores_dict["u_timestamp"]),
    )
    result = c.fetchone()[0]

    results_filename = scores_dict["results_filename"]

    if result > 0:
        # If the combination exists, give a warning and skip the entry
        print(
            f"\nWarning: Entry {results_filename} already exists in database. Skipping entry."
        )
    else:
        # If the combination doesn't exist, call the insert_scores function to insert the entry
        insert_scores(scores_dict)

    # Commit the changes to the database and close the connection
    conn.commit()
    conn.close()


def determine_strategy_scores(strategy_name):
    results_list = get_backtest_results(strategy_name)
    for result in results_list:
        # print(type(result["profit_perc"]))
        # print(type(result["win_perc"]))
        scores_dict = determine_scores(result)
        # insert_scores(scores_dict)
        check_and_insert_scores(scores_dict)


# determine_strategy_scores("CMCWinner")

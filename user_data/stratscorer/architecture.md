# Inner workings

## Adding new database fields to the stratscorer.db backtest_results table

To add new fields to the backtest results table. Follow the next procedure:

* Determine the field names and their type (REAL, TXT, INTEGER etc.)
* Add the fields and types manually to the database table with SQLite DB browser or DBeaver (I will probably make a script for this later...)
* Add the fields to the following functions:
** initial_create_database_and_tables() in db_functions.py. For new setup creations.
** insert_backtest_results(...) in db_functions.py. For adding new table entries after backtests. Remember to also add the fields and corresponding ?, ?, ?... to the "INSERT INTO" line!
** add_backtest(...) in start.py. This function is the intermediary function between data collection from the JSON backtest output file and data insertion into the database.
** export_all_backtest_results_to_csv(conn) in data_output.py. To export the data from the table into a *.csv file. Remember to add to SQL statement and export headers for CSV.
** get_trade_results() in data_collection.py. This function is most likely the source of the new information for the table. It gets or calculates the information from the backtest output json file and is the input for the add_backtest() function above.
** Additionally you can also add the new columns to print_backtest_results(conn, strategy_name=None) in data_output.py for showing the new data on the terminal in a table.

Finally:

Do not forget to add the new field names to the manual export and import functions for the tool. Also there is a terminal output function to show backtest
results to the terminal screen. You might want to take a look at that as well.

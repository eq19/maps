#!/usr/bin/python3
# coding=utf-8

import os
import json
from sqlalchemy import create_engine, Column, Integer, Float, String
# from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

# Specify the import directory
import_dir = "./import_directory/"

# Set the path and name for the database
db_path = "./database/"
pair_results_db_name = "pair_results.db"

# Create the SQLAlchemy engine
engine = create_engine('sqlite:///database/pair_results_2.db')

# Create a session factory
Session = sessionmaker(bind=engine)
session = Session()

# Create the base class for declarative models
Base = declarative_base()


# Define the BestPair model
class BestPair(Base):
    __tablename__ = 'best_pair'

    key = Column(String, primary_key=True)
    trades = Column(Integer)
    profit_mean = Column(Float)
    profit_mean_pct = Column(Float)
    profit_sum = Column(Float)
    profit_sum_pct = Column(Float)
    profit_total_abs = Column(Float)
    profit_total = Column(Float)
    profit_total_pct = Column(Float)
    duration_avg = Column(String)
    wins = Column(Integer)
    draws = Column(Integer)
    losses = Column(Integer)
    strategy_name = Column(String)
    results_filename = Column(String, nullable=False, unique=True)
    timeframe = Column(String)
    timerange = Column(String)


# Define the WorstPair model
class WorstPair(Base):
    __tablename__ = 'worst_pair'

    key = Column(String, primary_key=True)
    trades = Column(Integer)
    profit_mean = Column(Float)
    profit_mean_pct = Column(Float)
    profit_sum = Column(Float)
    profit_sum_pct = Column(Float)
    profit_total_abs = Column(Float)
    profit_total = Column(Float)
    profit_total_pct = Column(Float)
    duration_avg = Column(String)
    wins = Column(Integer)
    draws = Column(Integer)
    losses = Column(Integer)
    strategy_name = Column(String)
    results_filename = Column(String, nullable=False, unique=True)
    timeframe = Column(String)
    timerange = Column(String)


# Define the PairResult model
class PairResult(Base):
    __tablename__ = 'pair_result'

    key = Column(String, primary_key=True)
    trades = Column(Integer)
    profit_mean = Column(Float)
    profit_mean_pct = Column(Float)
    profit_sum = Column(Float)
    profit_sum_pct = Column(Float)
    profit_total_abs = Column(Float)
    profit_total = Column(Float)
    profit_total_pct = Column(Float)
    duration_avg = Column(String)
    wins = Column(Integer)
    draws = Column(Integer)
    losses = Column(Integer)
    strategy_name = Column(String)
    results_filename = Column(String, nullable=False, unique=True)
    timeframe = Column(String)
    timerange = Column(String)


# Create the tables if they don't exist
Base.metadata.create_all(engine)


def import_best_pair_data():
    json_files = [file for file in os.listdir(
        import_dir) if file.endswith('.json')]

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
            existing_file = session.query(BestPair).filter_by(
                results_filename=results_filename).first()

            if existing_file:
                print(
                    f"Skipping file '{results_filename}' as it already exists in the best pair table.")
                continue

            # Insert the data into the database
            best_pair = BestPair(
                key=key,
                trades=trades,
                profit_mean=profit_mean,
                profit_mean_pct=profit_mean_pct,
                profit_sum=profit_sum,
                profit_sum_pct=profit_sum_pct,
                profit_total_abs=profit_total_abs,
                profit_total=profit_total,
                profit_total_pct=profit_total_pct,
                duration_avg=duration_avg,
                wins=wins,
                draws=draws,
                losses=losses,
                strategy_name=strategy_name,
                results_filename=results_filename,
                timeframe=timeframe,
                timerange=timerange
            )
            session.add(best_pair)

    # Commit the changes and close the session
    session.commit()
    session.close()


def import_worst_pair_data():
    json_files = [file for file in os.listdir(
        import_dir) if file.endswith('.json')]

    for file_name in json_files:
        with open(os.path.join(import_dir, file_name)) as of:
            data = json.load(of)

            # Strategy data
            strategy_name = data["strategy_comparison"][0].get("key")
            results_filename = file_name  # Index value for the database
            timeframe = data["strategy"][strategy_name]["timeframe"]
            timerange = data["strategy"][strategy_name]["timerange"]

            # Worst pair data
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
            existing_file = session.query(WorstPair).filter_by(
                results_filename=results_filename).first()

            if existing_file:
                print(
                    f"Skipping file '{results_filename}' as it already exists in the worst pair table.")
                continue

            # Insert the data into the database
            worst_pair = WorstPair(
                key=key,
                trades=trades,
                profit_mean=profit_mean,
                profit_mean_pct=profit_mean_pct,
                profit_sum=profit_sum,
                profit_sum_pct=profit_sum_pct,
                profit_total_abs=profit_total_abs,
                profit_total=profit_total,
                profit_total_pct=profit_total_pct,
                duration_avg=duration_avg,
                wins=wins,
                draws=draws,
                losses=losses,
                strategy_name=strategy_name,
                results_filename=results_filename,
                timeframe=timeframe,
                timerange=timerange
            )
            session.add(worst_pair)

    # Commit the changes and close the session
    session.commit()
    session.close()


def import_pair_data():
    json_files = [file for file in os.listdir(
        import_dir) if file.endswith('.json')]

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

            for pair in pairs:
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

                # Check if the table exists
                table_name = f"results_per_pair_{key}"
                existing_table = session.execute(
                    f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'").scalar()

                if not existing_table:
                    print(
                        f"Table 'results per pair' for pair {key} does not exist. Creating...")
                    # Create the table dynamically

                    class ResultsPerPair(Base):
                        __tablename__ = table_name

                        key = Column(String, primary_key=True)
                        trades = Column(Integer)
                        profit_mean = Column(Float)
                        profit_mean_pct = Column(Float)
                        profit_sum = Column(Float)
                        profit_sum_pct = Column(Float)
                        profit_total_abs = Column(Float)
                        profit_total = Column(Float)
                        profit_total_pct = Column(Float)
                        duration_avg = Column(String)
                        wins = Column(Integer)
                        draws = Column(Integer)
                        losses = Column(Integer)
                        strategy_name = Column(String)
                        results_filename = Column(
                            String, nullable=False, unique=True)
                        timeframe = Column(String)
                        timerange = Column(String)

                    # Create the table
                    ResultsPerPair.__table__.create(bind=engine)

                # Check if the results_filename already exists in the table
                existing_file = session.query(ResultsPerPair).filter_by(
                    results_filename=results_filename).first()

                if existing_file:
                    print(
                        f"Skipping file '{results_filename}' as it already exists in the pair table.")
                    continue

                # Insert the data into the database
                pair_result = PairResult(
                    key=key,
                    trades=trades,
                    profit_mean=profit_mean,
                    profit_mean_pct=profit_mean_pct,
                    profit_sum=profit_sum,
                    profit_sum_pct=profit_sum_pct,
                    profit_total_abs=profit_total_abs,
                    profit_total=profit_total,
                    profit_total_pct=profit_total_pct,
                    duration_avg=duration_avg,
                    wins=wins,
                    draws=draws,
                    losses=losses,
                    strategy_name=strategy_name,
                    results_filename=results_filename,
                    timeframe=timeframe,
                    timerange=timerange
                )
                session.add(pair_result)

    # Commit the changes and close the session
    session.commit()
    session.close()


initial_create_pair_results_database_and_tables()
import_best_pair_data()
import_worst_pair_data()
import_pair_data()

#!/usr/bin/python3
# coding=utf-8
import os
import shutil
import time
from config import *


def copy_strategy(strategy_name, strategy_filename, strategy_dir):
    strategies_dir = os.path.join(ft_dir, "user_data", "strategies")

    if os.path.isdir(strategy_dir):
        print(
            f"\nThe directory {strategy_name} already exists. \nStrategy files will be added to this directory."
        )
    else:
        os.makedirs(strategy_dir)
        print(f"Created directory for {strategy_name} for the Freqtrade files")

    dest_dir = strategy_dir
    strategy_name, _ = os.path.splitext(strategy_filename)

    for ext in [".py", ".json"]:
        filename = strategy_name + ext
        src_file = os.path.join(strategies_dir, filename)
        dest_file = os.path.join(dest_dir, filename)

        if os.path.exists(dest_file):
            src_size = os.path.getsize(
                src_file) if os.path.exists(src_file) else None
            dest_size = os.path.getsize(dest_file)
            if src_size == dest_size:
                print(
                    f"\n{filename} already exists and is the same size, skipping")
                continue
            else:
                print(f"\n{filename} already exists but has a different size")
                action = input("Enter 'c' to copy or 's' to skip: ")
                if action != "c":
                    print(f"Skipping {filename}")
                    continue

        try:
            shutil.copy(src_file, dest_file)
            print(f"Copied {filename} to {dest_dir}")
        except FileNotFoundError:
            print(f"File {filename} not found, skipping")


def collect_strategy(strategy_filename):
    # Set the path to the strategies directory
    strategies_dir = os.path.join(ft_dir, "user_data", "strategies")

    # Check if 'all_strategies' directory already exists
    if os.path.isdir(all_strategies_dir):
        print("The 'all_strategies' directory already exists.")
    else:
        # Create the 'all_strategies' directory
        os.makedirs(all_strategies_dir)
        print("Created 'all_strategies' directory for the Freqtrade files")

    # Extract the strategy name from the strategy filename
    strategy_name, _ = os.path.splitext(strategy_filename)

    for ext in [".py", ".json"]:
        filename = strategy_name + ext
        src_file = os.path.join(strategies_dir, filename)
        dest_file = os.path.join(all_strategies_dir, filename)

        # Check if the destination file already exists
        if os.path.exists(dest_file):
            src_size = os.path.getsize(
                src_file) if os.path.exists(src_file) else None
            dest_size = os.path.getsize(dest_file)
            if src_size == dest_size:
                # If the destination file has the same size, skip copying
                print(
                    f"\n{filename} already exists and is the same size, skipping")
                return
            else:
                # If the destination file has a different size, ask for action
                print(f"\n{filename} already exists but has a different size")
                action = input("Enter 'c' to copy or 's' to skip: ")
                if action != "c":
                    # Skip copying if action is not 'c'
                    print(f"Skipping {filename}")
                    return

        try:
            # Copy the source file to the destination file
            shutil.copy(src_file, dest_file)
            print(f"Copied {filename} to {all_strategies_dir}")
        except FileNotFoundError:
            # Handle the case when the source file is not found
            print(f"File {filename} not found, skipping")


def move_results(strategy_name, strategy_dir):
    # Check if directory already exists
    if os.path.isdir(strategy_dir):
        print(
            f"\nThe directory {strategy_name} already exists. \nFiles will be moved to this directory."
        )
    else:
        # Create directory for strategy
        os.makedirs(strategy_dir)
        print(f"Created directory for {strategy_name} for the Freqtrade files")

    # move files from backtest_results to strategy directory
    results_dir = f"{ft_dir}/user_data/backtest_results"
    for filename in os.listdir(results_dir):
        if strategy_name in filename:
            shutil.move(
                os.path.join(results_dir, filename),
                os.path.join(strategy_dir, filename),
            )

    print(f"Freqtrade json logfiles moved to {strategy_dir}")


def move_backtest_logs(strategy_name, strategy_dir):
    # Check if directory already exists
    if os.path.isdir(strategy_dir):
        print(
            f"\nThe directory {strategy_name} already exists. \nFiles will be copied to this directory."
        )
    else:
        # Create directory for strategy
        os.makedirs(strategy_dir)
        print(
            f"Created directory for {strategy_name} for the backtest logfiles")

    # move files from backtest_results to strategy directory
    # logs_dir = f"{ft_dir}/user_data/backtest_results"
    for filename in os.listdir(logs_dir):
        if strategy_name in filename:
            shutil.move(
                os.path.join(logs_dir, filename),
                os.path.join(strategy_dir, filename),
            )

    print(f"Freqtrade backtest logfiles moved to {strategy_dir}")


def backup_db():
    # Create the backup directory if it doesn't exist
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)

    # Get a list of all files in the db directory
    # db_dir = "./db"
    db_files = os.listdir(db_path)

    # Loop through each file in the db directory
    for file_name in db_files:
        # Construct the paths to the source and backup files
        source_path = os.path.join(db_path, file_name)
        backup_file_name = f"{file_name}_{int(time.time())}"
        backup_path = os.path.join(backup_dir, backup_file_name)

        # Copy the source file to the backup directory
        shutil.copy(source_path, backup_path)

    # Get a list of all files in the backup directory
    backup_files = os.listdir(backup_dir)

    # Loop through each file in the backup directory
    for file_name in backup_files:
        # Split the filename into the base name and timestamp
        base_name, timestamp = file_name.rsplit("_", 1)

        # Find all files in the backup directory with the same base name
        same_base_files = [f for f in backup_files if f.startswith(base_name)]

        # Sort the list of same base files by timestamp (most recent first)
        same_base_files.sort(key=lambda f: int(
            f.rsplit("_", 1)[-1]), reverse=True)

        # Remove all but the five [5:] most recent same base files
        for old_file_name in same_base_files[5:]:
            old_file_path = os.path.join(backup_dir, old_file_name)
            try:
                print(f"Deleting old file: {old_file_path}")
                os.remove(old_file_path)
                backup_files.remove(old_file_name)
            except FileNotFoundError:
                print(f"WARNING: File not found: {old_file_path}")
                continue


# test
# backup_db()
# copy_strategy("AverageStrategy", "AverageStrategy.py")

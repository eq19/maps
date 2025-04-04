from time import perf_counter
from functools import wraps
import sqlite3
from functools import wraps
from config import db_path, league_db_name, db_name


def timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = perf_counter()
        result = func(*args, **kwargs)
        end = perf_counter()
        duration = end - start
        arg = ", ".join(str(arg) for arg in args)
        print(f"function {func.__name__}({arg}) took {duration:.4f} seconds")
        return result

    return wrapper


def db_league_connection(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect(db_path + league_db_name)
        try:
            result = func(conn, *args, **kwargs)
            conn.commit()
        finally:
            conn.close()
        return result

    return wrapper


def db_connection(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect(db_path + db_name)
        try:
            result = func(conn, *args, **kwargs)
            conn.commit()
        finally:
            conn.close()
        return result

    return wrapper

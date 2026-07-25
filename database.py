# ============================================================
#  database.py — PostgreSQL connection helper
#  Reads the connection string from the .env file.
# ============================================================

import os
import psycopg2
from dotenv import load_dotenv

# load_dotenv() reads the .env file and puts every line into
# the environment so os.getenv() can find them.
load_dotenv()


def get_db():
    """
    Open and return a new PostgreSQL connection.

    The connection string (DATABASE_URL) comes from the .env file.
    Example:  postgresql://postgres:postgres@db:5432/taskdb

    psycopg2 is the standard Python driver for PostgreSQL.
    """
    return psycopg2.connect(os.getenv("DATABASE_URL"))

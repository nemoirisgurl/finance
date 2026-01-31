import sqlite3
import os
from datetime import datetime

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(CURRENT_DIR)
DB_PATH = os.path.join(ROOT_DIR, "database", "finances.db")


def is_valid_date(date):
    try:
        return datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        return False


def calc_interest(
    principal, rate, years, monthly_contribution=0, compounds_per_year=12
):
    data = []
    r = rate / 100
    n = compounds_per_year
    for year in range(1, years + 1):
        if r == 0:
            new_principal = principal + (monthly_contribution * 12 * year)
        else:
            fv_principal = principal * (1 + r / n) ** (n * year)
            fv_contributions = monthly_contribution * (
                ((1 + r / n) ** (n * year) - 1) / (r / n)
            )
            new_principal = fv_principal + fv_contributions
        data.append(
            {
                "year": year,
                "principal": round(new_principal, 2),
            }
        )
    return data

def get_data():
    with sqlite3.connect(DB_PATH) as con:
        try:
            cur = con.execute(
                "SELECT * FROM transactions")
            return cur.fetchall()
        except sqlite3.IntegrityError as e:
            print("Error fetching data from the database.")
            return []

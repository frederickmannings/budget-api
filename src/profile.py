import sqlite3
from sqlite3 import Error, Connection
from pathlib import Path
import logging
from typing import Optional
from constants import DEFAULT_TAX_FREE_ALLOWANCE

LOGGER = logging.Logger(__name__)


BASE_PATH_TO_DB = Path("/Users/FMannings/git/finance/budgeting-api")


def connect_to_account(path_to_account: Path) -> Connection:
    connection = None
    try:
        connection = sqlite3.connect(str(path_to_account / "profile.db"))
        print("Connection to sq")
    except Error as e:
        raise e
    return connection


def create_account(
    path_to_account: Path,
    income_per_anum: float = None,
    tax_free_allowance: float = None,
    pension_contribution: float = None,
) -> Connection:
    conn = connect_to_account(path_to_account=path_to_account)
    cursor = conn.cursor()
    try:
        cursor.execute(
            """CREATE TABLE profile (
        salary real,
        tax_free_allowance real,
        pension_contribution
        )
        """
        )
    except Exception as e:
        print(e)

    cursor.execute(
        "INSERT INTO profile VALUES ("
        + f"{income_per_anum},"
        + f"{tax_free_allowance},"
        + f"{pension_contribution}))"
    )

    conn.commit()
    conn.close()
    return conn


class Profile:
    salary_per_anum: float
    pension_contribution: float
    tax_free_allowance: float
    columns = ["salary", "tax_free_allowance", "pension_contribution"]
    name = str

    def __init__(
        self,
        name: str,
        path_to_db: Optional[Path] = None,
        salary_per_anum=None,
        pension_contribution=None,
        tax_free_allowance=DEFAULT_TAX_FREE_ALLOWANCE,
    ):
        # set the path to the profile
        self.profile_db_path = (
            path_to_db / "profile.db"
            if path_to_db
            else BASE_PATH_TO_DB / f"{name}_profile.db"
        )

        # connect and initiate cursors
        self.conn = self.connect_to_profile()
        self.cursor = self.conn.cursor()

        # check that there is a profiles table
        self.cursor.execute(
            """ SELECT count(name)
            FROM sqlite_master
            WHERE type='table' AND name='profile' """
        )
        if self.cursor.fetchone()[0] < 1:
            self.cursor.execute(
                """CREATE TABLE IF NOT EXISTS profile (
                    name text,
                    salary real,
                    tax_free_allowance real,
                    pension_contribution real
                    )"""
            )
            # create an index attached to name
            self.cursor.execute("""CREATE UNIQUE INDEX id ON profile (name)""")

        # write values
        if salary_per_anum:
            self.write_to_profile(name, "salary", salary_per_anum)

        if tax_free_allowance:
            self.write_to_profile(name, "tax_free_allowance", tax_free_allowance)

        if pension_contribution:
            self.write_to_profile(name, "pension_contribution", pension_contribution)

        # commit changes and close the connection
        self.conn.close()

    def write_to_profile(self, row, column, value):
        self.cursor.execute(f"""SELECT * FROM profile WHERE name = '{row}' """)
        data = self.cursor.fetchall()
        replace_idx = [ii for ii, x in enumerate(self.columns) if x == column]

        if data:
            data_to_write = list(data[0])[1:]
            data_to_write[replace_idx[0]] = value
            data_to_write = [
                (d, c) for d, c in zip(data_to_write, self.columns) if d is not None
            ]
            columns = [c for d, c in data_to_write]
            values = [d for d, c in data_to_write]
            values = ",".join([str(x) for x in values])
            columns = ",".join(columns)

            self.cursor.execute(
                "REPLACE INTO profile " + f"(name,{columns}) VALUES ('{row}', {values})"
            )
            self.conn.commit()
        else:
            self.cursor.execute(
                "INSERT INTO profile " + f"(name,{column}) VALUES ('{row}', {value})"
            )

    def connect_to_profile(self) -> Connection:
        connection = None
        try:
            connection = sqlite3.connect(
                str(self.profile_db_path),
            )
        except Error as e:
            raise e
        return connection
    
    def add_in_out_going(self, type, in, out):
        return


if __name__ == "__main__":
    acc = Path("/Users/FMannings/git/finance/budgeting-api")
    p1 = Profile(
        "fred",
        path_to_db=acc,
        salary_per_anum=45000,
        pension_contribution=0.01,
    )
    p2 = p = Profile(
        "jasz",
        path_to_db=acc,
        salary_per_anum=33000,
        pension_contribution=0.03,
    )

    print(p)

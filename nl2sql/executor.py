"""
DB executor with safe error handling.
"""
from typing import Tuple, Union
import pandas as pd
from sqlalchemy import create_engine, text

class Database:
    def __init__(self, url: str):
        self.engine = create_engine(url, future=True)

    def run_query(self, sql: str) -> Tuple[bool, Union[pd.DataFrame, str]]:
        """
        Returns (ok, DataFrame | error_message).
        """
        try:
            with self.engine.connect() as conn:
                df = pd.read_sql(text(sql), conn)
            return True, df
        except Exception as e:
            return False, str(e)

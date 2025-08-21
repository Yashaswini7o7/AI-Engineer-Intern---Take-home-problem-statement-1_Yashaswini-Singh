"""
Format DB results for UI/CLI.
"""
import pandas as pd

def format_result(df: pd.DataFrame, max_rows: int = 100):
    if df is None or df.empty:
        return "Sorry, no results found."
    # If it's a single scalar value, prefer printing the number
    if df.shape == (1, 1):
        val = df.iat[0, 0]
        return f"{val}"
    # Cap rows for readability
    if len(df) > max_rows:
        df = df.head(max_rows).copy()
        df.loc[len(df)] = ["…"] * len(df.columns)
    return df

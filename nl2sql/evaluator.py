"""
Evaluation utilities:
- Execute system SQL vs ground-truth SQL and compare results.
- Report accuracy and sample successes/failures.
"""
from typing import Dict, List, Tuple
import json
import pandas as pd
from sqlalchemy import create_engine, text

def _normalize(df: pd.DataFrame) -> pd.DataFrame:
    """
    Normalize DF for comparison: sort columns & rows, reset index.
    """
    if df is None:
        return pd.DataFrame()
    df = df.copy()
    
    for c in df.columns:
        try:
            df[c] = pd.to_numeric(df[c])
        except Exception:
            pass
    df = df.sort_index(axis=1)
    df = df.sort_values(by=list(df.columns)).reset_index(drop=True)
    return df

def evaluate(test_path: str, db_url: str, parser_fn) -> Dict:
    engine = create_engine(db_url, future=True)
    tests = json.load(open(test_path))
    results = []
    with engine.connect() as conn:
        for t in tests:
            q = t["question"]
            gold_sql = t["gold_sql"]
            sys_sql = parser_fn(q)

            if sys_sql is None:
                results.append({"question": q, "ok": False, "reason": "parser_none"})
                continue

            try:
                gold_df = pd.read_sql(text(gold_sql), conn)
                sys_df  = pd.read_sql(text(sys_sql), conn)
                ok = _normalize(gold_df).equals(_normalize(sys_df))
                results.append({
                    "question": q,
                    "ok": bool(ok),
                    "sys_sql": sys_sql.strip(),
                    "gold_sql": gold_sql.strip()
                })
            except Exception as e:
                results.append({"question": q, "ok": False, "reason": f"exec_error: {e}"})

    total = len(results)
    correct = sum(1 for r in results if r["ok"])
    acc = round(100.0 * correct / total, 2) if total else 0.0
    return {"accuracy": acc, "total": total, "correct": correct, "details": results}

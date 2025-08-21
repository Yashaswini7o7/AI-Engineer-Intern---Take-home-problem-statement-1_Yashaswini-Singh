"""
Simple CLI for quick checks.
Usage:
  python cli.py "Who are the top 10 tenants by total rent paid?"
"""
import sys
import yaml
from nl2sql.parser import nl_to_sql
from nl2sql.executor import Database
from nl2sql.response_formatter import format_result

def main():
    if len(sys.argv) < 2:
        print("Usage: python cli.py \"<your question>\"")
        sys.exit(1)
    question = sys.argv[1]
    with open("config.yaml", "r") as f:
        CFG = yaml.safe_load(f)
    db = Database(CFG["database"]["url"])
    sql = nl_to_sql(question)
    if not sql:
        print("Sorry, unable to answer at this point in time.")
        return
    ok, res = db.run_query(sql)
    if not ok:
        print("Sorry, unable to answer at this point in time.")
        print("Details:", res)
    else:
        out = format_result(res, max_rows=CFG["app"]["max_rows"])
        if hasattr(out, "to_string"):
            print(out.to_string(index=False))
        else:
            print(out)

if __name__ == "__main__":
    main()


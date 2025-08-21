"""
Streamlit front-end for CXO-friendly NL→SQL querying.
"""

import streamlit as st
import yaml
from nl2sql.parser import nl_to_sql
from nl2sql.executor import Database
from nl2sql.response_formatter import format_result


with open("config.yaml", "r") as f:
    CFG = yaml.safe_load(f)

DB = Database(CFG["database"]["url"])

st.set_page_config(page_title="Rental NL→SQL POC", layout="wide")
st.title("🏠 Rental App — Natural Language to SQL (POC)")

st.caption("Type a business question in English. The system will translate it to SQL and execute on the demo DB.")

q = st.text_input(
    "Your question",
    value="Who are the top 10 tenants by total rent paid?",
    placeholder="e.g., What's the occupancy rate of properties in Bradford in Q2 2024?"
)

if st.button("Run") or q:
    sql = nl_to_sql(q)
    if not sql:
        st.error("Sorry, unable to answer at this point in time.")
    else:
        if CFG["app"].get("show_sql", True):
            with st.expander("Generated SQL"):
                st.code(sql, language="sql")
        ok, res = DB.run_query(sql)
        if not ok:
            st.error("Sorry, unable to answer at this point in time.")
            st.caption(f"Details: {res}")
        else:
            table_or_text = format_result(res, max_rows=CFG["app"]["max_rows"])
            if hasattr(table_or_text, "to_markdown"):
                st.markdown(table_or_text.to_markdown(index=False))
            else:
                st.write(table_or_text)

st.markdown("---")
st.subheader("🔎 Sample queries")
st.code(
    "What’s the occupancy rate of properties in Bradford in Q2 2024?\n"
    "Who are the top 10 tenants by total rent paid?\n"
    "What’s the average rating of apartments vs houses?\n"
    "Which landlords generated the most revenue in 2024?\n"
    "List all currently available 2BHKs under $2500 in London."
)


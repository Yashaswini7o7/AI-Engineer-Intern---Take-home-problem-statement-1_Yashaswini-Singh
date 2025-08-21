# Rental App NL→SQL POC

A hackathon-style Proof of Concept that converts **natural language** queries into **SQL**, executes on a relational DB (SQLite for simplicity), and returns results in a CXO-friendly UI (Streamlit) or CLI.

## 🧰 Tech
- Python 3.9+
- SQLite (file DB)
- Streamlit (UI)
- Pandas, SQLAlchemy, PyYAML

## 🔧 Setup (Local)
```bash
git clone <your-repo-url> rental_nl2sql_poc
cd rental_nl2sql_poc
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python scripts/init_db.py                            # creates rental_app.db with schema + seed data


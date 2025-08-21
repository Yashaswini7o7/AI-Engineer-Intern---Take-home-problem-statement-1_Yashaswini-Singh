# 🏠 NLP-to-SQL Demo for Rental App Database

This repository contains a Proof of Concept (POC) system that allows a CXO to type queries in natural language (English). The system converts these queries into SQL, executes them on a sample `rental_app` database, and returns results in a clear format. If the query cannot be answered, the system gracefully responds with:  
**“Sorry, unable to answer at this point in time.”**

---

## 📂 Project Structure

nlp-sql-demo/
│
├── main.py # Streamlit UI for natural language queries
├── config.yaml # Configurations (DB path, model settings)
├── requirements.txt # Python dependencies
├── README.md # Setup & usage instructions
│
├── data/
│ └── test_dataset.csv # Test dataset for evaluation
│
├── db/
│ └── rental_app.db # SQLite sample database
│
├── scripts/
│ ├── init_db.py # Creates and populates rental_app.db
│ └── evaluate.py # Runs evaluation using test dataset
│
├── models/
│ └── nlp_to_sql.py # Core logic: NLP → SQL conversion
│
└── report/
└── evaluation_report.md # Accuracy results & test set methodology


---

## ⚙️ Setup & Installation

Clone the repository:
```bash
git clone https://github.com/<your-username>/nlp-sql-demo.git
cd nlp-sql-demo

Create a virtual environment and install dependencies:

python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows

pip install -r requirements.txt

Initialize the database:

python scripts/init_db.py
This creates db/rental_app.db with sample tables (properties, tenants, rentals) and inserts example data.

🚀 Running the Application
Start the Streamlit app:

streamlit run main.py
This opens a browser interface where you can type queries such as:

“What’s the occupancy rate of properties in Bradford last quarter?”

“List top 10 tenants by total rent paid.”

“Show properties with average rent greater than 800.”

If the system cannot map the query to SQL, it returns the fallback response.

🧪 Testing & Evaluation
Run automated evaluation on the included test dataset:

python scripts/evaluate.py
This script:

Loads natural language test queries (data/test_dataset.csv).

Generates SQL using the model (models/nlp_to_sql.py).

Executes SQL against rental_app.db.

Compares results to expected outputs.

Saves detailed results in report/evaluation_report.md.

📊 Report
The evaluation report (report/evaluation_report.md) documents:

Accuracy of the system on the test dataset.

Methodology for building an exhaustive test set.

Error cases and suggestions for improvements.

✅ Scope & Capabilities
Understands multi-condition queries.

Handles joins (e.g., tenants + properties).

Supports aggregations (SUM, AVG, COUNT).

Returns tabular numeric/text results.

Provides graceful fallback when queries cannot be resolved.

👩‍💻 Tech Stack
Python 3.10+

Streamlit → front-end for user queries

SQLite → database for rentals

NLTK / HuggingFace → natural language parsing

SQLAlchemy → database interaction

LangChain (optional) → advanced query translation

🔮 Future Enhancements
Add support for visual charts (occupancy trends, rent distributions).

Improve accuracy with fine-tuned NLP models.

Extend to other databases (Postgres, MySQL).

Add authentication & logging for production use.

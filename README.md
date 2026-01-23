# 💰Finance Management Tracker💰

A personal finance tracker built with **Python** and **SQLite**.

This app allows you to manage your daily transactions directly from the terminal with a clean, tabulated interface. It is designed for simplicity and speed, keeping your financial data stored locally and securely without the need for complex spreadsheets or internet access.

## Contents
1. [Features](#features) 
2. [Prerequisites](#prerequisites)
3. [Installation](#installation)
4. [Usage](#usage)
5. [Project Structure](#project-structure)

## Features
- **Transaction Manager:** Add income and expenses with descriptions and custom dates.
- **Data Visualization:** View a visualized table of all transactions or a filtered table by income or expense.
- **Financial Analysis:** View your total income, total expense and net balance between custom date range.
- **Graph Generation:** Generate visual trend lines of your net balance or predicted compound product over time using Matplotlib.
- **Secure & Local:** All data is stored in a local SQLite database (`finances.db`), ensuring privacy.

## Prerequisites
* **Python 3.x**
* **Dependencies** (Lists in `requirements.txt`)
    * `pandas` (Data analysis)
    * `matplotlib` (Graph plotting)
    * `tabulate` (Pretty printing tables)

## Installation 
1. **Clone the repository**
```bash
git clone https://github.com/nemoirisgurl/finance.git
cd finance
```
2.  **Set up a virtual environment (Recommended):**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3.  **Install dependencies:**
```bash
pip install -r requirements.txt
```

## Usage
Run the application from the **root directory** (*/finance):

```bash
python main.py
```
Choose a feature to use
1. **Initialize Database:** Creates the necessary tables if they don't exist.

2. **Add Transaction:** Enter details like Name, Type (Income/Expense), Amount, and Date.

3. **Update Transaction:** Update transaction details via ID.

4. **View Transactions:** See a tabulated history of your finances.

5. **Delete Transaction:** Remove a specific entry by its ID (To view ID use View Transactions).

6. **Delete All:** Clears the entire database.

7. **Calculate Balance:** Shows net worth for a specific date range.

8. **Plot Balance:** Opens a window displaying your financial trend graph.

9. **Exit:** Exits the application.

11. **Calculate Interest** Shows a tabulated growth table and compound interest growth graph.

To return to main menu, press `Ctrl+C`.

## Project Structure
```bash
finance
├── README.md # Project Instruction
├── .gitignore # Files to exclude list from Git
├── database
│   ├── database.py # Handles DB connections and CRUD logic
│   └── finances.db # SQLite database file
├── doc
│   └── Personal Finance Tracker.docx # Commit note (Word/Google Docs)
├── helpers
│   └── helpers.py # Utility functions (e.g., date validation)
├── main.py # Main entry to the application
├── requirements.txt # List of dependencies
└── schema
    └── schema.sql # SQLite queries to create transactions table
```
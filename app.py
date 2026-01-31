import database.database as db
import helpers.helpers as hlp
from datetime import date
import sys
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
    QMessageBox,
    QPushButton,
    QSizePolicy,
    QLabel,
    QMessageBox,
    QFormLayout,
    QLineEdit,
    QComboBox,
    QDateEdit,
    QTableWidget,
)
from PyQt6.QtCore import Qt


class AddTransactionForm(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add Transaction")
        self.resize(300, 200)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        form_layout = QFormLayout()

        self.name_input = QLineEdit()
        form_layout.addRow("Transaction Name:", self.name_input)

        self.amount_input = QLineEdit()
        form_layout.addRow("Amount:", self.amount_input)

        self.type_input = QComboBox()
        self.type_input.addItems(["income", "expense"])
        form_layout.addRow("Transaction Type:", self.type_input)

        self.date_input = QDateEdit()
        self.date_input.setCalendarPopup(True)
        form_layout.addRow("Transaction Date:", self.date_input)

        submit_button = QPushButton("Add Transaction")
        submit_button.clicked.connect(self.submit_transaction)
        self.layout.addLayout(form_layout)
        self.layout.addWidget(submit_button)

    def submit_transaction(self):
        name = self.name_input.text()
        amount = self.amount_input.text()
        transaction_type = self.type_input.currentText()
        date = self.date_input.date().toString("yyyy-MM-dd")
        print(name, amount, transaction_type, date)

        if not name or not amount:
            QMessageBox.warning(self, "Error", "Please fill in all fields.")
            return

        try:
            amount = float(amount)
        except ValueError:
            QMessageBox.warning(self, "Error", "Please enter a valid amount.")
            return

        db.add_transaction(name, transaction_type, amount, date)
        QMessageBox.information(self, "Success", f"Transaction added: {name}")


class ViewTransactionTable(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("View Transactions")
        self.resize(600, 400)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.table = QTableWidget()
        self.layout.addWidget(self.table)

        self.load_data()

    def load_data(self):
        data = hlp.get_data()
        if not data:
            QMessageBox.information(self, "Info", "No transactions found.")
            return

        self.table.setRowCount(len(data))
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(
            ["ID", "Transaction Name", "Transaction Type", "Amount", "Transaction Date"]
        )

        for row_idx, row_data in enumerate(data):
            for col_idx, item in enumerate(row_data):
                self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(item)))

        self.table.resizeColumnsToContents()


class FinanceManager(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Finance Manager")
        self.resize(600, 400)

        center_widget = QWidget()
        self.setCentralWidget(center_widget)

        self.layout = QVBoxLayout()
        center_widget.setLayout(self.layout)

        title = QLabel("Finance Manager")
        self.layout.addWidget(title)
        init_button = QPushButton("Initialize Database", self)
        self.layout.addWidget(init_button)
        init_button.clicked.connect(self.init_db)

        add_button = QPushButton("Add Transaction", self)
        self.layout.addWidget(add_button)
        add_button.clicked.connect(self.add_transaction)

        view_button = QPushButton("View Transactions", self)
        self.layout.addWidget(view_button)
        view_button.clicked.connect(self.view_transactions)

    def init_db(self):
        try:
            db.init_db()
            QMessageBox.information(
                self, "Success", "Database initialized successfully."
            )
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to initialize database: {e}")

    def add_transaction(self):
        self.add_form = AddTransactionForm()
        self.add_form.show()

    def view_transactions(self):
        self.view_table = ViewTransactionTable()
        self.view_table.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FinanceManager()
    window.show()
    sys.exit(app.exec())

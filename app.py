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
from PyQt6.QtGui import QIcon


class AddTransactionForm(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add Transaction")
        self.resize(300, 200)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        form_layout = QFormLayout()

        self.transaction_name_input = QLineEdit()
        form_layout.addRow("Transaction transaction_name:", self.transaction_name_input)

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
        transaction_name = self.transaction_name_input.text()
        amount = self.amount_input.text()
        transaction_type = self.type_input.currentText()
        date = self.date_input.date().toString("yyyy-MM-dd")
        print(transaction_name, amount, transaction_type, date)

        if not transaction_name or not amount:
            QMessageBox.warning(self, "Error", "Please fill in all fields.")
            return

        try:
            amount = float(amount)
        except ValueError:
            QMessageBox.warning(self, "Error", "Please enter a valid amount.")
            return

        db.add_transaction(transaction_name, transaction_type, amount, date)
        QMessageBox.information(
            self, "Success", f"Transaction added: {transaction_name}"
        )


class ViewTransactionTable(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("View Transactions")
        self.resize(600, 400)

        self.is_loading = False
        self.modified_rows = set()

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.table = QTableWidget()
        self.table.itemChanged.connect(self.handle_item_changed)
        self.layout.addWidget(self.table)

        button_layout = QVBoxLayout()

        self.save_button = QPushButton("Save Changes")
        self.save_button.setEnabled(False)
        self.save_button.clicked.connect(self.save_changes)
        button_layout.addWidget(self.save_button)

        self.discard_button = QPushButton("Discard Changes")
        self.discard_button.setEnabled(False)
        self.discard_button.clicked.connect(self.load_data)
        button_layout.addWidget(self.discard_button)

        self.delete_button = QPushButton("Delete Selected")
        self.delete_button.clicked.connect(self.delete_transaction)
        button_layout.addWidget(self.delete_button)

        self.reset_button = QPushButton("Reset Database")
        self.reset_button.clicked.connect(self.reset_db)
        button_layout.addWidget(self.reset_button)

        self.exit_button = QPushButton("Exit")
        self.exit_button.clicked.connect(self.close)
        button_layout.addWidget(self.exit_button)

        self.layout.addLayout(button_layout)

        self.load_data()

    def load_data(self):
        self.is_loading = True
        self.modified_rows.clear()

        self.save_button.setEnabled(False)
        self.discard_button.setEnabled(False)

        data = hlp.get_data()
        self.table.setRowCount(0)

        if not data:
            QMessageBox.information(self, "Info", "No transactions found.")
            self.is_loading = False
            return

        self.table.setRowCount(len(data))
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(
            [
                "ID",
                "Transaction Name",
                "Transaction Type",
                "Amount",
                "Transaction Date",
            ]
        )

        for row_idx, row_data in enumerate(data):
            for col_idx, item in enumerate(row_data):
                table_item = QTableWidgetItem(str(item))
                if col_idx == 0:
                    table_item.setFlags(
                        Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled
                    )
                self.table.setItem(row_idx, col_idx, table_item)

        self.table.resizeColumnsToContents()
        self.is_loading = False

    def handle_item_changed(self, item):
        if self.is_loading:
            return

        self.modified_rows.add(item.row())
        self.save_button.setEnabled(True)
        self.save_button.setText("Save Changes")
        self.discard_button.setEnabled(True)

    def save_changes(self):
        try:
            for row in self.modified_rows:
                transaction_id = self.table.item(row, 0).text()
                transaction_name = self.table.item(row, 1).text()
                transaction_type = self.table.item(row, 2).text()
                amount = self.table.item(row, 3).text()
                date = self.table.item(row, 4).text()
                if transaction_type not in ["income", "expense"]:
                    raise ValueError(f"Row {row+1}: Type must be 'income' or 'expense'")
                if not hlp.is_valid_date(date):
                    raise ValueError(
                        f"Row {row+1}: Invalid date format, should be YYYY-MM-DD"
                    )
                amount = float(amount)
                if amount < 0:
                    raise ValueError(f"Row {row+1}: Amount must be a positive number")
                db.update_transactions(
                    transaction_id, transaction_name, transaction_type, amount, date
                )
            QMessageBox.information(self, "Success", "All changes saved!")
            self.load_data()
        except Exception as e:
            QMessageBox.critical(self, "Save Failed", str(e))

    def delete_transaction(self):
        current_row = self.table.currentRow()
        if current_row == -1:
            QMessageBox.warning(self, "Error", "No row selected.")
            return
        transaction_id = self.table.item(current_row, 0).text()
        confirm = QMessageBox.question(
            self,
            "Confirm Delete",
            f"Are you sure you want to delete transaction ID {transaction_id}?",
        )
        if confirm == QMessageBox.StandardButton.Yes:
            db.delete_transaction(transaction_id)
            QMessageBox.information(
                self, "Deleted", f"Transaction ID {transaction_id} deleted."
            )
            self.load_data()
            self.modified_rows.discard(current_row)

    def reset_db(self):
        confirm = QMessageBox.question(
            self, "Reset Database", "Are you sure you want to reset the database?"
        )
        if confirm == QMessageBox.StandardButton.Yes:
            db.delete_all_transactions()
            self.load_data()


class FinanceManager(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Finance Manager")
        self.resize(600, 400)
        self.setWindowIcon(QIcon("src/logo.png"))

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

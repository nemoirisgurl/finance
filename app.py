import database.database as db
import helpers.helpers as hlp
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
)
from PyQt6.QtCore import Qt


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

    def init_db(self):
        try:
            db.init_db()
            QMessageBox.information(
                self, "Success", "Database initialized successfully."
            )
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to initialize database: {e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FinanceManager()
    window.show()
    sys.exit(app.exec())

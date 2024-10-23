import sys
import json
from PyQt6 import QtWidgets
from PyQt6.QtGui import QFont, QDragEnterEvent, QDropEvent
from PyQt6.QtWidgets import QListWidgetItem
from PyQt6.QtCore import Qt
from ui_mainwindow import Ui_MainWindow

class MainApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.showMaximized() # will show full window
        # Enable drag-and-drop
        self.ui.listWidget.setAcceptDrops(True)

        # Connecting menu actions
        self.ui.actionPurchaseBill.triggered.connect(lambda: self.add_button("PurchaseBill"))
        self.ui.actionBill.triggered.connect(lambda: self.add_button("Bill"))
        self.ui.actiontool3.triggered.connect(lambda: self.add_button("Tool3"))

        # Load saved buttons
        self.load_buttons()

        # ComboBox setup
        self.ui.comboBox.addItems(["Favorites", "PurchaseBill", "Bill", "Tool3"])
        self.ui.comboBox.currentIndexChanged.connect(self.store_current_selection)

        # Set font size for ComboBox
        font = QFont()
        font.setPointSize(14)
        self.ui.comboBox.setFont(font)

    def add_button(self, name):
        """Add a button to the ListWidget."""
        if not any(self.ui.listWidget.item(i).text() == name for i in range(self.ui.listWidget.count())):
            item = QListWidgetItem(name)
            self.ui.listWidget.addItem(item)
            self.save_buttons()
        else:
            QtWidgets.QMessageBox.warning(self, "Duplicate Button", f"'{name}' is already in your favorites.")

    def store_current_selection(self):
        """Store the current ComboBox selection."""
        current_selection = self.ui.comboBox.currentText()
        print(f"Current ComboBox selection: {current_selection}")

    def save_buttons(self):
        """Save current buttons to a JSON file."""
        items = [self.ui.listWidget.item(i).text() for i in range(self.ui.listWidget.count())]
        with open("buttons.json", "w") as f:
            json.dump(items, f)

    def load_buttons(self):
        """Load buttons from a JSON file."""
        try:
            with open("buttons.json", "r") as f:
                items = json.load(f)
                for item in items:
                    self.ui.listWidget.addItem(item)
        except (FileNotFoundError, json.JSONDecodeError):
            pass

    def dragEnterEvent(self, event: QDragEnterEvent):
        """Handle drag enter events."""
        if event.mimeData().hasFormat("text/plain"):
            event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent):
        """Handle drop events."""
        if event.mimeData().hasFormat("text/plain"):
            item = QListWidgetItem(event.mimeData().text())
            self.ui.listWidget.addItem(item)
            event.acceptProposedAction()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec())

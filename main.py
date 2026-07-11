import sys

from PySide6.QtWidgets import QApplication

from gui.main_window import MainWindow
from utils.logger import setup_logger
from database.database import initialize_database
from themes.dark import STYLE


def main():

    setup_logger()

    initialize_database()

    app = QApplication(sys.argv)

    app.setApplicationName("NetWatch")
    app.setStyleSheet(STYLE)

    window = MainWindow()

    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()

import sys
from typing import List

from PyQt6.QtCore import QSize
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import (
    QApplication,
    QFrame,
    QHeaderView,
    QHBoxLayout,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QSpacerItem,
    QSizePolicy,
    QTableWidget,
    QTableWidgetItem,
    QToolBar,
    QVBoxLayout,
    QWidget,
)

# Local modules
from database_manager import db_manager
from insert_student_dialog import InsertStudentDialog


class StudentManagementForm(QMainWindow):
    """GUI principale per la gestione degli studenti (PyQt6 + MySQL)."""

    # ------------------------------------------------------------------
    # Costruzione -------------------------------------------------------
    # ------------------------------------------------------------------
    def __init__(self) -> None:
        super().__init__()
        self.students_data: List[List[str]] = []
        self._init_ui()
        self._load_students_from_database()

    # ------------------------------------------------------------------
    # Inizializzazione UI ----------------------------------------------
    # ------------------------------------------------------------------
    def _init_ui(self) -> None:
        self.setWindowTitle("Student Management System – MySQL")
        self.resize(900, 600)

        # Widget centrale e layout principale
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)

        # Creazione componenti
        self._create_menu_bar()
        self._create_tool_bar()
        self._create_table()
        main_layout.addWidget(self.table)
        self._create_footer()
        main_layout.addWidget(self.footer_frame)

        # Style‑sheet (senza proprietà non supportate)
        self.setStyleSheet(
            """
            QMainWindow { background-color: #f0f0f0; }

            QTableWidget {
                border: 2px solid #333;
                background: #ffffff;
                gridline-color: #333;
                selection-background-color: #0078d4;
            }
            QTableWidget::item {
                border-right: 1px solid #333;
                border-bottom: 1px solid #333;
                padding: 4px;
            }
            QHeaderView::section {
                background: #e0e0e0;
                border: 1px solid #333;
                padding: 6px;
                font-weight: bold;
            }
            QPushButton {
                background: #e0e0e0;
                border: 2px solid #333;
                padding: 6px 14px;
                font-size: 11px;
                min-width: 110px;
            }
            QPushButton:hover  { background: #d0d0d0; }
            QPushButton:pressed{ background: #c0c0c0; }
            QToolBar { background: #f0f0f0; spacing: 5px; border: none; }
            QMenuBar { background: #f0f0f0; }
            QMenuBar::item { padding: 4px 8px; }
            QMenuBar::item:selected { background: #e0e0e0; }
            """
        )

    # ------------------------------------------------------------------
    # Menu bar ----------------------------------------------------------
    # ------------------------------------------------------------------
    def _create_menu_bar(self) -> None:
        menubar = self.menuBar()

        file_menu = menubar.addMenu("&File")
        file_menu.addAction(
            QAction("&New", self, triggered=self._open_add_student_dialog))
        file_menu.addAction(
            QAction("&Refresh", self, triggered=self._refresh_data))
        file_menu.addSeparator()
        file_menu.addAction(QAction("E&xit", self, triggered=self.close))

        help_menu = menubar.addMenu("&Help")
        help_menu.addAction(
            QAction(
                "&About",
                self,
                triggered=lambda: self._show_message(
                    "About",
                    "Student Management System\\nVersione 1.0 – backend MySQL",
                ),
            )
        )

    # ------------------------------------------------------------------
    # Tool bar ----------------------------------------------------------
    # ------------------------------------------------------------------
    def _create_tool_bar(self) -> None:
        toolbar = QToolBar(movable=False, iconSize=QSize(24, 24))
        self.addToolBar(toolbar)

        toolbar.addAction(QAction("➕", self, toolTip="Add New",
                          triggered=self._open_add_student_dialog))
        toolbar.addAction(
            QAction("🔄", self, toolTip="Refresh", triggered=self._refresh_data))
        toolbar.addAction(
            QAction("🔍", self, toolTip="Search (TODO)", triggered=self._search_records))

    # ------------------------------------------------------------------
    # Table -------------------------------------------------------------
    # ------------------------------------------------------------------
    def _create_table(self) -> None:
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(
            ["ID", "Name", "Course", "Mobile"])
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)
        self.table.setColumnWidth(0, 80)
        self.table.verticalHeader().hide()
        self.table.setSelectionBehavior(
            QTableWidget.SelectionBehavior.SelectRows)

    # ------------------------------------------------------------------
    # Footer ------------------------------------------------------------
    # ------------------------------------------------------------------
    def _create_footer(self) -> None:
        self.footer_frame = QFrame()
        self.footer_frame.setFrameStyle(QFrame.Shape.Box)
        self.footer_frame.setLineWidth(2)
        self.footer_frame.setFixedHeight(60)

        layout = QHBoxLayout(self.footer_frame)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.addItem(QSpacerItem(
            40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))

        layout.addWidget(QPushButton("Edit Record", clicked=self._edit_record))
        layout.addWidget(QPushButton(
            "Delete Record", clicked=self._delete_record))

    # ------------------------------------------------------------------
    # Data helpers ------------------------------------------------------
    # ------------------------------------------------------------------
    def _load_students_from_database(self) -> None:
        try:
            self.students_data = db_manager.get_all_students()
            if self.students_data:
                self._populate_table()
                print(
                    f"Caricati {len(self.students_data)} studenti dal database")
            else:
                self.table.setRowCount(0)
                self._show_message(
                    "Info",
                    "Nessun studente trovato nel database.\\nUsa 'File → New' per crearne uno.",
                )
        except Exception as exc:  # noqa: BLE001
            self._show_error("Errore DB", str(exc))

    def _populate_table(self) -> None:
        self.table.setRowCount(len(self.students_data))
        for r, row in enumerate(self.students_data):
            for c, value in enumerate(row):
                self.table.setItem(r, c, QTableWidgetItem(str(value)))

    def _refresh_data(self) -> None:
        print("Refresh data")
        self._load_students_from_database()

    # ------------------------------------------------------------------
    # CRUD implementations ---------------------------------------------
    # ------------------------------------------------------------------
    def _open_add_student_dialog(self) -> None:
        dialog = InsertStudentDialog(self)
        dialog.student_added.connect(self._add_student_to_database)
        dialog.exec()

    def _add_student_to_database(self, student_data: List[str]) -> None:
        _, name, course, mobile = student_data  # id is autogenerated
        if db_manager.insert_student(name, course, mobile):
            self._refresh_data()
            self._show_message(
                "Successo", f"Studente '{name}' inserito correttamente")
        else:
            self._show_error(
                "Errore", "Impossibile inserire il record nel database")

    def _edit_record(self) -> None:
        row = self.table.currentRow()
        if row < 0:
            self._show_message(
                "Attenzione", "Seleziona un record da modificare")
            return
        # TODO: implement edit dialog
        print(f"Edit clicked – row {row}")

    def _delete_record(self) -> None:
        row = self.table.currentRow()
        if row < 0:
            self._show_message(
                "Attenzione", "Seleziona un record da eliminare")
            return
        student_id = int(self.table.item(row, 0).text())
        student_name = self.table.item(row, 1).text()
        reply = QMessageBox.question(
            self,
            "Conferma eliminazione",
            f"Eliminare definitivamente '{student_name}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )
        if reply == QMessageBox.StandardButton.Yes:
            if db_manager.delete_student(student_id):
                self._refresh_data()
                self._show_message(
                    "Successo", f"Studente '{student_name}' eliminato correttamente")
            else:
                self._show_error(
                    "Errore", "Impossibile eliminare il record dal database")

    def _search_records(self) -> None:
        self._show_message("Info", "Funzionalità di ricerca da implementare")

    # ------------------------------------------------------------------
    # Utility dialogs ---------------------------------------------------
    # ------------------------------------------------------------------
    def _show_message(self, title: str, message: str) -> None:
        QMessageBox.information(self, title, message)

    def _show_error(self, title: str, message: str) -> None:
        QMessageBox.critical(self, title, message)

    # ------------------------------------------------------------------
    # Event override ----------------------------------------------------
    # ------------------------------------------------------------------
    def closeEvent(self, event) -> None:  # noqa: N802
        db_manager.disconnect()
        event.accept()


# ----------------------------------------------------------------------
# MAIN ENTRY POINT
# ----------------------------------------------------------------------
def main() -> None:
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    if not db_manager.test_connection():
        QMessageBox.critical(
            None,
            "Errore Database",
            "Impossibile connettersi al database MySQL.\\n"
            "Verifica che il server sia in esecuzione e che i parametri di connessione siano corretti.",
        )
        sys.exit(1)

    window = StudentManagementForm()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

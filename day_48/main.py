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
from search_student_dialog import SearchStudentDialog
import re
import unicodedata


def normalize(text: str) -> str:
    """Converte in minuscolo "aggressivo", rimuove diacritici e spazi superflui."""
    # ① Decompone i caratteri Unicode (NFKD) → 'ä' ⇒ 'a' + '¨'
    nfkd = unicodedata.normalize("NFKD", text)
    # ② Elimina i caratteri diacritici combinati
    no_marks = "".join(c for c in nfkd if not unicodedata.combining(c))
    # ③ Riduce sequenze di whitespace a un singolo spazio e trim
    collapsed = re.sub(r"\s+", " ", no_marks).strip()
    # ④ Case-fold (più completo di lower()) → insensibilità a maiuscole/minuscole
    return collapsed.casefold()


class StudentManagementForm(QMainWindow):
    """GUI principale per la gestione degli studenti (PyQt6 + MySQL)."""

    # ------------------------------------------------------------------
    # Costruzione -------------------------------------------------------
    # ------------------------------------------------------------------
    def __init__(self) -> None:
        super().__init__()
        self.students_data: List[List[str]] = []
        self.filtered_data: List[List[str]] = []  # Dati filtrati
        self.is_filtered: bool = False  # Stato del filtro
        self.current_search_term: str = ""  # Termine di ricerca corrente
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
                    "Student Management System\nVersione 1.0 – backend MySQL",
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
            QAction("🔍", self, toolTip="Search", triggered=self._search_records))

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

        # Pulsante per rimuovere il filtro (inizialmente nascosto)
        self.clear_filter_button = QPushButton("Clear Filter")
        self.clear_filter_button.clicked.connect(self._clear_filter)
        self.clear_filter_button.setVisible(False)
        layout.addWidget(self.clear_filter_button)

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
                    "Nessun studente trovato nel database.\nUsa 'File → New' per crearne uno.",
                )
        except Exception as exc:
            self._show_error("Errore DB", str(exc))

    def _populate_table(self) -> None:
        """Popola la tabella con i dati correnti (filtrati o completi)."""
        data_to_show = self.filtered_data if self.is_filtered else self.students_data

        self.table.setRowCount(len(data_to_show))
        for r, row in enumerate(data_to_show):
            for c, value in enumerate(row):
                self.table.setItem(r, c, QTableWidgetItem(str(value)))

        # Aggiorna il titolo della finestra per mostrare lo stato del filtro
        if self.is_filtered:
            self.setWindowTitle(
                f"Student Management System – MySQL (Filtro: '{self.current_search_term}' - {len(data_to_show)} risultati)")
        else:
            self.setWindowTitle("Student Management System – MySQL")

    def _refresh_data(self) -> None:
        """Ricarica i dati dal database e mantiene il filtro se attivo."""
        print("Refresh data")
        self._load_students_from_database()

        # Se c'è un filtro attivo, riapplicalo
        if self.is_filtered and self.current_search_term:
            self._apply_filter(self.current_search_term)

    def _apply_filter(self, search_term: str) -> None:
        """Applica il filtro ai dati basandosi sul termine di ricerca."""
        pattern_norm = normalize(search_term)
        self.filtered_data = []

        for row in self.students_data:
            # Cerca in tutte le colonne (Name, Course, Mobile)
            name_norm = normalize(row[1])  # Nome
            course_norm = normalize(row[2])  # Corso
            mobile_norm = normalize(row[3])  # Telefono

            if (pattern_norm in name_norm or
                pattern_norm in course_norm or
                    pattern_norm in mobile_norm):
                self.filtered_data.append(row)

        self.is_filtered = True
        self.current_search_term = search_term
        self.clear_filter_button.setVisible(True)
        self._populate_table()

    def _clear_filter(self) -> None:
        """Rimuove il filtro e mostra tutti i dati."""
        self.is_filtered = False
        self.current_search_term = ""
        self.filtered_data = []
        self.clear_filter_button.setVisible(False)
        self._populate_table()

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
        """Apre la dialog di ricerca e applica il filtro."""
        dialog = SearchStudentDialog(self)

        if dialog.exec():  # Se l'utente clicca "Search"
            search_term = dialog.search_text()

            if search_term:
                self._apply_filter(search_term)

                # Mostra risultati
                if self.filtered_data:
                    self._show_message(
                        "Ricerca",
                        f"Trovati {len(self.filtered_data)} studenti che corrispondono a '{search_term}'"
                    )
                    # Seleziona la prima riga se ci sono risultati
                    if self.table.rowCount() > 0:
                        self.table.selectRow(0)
                        self.table.scrollToItem(
                            self.table.item(0, 1),
                            QTableWidget.ScrollHint.PositionAtCenter
                        )
                else:
                    self._show_message(
                        "Ricerca", f"Nessun studente trovato per '{search_term}'")
                    self._clear_filter()  # Rimuove il filtro se non ci sono risultati

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
    def closeEvent(self, event) -> None:
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
            "Impossibile connettersi al database MySQL.\n"
            "Verifica che il server sia in esecuzione e che i parametri di connessione siano corretti.",
        )
        sys.exit(1)

    window = StudentManagementForm()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

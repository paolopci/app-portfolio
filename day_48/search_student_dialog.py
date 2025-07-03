from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QLineEdit, QPushButton,
    QSpacerItem, QSizePolicy
)
from PyQt6.QtCore import Qt


class SearchStudentDialog(QDialog):
    """Finestra modale per la ricerca di studenti per nome."""

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Search Student")
        self.setFixedSize(400, 200)
        self.setModal(True)
        self._init_ui()

    # -------------------------- UI -----------------------------------
    def _init_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(20)

        # Spazio superiore → centratura verticale
        layout.addItem(QSpacerItem(
            20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        # Input di ricerca
        self.line_edit = QLineEdit()
        self.line_edit.setPlaceholderText("Valore da ricercare")
        self.line_edit.setFixedHeight(40)
        self.line_edit.textChanged.connect(self._toggle_button)
        self.line_edit.returnPressed.connect(self._do_search)
        layout.addWidget(
            self.line_edit, alignment=Qt.AlignmentFlag.AlignCenter)

        # Pulsante Search
        self.search_btn = QPushButton("Search")
        self.search_btn.setFixedHeight(45)
        self.search_btn.setEnabled(False)
        self.search_btn.clicked.connect(self._do_search)
        layout.addWidget(
            self.search_btn, alignment=Qt.AlignmentFlag.AlignCenter)

        # Spazio inferiore → centratura verticale
        layout.addItem(QSpacerItem(
            20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        # Stile minimale (coerente con la figura)
        self.setStyleSheet("""
            QDialog  { background-color: #ffffff; border: 2px solid #000000; }
            QLineEdit{ border: 2px solid #000000; padding: 8px 12px; }
            QPushButton { border: 2px solid #000000; padding: 10px 20px; }
            QPushButton:disabled { color: #aaaaaa; border: 2px solid #888888; }
        """)

    # ----------------------- Helpers ---------------------------------
    def _toggle_button(self) -> None:
        self.search_btn.setEnabled(bool(self.line_edit.text().strip()))

    def _do_search(self) -> None:
        if not self.line_edit.text().strip():
            return
        self.accept()                                # chiude la dialog

    # --------------------- API pubblica ------------------------------
    def search_text(self) -> str:
        """Restituisce la stringa digitata dall’utente (trimmed)."""
        return self.line_edit.text().strip()

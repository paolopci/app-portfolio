import time
from typing import List, Optional, Tuple

import mysql.connector
from mysql.connector import Error


class DatabaseManager:
    """Layer di accesso dati per il progetto Student‑Management.

    • Gestisce connessione / disconnessione con retry.
    • Espone CRUD per tabelle *students* e *courses*.
    • Garantisce che ogni query disponga di una connessione aperta.
    """

    # ------------------------------------------------------------------
    # COSTRUZIONE E PARAMETRI ------------------------------------------
    # ------------------------------------------------------------------
    def __init__(self) -> None:
        self.connection_config = {
            "host": "localhost",
            "port": 3306,
            "database": "SchoolDb",
            "user": "root",
            "password": "Venerina@07",
            "charset": "utf8mb4",
            "autocommit": True,
            "connect_timeout": 10,
            "raise_on_warnings": True,
        }
        self.connection: Optional[mysql.connector.MySQLConnection] = None
        self.max_retries: int = 3
        self.retry_delay: int = 1  # secondi

    # ------------------------------------------------------------------
    # CONNESSIONE / DISCONNESSIONE -------------------------------------
    # ------------------------------------------------------------------
    def _ensure_connection(self) -> bool:
        """Verifica che *self.connection* sia aperta, altrimenti prova a riconnettere."""
        if self.connection and self.connection.is_connected():
            return True
        return self.connect()

    def connect(self) -> bool:
        """Apre la connessione a MySQL con meccanismo di retry."""
        for attempt in range(1, self.max_retries + 1):
            try:
                print(
                    f"Tentativo di connessione {attempt}/{self.max_retries}…")
                self.connection = mysql.connector.connect(
                    **self.connection_config)
                server_ver = self.connection.get_server_info()
                print(
                    "Connessione al database MySQL stabilita (server " f"{server_ver})")
                return True
            except Error as e:
                print(f"Tentativo {attempt} fallito: {e.msg} ({e.errno})")
                if e.errno in (1045, 1049):
                    # Credenziali errate o database inesistente → inutile ritentare
                    break
                time.sleep(self.retry_delay)
        return False

    def disconnect(self) -> None:
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("Connessione al database chiusa")
            self.connection = None

    # ------------------------------------------------------------------
    # ESECUZIONE QUERY --------------------------------------------------
    # ------------------------------------------------------------------
    def execute_query(self, query: str, params: Optional[Tuple] = None) -> List[Tuple]:
        if not self._ensure_connection():
            print("MySQL Connection not available (execute_query)")
            return []
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, params)
            rows = cursor.fetchall()
            cursor.close()
            return rows
        except Error as e:
            print(
                f"Errore durante l'esecuzione della query: {e.msg} ({e.errno})")
            print(f"Query: {query}")
            return []

    def execute_non_query(self, query: str, params: Optional[Tuple] = None) -> bool:
        if not self._ensure_connection():
            print("MySQL Connection not available (execute_non_query)")
            return False
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, params)
            self.connection.commit()
            cursor.close()
            return True
        except Error as e:
            print(
                f"Errore durante l'esecuzione della query: {e.msg} ({e.errno})")
            print(f"Query: {query}\nParametri: {params}")
            return False

    # ------------------------------------------------------------------
    # CRUD STUDENTI -----------------------------------------------------
    # ------------------------------------------------------------------
    def get_all_students(self) -> List[List[str]]:
        """Restituisce tutti gli studenti (id, name, course, mobile)."""
        query = "SELECT id, name, course, mobile FROM students ORDER BY id"
        rows = self.execute_query(query)
        return [[str(r[0]), r[1], r[2], r[3]] for r in rows]

    def get_next_student_id(self) -> int:
        """Restituisce il prossimo ID disponibile per un nuovo studente."""
        query = "SELECT MAX(id) FROM students"
        rows = self.execute_query(query)
        if rows and rows[0][0] is not None:
            return rows[0][0] + 1
        return 1

    def insert_student(self, name: str, course: str, mobile: str) -> bool:
        query = "INSERT INTO students (name, course, mobile) VALUES (%s, %s, %s)"
        return self.execute_non_query(query, (name, course, mobile))

    def update_student(self, student_id: int, name: str, course: str, mobile: str) -> bool:
        query = "UPDATE students SET name = %s, course = %s, mobile = %s WHERE id = %s"
        return self.execute_non_query(query, (name, course, mobile, student_id))

    def delete_student(self, student_id: int) -> bool:
        query = "DELETE FROM students WHERE id = %s"
        return self.execute_non_query(query, (student_id,))

    # ------------------------------------------------------------------
    # CRUD CORSI --------------------------------------------------------
    # ------------------------------------------------------------------
    def get_all_courses(self) -> List[str]:
        query = "SELECT course FROM courses ORDER BY course"
        rows = self.execute_query(query)
        return [r[0] for r in rows]

    # ------------------------------------------------------------------
    # DIAGNOSTICA -------------------------------------------------------
    # ------------------------------------------------------------------
    def test_connection(self) -> bool:
        """Verifica la raggiungibilità del DB **senza** chiudere la connessione."""
        ok = self.connect()
        print("Test di connessione:", "SUCCESSO" if ok else "FALLITO")
        return ok


# Singleton globale
db_manager = DatabaseManager()

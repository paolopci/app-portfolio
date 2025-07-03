import mysql.connector
from mysql.connector import Error
from typing import List, Optional, Tuple


class DatabaseManager:
    """Gestisce le operazioni del database MySQL per il sistema di gestione studenti"""

    def __init__(self):
        self.connection_config = {
            'host': 'localhost',  # CORREZIONE: rimosso '1' da 'localhost1'
            'port': 3306,
            'database': 'SchoolDb',
            'user': 'root',
            'password': 'Venerina@07',
            'charset': 'utf8mb4',
            'autocommit': True
        }
        self.connection = None

    def connect(self) -> bool:
        """Stabilisce la connessione al database MySQL"""
        try:
            self.connection = mysql.connector.connect(**self.connection_config)
            if self.connection.is_connected():
                print("Connessione al database MySQL stabilita con successo")
                return True
        except Error as e:
            print(f"Errore durante la connessione al database: {e}")
            return False
        return False

    def disconnect(self):
        """Chiude la connessione al database"""
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("Connessione al database chiusa")

    def execute_query(self, query: str, params: tuple = None) -> Optional[List[Tuple]]:
        """Esegue una query SELECT e restituisce i risultati"""
        if not self.connection or not self.connection.is_connected():
            if not self.connect():
                return None

        try:
            cursor = self.connection.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)

            results = cursor.fetchall()
            cursor.close()
            return results
        except Error as e:
            print(f"Errore durante l'esecuzione della query: {e}")
            return None

    def execute_non_query(self, query: str, params: tuple = None) -> bool:
        """Esegue una query INSERT, UPDATE, DELETE"""
        if not self.connection or not self.connection.is_connected():
            if not self.connect():
                return False

        try:
            cursor = self.connection.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)

            self.connection.commit()
            cursor.close()
            print(
                f"Query eseguita con successo. Righe interessate: {cursor.rowcount}")
            return True
        except Error as e:
            print(f"Errore durante l'esecuzione della query: {e}")
            self.connection.rollback()
            return False

    def get_all_students(self) -> List[List[str]]:
        """Recupera tutti gli studenti dalla tabella students"""
        query = "SELECT id, name, courses, mobile FROM students ORDER BY id"
        results = self.execute_query(query)

        if results:
            return [[str(row[0]), row[1], row[2], row[3]] for row in results]
        return []

    def get_all_courses(self) -> List[str]:
        """Recupera tutti i corsi dalla tabella courses"""
        query = "SELECT course FROM courses ORDER BY course"
        results = self.execute_query(query)

        if results:
            return [row[0] for row in results]
        return []

    def insert_student(self, name: str, course: str, mobile: str) -> bool:
        """Inserisce un nuovo studente nella tabella students"""
        query = "INSERT INTO students (name, courses, mobile) VALUES (%s, %s, %s)"
        params = (name, course, mobile)
        return self.execute_non_query(query, params)

    def update_student(self, student_id: int, name: str, course: str, mobile: str) -> bool:
        """Aggiorna un studente esistente"""
        query = "UPDATE students SET name = %s, courses = %s, mobile = %s WHERE id = %s"
        params = (name, course, mobile, student_id)
        return self.execute_non_query(query, params)

    def delete_student(self, student_id: int) -> bool:
        """Elimina uno studente dalla tabella students"""
        query = "DELETE FROM students WHERE id = %s"
        params = (student_id,)
        return self.execute_non_query(query, params)

    def get_next_student_id(self) -> int:
        """Ottiene il prossimo ID disponibile per un nuovo studente"""
        query = "SELECT MAX(id) FROM students"
        results = self.execute_query(query)

        if results and results[0][0] is not None:
            return results[0][0] + 1
        return 1

    def initialize_sample_data(self):
        """Inizializza il database con dati di esempio se vuoto"""
        # Controlla se ci sono già dati
        existing_students = self.get_all_students()
        if existing_students:
            print("Il database contiene già dati studenti")
            return

        # Inserisce i corsi di esempio
        sample_courses = ["Biology", "Math", "Astronomy",
                          "Physics", "Computer Science", "Mathematics", "Chemistry"]

        for course in sample_courses:
            query = "INSERT IGNORE INTO courses (course) VALUES (%s)"
            self.execute_non_query(query, (course,))

        # Inserisce gli studenti di esempio
        sample_students = [
            ('Mario Rossi', 'Computer Science', '333-1234567'),
            ('Anna Bianchi', 'Mathematics', '333-2345678'),
            ('Luca Verdi', 'Physics', '333-3456789'),
            ('Sara Neri', 'Chemistry', '333-4567890'),
            ('Marco Blu', 'Biology', '333-5678901')
        ]

        for student in sample_students:
            self.insert_student(student[0], student[1], student[2])

        print("Dati di esempio inseriti nel database")

    def test_connection(self) -> bool:
        """Testa la connessione al database"""
        if self.connect():
            print("Test di connessione: SUCCESSO")
            self.disconnect()
            return True
        else:
            print("Test di connessione: FALLITO")
            return False


# Istanza globale del database manager
db_manager = DatabaseManager()

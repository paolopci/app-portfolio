import mysql.connector
from mysql.connector import Error
import socket
import sys
import traceback


def test_port_connection(host, port):
    """Testa se la porta è raggiungibile"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        result = sock.connect_ex((host, port))
        sock.close()
        return result == 0
    except Exception as e:
        print(f"Errore nel test della porta: {e}")
        return False


def test_database_connection():
    """Test completo della connessione al database"""
    print("=== DIAGNOSI CONNESSIONE DATABASE ===\n")

    # Configurazioni da testare
    configs = [
        {
            'name': 'Configurazione Docker (localhost)',
            'host': 'localhost',
            'port': 3306,
            'database': 'SchoolDb',
            'user': 'root',
            'password': 'Venerina@07',
            'charset': 'utf8mb4',
            'autocommit': True
        },
        {
            'name': 'Configurazione Docker (127.0.0.1)',
            'host': '127.0.0.1',
            'port': 3306,
            'database': 'SchoolDb',
            'user': 'root',
            'password': 'Venerina@07',
            'charset': 'utf8mb4',
            'autocommit': True
        },
        {
            'name': 'Configurazione Docker (senza database specifico)',
            'host': 'localhost',
            'port': 3306,
            'user': 'root',
            'password': 'Venerina@07',
            'charset': 'utf8mb4',
            'autocommit': True
        }
    ]

    for config in configs:
        print(f"\n--- Test: {config['name']} ---")

        # Test 1: Verifica raggiungibilità porta
        print(f"1. Test porta {config['host']}:{config['port']}...")
        if test_port_connection(config['host'], config['port']):
            print("   ✓ Porta raggiungibile")
        else:
            print("   ✗ Porta NON raggiungibile")
            print("   Suggerimento: Verifica che Docker MySQL sia in esecuzione")
            print("   Comando: docker ps | grep mysql")
            continue

        # Test 2: Connessione MySQL
        print("2. Test connessione MySQL...")
        try:
            connection = mysql.connector.connect(**config)

            if connection.is_connected():
                print("   ✓ Connessione MySQL riuscita")

                # Test 3: Verifica database
                cursor = connection.cursor()
                cursor.execute("SELECT DATABASE();")
                current_db = cursor.fetchone()
                print(
                    f"   Database attuale: {current_db[0] if current_db[0] else 'Nessuno'}")

                # Test 4: Lista dei database
                cursor.execute("SHOW DATABASES;")
                databases = cursor.fetchall()
                print("   Database disponibili:")
                for db in databases:
                    print(f"     - {db[0]}")

                # Test 5: Se connesso a SchoolDb, verifica tabelle
                if 'database' in config and config['database']:
                    try:
                        cursor.execute("SHOW TABLES;")
                        tables = cursor.fetchall()
                        print(f"   Tabelle in {config['database']}:")
                        for table in tables:
                            print(f"     - {table[0]}")

                        # Test 6: Verifica dati nelle tabelle
                        if tables:
                            for table in tables:
                                table_name = table[0]
                                cursor.execute(
                                    f"SELECT COUNT(*) FROM {table_name};")
                                count = cursor.fetchone()[0]
                                print(f"     {table_name}: {count} righe")

                    except Error as e:
                        print(
                            f"   ⚠ Errore nell'accesso al database {config['database']}: {e}")

                cursor.close()
                connection.close()
                print("   ✓ Connessione chiusa correttamente")

                # Se arriviamo qui, la connessione funziona
                print(f"\n🎉 SUCCESSO! Configurazione funzionante:")
                print(f"   Host: {config['host']}")
                print(f"   Port: {config['port']}")
                print(f"   Database: {config.get('database', 'N/A')}")
                print(f"   User: {config['user']}")
                return True

        except Error as e:
            print(f"   ✗ Errore MySQL: {e}")
            print(f"   Codice errore: {e.errno}")
            print(f"   Messaggio: {e.msg}")

            # Suggerimenti specifici per errori comuni
            if e.errno == 1045:  # Access denied
                print("   Suggerimento: Verifica username e password")
            elif e.errno == 1049:  # Database non esiste
                print("   Suggerimento: Il database 'SchoolDb' non esiste")
            elif e.errno == 2003:  # Can't connect
                print("   Suggerimento: MySQL server non raggiungibile")
            elif e.errno == 1251:  # Client does not support
                print("   Suggerimento: Problema di autenticazione MySQL 8.0")

        except Exception as e:
            print(f"   ✗ Errore generico: {e}")
            print(f"   Traceback: {traceback.format_exc()}")

    print("\n❌ NESSUNA CONFIGURAZIONE FUNZIONANTE TROVATA")
    return False


def suggest_solutions():
    """Fornisce suggerimenti per risolvere i problemi comuni"""
    print("\n=== SUGGERIMENTI PER RISOLVERE I PROBLEMI ===\n")

    print("1. VERIFICA DOCKER:")
    print("   docker ps | grep mysql")
    print("   docker logs [container_id]")
    print()

    print("2. VERIFICA PORTA:")
    print("   netstat -an | grep 3306")
    print("   telnet localhost 3306")
    print()

    print("3. CONNESSIONE DIRETTA A MYSQL:")
    print("   mysql -h localhost -P 3306 -u root -p")
    print("   (inserire password: Venerina@07)")
    print()

    print("4. RICREA DATABASE SE NECESSARIO:")
    print("   CREATE DATABASE SchoolDb;")
    print("   USE SchoolDb;")
    print("   CREATE TABLE students (")
    print("       id INT AUTO_INCREMENT PRIMARY KEY,")
    print("       name VARCHAR(255) NOT NULL,")
    print("       courses VARCHAR(255),")
    print("       mobile VARCHAR(20)")
    print("   );")
    print("   CREATE TABLE courses (")
    print("       id INT AUTO_INCREMENT PRIMARY KEY,")
    print("       course VARCHAR(255) NOT NULL UNIQUE")
    print("   );")
    print()

    print("5. PROBLEMA AUTENTICAZIONE MYSQL 8.0:")
    print("   ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'Venerina@07';")
    print("   FLUSH PRIVILEGES;")


if __name__ == "__main__":
    print("Avvio diagnosi connessione database...")
    print("Python version:", sys.version)

    try:
        import mysql.connector
        print("mysql-connector-python version:", mysql.connector.__version__)
    except ImportError:
        print("❌ mysql-connector-python NON INSTALLATO!")
        print("Installare con: pip install mysql-connector-python")
        sys.exit(1)

    success = test_database_connection()

    if not success:
        suggest_solutions()

    print("\n=== FINE DIAGNOSI ===")

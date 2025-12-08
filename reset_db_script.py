import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# Database credentials
DB_NAME = 'student_db'
DB_USER = 'django_user'
DB_PASS = '1234567890'
DB_HOST = 'localhost'
DB_PORT = '5432'

def reset_database():
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASS,
            host=DB_HOST,
            port=DB_PORT
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()

        # Get all table names
        cur.execute("""
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public'
            AND table_type = 'BASE TABLE';
        """)
        tables = cur.fetchall()

        if not tables:
            print("No tables found to drop.")
        else:
            print(f"Found {len(tables)} tables. Dropping...")
            for table in tables:
                table_name = table[0]
                print(f"Dropping table {table_name}...")
                cur.execute(f'DROP TABLE IF EXISTS "{table_name}" CASCADE;')

        cur.close()
        conn.close()
        print("All tables dropped successfully.")

    except Exception as e:
        print(f"Error resetting database: {e}")

if __name__ == "__main__":
    reset_database()

import sqlite3

class Database:
    def __init__(self, db_name="store.db"):
        self.conn = sqlite3.connect(db_name, check_same_thread=False)  # Поддержка многопоточности
        self.create_tables()

    def create_tables(self):
        with self.conn:
            # Таблица пользователей
            self.conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE,
                password TEXT,
                role TEXT CHECK(role IN ('admin', 'user')) NOT NULL
            )
            """)

            # Таблица заказов
            self.conn.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                order_number TEXT,
                status TEXT DEFAULT 'ожидание',
                FOREIGN KEY(user_id) REFERENCES users(id)
            )
            """)

            # Таблица позиций заказа
            self.conn.execute("""
            CREATE TABLE IF NOT EXISTS order_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_id INTEGER,
                product_id INTEGER,
                quantity INTEGER,
                price REAL,
                FOREIGN KEY(order_id) REFERENCES orders(id),
                FOREIGN KEY(product_id) REFERENCES products(id)
            )
            """)

            # Таблица товаров
            self.conn.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                price REAL,
                quantity INTEGER DEFAULT 0
            )
            """)

    def query(self, query, params=()):
        with self.conn:
            cursor = self.conn.execute(query, params)
            self.conn.commit()
            return cursor

    def fetch_all(self, query, params=()):
        cursor = self.query(query, params)
        return cursor.fetchall()

    def fetch_one(self, query, params=()):
        cursor = self.query(query, params)
        return cursor.fetchone()

if __name__ == "__main__":
    db = Database()
    print("Database initialized.")

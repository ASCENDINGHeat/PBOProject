import sqlite3


class User:
    def __init__(self, id, username):
        self.id = id
        self.username = username

class AuthSystem:
    def __init__(self, conn):
        self.conn = conn

    def register(self, username, email, password):
        cursor = self.conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO users (username, email, password)
                VALUES (?, ?, ?)
            """, (username, email, password))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError as e:
            self.conn.rollback()
            return False, str(e)

    def login(self, identifier, password):
        cursor = self.conn.cursor()
        query = """
            SELECT id, username FROM users 
            WHERE (username = ? OR email = ?) AND password = ?
        """
        cursor.execute(query, (identifier, identifier, password))
        user_data =  cursor.fetchone()
        if user_data:
            return User(user_data[0], user_data[1])
        return None
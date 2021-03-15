from sqlite3 import connect
from datetime import datetime
from shutil import copyfile

class BidulaxCenterDataBase:

    def __init__(self):
        self.connection = connect("database/database.db")
        self.cursor = self.connection.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS users(username TEXT PRIMARY KEY, password TEXT)")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS permissions(username TEXT, permission TEXT)")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS informations(key TEXT PRIMARY KEY, value TEXT)")
        self.connection.commit()

    def backup(self):
        self.cursor.close()
        self.connection.close()
        copyfile("database/database.db", f"database/backups/{str(datetime.now())[:16].replace(' ', '-').replace(':', '-')}.db")
        self.__init__()
        return self

    def close(self):
        self.cursor.close()
        self.connection.close()

    def add_user(self, username, password):
        self.cursor.execute(f"INSERT INTO users (username, password) VALUES (\"{username}\", \"{password}\")")
        self.connection.commit()
        return self.cursor

    def remove_user(self, username):
        self.cursor.execute(f"DELETE FROM users WHERE username=\"{username}\"")
        self.connection.commit()
        return self.cursor

    def user_exists(self, username, password=None):
        if password:
            self.cursor.execute(f"SELECT * FROM users WHERE username=\"{username}\" AND password=\"{password}\"")
        else: self.cursor.execute(f"SELECT * FROM users WHERE username=\"{username}\"")
        for value in self.cursor:
            return True
        return False

    def add_permission(self, username, permission):
        self.cursor.execute(f"INSERT INTO permissions (username, permission) VALUES (\"{username}\", \"{permission}\")")
        self.connection.commit()
        return self.cursor

    def remove_permission(self, username, permission):
        self.cursor.execute(f"DELETE FROM permissions WHERE username=\"{username}\" AND permission=\"{permission}\"")
        self.connection.commit()
        return self.cursor

    def has_permission(self, username, permission):
        self.cursor.execute(f"SELECT * FROM permissions WHERE username=\"{username}\" AND permission=\"{permission}\"")
        for value in self.cursor:
            return True
        self.cursor.execute(f"SELECT * FROM permissions WHERE username=\"{username}\" AND permission=\"admin\"")
        for value in self.cursor:
            return True
        return False

    def get_permissions_of_user(self, username):
        permissions = []
        self.cursor.execute(f"SELECT * FROM permissions WHERE username=\"{username}\"")
        for value in self.cursor:
            permissions.append(value)
        return permissions

    def get_users_who_have_permission(self, permission):
        users = []
        self.cursor.execute(f"SELECT * FROM permissions WHERE permission=\"{permission}\"")
        for value in self.cursor:
            users.append(value)
        return users

    def add_information(self, key, value):
        self.cursor.execute(f"INSERT INTO informations (key, value) VALUES (\"{key}\", \"{value}\")")
        self.connection.commit()
        return self.cursor

    def remove_information(self, key):
        self.cursor.execute(f"DELETE FROM informations WHERE key=\"{key}\"")
        self.connection.commit()
        return self.cursor

    def get_information(self, key):
        self.cursor.execute(f"SELECT * FROM informations WHERE key=\"{key}\"")
        for value in self.cursor:
            return value
        return None

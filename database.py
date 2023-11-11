import random
import sqlite3


class DataBase:
    def __init__(self, database=None):
        if database is None:
            database = sqlite3.connect("database.db")
            database.row_factory = sqlite3.Row
        self.__db = database
        self.__cur = database.cursor()

    def create_user(self, telegram_id, words):
        try:
            words = ",".join([str(i) for i in words])
            self.__cur.execute("INSERT INTO users VALUES (NULL, ?, ?, ?)",
                               (telegram_id, words, "1"))
            self.__db.commit()
            return self.get_user(telegram_id)
        except Exception as e:
            print('Ошибка добавления в БД', e)
            return False

    def get_user(self, telegram_id):
        try:
            self.__cur.execute("SELECT * FROM users WHERE telegram_id = ?",
                               (telegram_id,))
            return self.__cur.fetchone()
        except Exception as e:
            print('Ошибка чтения в БД', e)
            return False

    def get_words(self, telegram_id):
        try:
            self.__cur.execute("SELECT * FROM users WHERE telegram_id = ?",
                               (telegram_id,))
            return self.__cur.fetchone()["words"].split(",")
        except Exception as e:
            print('Ошибка чтения в БД', e)
            return False

    def remove_word(self, telegram_id):
        try:
            words = self.get_words(telegram_id)
            self.__cur.execute("UPDATE users SET words = ? WHERE telegram_id = ?",
                               (",".join(words[1:]), telegram_id,))
            self.__db.commit()
            return True
        except Exception as e:
            print('Ошибка удаления из БД', e)
            return False

    def shuffle_words(self, telegram_id):
        try:
            words = self.get_words(telegram_id)
            random.shuffle(words)
            self.__cur.execute("UPDATE users SET words = ? WHERE telegram_id = ?",
                               (",".join(words), telegram_id,))
            self.__db.commit()
            return True
        except Exception as e:
            print('Ошибка удаления из БД', e)
            return False


if __name__ == "__main__":
    db = DataBase()


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
            self.__cur.execute("INSERT INTO users VALUES (NULL, ?, ?, ?, ?, ?)",
                               (telegram_id, words, "1", "0", "0"))
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

    def update_words(self, telegram_id, words):
        try:
            self.__cur.execute("UPDATE users SET words = ? WHERE telegram_id = ?",
                               (",".join(words), telegram_id,))
            self.__db.commit()
            return True
        except Exception as e:
            print('Ошибка удаления из БД', e)
            return False

    def update_user(self, user):
        try:
            self.__cur.execute("UPDATE users SET words = ?, testing = ?, right_answers = ?, wrong_answers = ? WHERE telegram_id = ?",
                               (",".join(user.words), user.testing, user.right_answers, user.wrong_answers, user.telegram_id,))
            self.__db.commit()
            return True
        except Exception as e:
            print('Ошибка удаления из БД', e)
            return False


class User:
    def __init__(self, user: sqlite3.Row):
        for key in user.keys():
            setattr(self, key, user[key])
        print(self.__dict__)
        self.right_answers = int(self.right_answers)
        self.wrong_answers = int(self.wrong_answers)
        self.testing = int(self.testing)
        self.words = [i for i in self.words.split(",")]

    def update(self, database: DataBase):
        database.update_user(self)


if __name__ == "__main__":
    db = DataBase()


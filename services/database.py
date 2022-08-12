import psycopg2
import psycopg2.extras


# Класс для работы с БД

class DBHelper:
    def __init__(self):
        self.host = 'db'
        self.dbname = 'test_db'
        self.user = 'postgres'
        self.port = '5432'
        self.password = 'test'

    def __connect__(self):
        self.con = psycopg2.connect(user=self.user, password=self.password, host=self.host, port=self.port,
                                    dbname=self.dbname)
        self.cur = self.con.cursor()

    def __disconnect__(self):
        self.con.commit()
        self.con.close()

    def __fetch_all__(self, sql, params):
        self.__connect__()
        self.cur.execute(sql, params)
        result = self.cur.fetchall()
        self.__disconnect__()
        return result

    def __fetch_one__(self, sql, params):
        self.__connect__()
        self.cur.execute(sql, params)
        result = self.cur.fetchone()
        self.__disconnect__()
        return result

    def __execute__(self, sql, params):
        self.__connect__()
        try:
            self.cur.execute(sql, params)
        except Exception as e:
            print(e)
        self.__disconnect__()

    def __execute_batch__(self, sql, params):
        self.__connect__()
        try:
            psycopg2.extras.execute_batch(self.cur, sql, params)
        except psycopg2.Error as e:
            print('Ooops: '+str(e))
        self.__disconnect__()

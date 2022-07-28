import sqlite3
from sqlite3 import Error

#TODO

class Sqlite_Helper():
    def __init__(self):
        database = r"xtract_db.sqlite3"
        # create a database connection
        self.conn = sqlite3.connect(database)


    def get_whole_semester_table(self):
        """
        Query all rows in the tasks table
        :param conn: the Connection object
        :return:
        """

        whole_table = []
        cur = self.conn.cursor()
        data = cur.execute("SELECT * FROM semester")

        for row in data:
            whole_table.append(row)
        print(whole_table)
        self.conn.close()
        return whole_table

    def get_whole_tmp_grades(self):
        """
        Query all rows in the tasks table
        :param conn: the Connection object
        :return:
        """

        all_grades = []
        cur = self.conn.cursor()
        data = cur.execute("SELECT module FROM tmp")

        for row in data:
            all_grades.append(row[0])
        print(all_grades)
        self.conn.close()
        return all_grades

    def add_semester_row(self, module, grade, prof, time):
        cur = self.conn.cursor()
        # Insert a row of data
        try:
            cur.execute("INSERT INTO semester (module, grade, prof, timestamp) VALUES ('%s','%s','%s', '%s')" %(module, grade, prof, time))
            self.conn.commit()
            self.conn.close()
        except Exception as ex:
            print(ex)
            return False
        return True

    def add_tmp_module(self, module, time):
        cur = self.conn.cursor()
        # Insert a row of data
        try:
            cur.execute("INSERT INTO tmp (module, timestamp) VALUES ('%s','%s')" %(module, time))
            self.conn.commit()
            self.conn.close()
        except Exception as ex:
            print(ex)
            return False
        return True









if __name__ == '__main__':
    Sqlite_Helper().get_whole_semester_table()
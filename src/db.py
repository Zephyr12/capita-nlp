import sqlite3


class MyDB:
    def __init__(self, db_path):
        try:
            self.conn = sqlite3.connect(db_path)
        except Exception as e:
            print(e)
            raise


    """ create a table from the create_table_sql statement
            :param create_table_sql: a CREATE TABLE statement
            :return:"""
    def create_table(self):
        sql_create_a_table = """ CREATE TABLE IF NOT EXISTS  (
                                                    id integer PRIMARY KEY,
                                                    raw_text text NOT NULL,
                                                    concern_id integer NOT NULL,
                                                    sentiment integer NOT NULL,
                                                    concerns text NOT NULL
                                                ); """
        try:
            c = self.conn.cursor()
            c.execute(sql_create_a_table)
            c.close()
        except Exception as e:
            print(e)
            raise


    """ Add a new row into the table
    param row:
    return: row id"""
    def add_row(self, row):
        sql = """ INSERT INTO reviews(raw_text,concern_id,sentiment,concerns)
                     VALUES(?,?,?,?);"""
        try:
            c = self.conn.cursor()
            c.execute(sql, row)
            self.conn.commit()
        except Exception as e:
            print(e)
            raise
        return c.lastrowid


    """Delete a task by task id
    param id: id of the task
    return:"""
    def delete_row_by_id(self, id):
        sql = """DELETE FROM reviews WHERE id=?;"""
        try:
            c = self.conn.cursor()
            c.execute(sql, (id, ))
            self.conn.commit()
        except Exception as e:
            print(e)
            raise


    def close(self):
        self.conn.close()



#function to create the table
def main():
    db = MyDB("/Users/ana9712/testdb.sqlite")
    db.create_table()
    #db.add_row(("UCL is great!", 1, 1.4782374, "UCL"))
    db.delete_row_by_id(3)
    db.delete_row_by_id(4)

if __name__ == '__main__':
    main()
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
        sql_create_a_table = """ CREATE TABLE IF NOT EXISTS  reviews(
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
    def add_row(self, table_name, key_value_pairs):
        # sql = """INSERT INTO reviews(raw_text,concern_id,sentiment,concerns)
        #              VALUES(?,?,?,?);"""
        sql = f"INSERT INTO {table_name}("
        for key, value in key_value_pairs.items():
            sql += f"{key},"
        sql = sql[:-1]
        sql += ")\n"
        sql += "VALUES("
        for key, value in key_value_pairs.items():
            if isinstance(value, str):
                sql += f"\"{value}\"," # since value it's a string, it needs to have quotation marks
                                       # protect quotation marks inside a quotated string with a backslash.
            else:
                sql += f"{value},"
        sql = sql[:-1]
        sql += ")\n"
        try:
            print(sql)
            c = self.conn.cursor()
            c.execute(sql)
            self.conn.commit()
        except Exception as e:
            print(e)
            raise
        #return c.lastrowid


    """Delete a task by task id
    param id: id of the task
    return:"""
    def delete_row_by_id(self, table_name, table_id):
        #sql = """DELETE FROM reviews WHERE id=?;"""
        sql = f"DELETE FROM {table_name} WHERE id={table_id};"
        try:
            print(sql)
            c = self.conn.cursor()
            c.execute(sql)
            self.conn.commit()
        except Exception as e:
            print(e)
            raise


    def update_row(self, table_name, key_value_pairs):
        sql = f"UPDATE {table_name} SET "
        for key, value in key_value_pairs.items():
            if isinstance(value, str):
                sql += f"{key}=\"{value}\","
            else:
                sql += f"{key}={value},"
        sql = sql[:-1] #delete the last comma
        sql += f" WHERE id={key_value_pairs.get('id')};" #get value of id
        try:
            print(sql)
            c = self.conn.cursor()
            c.execute(sql)
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
    db.add_row("reviews", {"raw_text": "UCL is not that great!", "concern_id": 1, "sentiment": 1.4782374, "concerns": "UCL"})
    db.update_row("reviews", {"id": 4, "raw_text": "new textyt"})
    db.delete_row_by_id("reviews", 3)

if __name__ == '__main__':
    main()
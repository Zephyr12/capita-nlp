import psycopg2


class MyDB:
    def __init__(self, db_path):
        try:
            self.conn = psycopg2.connect(db_path)#, check_same_thread = False)
        except Exception as e:
            print(e)
            raise


    """ create a table from the create_table_sql statement
            :param create_table_sql: a CREATE TABLE statement
            :return:"""
    def create_table(self, table_name, key_value_pairs):
        sql_create_a_table = f"CREATE TABLE IF NOT EXISTS {table_name}(\n"
        for key, value in key_value_pairs.items():
            sql_create_a_table += f"{key} {value},\n"
        sql_create_a_table = sql_create_a_table[:-2] #delete the last comma
        sql_create_a_table += "\n);"

        try:
            #print(sql_create_a_table)
            c = self.conn.cursor()
            c.execute(sql_create_a_table)
            self.conn.commit()
            c.close()
        except Exception as e:
            print(e)
            raise

    def drop_table(self, table_name):
        sql_drop_table = f"DROP TABLE IF EXISTS {table_name};"
        try:
            c = self.conn.cursor()
            c.execute(sql_drop_table)
            self.conn.commit()

            c.close()
        except Exception as e:
            print(e)
            raise


    """ Add a new row into the table
    param row:
    return: row id"""
    def add_row(self, table_name, key_value_pairs):
        sql = f"INSERT INTO {table_name}("
        for key, value in key_value_pairs.items():
            sql += f"{key},"
        sql = sql[:-1]
        sql += ")"
        sql += " VALUES("
        sql += "%s," * len(key_value_pairs)
        sql = sql[:-1]
        sql += ");"
        print(sql)
        try:
            #print(sql)
            c = self.conn.cursor()
            c.execute(sql, list(key_value_pairs.values()))
            self.conn.commit()
            return key_value_pairs
        except Exception as e:
            print(e)
            raise
        #return c.lastrowid


    """Delete a task by task id
    param id: id of the task
    return:"""
    def delete_row_by_id(self, table_name, table_id):
        sql = f"DELETE FROM {table_name} WHERE id=%s;"
        try:
            #print(sql)
            c = self.conn.cursor()
            c.execute(sql, table_id)
            self.conn.commit()
        except Exception as e:
            print(e)
            raise


    def update_row(self, table_name, id, key_value_pairs):
        sql = f"UPDATE {table_name} SET "
        for key, value in key_value_pairs.items():
            sql += f"{key}=%s,"
        sql = sql[:-1]
        sql += f" WHERE id=%s;" #get value of id
        try:
            #print(sql)
            c = self.conn.cursor()
            c.execute(sql, list(key_value_pairs.values()) + [id])
            self.conn.commit()
        except Exception as e:
            print(e)
            raise


    def close(self):
        self.conn.close()



def main():
    db = MyDB('dbname=ana9712 user=ana9712 password=test')

    #TODO: In change to SQLServer Change Primary Key
    #db.create_table("reviews", {"id": "int GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY", "raw_text": "text NOT NULL", "concern_id": "integer NOT NULL", "sentiment": "integer NOT NULL", "concerns": "text NOT NULL"})
    #db.add_row("reviews", {"raw_text": "UCL is not that greatlala!", "concern_id": 1, "sentiment": 1.4782374, "concerns": "UCL"})
    #db.update_row("reviews", 1, {"raw_text": "new textyt"})
    #db.delete_row_by_id("reviews", 7)

if __name__ == '__main__':
    main()
import psycopg2


class MyDB:
    def __init__(self, db_path):
        try:
            self.conn = psycopg2.connect(db_path)#, check_same_thread = False)
        except Exception as e:
            print(e)
            raise


    def create_table(self, table_name, key_value_pairs):
        """ create a table from the create_table_sql statement
            :param create_table_sql: a CREATE TABLE statement
            :return:"""
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
        sql_drop_table = f"DROP TABLE IF EXISTS {table_name} CASCADE;"
        try:
            c = self.conn.cursor()
            c.execute(sql_drop_table)
            self.conn.commit()
            c.close()
        except Exception as e:
            print(e)
            raise


    def add_row(self, table_name, key_value_pairs, returning=""):
        """ Add a new row into the table
        param row:
        return: row id"""
        sql = f"INSERT INTO {table_name}("
        for key, value in key_value_pairs.items():
            sql += f"{key},"
        sql = sql[:-1]
        sql += ")"
        sql += " VALUES("
        sql += "%s," * len(key_value_pairs)
        sql = sql[:-1]
        sql += ") ON CONFLICT DO NOTHING "+ (" RETURNING " + returning if returning != "" else "")+ ";"
        print(sql)
        try:
            #print(sql)
            c = self.conn.cursor()
            try:
                c.execute(sql, list(key_value_pairs.values()))
                self.conn.commit()
            except:
                self.conn.rollback()
            if returning:
                return c.fetchall()
            else:
                return None
        except Exception as e:
            print(e)
            raise
        #return c.lastrowid


    def delete_row_by_id(self, table_name, table_id):
        """Delete a task by task id
        param id: id of the task
        return:"""
        sql = f"DELETE FROM {table_name} WHERE id=%s;"
        try:
            #print(sql)
            c = self.conn.cursor()
            c.execute(sql, table_id)
            self.conn.commit()
        except Exception as e:
            print(e)
            raise


    def update_row(self, table_name, id, key_value_pairs, id_field='id'):
        sql = f"UPDATE {table_name} SET "
        for key, value in key_value_pairs.items():
            sql += f"{key}=%s,"
        sql = sql[:-1]
        sql += f" WHERE {id_field}=%s;" #get value of id
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

    def select(self, sql, *params):
        curs = self.conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
        curs.execute(sql, params)
        return curs.fetchall()


def main():
    db = MyDB('dbname=ana9712 user=ana9712 password=test')

if __name__ == '__main__':
    main()

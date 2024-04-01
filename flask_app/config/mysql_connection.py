import pymysql.cursors


class MySQLConnection:
    def __init__(self, db):
        connection = pymysql.connect(
            host='localhost',
            user='root',
            password='8mGq&v-p6RLfy-FuYZ!5',
            db=db,
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=False
        )
        self.connection = connection

    def query_db(self, query: str, data: dict = None):
        with self.connection.cursor() as cursor:
            try:
                query = cursor.mogrify(query, data)
                print("Running Query:", query)

                cursor.execute(query)
                if query.lower().find("insert") >= 0:
                    self.connection.commit()
                    return cursor.lastrowid
                elif query.lower().find("select") >= 0:
                    result = cursor.fetchall()
                    return result
                else:
                    self.connection.commit()
            # except Exception as e:
                # if the query fails the method will return FALSE
                # print("Something went wrong", e)
                # return False
            finally:
                self.connection.close()


def connectToMySQL(db):
    return MySQLConnection(db)

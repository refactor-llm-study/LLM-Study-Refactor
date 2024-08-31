import pymysql

class MySQLClient:
    def __init__(self, host, user, password, db):
        self.connection = pymysql.connect(
            host=host,
            user=user,
            password=password,
            db=db,
            charset="utf8mb4",
            cursorclass=pymysql.cursors.DictCursor,
        )

    def fetch_data(self, table_name, limit=100):
        try:
            with self.connection.cursor() as cursor:
                sql = f"SELECT * FROM {table_name} LIMIT {limit}"
                cursor.execute(sql)
                results = cursor.fetchall()
        finally:
            self.connection.close()
        return results

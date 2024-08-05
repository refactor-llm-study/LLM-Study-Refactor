import pymysql
from tqdm import tqdm


mysql_host = "refactor-llm-study.c2wfdzhextbr.us-east-1.rds.amazonaws.com"
mysql_user = "admin"
mysql_password = "llmstudy1"
mysql_db = "llm_study"
table_name = "crawl_raw_data"

# 데이터베이스에 연결
connection = pymysql.connect(
    host=mysql_host,
    user=mysql_user,
    password=mysql_password,
    db=mysql_db,
    charset="utf8mb4",
    cursorclass=pymysql.cursors.DictCursor,
)


def save_data_from_mysql():
    try:
        with connection.cursor() as cursor:
            sql = f"""
            SELECT *
            FROM {table_name}
            """
            cursor.execute(sql)
            results = cursor.fetchall()
    finally:
        connection.close()

    for result in tqdm(results):
        id, json = result["id"], result["json"]

        with open(f"company_info/{id}.json", "w") as f:
            f.write(json)


def get_table_name():
    try:
        with connection.cursor() as cursor:
            sql = "SHOW TABLES"
            cursor.execute(sql)
            result = cursor.fetchall()
            table_names = [row[f"Tables_in_{mysql_db}"] for row in result]
            print("테이블 목록:", table_names)
    finally:
        connection.close()


if __name__ == "__main__":
    # get_table_name()
    save_data_from_mysql()

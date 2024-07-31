import pymysql

def insert_into_crawl_raw_data(job_id, json_data):
    # 데이터베이스 연결 설정
    connection = pymysql.connect(
        host='refactor-llm-study.c2wfdzhextbr.us-east-1.rds.amazonaws.com',
        user='admin',
        password='llmstudy1',
        database='llm_study',
        charset="utf8mb4"
    )

    try:
        with connection.cursor() as cursor:
            # SQL 쿼리 작성
            sql = """
                INSERT INTO crawl_raw_data (id, json) 
                VALUES (%s, %s)
                ON DUPLICATE KEY UPDATE
                json = VALUES(json)
            """
            
            # 데이터 삽입
            cursor.execute(sql, (job_id, json_data))
        
        # 변경사항 커밋
        connection.commit()
        print("save success")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # 연결 종료
        connection.close()

def select_start_index_from_db():
    # 데이터베이스 연결 설정
    connection = pymysql.connect(
        host='refactor-llm-study.c2wfdzhextbr.us-east-1.rds.amazonaws.com',
        user='admin',
        password='llmstudy1',
        database='llm_study',
        charset="utf8mb4"
    )

    try:
        ## 최신(추정) 233363
        with connection.cursor() as cursor:
            # id 컬럼의 가장 낮은 값을 찾는 쿼리
            sql = "SELECT MIN(id) FROM crawl_raw_data"
            cursor.execute(sql)
            result = cursor.fetchone()
            lowest_id = result[0]
            print(f"The lowest id value is: {lowest_id}")
            return lowest_id
    finally:
        connection.close()
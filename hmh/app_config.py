import os
from dotenv import load_dotenv

load_dotenv()

print(f"Loaded OpenAI API Key: {os.getenv('OPENAI_API_KEY')}")

class Config:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    QDRANT_HOST = "http://3.38.106.92:6333/"
    COLLECTION_NAME = "company_info_hmh"
    MYSQL_HOST = "refactor-llm-study.c2wfdzhextbr.us-east-1.rds.amazonaws.com"
    MYSQL_USER = "admin"
    MYSQL_PASSWORD = "llmstudy1"
    MYSQL_DB = "llm_study"
    TABLE_NAME = "crawl_raw_data"

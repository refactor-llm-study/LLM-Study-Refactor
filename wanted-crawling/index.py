import os
import json
from dotenv import load_dotenv

from crawling.util import get_all_urls
from crawling.crawl_run import client_side_crawl
from prompts.main import check_is_dev_jd, jd_to_json
from mysql.main import insert_into_crawl_raw_data, select_start_index_from_db

load_dotenv()

def main():
    end_index = select_start_index_from_db()
    start_index = end_index - 1000
    urls = get_all_urls(start_index, end_index)
    for url in urls:
        crawl_data = client_side_crawl(url)
        if(check_is_dev_jd(crawl_data.title)):
            print(crawl_data.title)
            json_file_path = os.path.join('wanted-crawling/data', url.split('/')[-1] + '.json')

            # JSON 파일로 저장
            new_file = {
                'company_name': crawl_data.company_name,
                'title': crawl_data.title,
                'tags': crawl_data.tags,
                'detail': crawl_data.detail,
                'expect': crawl_data.expect,
                'requirement': crawl_data.requirement,
                'prefer': crawl_data.prefer,
                'location': crawl_data.location
            }

            insert_into_crawl_raw_data(url.split('/')[-1], json.dumps(new_file, ensure_ascii=False))

            with open(json_file_path, 'w', encoding='utf-8') as json_file:
                json.dump(new_file, json_file, ensure_ascii=False, indent=4)
        else:
            print("Not a developer job")
          
main()
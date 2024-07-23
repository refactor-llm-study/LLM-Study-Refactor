import os
import json
from crawling.main import get_all_urls
from crawling.crawl_run import client_side_crawl
from prompts.main import check_is_dev_jd, jd_to_json

os.environ['OPENAI_API_KEY'] = os.environ.get('OPENAI_API_KEY')
START_INDEX = 225900
END_INDEX = 226000

def main():
    urls = get_all_urls(START_INDEX, END_INDEX)
    for url in urls:
        crawl_data = client_side_crawl(url)
        if(check_is_dev_jd(crawl_data.title) == "Yes"):
            print(crawl_data.title)
            json_form_jd=jd_to_json(crawl_data.content)
            print(json_form_jd)
            # the file name should be url's last part
            json_file_path = os.path.join('data', url.split('/')[-1] + '.json')

            # JSON 파일로 저장
            with open(json_file_path, 'w', encoding='utf-8') as json_file:
                json.dump({
                    'company_name': crawl_data.company_name,
                    'title': crawl_data.title,
                    'content': json_form_jd
                }, json_file, ensure_ascii=False, indent=4)
        else:
            print("Not a developer job")
        
main()
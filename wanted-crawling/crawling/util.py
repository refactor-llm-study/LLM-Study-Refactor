import re
BASE_URL = "https://wanted.co.kr/wd/"

def get_all_urls(start_index, end_index):
    urls = []
    # start_index가 end_index보다 클 경우 정상 작동을 위해 swap
    if start_index < end_index:
        start_index, end_index = end_index, start_index
    for i in range(start_index, end_index, -1):
        urls.append(BASE_URL + str(i))
    return urls


def extract_text_between_keywords(text ):
    start_keyword = "포지션 상세"
    end_keyword = "주요업무"
    # start_keyword와 end_keyword를 포함하여 텍스트 추출
    pattern = re.compile(f'{re.escape(start_keyword)}(.*?){re.escape(end_keyword)}', re.DOTALL)
    match = pattern.search(text)
    if match:
        return match.group(1).strip()
    else:
        return None

def split_and_remove_prefix(text):
    # \n을 기준으로 텍스트를 split
    lines = text.split('\n')
    
    # 각 줄에서 앞에 있는 "- " 또는 "• " 텍스트를 제거
    cleaned_lines = [line[2:] if line.startswith('- ') or line.startswith('• ') else line for line in lines]
    
    return cleaned_lines
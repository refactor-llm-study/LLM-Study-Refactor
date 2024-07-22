BASE_URL = "https://wanted.co.kr/wd/"

def get_all_urls(start_index, end_index):
    urls = []
    for (i) in range(start_index, end_index + 1):
        urls.append(BASE_URL + str(i))
    return urls

# def run_crawl():
#     urls = get_all_urls()
#     for url in urls:
#         print(url)
#         try:
#             # 웹 페이지 데이터 가져오기
#             response = requests.get(url)
#             response.raise_for_status()  # HTTP 에러가 발생하면 예외가 발생합니다.
#             data = response.text

#             # BeautifulSoup로 HTML 파싱
#             soup = BeautifulSoup(data, 'html.parser')

#              # <h1> 태그 선택
#             h1_tags = soup.find_all('h1')
#             for h1 in h1_tags:
#                 isDeveloperJob = checkDeveloperJob(h1.get_text())
#                 if(isDeveloperJob == "Yes"):
#                     print(h1.get_text())
#                     elements = soup.find_all('article', class_=lambda x: x and 'JobDescription_JobDescription' in x)
#                     for element in elements:
#                       print(element.get_text())
#                       print(getJdContent(element))
#                 if(isDeveloperJob == "No"):
#                     print("Not a developer job")
            

#         except requests.exceptions.RequestException as e:
#             # HTTP 요청 관련 에러 처리
#             print(f"HTTP 요청 에러")

#         except Exception as e:
#             # 그 외 모든 예외 처리
#             print(f"오류 발생",e)
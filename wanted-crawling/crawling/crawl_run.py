from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from crawling.util import extract_text_between_keywords
from crawling.util import split_and_remove_prefix

# WebDriver 초기화
driver = webdriver.Chrome()

class JDData:
    content = ""
    company_name = ""
    title = ""
    tags = []
    detail = ""
    expect = []
    requirement = []
    prefer =[]
    location = ""

def client_side_crawl(url):
    # 특정 요소가 로드될 때까지 기다림
    driver.get(url)
    crawl_data = JDData()
    try:
        # 1 JD 이름 찾기
        # 유일한 h1 태그가 JD의 이름
        h1_tag = WebDriverWait(driver, 2).until(
            EC.presence_of_element_located((By.TAG_NAME, 'h1'))
        )
        
        # 2 회사 이름 찾기
        # JobHeader_JobHeader className의 a tag 컴포넌트에 회사 이름이 적혀있음
        company_name = WebDriverWait(driver, 2).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "a[class*='JobHeader_JobHeader__Tools__Company']"))
        )

        # 3 JD 텍스트 전문
        # JobDescription_JobDescription className을 포함하는 article tag에 JD 텍스트가 존재
        article_dom = WebDriverWait(driver, 2).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "article[class*='JobDescription_JobDescription']"))
        )

        # 4 article 내 첫 번째 button에 click 이벤트 실행
        # 확장된 JD 텍스트를 가져오기 위함
        button = article_dom.find_element(By.TAG_NAME, "button")
        button.click()

        article_text = article_dom.text

        # 5 "CompanyTags_CompanyTags" 텍스트가 포함된 article tag 찾기
        # CompanyTags_CompanyTags라는 className의 article 아래에 각 ul tag가 있고, 이 내부 button tag에 tag가 존재
        tag_dom = WebDriverWait(driver, 2).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "article[class*='CompanyTags_CompanyTags']"))
        )
        ul_tags = tag_dom.find_elements(By.TAG_NAME, "ul")
        tag_names = []
        for ul in ul_tags:
            buttons = ul.find_elements(By.TAG_NAME, "button")
            for button in buttons:
                tag_name = button.get_attribute('data-tag-name')
                if tag_name:
                    tag_names.append(tag_name)

        
        # 6 "주요업무" 찾기
        # "주요업무" 텍스트를 포함한 h3 태그 바로 다음의 p tag가 주요업무
        h3_expect = WebDriverWait(driver, 2).until(
            EC.presence_of_element_located((By.XPATH, "//h3[contains(text(), '주요업무')]"))
        )
        p_tag_expect = h3_expect.find_element(By.XPATH, 'following-sibling::p[1]')
        expect = p_tag_expect.text

        # 7 "자격요건" 찾기
        # "자격요건" 텍스트를 포함한 h3 태그 바로 다음의 p tag가 자격요건
        h3_tag_requirement = WebDriverWait(driver, 2).until(
            EC.presence_of_element_located((By.XPATH, "//h3[contains(text(), '자격요건')]"))
        )
        p_tag_requirement = h3_tag_requirement.find_element(By.XPATH, 'following-sibling::p[1]')
        requirement = p_tag_requirement.text

        # 8 "우대사항" 찾기
        # "우대사항" 텍스트를 포함한 h3 태그 바로 다음의 p tag가 우대사항
        h3_tag_prefer = WebDriverWait(driver, 2).until(
            EC.presence_of_element_located((By.XPATH, "//h3[contains(text(), '우대사항')]"))
        )
        p_tag_prefer = h3_tag_prefer.find_element(By.XPATH, 'following-sibling::p[1]')
        prefer = p_tag_prefer.text

        # 9 사무실 location 찾기
        # "JobWorkPlace_JobWorkPlace__map__location" class를 포함한 div 태그에 포함된 텍스트가 사무실 위치
        location_div = WebDriverWait(driver, 2).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div[class*='JobWorkPlace_JobWorkPlace__map__location']"))
        )
        location_text = location_div.text

        crawl_data.title = h1_tag.text
        crawl_data.content = article_text
        crawl_data.detail = extract_text_between_keywords(article_text)
        crawl_data.company_name = company_name.text
        crawl_data.tags = tag_names
        crawl_data.expect = split_and_remove_prefix(expect)
        crawl_data.requirement = split_and_remove_prefix(requirement)
        crawl_data.prefer = split_and_remove_prefix(prefer)
        crawl_data.location = location_text
        
        print("title: ", crawl_data.title)
        print("포지션 상세", extract_text_between_keywords(crawl_data.content))
        print("Company Name:", crawl_data.company_name)
        print("Data-tag-name attributes:", tag_names)
        print("주요업무:", expect)
        print("자격요건:", requirement)
        print("우대사항:", prefer)
        print("Location:", location_text)
        
    except Exception as e:
        print(f"Error: {e}")
    return crawl_data
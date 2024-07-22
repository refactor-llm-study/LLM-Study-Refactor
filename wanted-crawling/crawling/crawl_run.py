from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# WebDriver 초기화
driver = webdriver.Chrome()

class JDData:
    content = ""
    company_name = ""
    title = ""

def client_side_crawl(url):
    # 특정 요소가 로드될 때까지 기다림
    driver.get(url)
    crawl_data = JDData()
    try:
        # 첫 번째 h1 태그 찾기
        h1_tag = WebDriverWait(driver, 2).until(
            EC.presence_of_element_located((By.TAG_NAME, 'h1'))
        )
        
        company_name = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "a[class*='JobHeader_JobHeader__Tools__Company']"))
        )

        # 1. "JobDescription_JobDescription" 텍스트가 포함된 article tag 찾기
        article = WebDriverWait(driver, 2).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "article[class*='JobDescription_JobDescription']"))
        )

        # 2. article 내 첫 번째 button에 click 이벤트 실행
        button = article.find_element(By.TAG_NAME, "button")
        button.click()

        # 3. article 내 모든 텍스트 가져오기
        article_text = article.text
        
        crawl_data.content = article_text
        crawl_data.title = h1_tag.text
        crawl_data.company_name = company_name.text
    
    except Exception as e:
        print(f"Error: {e}")
    
    print("title: ", crawl_data.title)
    print("Article Text:", crawl_data.content)
    print("Company Name:", crawl_data.company_name)
    return crawl_data
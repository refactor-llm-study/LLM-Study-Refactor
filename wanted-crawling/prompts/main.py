from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
import json
def check_is_dev_jd(title):
      if(title == ""):
            return "No"
      llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
      prompt = ChatPromptTemplate.from_template(
            """
            Check if the job title is related to developer job.
            If the job description is related to developer job, return "Yes". Otherwise, return "No".
            
            Title:
            {title}
            """)


      chain = prompt | llm
      result = chain.invoke({"title": title}).content
      
      return result == "Yes"

def jd_to_json(title):
      llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
      prompt = ChatPromptTemplate.from_template(
            """
            요구사항:
            아래 JD에서 기대업무, 자격요건, 우대사항을 추출해서 json 형태로 반환하세요.
            각각을 expect, requirement, prefer 이라는 key 에 배열로 저장하세요. 
            결과는 다른 설명이나 ``` 같은 prefix 없이 json 객체만을 반환하세요. 
            
            JD:
            {title}
            """)


      chain = prompt | llm
      result = chain.invoke({"title": title}).content
      print(result,'결과')
      return json.loads(result)
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

def run_rag(documents, question):
    # 메타데이터에서 필요한 정보를 추출하여 정리하고, 로그로 출력
    context = "\n".join(
        [
            f"회사명: {doc['metadata']['company_name']}, 직무: {doc['metadata']['title']}\n"
            f"요구사항: {', '.join(doc['metadata']['requirement'])}\n"
            f"우대사항: {', '.join(doc['metadata']['prefer'])}\n"
            f"혜택: {', '.join(doc['metadata']['tags'])}\n"
            f"모집공고 URL: https://www.wanted.co.kr/wd/{doc['metadata']['id']}\n"
            for doc in documents
        ]
    )
    
    # 로그: 검색된 문서 정보 출력
    print("### 검색된 문서 목록:")
    for doc in documents:
        print(f"회사명: {doc['metadata']['company_name']}, 직무: {doc['metadata']['title']}, URL: https://www.wanted.co.kr/wd/{doc['metadata']['id']}")
    
    model = ChatOpenAI(model="gpt-4")

    # 템플릿에 추가 정보를 전달하도록 수정
    template = """당신은 채용 전문가 AI입니다. 아래에는 다양한 직무 설명(Job Descriptions)과 사용자가 입력한 요청 사항이 제공됩니다. 
        이를 바탕으로 사용자에게 최적의 포지션을 추천해 주세요.
        응답은 심플하게 합니다. 포지션을 추천하는 이유도 2줄 이하로 첨부합니다. 문장은 자연스럽고 명확하게 만들어야 합니다.

        ### 직무 설명 목록:
        {context}
        ...

        ### 사용자 요청 사항:
        {question}

        위의 정보를 바탕으로, 사용자에게 최적의 포지션을 추천해 주세요.
    """
    
    # 로그: 프롬프트 내용 출력
    print("\n### 생성된 프롬프트:")
    print(template.format(context=context, question=question))

    prompt = ChatPromptTemplate.from_template(template)
    
    rag_chain = (
        prompt
        | model
        | StrOutputParser()
    )

    # 최종 답변 받기
    result = rag_chain.invoke({"context": context, "question": question})

    # 로그: 최종 결과 출력
    print("\n### 모델의 최종 답변:")
    print(result)

    return result

from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

def run_rag(documents, question):
    print(*[(document.metadata["company_name"],document.metadata["id"]) for document in documents], sep="\n")
    model = ChatOpenAI(model="gpt-4o-mini")

    template = """당신은 채용 전문가 AI입니다. 아래에는 다양한 직무 설명(Job Descriptions)과 사용자가 입력한 요청 사항이 제공됩니다. 
        이를 바탕으로 사용자에게 최적의 포지션을 추천해 주세요.
        응답은 심플하게 합니다. 포지션을 추천하는 이유도 2줄 이하로 첨부합니다. 문장은 자연스럽고 명확하게 만들어야 합니다.

        직무 설명은 
        'company_name': 회사이름,
        'title': jd 이름,
        'tags': 부가 설명을 정리한 태그,
        'detail': 세부 설명,
        'expect': 기대 역할,
        'requirement': 필수 사항,
        'prefer': 우대 사항,
        'location': 지역

        ### 직무 설명 목록:
        {context}
        ...

        ### 사용자 요청 사항:
        {question}

        위의 정보를 바탕으로, 사용자에게 최적의 포지션을 추천해 주세요.
    """
    prompt = ChatPromptTemplate.from_template(template)


    rag_chain = (
        prompt
        | model
        | StrOutputParser()
    )

    return rag_chain.invoke({"context": documents, "question": question})


# 테스트
# run_rag(, "백엔드 엔지니어 포지션 추천해줘 근데 프론트 작업도 할 수 있었으며 좋겠어!")
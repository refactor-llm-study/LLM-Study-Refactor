from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

def run_rag(documents, question):
    print(*[(doc["metadata"]["company_name"], doc["metadata"].get("id", "N/A")) for doc in documents], sep="\n")
    
    model = ChatOpenAI(model="gpt-4o-mini")

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
    prompt = ChatPromptTemplate.from_template(template)
    
    rag_chain = (
        prompt
        | model
        | StrOutputParser()
    )

    return rag_chain.invoke({"context": documents, "question": question})


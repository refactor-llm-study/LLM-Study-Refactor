from insert_point_to_collection import get_point_from_collection, get_query_vector
from rag.rag import run_rag

def run_llm(question: str):
    payloads = get_point_from_collection("whole_text", get_query_vector(query_sentence=question))
    result = run_rag(payloads, question)
    print(result)


if __name__ == "__main__":
    run_llm("")

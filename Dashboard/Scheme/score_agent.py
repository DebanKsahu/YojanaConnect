from pydantic import BaseModel,Field
from typing import List
from langchain_qdrant import QdrantVectorStore
from langchain.prompts import ChatPromptTemplate
from langchain_core.documents import Document
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langchain_core.runnables import RunnableLambda
import os

load_dotenv()

class ResponseFormatter(BaseModel):
    """
    Response formatter for government scheme matching.
    """
    matching_score: float = Field(
        description="Matching score calculated as (satisfied_criteria / total_criteria)"
    )
    total_criteria: int = Field(
        description="Total number of eligibility criteria"
    )
    satisfied_criteria: int = Field(
        description="Number of criteria that are satisfied"
    )
    matching_criteria: List[str] = Field(
        description="List of criteria that were satisfied"
    )
    reason_for_failure: str | None = Field(
        default=None,
        description="Reason if matching failed"
    )

retriever_query = "List all conditions that determine whether a person is eligible to receive benefits. In other words list all eligibility criteria"

prompt = ChatPromptTemplate.from_messages([
    ("system", """
        You are an expert assistant in Indian government schemes and a skilled mathematician. 
        You MUST follow the exact output format specified below.
        Always provide responses in the exact JSON structure requested.
        CRITICAL: Never return template variables or placeholders in your response.
        Examples of what NOT to return:
        - matching_score
        - total_criteria
        - variable_name

        Instead, always return actual calculated values:
        - 0.75 (not matching_score)
        - 4 (not total_criteria)
        - ["Age requirement met"] (not matching_criteria)
    """),
    ("human", """
        Task: Calculate the matching score for a government scheme based on user eligibility.
        
        Formula: matching_score = (number of satisfied eligibility criteria) / (total eligibility criteria)
        
        CRITICAL: Return ONLY valid JSON with actual calculated values, NOT template placeholders.
        
        REQUIRED OUTPUT FORMAT (with actual values, not placeholders):
        {{
            "matching_score": 0.75,
            "total_criteria": 4,
            "satisfied_criteria": 3,
            "matching_criteria": [
                "Age between 18-65",
                "Annual income below 2 lakh"
            ],
            "reason_for_failure": null
        }}
        
        STEP-BY-STEP PROCESS:
        1. Extract ALL eligibility criteria from the context section
        2. Compare each criterion against the user_data
        3. Count satisfied criteria (exact matches only)
        4. Calculate: satisfied_criteria ÷ total_criteria (rounded to 2 decimals)
        5. Return JSON with ACTUAL CALCULATED VALUES
        
        IMPORTANT RULES:
        - Calculate actual numeric values, don't use placeholders
        - If no context or user_data provided, return matching_score: 0.00
        - Only count criteria as satisfied if they EXACTLY match user data
        - Return ONLY the JSON object, no additional text
        - Use actual values, never template variables like matching_score
        
        <context>
        {context}
        </context>
        
        <user_data>
        {user_data}
        </user_data>
    """)
])


def format_docs(docs: list[Document]) -> str:
    return "\n\n".join(doc.page_content for doc in docs)

llm = ChatGoogleGenerativeAI(
    model = "models/gemini-2.0-flash",
    temperature = 0.2
)
testing_llm = llm

llm_with_structured_output = llm.with_structured_output(ResponseFormatter)

def agent_pipeline(scheme_id: int, qdrant: QdrantVectorStore, user_input: str, llm = llm_with_structured_output, retriever_query: str = retriever_query):

    qdrant_retriver = qdrant.as_retriever(
        search_type = "mmr",
        search_kwargs = {
            'k': 10,
            "filter": {
                "must": [
                    {
                        "key": "scheme_id",         
                        "match": {
                            "value": scheme_id            
                        }
                    }
                ]
            }
        },
    )
    testing_prompt = prompt.invoke({
        "context" : format_docs(qdrant_retriver.invoke(retriever_query)),
        "user_data": user_input
    })
    testing_result = testing_llm.invoke(testing_prompt)
    print(testing_result)
    qa_chain = (
        {
            "context":  RunnableLambda(lambda _: format_docs(qdrant_retriver.invoke(retriever_query))),
            "user_data": RunnableLambda(lambda x: x["user_data"])
        }
        | prompt
        | llm
    )

    result = qa_chain.invoke({
        "user_data": user_input
    })
    result = ResponseFormatter.model_validate(result)
    return result.matching_score
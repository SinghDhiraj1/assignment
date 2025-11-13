# query_engine.py
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from config import EMBEDDING_MODEL, LLM_MODEL, TOP_K
import os

class RAGEngine:
    def __init__(self):
        self.embeddings = OpenAIEmbeddings(
            model=EMBEDDING_MODEL,
            openai_api_base="https://openrouter.ai/api/v1",
            openai_api_key=os.getenv("OPENROUTER_API_KEY")
        )
        self.vectorstore = FAISS.load_local("vector_store", self.embeddings, allow_dangerous_deserialization=True)
        self.retriever = self.vectorstore.as_retriever(search_kwargs={"k": TOP_K})

        self.llm = ChatOpenAI(
            model=LLM_MODEL,
            temperature=0.0,
            max_tokens=512,
            openai_api_base="https://openrouter.ai/api/v1",
            openai_api_key=os.getenv("OPENROUTER_API_KEY")
        )

        template = """You are a process engineer. Extract exact values from the technical datasheet.

Context (includes tables):
{context}

Question: {question}

Answer only the exact value with unit and source if possible.
Examples:
→ Operating temperature of P-1203 A/B → 39 °C
→ Max operating temperature of T70-C-0102 → 280 °F
→ Shell material of T70-C-0102 → SA-516 GR 70N with SS 316 L cladding

Answer directly:"""

        prompt = ChatPromptTemplate.from_template(template)

        def format_docs(docs):
            return "\n\n".join(
                f"[Source: {d.metadata['source']} | Page {d.metadata.get('page','?')}]\n{d.page_content}"
                for d in docs
            )

        self.chain = (
            {"context": self.retriever | format_docs, "question": RunnablePassthrough()}
            | prompt | self.llm | StrOutputParser()
        )

    def ask(self, question):
        return self.chain.invoke(question)
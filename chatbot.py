from query_engine import RAGEngine
import warnings
warnings.filterwarnings("ignore")

engine = RAGEngine()
print("Chatbot ready! Type 'quit' to exit.\n")

while True:
    q = input("You: ").strip()
    if q.lower() in ["quit", "exit"]:
        break
    if q:
        print("Answer:", engine.ask(q), "\n")
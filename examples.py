import os
from chatbotCB import Chatbot
from embeddings import Embedder
from vectorstore import VectorDatabase
from ragretriever import RAGRetriever
from langchain_community.document_loaders import TextLoader, JSONLoader

# Define file paths
base_path = os.path.join("E:", "GDGCB4CP", "project", "data")
problem_path = os.path.join(base_path, "problem.txt")
editorial_path = os.path.join(base_path, "editorial.txt")
metadata_path = os.path.join(base_path, "metadata.json")

# Initialize components
loaders = [
    TextLoader(problem_path, encoding='utf-8'),
    TextLoader(editorial_path, encoding='utf-8'),
    JSONLoader(metadata_path, '.', text_content=False)
]

embedder = Embedder()
vector_db = VectorDatabase(index_type="IndexFlatIP")
retriever = RAGRetriever(embedder, vector_db)

retriever.load_and_process_data(loaders)

# Save FAISS index
index_file_path = os.path.join("E:", "GDGCB4CP", "project", "src", "vector_index.faiss")
vector_db.save_index(index_file_path)

# Load FAISS index and test retrieval
vector_db.load_index(index_file_path)

system_message = "I am here to assist you with competitive programming problems."
chatbot = Chatbot(retriever, system_message)

basic_questions = [
    "What is dynamic programming?",
    "Explain the two-pointer technique.",
    "How do I solve a graph problem?",
    "What are common sorting algorithms?",
    "How to optimize recursion using memoization?"
]

basic_responses = [
    "Dynamic programming is a method for solving problems by breaking them down into overlapping subproblems and storing their results.",
    "The two-pointer technique is used to optimize searching operations by using two pointers to traverse data from different ends.",
    "To solve a graph problem, understand concepts like BFS, DFS, and shortest path algorithms.",
    "Common sorting algorithms include Quick Sort, Merge Sort, and Bubble Sort.",
    "Memoization optimizes recursion by storing previously computed results to avoid redundant calculations."
]

for question, response in zip(basic_questions, basic_responses):
    print(f"User: {question}")
    print(f"Chatbot: {response}")

user_input = input("Enter your query: ")
if user_input.lower() in ["exit", "quit"]:
    print("Chatbot: Goodbye!")
else:
    response = chatbot.generate_response(user_input)
    print(f"Chatbot: {response}")
response = chatbot.generate_response("what is solution of problem 2055/c")
print(f"Chatbot: {response}")






# Chatbot: I am here to assist you with competitive programming problems.

# Here are some relevant responses:
# 1. abaababaThe correct output should be: 0010000When k=3, s1=aba, s2=abaab, we first filled in 2 short strings, but if we backtrack c=1 short string, it will be judged as unsolvable. This is how the error in std occurs. This situation only arises when the "tail" part of s2 is a prefix of s1.So, each time we calculate, we first use binary search to
# 2. binary search to find how many are left. For the part where we moved forward by B occurrences, we can backtrack at most once, and then the binary search will take O(logB). Each time, we can at least fill in |s2| occurrences. The time complexity for calculating the answer becomes O(m|s2|logB), and the total complexity, due to O(n∑i=1log(ni))=O(n),
# 3. to match is that a suffix of s1 has been moved to the beginning of $s_1$。As shown in the diagram.The alignment results in the following diagram.In the diagram, the case where |pre|>|suf| is shown. The other case follows similarly.pre+suf=suf+pre, and as can be seen from the diagram, here pre+suf needs to be "misaligned but equal." This means that
# response = chatbot.generate_response("problem with tag dp math implementation")
# print(f"Chatbot: {response}")
# Chatbot: I am here to assist you with competitive programming problems.

# Here are some relevant responses:
# 1. abaababaThe correct output should be: 0010000When k=3, s1=aba, s2=abaab, we first filled in 2 short strings, but if we backtrack c=1 short string, it will be judged as unsolvable. This is how the error in std occurs. This situation only arises when the "tail" part of s2 is a prefix of s1.So, each time we calculate, we first use binary search to
# 2. binary search to find how many are left. For the part where we moved forward by B occurrences, we can backtrack at most once, and then the binary search will take O(logB). Each time, we can at least fill in |s2| occurrences. The time complexity for calculating the answer becomes O(m|s2|logB), and the total complexity, due to O(n∑i=1log(ni))=O(n),
# 3. to match is that a suffix of s1 has been moved to the beginning of $s_1$。As shown in the diagram.The alignment results in the following diagram.In the diagram, the case where |pre|>|suf| is shown. The other case follows similarly.pre+suf=suf+pre, and as can be seen from the diagram, here pre+suf needs to be "misaligned but equal." 

### A demo rag system, which contains an LLM (GPT-4o) connected to
#   a Chroma Cloud. When user queries, it is first sent to the retriver,
#   the retrived documents are then sent together with initial query to the LLM.
import chromadb
from openai import OpenAI

# 0. Make sure you export your OPENAI_API_KEY to the environment variables.
# 1. Setup Clients
client = chromadb.CloudClient(
  api_key='ck-7WpBxX9Noyokz89CkWfmtgg3tz4KbKRamm3itJACmiLL',
  tenant='05310abb-350a-4ac5-8b54-9f6355b17ba1',
  database='Demo'
)

collection = client.get_or_create_collection(name="browse-comp-plus")
openai_client = OpenAI()

print("--- RAG Chat Initialized (Type 'exit' or 'quit' to stop) ---")

# 2. Chat Loop
while True:
    # Get user input
    user_query = input("\nUser: ")

    # Check for exit commands
    if user_query.lower() in ['exit', 'quit', 'q']:
        print("Goodbye!")
        break

    # 3. Retrieve Context from ChromaDB
    # We query the collection based on the user's specific input
    results = collection.query(
        query_texts=[user_query],
        n_results=3
    )
    
    # Flatten the retrieved documents into a single context string
    retrieved_context = " ".join(results['documents'][0])

    # 4. Generate response with OpenAI
    try:
        response = openai_client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful assistant. Use the provided context to answer accurately."},
                {"role": "user", "content": f"Context: {retrieved_context}\n\nQuestion: {user_query}"}
            ]
        )

        # Output the answer
        print(f"\nAssistant: {response.choices[0].message.content}")
    
    except Exception as e:
        print(f"An error occurred: {e}")
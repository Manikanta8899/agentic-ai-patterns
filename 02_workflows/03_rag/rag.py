import os
import glob
import numpy as np
from openai import OpenAI
from termcolor import colored

# 1. Initialize Client
client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"
)
MODEL_ID = "llama3.2"
EMBED_MODEL_ID = "nomic-embed-text"

# --- RAG Pipeline ---

# Step 1: Load Documents
def load_documents(directory: str) -> list[dict]:
    """Loads all .txt files from a directory."""
    documents = []
    for filepath in glob.glob(os.path.join(directory, "*.txt")):
        with open(filepath, "r") as f:
            documents.append({
                "filename": os.path.basename(filepath),
                "content": f.read()
            })
    print(colored(f"  Loaded {len(documents)} documents.", "cyan"))
    return documents

# Step 2: Chunk Documents
def chunk_documents(documents: list[dict], chunk_size: int = 300) -> list[dict]:
    """Splits documents into smaller chunks based on character count."""
    chunks = []
    for doc in documents:
        text = doc["content"]
        # Split by double newlines first (paragraphs), then by chunk_size
        paragraphs = text.split("\n\n")
        current_chunk = ""
        for para in paragraphs:
            if len(current_chunk) + len(para) < chunk_size:
                current_chunk += para + "\n\n"
            else:
                if current_chunk.strip():
                    chunks.append({
                        "source": doc["filename"],
                        "text": current_chunk.strip()
                    })
                current_chunk = para + "\n\n"
        if current_chunk.strip():
            chunks.append({
                "source": doc["filename"],
                "text": current_chunk.strip()
            })
    print(colored(f"  Created {len(chunks)} chunks.", "cyan"))
    return chunks

# Step 3: Create Embeddings
def get_embeddings(texts: list[str]) -> list[list[float]]:
    """Gets embeddings for a list of texts using Ollama."""
    embeddings = []
    for text in texts:
        response = client.embeddings.create(
            model=EMBED_MODEL_ID,
            input=text
        )
        embeddings.append(response.data[0].embedding)
    return embeddings

# Step 4: Cosine Similarity Search
def cosine_similarity(a, b):
    """Computes cosine similarity between two vectors."""
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def retrieve(query: str, chunks: list[dict], chunk_embeddings: list, top_k: int = 3) -> list[dict]:
    """Retrieves the top-K most relevant chunks for a query."""
    query_embedding = get_embeddings([query])[0]
    
    similarities = []
    for i, emb in enumerate(chunk_embeddings):
        sim = cosine_similarity(query_embedding, emb)
        similarities.append((i, sim))
    
    # Sort by similarity (highest first)
    similarities.sort(key=lambda x: x[1], reverse=True)
    
    results = []
    for idx, score in similarities[:top_k]:
        results.append({
            "text": chunks[idx]["text"],
            "source": chunks[idx]["source"],
            "score": round(score, 4)
        })
    return results

# Step 5: Generate Answer
def generate_answer(query: str, context_chunks: list[dict]) -> str:
    """Sends the query and retrieved context to the LLM."""
    context_text = "\n\n---\n\n".join(
        [f"[Source: {c['source']}]\n{c['text']}" for c in context_chunks]
    )
    
    messages = [
        {
            "role": "system",
            "content": (
                "You are a helpful customer support assistant for NovaTech Solutions. "
                "Answer the user's question based ONLY on the provided context below. "
                "If you cannot find the answer in the context, say 'I don't have enough "
                "information to answer that question.' Do not make up information.\n\n"
                f"--- CONTEXT ---\n{context_text}\n--- END CONTEXT ---"
            )
        },
        {"role": "user", "content": query}
    ]
    
    response = client.chat.completions.create(
        model=MODEL_ID,
        messages=messages,
        temperature=0
    )
    return response.choices[0].message.content

def generate_answer_no_rag(query: str) -> str:
    """Sends the query to the LLM WITHOUT any context (no RAG)."""
    messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant. Answer the user's question."
        },
        {"role": "user", "content": query}
    ]
    
    response = client.chat.completions.create(
        model=MODEL_ID,
        messages=messages,
        temperature=0
    )
    return response.choices[0].message.content

# --- Main ---
def main():
    print(colored("📚 Agentic AI - Level 2: Workflows - RAG Pipeline", "cyan", attrs=["bold"]))

    # 1. Load & Chunk
    print(colored("\n--- Step 1: Loading & Chunking Documents ---", "yellow"))
    kb_dir = os.path.join(os.path.dirname(__file__), "knowledge_base")
    documents = load_documents(kb_dir)
    chunks = chunk_documents(documents)

    # 2. Embed all chunks
    print(colored("\n--- Step 2: Creating Embeddings ---", "yellow"))
    print(colored("  Embedding chunks (this may take a moment)...", "cyan"))
    chunk_texts = [c["text"] for c in chunks]
    chunk_embeddings = get_embeddings(chunk_texts)
    print(colored(f"  Created {len(chunk_embeddings)} embeddings.", "cyan"))

    # 3. Query
    query = "What is NovaTech's refund policy for annual subscriptions?"
    print(colored(f"\n--- Step 3: User Query ---", "yellow"))
    print(colored(f"Query: {query}", "green"))

    # 4. Retrieve
    print(colored("\n--- Step 4: Retrieving Relevant Context ---", "yellow"))
    results = retrieve(query, chunks, chunk_embeddings, top_k=3)
    for i, r in enumerate(results):
        print(colored(f"\n  Chunk {i+1} (Score: {r['score']}, Source: {r['source']}):", "magenta"))
        # Show a preview of the chunk
        preview = r["text"][:150] + "..." if len(r["text"]) > 150 else r["text"]
        print(f"  {preview}")

    # 5. Generate (With RAG)
    print(colored("\n--- Step 5a: Answer WITH RAG (Grounded) ---", "yellow"))
    answer_rag = generate_answer(query, results)
    print(colored("Bot (RAG): ", "blue", attrs=["bold"]) + answer_rag)

    # 6. Generate (Without RAG) for comparison
    print(colored("\n--- Step 5b: Answer WITHOUT RAG (Ungrounded) ---", "yellow"))
    answer_no_rag = generate_answer_no_rag(query)
    print(colored("Bot (No RAG): ", "red", attrs=["bold"]) + answer_no_rag)

if __name__ == "__main__":
    main()

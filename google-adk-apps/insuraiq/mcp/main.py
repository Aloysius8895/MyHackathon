from fastmcp import FastMCP
from chromadb import Documents, EmbeddingFunction, Embeddings
import chromadb
from google import genai
from dotenv import load_dotenv

# Initialize MCP server
mcp = FastMCP("policy-finder")

# Initialize embedding model and chromadb
load_dotenv()
embedding_client = genai.Client()

class GeminiEmbeddingFunction(EmbeddingFunction):
    def __call__(self, input: Documents) -> Embeddings:
        embeddings = []
        for doc in input:
            embedding = embedding_client.models.embed_content(model="text-embedding-004", contents=doc)
            embeddings.append(embedding.embeddings[0].values)
        return embeddings

chroma_client = chromadb.PersistentClient(path="insurance_db")
insurance_collection = chroma_client.get_collection(name="insurance_plan_details", embedding_function=GeminiEmbeddingFunction())

# Initialize MCP tool
@mcp.tool
def get_insurance_plan(query: str) -> dict:
    """Retrieves relevant insurance plan information based on a user's query.

    This tool queries a vector database of insurance documents to find the most
    relevant plan details. Use the user's requirements and their medical profile
    to form a comprehensive query.

    Args:
        query (str): A natural language question or search term about
                     insurance plans (e.g., "Maternity coverage for low-risk profile", "dental plan for family with diabetes history").

    Returns:
        dict: A dictionary containing the query result with a list of plans.
    """
    print(f"\n--- Tool: get_insurance_plan called with query: '{query}' ---")
    query_results = insurance_collection.query(query_texts=[query], n_results=2)
    print("\n--- CHROMADB QUERY RESULTS:", query_results)
    return query_results

# Start the server using streamable http transport
if __name__ == "__main__":
    mcp.run(transport="streamable-http",host="0.0.0.0", port=15001)
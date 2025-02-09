import os
import nest_asyncio
from llama_index.core import Settings
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.huggingface import HuggingFaceEmbedding # type: ignore
from llama_index.core import VectorStoreIndex,StorageContext, PromptTemplate
from llama_index.core import SimpleDirectoryReader
import asyncio

# Apply nested asyncio to avoid event loop issues
nest_asyncio.apply()

# Function to asynchronously load data from the input directory
async def async_load_data(input_dir_path):
    def load_sync():
        loader = SimpleDirectoryReader(
            input_dir=input_dir_path,
            required_exts=[".xlsx", ".csv", ".tsv", ".txt", ".pdf"],
            recursive=True
        )
        return loader.load_data()

    # Run the synchronous reader in a thread (non-blocking for your event loop)
    documents = await asyncio.to_thread(load_sync)
    return documents

# Function to set up and return the query engine
def setup_query_engine(input_dir_path="test-dir", index_file_path="index.json"):
    # Specify the directory containing the input documents
    input_dir_path = os.path.abspath(input_dir_path)

    # Load the embedding model (using a smaller, faster model for optimization)
    embed_model = HuggingFaceEmbedding(model_name="all-MiniLM-L6-v2")

    # Check if the index file already exists to save time
    if os.path.exists(index_file_path):
        print(f"Loading index from {index_file_path}...")
        index = VectorStoreIndex.load_from_disk(index_file_path)
    else:
        print("Loading and embedding data...")
        # Load data asynchronously
        docs = asyncio.run(async_load_data(input_dir_path))

        # Embed documents and create an index
        Settings.embed_model = embed_model
        index = VectorStoreIndex.from_documents(docs, show_progress=True)

        # Save the index to disk for future use
        index.storage_context.persist(persist_dir=input_dir_path)
        
        print(f"Index saved to {index_file_path}")

    # Initialize the LLM (Ollama model)
    llm = Ollama(model="deepseek-r1:7b", request_timeout=120.0)
    Settings.llm = llm

    # Create a query engine
    query_engine = index.as_query_engine()

    # Customize the prompt (simplify to reduce token usage)
    qa_prompt_tmpl_str = (
        "Given the following context:\n"
        "{context_str}\n"
        "Answer the query:\n"
        "{query_str}\n"
    )
    qa_prompt_tmpl = PromptTemplate(qa_prompt_tmpl_str)
    query_engine.update_prompts({"response_synthesizer:text_qa_template": qa_prompt_tmpl})

    return query_engine
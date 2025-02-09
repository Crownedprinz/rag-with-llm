import nest_asyncio
from dotenv import load_dotenv
from llama_index.core import Settings
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.huggingface import HuggingFaceEmbedding # type: ignore
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, ServiceContext
from llama_index.core import PromptTemplate

# Setup event loop
nest_asyncio.apply()
# Function to set up and return the query engine
def setup_query_engine(input_dir_path='test-dir'):
    # Add your documents in this directory
    input_dir_path = 'test-dir'

    # Setup the LLM and embedding model
    llm = Ollama(model="deepseek-r1:7b", request_timeout=120.0)
    embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-large-en-v1.5", trust_remote_code=True)

    # Load data
    loader = SimpleDirectoryReader(input_dir=input_dir_path, required_exts=[".xlsx", ".csv", ".tsv", ".txt", "pdf"], recursive=True)
    docs = loader.load_data()

    # Creating an index over loaded data
    Settings.embed_model = embed_model
    index = VectorStoreIndex.from_documents(docs, show_progress=True)

    # Create a query engine
    Settings.llm = llm
    query_engine = index.as_query_engine()

    # Customize the prompt
    qa_prompt_tmpl_str = (
        "Context information is below.\n"
        "---------------------\n"
        "{context_str}\n"
        "---------------------\n"
        "Given the context information above I want you to think step by step to answer the query.\n"
        "Query: {query_str}\n"
        "Answer: "
    )
    qa_prompt_tmpl = PromptTemplate(qa_prompt_tmpl_str)
    query_engine.update_prompts({"response_synthesizer:text_qa_template": qa_prompt_tmpl})
    return query_engine
    # Interactive loop for user queries
    # while True:
    #     query = input("\nEnter your query (type 'exit' to quit): ")
    #     if query.lower() == 'exit':
    #         print("Exiting...")
    #         break
    #     response = query_engine.query(query)
    #     print(f"Answer: {response}")
    # display(Markdown(str(response)))

    # llm = Ollama(model="deepseek-r1:7b", request_timeout=120.0)

    # resp = llm.complete("What is capital of France?")
    # resp

    # print(resp.text)
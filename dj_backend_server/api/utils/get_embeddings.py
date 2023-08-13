from langchain.embeddings.openai import OpenAIEmbeddings
from api.enums import EmbeddingProvider
import os
from dotenv import load_dotenv
from langchain.embeddings.base import Embeddings

load_dotenv()

# https://github.com/easonlai/azure_openai_langchain_sample/blob/main/chat_with_pdf.ipynb
import os


def get_embedding_provider():
    """Gets the chosen embedding provider from environment variables."""
    return os.environ.get("EMBEDDING_PROVIDER")

def get_azure_embedding():
    """Gets embeddings using the Azure embedding provider."""
    deployment = os.environ.get("AZURE_OPENAI_EMBEDDING_MODEL_NAME")
    openai_api_key = os.environ.get("AZURE_OPENAI_API_KEY")
    client = os.environ.get("AZURE_OPENAI_API_TYPE")
    openai_api_base = os.environ['AZURE_OPENAI_API_BASE']
    openai_api_version = os.environ['AZURE_OPENAI_API_VERSION']

    return OpenAIEmbeddings(
        openai_api_key=openai_api_key,
        deployment=deployment,
        client=client,
        chunk_size=8,
        openai_api_base=openai_api_base,
        openai_api_version=openai_api_version
    )

def get_openai_embedding():
    """Gets embeddings using the OpenAI embedding provider."""
    openai_api_key = os.environ.get("OPENAI_API_KEY")

    return OpenAIEmbeddings(openai_api_key=openai_api_key, chunk_size=1)

def choose_embedding_provider():
    """Chooses and returns the appropriate embedding provider instance."""
    embedding_provider = get_embedding_provider()

    if embedding_provider == EmbeddingProvider.azure.value:
        return get_azure_embedding()
    
    elif embedding_provider == EmbeddingProvider.OPENAI.value:
        return get_openai_embedding()

    else:
        available_providers = ", ".join([service.value for service in EmbeddingProvider])
        raise ValueError(
            f"Embedding service '{embedding_provider}' is not currently available. "
            f"Available services: {available_providers}"
        )

# Main function to get embeddings
def get_embeddings() -> Embeddings:
    """Gets embeddings using the chosen embedding provider."""
    return choose_embedding_provider()
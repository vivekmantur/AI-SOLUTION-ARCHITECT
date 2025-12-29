import requests
import numpy as np
def get_embeddings_ollama(texts):
    # Use the actual Ollama server address with the correct embedding model
    url = "http://192.168.1.81:11434/api/embed"
    payload = {"model": "nomic-embed-text", "input": texts}
    
    response = requests.post(url, json=payload)

    if response.status_code != 200:
        raise Exception(f"Ollama Embedding API Error: {response.text}")
    
    data = response.json()
    return np.array(data["embeddings"])

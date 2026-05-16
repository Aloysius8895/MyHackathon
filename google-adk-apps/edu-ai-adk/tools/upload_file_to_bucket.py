from google.cloud import storage
from datetime import datetime
import os

def upload_file_to_bucket(file_path: str, file_name: str) -> dict:
    """Faz upload de um arquivo para o Cloud Storage e retorna a URL pública."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Arquivo não encontrado: {file_path}")

    client = storage.Client()
    bucket = client.bucket("edu-ai-essays")  # ✅ Nome do seu bucket

    # Cria um caminho único para o arquivo
    blob_path = f"uploads/{datetime.utcnow().isoformat()}_{file_name}"
    blob = bucket.blob(blob_path)

    # Faz o upload
    blob.upload_from_filename(file_path)

    # Torna o arquivo público
    blob.make_public()

    return {"url": blob.public_url}

import base64, uuid, os

def save_uploaded_file(data: str, file_name: str) -> dict:
    """Salva arquivo base64 no disco local e retorna o caminho completo"""
    # Se o modelo enviar uma string vazia ou "None", trate aqui
    print(f"Trying to save file: {data} {file_name}")
    if not file_name or file_name.lower() == "none":
        file_name = f"{uuid.uuid4()}.jpg"

    file_path = f"/tmp/{file_name}"
    print(f"File path: {file_path}")
    
    with open(file_path, "wb") as f:
        f.write(base64.b64decode(data))

    return {"file_path": file_path, "file_name": file_name}
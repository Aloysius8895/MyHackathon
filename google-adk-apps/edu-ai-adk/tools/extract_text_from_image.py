from google.cloud import vision

def extract_text_from_image(url: str) -> dict:
  """Extrai texto de uma imagem de redação via OCR (Vision API)."""
  client = vision.ImageAnnotatorClient()
  image = vision.Image()
  image.source.image_uri = url
  response = client.document_text_detection(image=image)
  texto = response.full_text_annotation.text
  return {"text": texto}

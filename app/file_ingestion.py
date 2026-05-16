import csv
import json
import re
import zipfile
from dataclasses import dataclass
from html import unescape
from io import BytesIO, StringIO
from pathlib import Path
from xml.etree import ElementTree

from fastapi import UploadFile


class FileIngestionError(ValueError):
    pass


@dataclass(frozen=True)
class UploadedProfileText:
    file_name: str
    text: str
    content_type: str | None


async def extract_upload_text(file: UploadFile) -> UploadedProfileText:
    file_name = file.filename or "uploaded-file"
    content = await file.read()
    if not content:
        raise FileIngestionError(f"{file_name} is empty")

    suffix = Path(file_name).suffix.casefold()
    if suffix in {".txt", ".md", ".rtf"}:
        text = _decode_text(content)
    elif suffix in {".html", ".htm"}:
        text = _strip_html(_decode_text(content))
    elif suffix == ".csv":
        text = _csv_to_text(content)
    elif suffix == ".json":
        text = _json_to_text(content)
    elif suffix == ".pdf":
        text = _pdf_to_text(content, file_name)
    elif suffix == ".docx":
        text = _docx_to_text(content, file_name)
    elif (file.content_type or "").startswith("text/"):
        text = _decode_text(content)
    else:
        supported = ", ".join([".csv", ".docx", ".html", ".json", ".md", ".pdf", ".txt"])
        raise FileIngestionError(f"{file_name} is not supported. Supported file types: {supported}")

    cleaned = _clean_text(text)
    if len(cleaned) < 20:
        raise FileIngestionError(f"{file_name} did not contain enough readable text")
    return UploadedProfileText(file_name=file_name, text=cleaned, content_type=file.content_type)


def _decode_text(content: bytes) -> str:
    for encoding in ("utf-8-sig", "utf-8", "cp1252", "latin-1"):
        try:
            return content.decode(encoding)
        except UnicodeDecodeError:
            continue
    return content.decode("utf-8", errors="ignore")


def _csv_to_text(content: bytes) -> str:
    raw_text = _decode_text(content)
    reader = csv.DictReader(StringIO(raw_text))
    if not reader.fieldnames:
        return raw_text

    lines: list[str] = []
    for row_index, row in enumerate(reader, start=1):
        values = [f"{key}: {value}" for key, value in row.items() if key and value]
        if values:
            lines.append(f"Record {row_index}. " + "; ".join(values))
    return "\n".join(lines) or raw_text


def _json_to_text(content: bytes) -> str:
    try:
        payload = json.loads(_decode_text(content))
    except json.JSONDecodeError as exc:
        raise FileIngestionError("JSON file is not valid") from exc
    return _flatten_json(payload)


def _flatten_json(value: object) -> str:
    if isinstance(value, dict):
        parts = [f"{key}: {_flatten_json(item)}" for key, item in value.items()]
        return "; ".join(part for part in parts if part)
    if isinstance(value, list):
        return "; ".join(_flatten_json(item) for item in value if item is not None)
    return "" if value is None else str(value)


def _pdf_to_text(content: bytes, file_name: str) -> str:
    try:
        from pypdf import PdfReader
    except ImportError as exc:
        raise FileIngestionError("pypdf is required to read PDF files") from exc

    try:
        reader = PdfReader(BytesIO(content))
        return "\n".join(page.extract_text() or "" for page in reader.pages)
    except Exception as exc:
        raise FileIngestionError(f"{file_name} could not be parsed as a PDF") from exc


def _docx_to_text(content: bytes, file_name: str) -> str:
    try:
        with zipfile.ZipFile(BytesIO(content)) as archive:
            document_xml = archive.read("word/document.xml")
    except Exception as exc:
        raise FileIngestionError(f"{file_name} could not be parsed as a DOCX file") from exc

    root = ElementTree.fromstring(document_xml)
    namespace = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
    return "\n".join(node.text or "" for node in root.findall(".//w:t", namespace))


def _strip_html(raw_text: str) -> str:
    without_scripts = re.sub(r"<(script|style).*?</\1>", " ", raw_text, flags=re.IGNORECASE | re.DOTALL)
    return unescape(re.sub(r"<[^>]+>", " ", without_scripts))


def _clean_text(text: str) -> str:
    collapsed = re.sub(r"[ \t]+", " ", text)
    collapsed = re.sub(r"\n{3,}", "\n\n", collapsed)
    return collapsed.strip()

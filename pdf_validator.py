from pypdf import PdfReader

def extract_pdf_info(filepath):
    info = {"texto_completo": "", "metadatos": {}, "hallazgos": [], "recomendaciones": []}
    try:
        reader = PdfReader(filepath)

        if reader.metadata:
            for key, value in reader.metadata.items():
                info["metadatos"][key] = str(value)

        full_text = []
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                full_text.append(page_text)

        info["texto_completo"] = "\n".join(full_text)

    except Exception as e:
        info["hallazgos"].append(f"Error: {str(e)}")
        info["recomendaciones"].append("Verifica que el archivo sea PDF válido.")

    return info

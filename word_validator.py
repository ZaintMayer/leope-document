from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
import re

def validate_word_document(filepath):
    report = {"hallazgos": [], "recomendaciones": []}
    try:
        document = Document(filepath)

        for i, paragraph in enumerate(document.paragraphs):
            if paragraph.style.name.startswith('Heading'):
                if i == 0 and paragraph.style.name != 'Title':
                    report["hallazgos"].append(f"Primer párrafo no tiene estilo 'Title': {paragraph.style.name}")
                    report["recomendaciones"].append(f"Usar estilo 'Title' en el párrafo 1.")
            elif paragraph.style.name == 'Normal' and len(paragraph.text.split()) < 5 and paragraph.text.isupper():
                report["hallazgos"].append(f"Texto tipo título sin estilo en párrafo {i+1}")
                report["recomendaciones"].append(f"Aplicar estilo de título en párrafo {i+1}")

            if paragraph.style.name == 'Normal' and paragraph.paragraph_format.alignment != WD_ALIGN_PARAGRAPH.JUSTIFY:
                report["hallazgos"].append(f"Párrafo {i+1} no justificado")
                report["recomendaciones"].append(f"Alinear párrafo {i+1} a justificado")

            email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
            found_emails = re.findall(email_pattern, paragraph.text)
            for email in found_emails:
                if not email.endswith(('.com', '.org', '.net')):
                    report["hallazgos"].append(f"Correo con dominio no permitido: {email}")
                    report["recomendaciones"].append(f"Revisar correo '{email}'")

    except Exception as e:
        report["hallazgos"].append(f"Error: {str(e)}")
        report["recomendaciones"].append("Verifica que el archivo sea .docx válido.")

    return report

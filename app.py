from flask import Flask, request, jsonify
from validators.word_validator import validate_word_document
from validators.pdf_validator import extract_pdf_info
import os

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf', 'docx'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home():
    return "✅ Bienvenido a la aplicación de validación de documentos."

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No se encontró el archivo en la solicitud"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "Nombre de archivo vacío"}), 400

    if file and allowed_file(file.filename):
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)

        if file.filename.endswith('.docx'):
            resultado = validate_word_document(filepath)
        elif file.filename.endswith('.pdf'):
            resultado = extract_pdf_info(filepath)
        else:
            return jsonify({"error": "Formato de archivo no soportado"}), 400

        return jsonify(resultado), 200

    return jsonify({"error": "Archivo no permitido"}), 400

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import json
import uuid
from PyPDF2 import PdfReader
from utils.extract_academic_progress import extract_academic_progress

app = Flask(__name__)
CORS(app, supports_credentials=True)

# Get the current script's directory
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

@app.route('/')
def index():
    return "Hello World"

@app.route('/upload-pdf', methods=['POST'])
def upload_pdf():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    if file and file.filename.lower().endswith('.pdf'):
        # Extract text from PDF
        text = ""
        pdf_reader = PdfReader(file)
        for page in pdf_reader.pages:
            text += page.extract_text()
        
        # Extract data
        data = extract_academic_progress(text)
        
        return jsonify(data), 200
    else:
        return jsonify({"error": "Invalid file format. Please upload a PDF."}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
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
        output_folder = os.path.join(CURRENT_DIR, 'output')
        os.makedirs(output_folder, exist_ok=True)
        
        pdf_path = os.path.join(output_folder, file.filename)
        file.save(pdf_path)
        
        text = ""
        with open(pdf_path, 'rb') as pdf_file:
            pdf_reader = PdfReader(pdf_file)
            for page in pdf_reader.pages:
                text += page.extract_text()
        
        txt_filename = os.path.splitext(file.filename)[0] + '.txt'
        txt_path = os.path.join(output_folder, txt_filename)
        with open(txt_path, 'w', encoding='utf-8') as txt_file:
            txt_file.write(text)
        
        # Extract data
        data = extract_academic_progress(text)
        
        # Save JSON data with a unique ID
        unique_id = str(uuid.uuid4())
        json_filename = f"{unique_id}.json"
        json_path = os.path.join(output_folder, json_filename)
        with open(json_path, 'w') as json_file:
            json.dump(data, json_file, indent=2)
        
        return jsonify({
            "message": "File uploaded, text extracted, and JSON generated successfully",
            "pdf_path": pdf_path,
            "txt_path": txt_path,
            "json_path": json_path,
            "unique_id": unique_id
        }), 200
    else:
        return jsonify({"error": "Invalid file format. Please upload a PDF."}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
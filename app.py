from flask import Flask
from flask import request
from flask import jsonify
import os

import pdf_vector_store
from pdf_text_extract_utility import extract_text_from_pdf


app = Flask(__name__)

vector_store = pdf_vector_store.PDFVectorStore()

@app.route('/upload', methods=['POST'])
def upload_pdf():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']
    file_path = os.path.join('uploads', file.filename)
    file.save(file_path)

    chunks = extract_text_from_pdf(file_path)
    
    vector_store.add_documents(chunks)
    
    return jsonify({"message": "PDF processed successfully", "chunks": len(chunks)})

@app.route('/query', methods=['POST'])
def query_pdf():
    query = request.json.get('query', '')
    
    if not query:
        return jsonify({"error": "No query provided"}), 400
    
    similar_chunks = vector_store.search(query)
    
    response = " ".join(similar_chunks)
    
    return jsonify({
        "query": query,
        "similar_chunks": similar_chunks,
        "response": response
    })

if __name__ == '__main__':
    os.makedirs('uploads', exist_ok=True)
    app.run(debug=True)
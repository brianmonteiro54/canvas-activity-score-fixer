from flask import Flask, request, send_file, jsonify
import os
from processor import process_csv
import uuid

app = Flask(__name__)

# Limite de tamanho do arquivo (10 MB)
MAX_FILE_SIZE = 10 * 1024 * 1024

@app.route("/process-csv", methods=["POST"])
def upload_csv():
    if "file" not in request.files:
        return jsonify({"error": "Nenhum arquivo enviado"}), 400

    file = request.files["file"]

    # Verificar tamanho do arquivo
    if file.content_length > MAX_FILE_SIZE:
        return jsonify({"error": "Arquivo muito grande (máx: 10MB)"}), 400

    # Gerar nome de arquivo seguro
    file_path = os.path.join("/tmp", f"{uuid.uuid4()}.csv")
    file.save(file_path)

    corrected_file_path = process_csv(file_path)
    if corrected_file_path is None:
        return jsonify({"error": "Erro ao processar o arquivo"}), 500

    return send_file(corrected_file_path, as_attachment=True)

@app.route("/hello", methods=["GET"])
def hello_world():
    return jsonify({"message": "Olá, mundo!"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

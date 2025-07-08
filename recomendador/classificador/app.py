from flask import Flask, request, jsonify
from classificador_llm import classificar_usuario

app = Flask(__name__)

@app.route("/")
def home():
    return "✅ Agente Classificador Ativo"

@app.route("/classificar", methods=["POST"])
def classificar():
    dados = request.get_json()
    perfil = classificar_usuario(dados)
    return jsonify({"perfil": perfil})

if __name__ == "__main__":
    app.run(port=5001, debug=True)

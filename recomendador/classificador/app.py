from flask import Flask, request, jsonify
from classificador import classificar_ultima_entrada
import json
import os

app = Flask(__name__)

@app.route("/")
def home():
    return "✅ Agente Classificador Ativo"

@app.route("/classificar", methods=["POST"])
def classificar():
    perfil = classificar_ultima_entrada()

    # Garante que a pasta exista
    os.makedirs("/shared/classificador", exist_ok=True)

    # Salva o resultado classificado
    with open("/shared/classificador/resultado_classificacao.json", "w", encoding="utf-8") as f:
        json.dump({"perfil": perfil}, f, ensure_ascii=False, indent=2)

    return jsonify({"perfil": perfil})


@app.route("/perfil", methods=["GET"])
def obter_perfil_classificado():
    caminho = "/shared/classificador/resultado_classificacao.json"
    if os.path.exists(caminho):
        with open(caminho, "r", encoding="utf-8") as f:
            dados = json.load(f)
        return jsonify(dados)
    return jsonify({"erro": "Perfil ainda não classificado"}), 404

if __name__ == "__main__":
    app.run(port=5001, debug=True)

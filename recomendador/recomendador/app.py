from flask import Flask, request, jsonify
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)

def carregar_base(caminho):
    try:
        with open(caminho, encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Erro ao carregar base de regras: {e}")
        return {}

base = carregar_base("base_regras.json")

def gerar_recomendacoes(perfil, preferencia):
    recomendacoes = {}
    if preferencia in ["filme", "ambos"]:
        recomendacoes["filmes"] = base[perfil].get("filmes", [])
    if preferencia in ["livro", "ambos"]:
        recomendacoes["livros"] = base[perfil].get("livros", [])
    return recomendacoes

@app.route("/recomendar", methods=["POST"])
def recomendar():
    if not request.is_json:
        return jsonify({"erro": "Corpo da requisição deve estar em JSON."}), 400

    dados = request.get_json()
    perfil = dados.get("perfil")
    preferencia = dados.get("preferencia", "ambos")

    if not perfil:
        return jsonify({"erro": "Campo 'perfil' é obrigatório."}), 400
    if perfil not in base:
        return jsonify({
            "erro": "Perfil não encontrado",
            "mensagem": f"Não há recomendações para o perfil '{perfil}'"
        }), 404

    recomendacoes = gerar_recomendacoes(perfil, preferencia)

    return jsonify({
        "perfil": perfil,
        "recomendacoes": recomendacoes
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=False)

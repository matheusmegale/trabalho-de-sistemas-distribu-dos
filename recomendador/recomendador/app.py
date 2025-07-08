from flask import Flask, request, jsonify
import json

app = Flask(__name__)

# Carrega a base de recomendações
with open("base_regras.json", encoding="utf-8") as f:
    base = json.load(f)

@app.route("/recomendar", methods=["POST"])
def recomendar():
    dados = request.json

    perfil = dados.get("perfil")
    preferencia = dados.get("preferencia", "ambos")

    if perfil not in base:
        return jsonify({"erro": f"Perfil '{perfil}' não encontrado."}), 404

    recomendacoes = {}

    if preferencia == "filme" or preferencia == "ambos":
        recomendacoes["filmes"] = base[perfil].get("filmes", [])

    if preferencia == "livro" or preferencia == "ambos":
        recomendacoes["livros"] = base[perfil].get("livros", [])

    return jsonify({
        "perfil": perfil,
        "recomendacoes": recomendacoes
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)

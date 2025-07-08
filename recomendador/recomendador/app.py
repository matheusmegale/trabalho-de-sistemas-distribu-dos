from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os
import logging
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Configura logger
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

# Base de dados e controle de modificação
base = {}
ultimo_carregamento = None
CAMINHO_BASE = "base_regras.json"

def carregar_base_com_reload(caminho):
    global base, ultimo_carregamento
    try:
        modificado_em = os.path.getmtime(caminho)
        if ultimo_carregamento is None or modificado_em > ultimo_carregamento:
            with open(caminho, encoding="utf-8") as f:
                base = json.load(f)
            ultimo_carregamento = modificado_em
            logger.info("Base de regras recarregada.")
    except Exception as e:
        logger.error(f"Erro ao recarregar base de regras: {e}")

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
    preferencia = dados.get("preferencia", "ambos").lower()

    if not perfil:
        return jsonify({"erro": "Campo 'perfil' é obrigatório."}), 400

    # Normaliza perfil
    perfil = perfil.strip().lower()

    # Verifica validade da preferência
    if preferencia not in ["filme", "livro", "ambos"]:
        return jsonify({"erro": "Preferência inválida. Use 'filme', 'livro' ou 'ambos'."}), 400

    # Recarrega base se necessário
    carregar_base_com_reload(CAMINHO_BASE)

    if perfil not in base:
        logger.warning(f"Perfil não encontrado: {perfil}")
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

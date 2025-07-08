from flask import Flask, render_template, request
import os
import json
import requests
from datetime import datetime

app = Flask(__name__)

PASTA_PREFERENCIAS = 'preferencias'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/salvar', methods=['POST'])
def salvar_preferencias():
    nome = request.form.get('name')
    idade = request.form.get('age')
    preferencia = request.form.get('preference')
    generos = request.form.get('genres')

    if not nome or not idade or not preferencia or not generos:
        return "<h2>⚠️ Todos os campos são obrigatórios!</h2><a href='/'>← Voltar</a>"

    dados = {
        "nome": nome,
        "idade": idade,
        "preferencia": preferencia,
        "generos": [g.strip() for g in generos.split(',') if g.strip()]
    }

    # 1. Salvar JSON local
    os.makedirs(PASTA_PREFERENCIAS, exist_ok=True)
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    nome_arquivo = f'preferencias_{timestamp}.json'
    caminho = os.path.join(PASTA_PREFERENCIAS, nome_arquivo)

    with open(caminho, 'w', encoding='utf-8') as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)

    # 2. Enviar os dados para o Agente Classificador via POST
    try:
        resposta = requests.post("http://localhost:5001/classificar", json=dados)
        if resposta.status_code == 200:
            perfil = resposta.json().get("perfil", "perfil_indefinido")
        else:
            perfil = "erro_na_classificacao"
    except Exception as e:
        perfil = f"erro: {str(e)}"

    # 3. Exibir resultado
    return f"""
        <h2>✅ Preferências salvas com sucesso!</h2>
        <p><strong>Perfil classificado:</strong> {perfil}</p>
        <a href="/">← Voltar</a>
    """

if __name__ == '__main__':
    app.run(debug=True, port=5000)

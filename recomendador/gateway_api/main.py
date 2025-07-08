from flask import Flask, render_template, request
import os
import json
import requests
from datetime import datetime
from recomendador_ia import gerar_recomendacoes

app = Flask(__name__)

PASTA_PREFERENCIAS = 'preferencias'
CLASSIFICADOR_URL = "http://localhost:5001"  # Certifique-se que o classificador (Ollama) está rodando

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

    # 1. Salva JSON local
    os.makedirs(PASTA_PREFERENCIAS, exist_ok=True)
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    nome_arquivo = f'preferencias_{timestamp}.json'
    caminho = os.path.join(PASTA_PREFERENCIAS, nome_arquivo)

    with open(caminho, 'w', encoding='utf-8') as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)

    # 2. Envia para o Agente Classificador (Ollama via Flask)
    try:
        requests.post(f"{CLASSIFICADOR_URL}/classificar", json=dados)
        resp_perfil = requests.get(f"{CLASSIFICADOR_URL}/perfil")
        perfil = resp_perfil.json().get("perfil", "erro_classificacao")
    except Exception as e:
        return f"<h2>❌ Erro ao classificar perfil: {str(e)}</h2><a href='/'>← Voltar</a>"

    # 3. Gera recomendações via OpenAI (sem servidor Flask no agente 2)
    recomendacoes = gerar_recomendacoes(perfil, preferencia)

    # 4. Exibe o resultado na mesma tela
    html = f"""
        <div style='font-family: Poppins, sans-serif; background-color: #0f172a; color: #e2e8f0; min-height: 100vh; padding: 2rem;'>
        <h2 class="text-2xl font-bold text-indigo-300 mb-4">✅ Preferências salvas com sucesso!</h2>
        <p class="text-lg mb-4"><strong>Perfil classificado:</strong> <span class="text-indigo-400">{perfil}</span></p>
        <h3 class="text-xl font-semibold text-indigo-300 mb-2">📚 Recomendações personalizadas:</h3>
        <ul class="list-disc ml-6 text-slate-200">
    """

    for r in recomendacoes:
        if "erro" in r:
            html += f"<li><strong>Erro:</strong> {r['erro']}</li>"
        else:
            html += f"<li class='mb-2'><strong>{r['titulo']}</strong> ({r['tipo']}, {r['genero']})<br><em>🎯 {r['motivo']}</em></li>"

    html += "</ul><br><a href='/' class='text-indigo-400 underline'>← Voltar ao formulário</a></div>"
    return html

if __name__ == '__main__':
    app.run(debug=True, port=5000)

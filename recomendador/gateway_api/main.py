from flask import Flask, render_template, request
import os
import json
import requests
from datetime import datetime
from recomendador_ia import gerar_recomendacoes

app = Flask(_name_)

# Caminho no volume compartilhado Docker
PASTA_PREFERENCIAS = '/shared/preferencias'
CLASSIFICADOR_URL = "http://classificador:5001"

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

    # 1. Salvar JSON local no volume /shared
    os.makedirs(PASTA_PREFERENCIAS, exist_ok=True)
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    nome_arquivo = f'preferencias_{timestamp}.json'
    caminho = os.path.join(PASTA_PREFERENCIAS, nome_arquivo)

    with open(caminho, 'w', encoding='utf-8') as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)

    # 2. Enviar dados para o classificador
    try:
        resposta = requests.post(f"{CLASSIFICADOR_URL}/classificar", json=dados)
        if resposta.status_code == 200:
            perfil = resposta.json().get("perfil", "perfil_indefinido")
        else:
            perfil = "erro_na_classificacao"
    except Exception as e:
        perfil = f"erro: {str(e)}"

    # 3. Gerar recomendações com base no perfil
    recomendacoes = gerar_recomendacoes(perfil, preferencia)

    # 4. Exibir resultado estilizado com Tailwind
    return f"""
  <!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Resultado</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap" rel="stylesheet" />
    <style>
        body {
            font-family: 'Poppins', sans-serif;
            background-color: #0f172a;
            color: #e2e8f0;
        }
    </style>
</head>
<body class="min-h-screen flex items-center justify-center p-6">
    <div class="w-full max-w-3xl bg-slate-800 rounded-xl p-8 shadow-2xl">
        <h2 class="text-2xl font-bold text-green-400 mb-2">✅ Preferências salvas com sucesso!</h2>
        <p class="mb-6 text-lg text-indigo-200"><strong>Perfil classificado:</strong> {perfil}</p>

        <h3 class="text-xl font-semibold text-indigo-300 mb-4">📚 Recomendações personalizadas:</h3>
        <ul class="space-y-5">
            {''.join(f'''
                <li class="bg-slate-700 p-4 rounded-lg shadow-md transition-transform transform hover:scale-105">
                    <p class="text-white font-medium">• <strong>{item.get("titulo")}</strong> <span class="text-slate-400">({item.get("tipo")}, {item.get("genero")})</span></p>
                    <p class="text-sm text-indigo-200 mt-1">🎯 {item.get("motivo")}</p>
                </li>
            ''' for item in recomendacoes)}
        </ul>

        <div class="mt-8 text-center">
            <a href="/" class="text-indigo-400 hover:underline text-sm">← Voltar ao formulário</a>
        </div>
    </div>
</body>
</html>

    """
if _name_ == '_main_':
    app.run(debug=True, port=5000)
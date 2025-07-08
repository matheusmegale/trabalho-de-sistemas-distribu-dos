import requests
import json
import os

# 🔐 Chave de API da OpenAI
API_KEY = os.getenv("OPENAI_API_KEY", "chave_nao_encontrada")

API_URL = "https://api.openai.com/v1/chat/completions"
MODEL = "gpt-4o-mini"

HEADERS = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {API_KEY}"
}

def gerar_recomendacoes(perfil: str, preferencia: str) -> list:
    prompt = f"""
Você é um sistema recomendador cultural. Com base no perfil cultural '{perfil}' e na preferência por '{preferencia}', gere exatamente 10 recomendações culturais personalizadas no formato JSON puro.

❗ REGRAS OBRIGATÓRIAS:
- A resposta deve conter exatamente 10 itens.
- O formato deve ser um array JSON, com objetos no modelo abaixo.
- NÃO escreva nada fora do JSON.
- NÃO adicione frases antes ou depois.
- NÃO use emojis, comentários, markdown ou ```json.

Formato obrigatório:
[
  {{
    "titulo": "Nome da obra",
    "tipo": "filme" ou "livro",
    "genero": "gênero principal",
    "motivo": "Por que essa obra combina com o perfil"
  }},
  ...
]

Agora gere as 10 recomendações no formato acima:
"""

    payload = {
        "model": MODEL,
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7
    }

    try:
        response = requests.post(API_URL, headers=HEADERS, json=payload)

        if response.status_code != 200:
            return [{"erro": f"Erro HTTP {response.status_code}: {response.text}"}]

        conteudo = response.json()["choices"][0]["message"]["content"]

        print("🔍 RESPOSTA DA IA:\n", conteudo)  # Debug no terminal

        return json.loads(conteudo)

    except json.JSONDecodeError:
        return [{"erro": "A resposta da IA não estava em formato JSON válido."}]
    except Exception as e:
        return [{"erro": f"Erro inesperado: {str(e)}"}]

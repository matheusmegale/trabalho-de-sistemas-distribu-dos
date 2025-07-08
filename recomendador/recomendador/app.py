import openai
import os

# Token da OpenAI (evite deixar público no código real!)
openai.api_key = "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"

def gerar_recomendacoes_ia(perfil, preferencia):
    prompt = f"""
Você é um sistema recomendador cultural. Com base no perfil cultural '{perfil}' de um usuário, recomende 3 obras de {preferencia} personalizadas. 

Formato da resposta:
[
  {{
    "titulo": "...",
    "tipo": "filme" ou "livro",
    "genero": "...",
    "motivo": "..."
  }},
  ...
]
"""

    try:
        resposta = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
        )
        conteudo = resposta.choices[0].message.content.strip()
        return conteudo
    except Exception as e:
        return f"Erro na OpenAI: {e}"
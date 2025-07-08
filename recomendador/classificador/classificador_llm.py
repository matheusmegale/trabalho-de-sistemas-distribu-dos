import requests
import os
import json

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL_NAME = "mistral"

def classificar_usuario(preferencias: dict) -> str:
    nome = preferencias.get("nome", "Usuário")
    idade = preferencias.get("idade", "desconhecida")
    tipo = preferencias.get("preferencia", "conteúdos")
    generos = preferencias.get("generos", [])

    prompt = (
            "Você é um classificador de perfis culturais de usuários. Sua tarefa é gerar um rótulo único e específico com base nas preferências da pessoa.\n\n"
            "O rótulo deve obrigatoriamente seguir o padrão:\n"
            "<nível>_<tipo>_<gênero>\n\n"
            "Onde:\n"
            "- <nível>: iniciante, curioso, fã, experiente, veterano\n"
            "- <tipo>: cinefilo, leitor, misto\n"
            "- <gênero>: um gênero principal extraído da lista de gêneros favoritos (ex: acao, comedia, fantasia, romance, suspense, terror, etc)\n\n"
            "Exemplos válidos de rótulos:\n"
            "- iniciante_cinefilo_acao\n"
            "- curioso_leitor_fantasia\n"
    "- fã_misto_comedia\n"
    "- veterano_cinefilo_terror\n\n"
    "Regras:\n"
    "- Escolha apenas 1 gênero principal com base nos favoritos\n"
    "- Use 'misto' apenas se a pessoa consome livros e filmes\n"
    "- Responda **apenas o rótulo**, no formato slug (minúsculo, sem espaços, sem acentos, com underline)\n"
    "- Nenhuma explicação ou frase extra\n\n"
    f"Dados do usuário:\n"
    f"- Nome: {nome}\n"
    f"- Idade: {idade}\n"
    f"- Preferência declarada: {tipo}\n"
    f"- Gêneros favoritos: {', '.join(generos)}\n\n"
    "Classifique esse perfil:"
    )


    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "stream": False
    }

    try:
        response = requests.post(OLLAMA_URL, json=payload)
        response.raise_for_status()
        resposta = response.json()["message"]["content"]
        return resposta.strip().lower().replace(" ", "_")
    except Exception as e:
        print("Erro na classificação com Ollama:", str(e))
        return "erro_classificacao"


def classificar_ultima_entrada() -> str:
    caminho_pasta = os.path.join("..", "gateway_api", "preferencias")

    arquivos = [f for f in os.listdir(caminho_pasta) if f.endswith(".json")]
    if not arquivos:
        return "nenhum_arquivo_encontrado"

    # Pega o mais recente pelo timestamp no nome
    ultimo_arquivo = sorted(arquivos)[-1]
    caminho_completo = os.path.join(caminho_pasta, ultimo_arquivo)

    try:
        with open(caminho_completo, "r", encoding="utf-8") as f:
            preferencias = json.load(f)
            return classificar_usuario(preferencias)
    except Exception as e:
        print("Erro ao ler arquivo de preferências:", str(e))
        return "erro_leitura"

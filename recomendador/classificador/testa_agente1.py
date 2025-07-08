from classificador_llm import classificar_usuario

# Simulando leitura do JSON que vem da interface
preferencias = {
    "nome": "Eduardo Ruan Guimarães Fonseca",
    "idade": "22",
    "preferencia": "filmes",
    "generos": ["Ação"]
}

perfil = classificar_usuario(preferencias)
print("Perfil classificado:", perfil)

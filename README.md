# 📚 Recomendador Cultural com Agentes Inteligentes

Sistema distribuído com dois agentes de IA que classificam perfis culturais e geram recomendações de livros e filmes personalizados, com arquitetura segura e modular em Flask + Docker.

---

## 🔍 Visão Geral

Este projeto consiste em:

- Uma **interface web** para entrada de preferências (nome, idade, gêneros, etc.);
- Um **Agente Classificador** que utiliza LLM local (Mistral via GPT4All/Ollama) para analisar o perfil do usuário;
- Um **Agente Recomendador** que gera sugestões baseadas na classificação.

Toda a comunicação é feita via chamadas HTTP, com autenticação entre os agentes e compartilhamento controlado via Docker.

---

## 🧠 Validação do Problema

### Relevância do problema abordado

A sobrecarga de conteúdo digital dificulta a escolha de livros e filmes alinhados ao gosto do usuário. Muitos sistemas de recomendação existentes utilizam apenas histórico de navegação, sem considerar preferências declaradas de forma personalizada.

Este projeto busca resolver essa dor combinando:

- Um formulário intuitivo de preferências culturais;
- Classificação de perfil com IA local (LLM);
- Recomendações geradas com base no perfil detectado.

Segundo dados da [Nielsen](https://www.nielsen.com/us/en/insights/report/2023/the-era-of-choice/), 66% dos usuários desistem de consumir conteúdo por excesso de opções. Além disso, estudos acadêmicos demonstram que sistemas de recomendação personalizados aumentam o engajamento em até 47% (Silva et al., 2022).

### Interface de Coleta de Preferências

A tela abaixo exemplifica o formulário utilizado para entender os gostos do usuário de forma intuitiva. Essa etapa inicial é crucial para o funcionamento do sistema, pois serve como base para a classificação de perfil e a recomendação personalizada:

![image](https://github.com/user-attachments/assets/13a7a731-3365-440c-9a2d-8f18e9335e73)

### Documentação da "dor" a ser resolvida

O sistema visa resolver:

- A dificuldade dos usuários em encontrar conteúdo relevante de forma rápida;
- A falta de personalização de sistemas tradicionais;
- A ausência de soluções com uso de IA local, que respeitem privacidade.

Com isso, o projeto entrega uma experiência adaptativa e confiável mesmo em contextos com acesso restrito à internet ou onde privacidade é essencial.

---

## 🧱 Arquitetura

Ver documentos:

COLOCAR OS DOCUMENTOS AQUI

---

## 🚀 Como executar o projeto

### 1. Clone o repositório

```bash
git clone https://github.com/matheusmegale/trabalho-de-sistemas-distribu-dos.git
cd trabalho-de-sistemas-distribu-dos/recomendador
```

### 2. Instale o Ollama

O Ollama permite rodar modelos LLM localmente de forma eficiente.

Acesse: https://ollama.com/download

Instale o programa para seu sistema operacional.

Após instalar, execute:

```bash
ollama run mistral
```

### 3. Crie o arquivo .env

Crie um arquivo .env na raiz com sua chave da OpenAI (se desejar usar a API) e o token interno:

```env
OPENAI_API_KEY=sk-sua-chave-aqui
INTERNAL_API_TOKEN=chave_secreta_compartilhada
```

### 4. Instale dependências (modo local)

Se preferir rodar sem Docker:

```bash
pip install -r requirements.txt
```

Execute com Docker Compose:

```bash
docker-compose up --build
```

Esse comando irá:

Criar rede privada entre os containers;

Subir Gateway (porta 5000);

Subir Classificador;

Compartilhar arquivos em /shared.

 Acesse `http://localhost:5000` no navegador.

---

### 🧪 Testando o Sistema

Preencha o formulário com seus dados;

Clique em “Enviar Preferências”;

O sistema irá:

Salvar as preferências como JSON;

  • Enviar para o Agente Classificador;

  • Obter o perfil via IA local (Mistral);

  • Retornar recomendações com base nesse perfil.

## 📁 Estrutura de Pastas

```bash
recomendador/
├── classificador/
│   ├── app.py
│   ├── classificador.py
│   └── Dockerfile
│
├── gateway_api/
│   ├── main.py
│   ├── recomendador_ia.py
│   └── templates/index.html
│
├── docker-compose.yml
├── .env
└── README.md
```

---

## ✅ Funcionalidades

* [x] Interface web com formulário de entrada
* [x] Salvamento de preferências em JSON
* [x] Classificação de perfil via modelo LLM local (Agente 1)
* [x] Geração de recomendações personalizadas (Agente 2)
* [x] Comunicação via API com autenticação entre serviços
* [x] Isolamento por containers Docker e rede privada

---

## 🛡️ Segurança

* Uso de `.env` para proteger chaves sensíveis;
* Header interno `X-Internal-Token` entre containers;
* Rede privada com controle de acesso entre agentes;
* Volume compartilhado com escopo restrito.

---

## 📎 Referências

* Nielsen, The Era of Choice Report – 2023
* Silva et al., “Sistemas Inteligentes de Recomendação Baseados em Perfil”, UFSC, 2022
* OpenAI API Docs – [https://platform.openai.com/docs](https://platform.openai.com/docs)
* Ollama – [https://ollama.com/](https://ollama.com/)
* Flask Documentation – [https://flask.palletsprojects.com/](https://flask.palletsprojects.com/)

---

## 👨‍💻 Desenvolvido por

Eduardo Ruan Guimarães Fonseca – Sistemas de Informação – UFLA
Izac Moreira Souza Junior – Sistemas de Informação – UFLA
Matheus de Paula Megale – Sistemas de Informação – UFLA
Nadson Souza Matos  – Sistemas de Informação – UFLA


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

## 🎯 Dor (Problema Central)

Em um mundo com acesso ilimitado a filmes, séries e livros digitais, os usuários frequentemente se deparam com a chamada “paralisia por excesso de escolha”. Com milhares de títulos disponíveis em plataformas de streaming e catálogos online, muitos usuários gastam mais tempo tentando decidir o que consumir do que realmente aproveitando o conteúdo. Isso causa frustração, fadiga decisória e até abandono da experiência. Outro fator agravante é que os sistemas de recomendação atuais, mesmo sofisticados, tendem a se basear exclusivamente em dados comportamentais passados (como cliques, histórico de visualizações ou compras), sem considerar **as preferências declaradas pelo próprio usuário**. Isso limita a capacidade de entregar sugestões realmente significativas. A dor está em não se sentir compreendido ou representado pelas recomendações recebidas, o que compromete o engajamento e reduz o valor percebido das plataformas de conteúdo.

---

## 🧠 Validação do Problema

O problema da sobrecarga de conteúdo não é apenas percebido empiricamente; ele é confirmado por dados. Segundo o relatório da [Nielsen (2023)](https://www.nielsen.com/insights/2023/data-driven-personalization-2023-state-of-play-report/), **66% dos usuários desistem de consumir conteúdo digital por não conseguirem escolher o que assistir ou ler**. Isso revela um déficit claro de personalização inteligente nas plataformas. Além disso, pesquisas acadêmicas, como o estudo de Silva et al. (2022), apontam que o uso de recomendação personalizada com base em perfis declarados pode aumentar o engajamento em até **47%**. O projeto propõe resolver essa lacuna por meio de um sistema distribuído e modular que permite capturar preferências declaradas via formulário, processá-las com um classificador inteligente e gerar recomendações sob medida. Esse fluxo visa restaurar a confiança do usuário na recomendação automatizada, entregando valor real com base no que ele realmente gosta, e não apenas no que ele consumiu no passado.

### Interface de Coleta de Preferências

A tela abaixo exemplifica o formulário utilizado para entender os gostos do usuário de forma intuitiva. Essa etapa inicial é crucial para o funcionamento do sistema, pois serve como base para a classificação de perfil e a recomendação personalizada:

![image](https://github.com/user-attachments/assets/13a7a731-3365-440c-9a2d-8f18e9335e73)


## 🎬 Exemplo de Funcionamento

O sistema “Recomendador Cultural com Agentes Inteligentes” coleta preferências culturais do usuário por meio de uma interface web simples e responsiva, e entrega recomendações personalizadas com base em seu perfil classificado.

### 📝 Preenchimento do Formulário

O usuário informa nome, idade, tipo de mídia preferida (filmes, livros ou ambos) e os gêneros culturais favoritos.

![Captura de tela 2025-07-08 141233](https://github.com/user-attachments/assets/f3f564a6-7525-48cb-9200-6ddf335b3a04)

---

### 🤖 Resultado: Perfil + Recomendações Inteligentes

Após o envio, o sistema classifica o perfil automaticamente e exibe 10 recomendações personalizadas, utilizando IA local (Ollama + Mistral) e a API da OpenAI.

![Captura de tela 2025-07-08 142437](https://github.com/user-attachments/assets/111a46e5-a445-47f4-9def-ada19cb3cf4a)

---

## 🧱 Arquitetura

Ver documentos:

[Visão Inicial Pré-Modelagem de Ameaças.pdf](https://github.com/user-attachments/files/21132117/Visao.Inicial.Pre-Modelagem.de.Ameacas.pdf)

[Visão Final Após Implementação das Medidas de Mitigação.pdf](https://github.com/user-attachments/files/21132210/Visao.Final.Apos.Implementacao.das.Medidas.de.Mitigacao.pdf)

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

   • Criar rede privada entre os containers;

   • Subir Gateway (porta 5000);

   • Subir Classificador;

   • Compartilhar arquivos em /shared.

 Acesse `http://localhost:5000` no navegador.

---

### 🧪 Testando o Sistema

Preencha o formulário com seus dados;

Clique em “Enviar Preferências”;

O sistema irá:

  • Salvar as preferências como JSON;

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

* Eduardo Ruan Guimarães Fonseca – Sistemas de Informação – UFLA
* Izac Moreira Souza Junior – Sistemas de Informação – UFLA
* Matheus de Paula Megale – Sistemas de Informação – UFLA
* Nadson Souza Matos  – Sistemas de Informação – UFLA


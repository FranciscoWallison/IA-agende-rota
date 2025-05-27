# 🦷 Assistente de Saúde Bucal com Flask + Ollama + Redis

Este é um projeto de assistente virtual de saúde bucal, desenvolvido com **Flask**, **Ollama** e **Redis**. Ele foi criado para **orientar usuários sobre cuidados com a saúde bucal**, **vender planos odontológicos com desconto** e **redirecionar o usuário para telas específicas** com base em sua mensagem.

---

## 🧠 Tecnologias utilizadas

* **Flask**: framework web responsável por expor a API `/chat`, que processa a entrada do usuário e retorna a resposta.
* **Ollama**: servidor local que executa o modelo de linguagem (LLM `llama3`) para gerar respostas personalizadas com base em contexto.
* **Redis**: utilizado para cache de respostas geradas anteriormente, melhorando a performance.
* **RAG leve (Retrieval-Augmented Generation)**: utiliza um arquivo `documents.json` como base de conhecimento local, sem banco de dados ou vetorização pesada.

---

## 💡 Como funciona

1. O usuário envia uma mensagem (ex: "Quero marcar uma consulta").
2. O sistema verifica se há uma **resposta padrão** (para agilizar o atendimento).
3. Caso não haja, ele consulta o modelo `llama3`, incluindo contexto da base (`documents.json`) para enriquecer a resposta.
4. Se a resposta do modelo contiver termos como `consulta`, `horário`, etc., o sistema adiciona uma rota (`"app_rota": "agendamento"`) e pode incluir links promocionais.
5. A resposta é cacheada no Redis por 1 hora para reutilização.

---

## 🎯 Objetivo do projeto

Este assistente foi desenvolvido com foco em **direcionar clientes interessados em cuidados odontológicos**. Ele ajuda a:

* Coletar informações básicas do usuário.
* Redirecionar para o fluxo de **agendamento de consultas**.
* Promover **planos de saúde bucal com desconto**.
* Melhorar a experiência do usuário com respostas rápidas e personalizadas.

---

## 📁 Estrutura esperada

```
project/
│
├── app.py               # API Flask
├── documents.json       # Base de conhecimento textual
├── Dockerfile           # (opcional) build do app
├── docker-compose.yml   # Redis, Ollama, Flask
```

---

## ▶️ Como rodar com Docker Compose

Certifique-se de ter o modelo `llama3` já baixado e o Ollama funcionando.

```bash
docker compose up --build
```

A API estará disponível em: [http://localhost:5000/chat](http://localhost:5000/chat)

---

## 📌 Exemplo de requisição

```json
POST /chat
{
  "message": "Quero marcar uma consulta"
}
```

Resposta:

```json
{
  "reply": "Claro! Podemos marcar uma consulta. Informe a especialidade desejada.",
  "app_rota": "agendamento"
}
```


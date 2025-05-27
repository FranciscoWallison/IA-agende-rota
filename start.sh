#!/usr/bin/env bash
set -e

# 1) Inicia o Ollama em background de forma robusta
echo "Iniciando Ollama serve..."
nohup ollama serve > /tmp/ollama.log 2>&1 &

# 2) Espera o servidor HTTP do Ollama subir
echo "Aguardando servidor HTTP do Ollama..."
until curl -s http://localhost:11434/ > /dev/null; do
  sleep 1
done

# 3) Baixa o modelo somente se necessário
if ! ollama list | grep -q 'llama3'; then
  echo "Baixando modelo llama3..."
  ollama pull llama3
fi

# 4) Aguarda modelo responder com texto válido
echo "Aguardando modelo carregar..."
until curl -s -X POST http://localhost:11434/api/generate \
     -H 'Content-Type: application/json' \
     -d '{"model":"llama3","prompt":"Diga Olá","stream":false}' \
     | grep -q '"response"'; do
  printf '.'
  sleep 1
done
echo -e "\nModelo carregado!"

# 5) Inicia o Flask
echo "Iniciando Flask..."
exec python3 main.py

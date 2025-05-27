FROM ollama/ollama:latest

# Instalar dependências para Python e Flask
RUN apt-get update && apt-get install -y python3 python3-pip curl

# Criar diretório da aplicação
WORKDIR /app

# Copiar arquivos da API
COPY requirements.txt ./
COPY main.py ./
COPY start.sh ./
COPY documents.json ./

# Instalar dependências Python
RUN pip3 install --no-cache-dir -r requirements.txt

# Expor porta da API Flask
EXPOSE 5000


RUN chmod +x start.sh

# Comando para iniciar a API Flask
ENTRYPOINT ["./start.sh"]

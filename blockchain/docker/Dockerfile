FROM python:3.10-slim

# Instalar o curl e outras dependências necessárias
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copiar os arquivos necessários para o container
COPY ./blockchain /app/blockchain
COPY ./api /app/api
COPY ./frontend /app/frontend
COPY requirements.txt /app

# Instalar as dependências do projeto
RUN pip install -r requirements.txt

# Expor a porta da API Flask
EXPOSE 5000

# Se o front-end for um build estático, você pode fazer o build aqui:
# RUN cd frontend && npm install && npm run build

# Comando para iniciar a aplicação
CMD ["python", "api/app.py"]

# 1. Imagem Base: Começamos com uma imagem oficial do Python (versão 3.12, 'slim' é mais leve)
FROM python:3.12-slim

# 2. Pasta de Trabalho: Define o diretório principal dentro do contêiner
WORKDIR /code

# 3. Copia o arquivo de requisitos PRIMEIRO
# (O Docker faz cache, então só reinstala se esse arquivo mudar)
COPY requirements.txt .

# 4. Instala as bibliotecas Python
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copia TODO o resto do projeto (a pasta 'app', o 'demo.db', etc.) para dentro do /code
COPY . .

# 6. Comando de Execução: Diz ao contêiner o que fazer quando ele iniciar
# (Inicie o servidor 'uvicorn', aponte para o 'app' dentro de 'app.main',
# aceite conexões de qualquer host, na porta 8000)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
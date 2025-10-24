# API "Text-to-SQL" com Google Gemini e FastAPI

![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi)
![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker)
![Google Gemini](https://img.shields.io/badge/Google%20Gemini-4285F4?style=for-the-badge&logo=google)

## 📖 Sobre o Projeto

Este projeto é uma API simples que traduz perguntas em linguagem natural (como "Quantos clientes temos?") em consultas SQL reais. Ele usa a IA do Google Gemini para fazer a "tradução", e o FastAPI para servir a API. O projeto é totalmente conteinerizado com Docker, facilitando a execução.

O objetivo é criar um *endpoint* (`/query`) que permita a um usuário (ou outro sistema) consultar um banco de dados SQLite sem precisar saber escrever código SQL.

### Principais Funcionalidades

* **Tradução de Linguagem Natural para SQL:** Recebe uma pergunta e a transforma em uma *query* SQL.
* **Execução da Consulta:** Executa a *query* gerada no banco de dados SQLite.
* **Segurança:** Implementa uma verificação básica para permitir apenas consultas `SELECT`, prevenindo operações perigosas (como `DROP`, `UPDATE`, `INSERT`).
* **Base de Dados em Português:** O banco de dados e o *prompt* da IA são configurados em português para facilitar perguntas no idioma.

## 🛠️ Tecnologias Utilizadas

* **Python 3.12:** Linguagem base da aplicação.
* **Google Gemini (`gemini-1.0-pro`):** Modelo de IA usado para a tradução da pergunta para SQL.
* **FastAPI:** Framework web para a criação da API.
* **Uvicorn:** Servidor ASGI para rodar a aplicação FastAPI.
* **SQLAlchemy:** Utilizado para a conexão e execução de *queries* no banco.
* **SQLite:** O banco de dados de arquivo simples.
* **Docker & Docker Compose:** Para criar um ambiente de desenvolvimento e produção portátil e isolado.

## 🚀 Configuração e Instalação

Siga os passos abaixo para executar o projeto localmente.

### 1. Pré-requisitos

* **Git:** Para clonar o repositório.
* **Docker Desktop:** Essencial. [Instale aqui](https://www.docker.com/products/docker-desktop/).
* **Conta Google Cloud:** Necessária para obter a chave da API do Gemini.
* **SQLite3 (Linha de Comando):** Necessário para criar o banco de dados inicial. [Instale aqui](https://www.sqlite.org/download.html) (baixe o "sqlite-tools-win-x64-....zip" e adicione o `sqlite3.exe` ao seu `PATH`).

### 2. Configuração do Google Cloud

Este é o passo mais importante. O erro 404 (`model not found`) ocorre se esta etapa não for feita corretamente.

1.  Acesse o [Google Cloud Console](https://console.cloud.google.com/).
2.  Crie um novo projeto (ou use um existente).
3.  Vincule uma conta de faturamento ao projeto (**`Set up billing`**).
4.  No menu (☰), vá para **"APIs e Serviços"** -> **"Biblioteca"**.
5.  Procure e **ATIVE** as **DUAS** APIs a seguir:
    * **`Generative Language API`**
    * **`Vertex AI API`**
6.  No menu (☰), vá para **"APIs e Serviços"** -> **"Credenciais"**.
7.  Clique em "Criar Credenciais" -> "Chave de API" e copie sua nova chave.

### 3. Instalação Local

1.  Clone este repositório:
    ```bash
    git clone [https://github.com/SEU-USUARIO/SEU-REPOSITORIO.git](https://github.com/SEU-USUARIO/SEU-REPOSITORIO.git)
    cd text_to_sql_app
    ```

2.  Crie o arquivo `.env` com sua chave de API (substitua `SUA-CHAVE-API-AQUI`):
    ```bash
    echo "GOOGLE_API_KEY=SUA-CHAVE-API-AQUI" > .env
    ```

3.  Crie o banco de dados `demo.db` a partir do script SQL:
    ```bash
    sqlite3 demo.db < init_db.sql
    ```

4.  Construa a imagem Docker (isso pode levar alguns minutos):
    ```bash
    docker compose build
    ```

5.  Inicie o servidor em segundo plano:
    ```bash
    docker compose up -d
    ```
    A API agora está rodando em `http://localhost:8000`.

## ⚙️ Como Usar (Exemplos)

Você pode testar a API usando o `curl` no seu terminal.

### Exemplo 1: Contagem de Clientes

**Pergunta:** "Quantos clientes temos?"

**Comando `curl`:**
```bash
curl -X POST "http://localhost:8000/query" -H "Content-Type: application/json" -d "{\"question\":\"Quantos clientes temos?\"}"

**Resposta Esperada:**
```json
{
  "sql": "SELECT COUNT(*) AS total_clientes FROM clientes;",
  "result": [
    {
      "total_clientes": 4
    }
  ]
}
```

### Exemplo 2: Clientes por País

**Pergunta:** "Qual o nome dos clientes do Brasil?"

**Comando `curl`:**
```bash
curl -X POST "http://localhost:8000/query" -H "Content-Type: application/json" -d "{\"question\":\"Qual o nome dos clientes do Brasil?\"}"
```

**Resposta Esperada:**
```json
{
  "sql": "SELECT nome FROM clientes WHERE pais = 'BRASIL';",
  "result": [
    {
      "nome": "Daniel"
    }
  ]
}
```

### Exemplo 3: Pergunta Complexa (JOIN)

**Pergunta:** "Qual o nome do cliente que comprou um Notebook Pro?"

**Comando `curl`:**
```bash
curl -X POST "http://localhost:8000/query" -H "Content-Type: application/json" -d "{\"question\":\"Qual o nome do cliente que comprou um Notebook Pro?\"}"
```

**Resposta Esperada:**
```json
{
  "sql": "SELECT T1.nome FROM clientes AS T1 INNER JOIN pedidos AS T2 ON T1.id = T2.cliente_id INNER JOIN itens_pedido AS T3 ON T2.id = T3.pedido_id INNER JOIN produtos AS T4 ON T3.produto_id = T4.id WHERE T4.nome = 'Notebook Pro';",
  "result": [
    {
      "nome": "Alice"
    }
  ]
}
```

## 📂 Estrutura do Projeto

```
text_to_sql_app/
├── app/
│   ├── __init__.py           # Carrega o .env
│   ├── database.py           # Conexão com o banco (SQLAlchemy)
│   ├── gemini_utils.py       # Lógica de chamada da API Gemini
│   └── main.py               # Lógica da API (FastAPI)
├── demo.db                   # Banco de dados SQLite (criado pelo script)
├── init_db.sql               # Script de criação do banco e dados
├── requirements.txt          # Bibliotecas Python
├── Dockerfile                # Receita para construir a imagem Docker
├── docker-compose.yml        # Receita para rodar o contêiner
└── .env                      # Arquivo de chaves (local, não vai pro Git)
```
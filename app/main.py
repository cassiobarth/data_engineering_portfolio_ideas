from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import inspect

# Importa as partes que criamos nos outros arquivos
from .database import ENGINE, run_query
from .gemini_utils import text_to_sql

# Cria a aplicação FastAPI
app = FastAPI(title="Text-to-SQL com Gemini")

# --- Variável Global para o Esquema ---
# Vamos armazenar o esquema do banco de dados aqui quando a app iniciar
SCHEMA_STR = ""

# --- Modelo de Requisição (Pydantic) ---
# Define como deve ser o JSON que o usuário envia.
# Apenas uma chave "question" com um valor string.
class NLRequest(BaseModel):
    question: str

# --- Evento de Startup ---
# Esta função é executada UMA VEZ quando o servidor inicia.
@app.on_event("startup")
def capture_schema() -> None:
    """
    Inspeciona o banco de dados na inicialização e armazena
    o esquema (CREATE TABLES) em uma variável global.
    """
    global SCHEMA_STR
    
    # Cria um "inspetor" do SQLAlchemy
    insp = inspect(ENGINE)
    
    table_schemas = []
    # Pega o nome de todas as tabelas
    for t in insp.get_table_names():
        # Pega o nome de todas as colunas daquela tabela
        columns = [c['name'] for c in insp.get_columns(t)]
        
        # Formata o esquema como "CREATE TABLE nome (col1, col2, ...);"
        table_schemas.append(f"CREATE TABLE {t} ({', '.join(columns)});")
    
    # Junta todas as definições de tabela em uma única string
    SCHEMA_STR = "\n".join(table_schemas)
    print("--- ESQUEMA DO BANCO CAPTURADO ---")
    print(SCHEMA_STR)
    print("-----------------------------------")


# --- Endpoint da API ---
# Define o endpoint principal: /query
# Ele só aceita requisições do tipo POST.
@app.post("/query")
def query(req: NLRequest):
    """
    Recebe uma pergunta em linguagem natural, traduz para SQL,
    executa no banco e retorna o SQL e o resultado.
    """
    global SCHEMA_STR
    
    try:
        # 1. Traduz a pergunta para SQL usando o Gemini
        sql_query = text_to_sql(req.question, SCHEMA_STR)
        
        # 2. Medida de segurança simples:
        # Verifica se o SQL começa com "SELECT" (ignorando espaços e caixa)
        if not sql_query.lstrip().lower().startswith("select"):
            raise ValueError("Query SQL insegura. Apenas SELECT é permitido.")
            
        # 3. Executa a query no banco de dados
        result = run_query(sql_query)
        
        # 4. Retorna a resposta completa
        return {"sql": sql_query, "result": result}
    
    except Exception as e:
        # Se qualquer passo acima falhar (Gemini, Validação, Banco),
        # retorna um erro 400 para o usuário.
        raise HTTPException(status_code=400, detail=str(e))
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session

# Cria a "engine" (motor) de conexão.
# "sqlite:///demo.db" é o caminho para o arquivo do banco de dados.
# O "sqlite:///" com três barras indica um caminho relativo 
# (ou seja, 'demo.db' na mesma pasta onde o script for executado, 
# que será a raiz /code no Docker).
ENGINE = create_engine("sqlite:///demo.db", future=True, echo=False)

def run_query(sql: str) -> list[dict]:
    """
    Executa uma query SQL 'read-only' e retorna os resultados 
    como uma lista de dicionários.
    """
    # Abre uma nova sessão com o banco de dados
    with Session(ENGINE) as session:
        # Executa o SQL (o 'text()' é para segurança)
        # .mappings() converte as linhas em objetos que podemos ler
        # .all() pega todos os resultados
        rows = session.execute(text(sql)).mappings().all()
        
    # Converte o resultado em uma lista de dicionários simples
    # (ex: [{"nome": "Alice"}, {"nome": "Bob"}])
    return [dict(r) for r in rows]
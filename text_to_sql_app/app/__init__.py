from pathlib import Path
from dotenv import load_dotenv

# Define o caminho para o arquivo .env
# Path(__file__) é o arquivo atual (app/__init__.py)
# .resolve() encontra o caminho completo
# .parent é a pasta 'app'
# .parent de novo é a pasta 'text_to_sql_app' (a raiz do projeto)
# / ".env" junta esse caminho com o nome do arquivo .env
dotenv_path = Path(__file__).resolve().parent.parent / ".env"

# Carrega o arquivo .env
# override=False significa que se a variável de ambiente já existir 
# no sistema, ela não será sobrescrita (boa prática)
load_dotenv(dotenv_path=dotenv_path, override=False)
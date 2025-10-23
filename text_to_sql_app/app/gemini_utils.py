import os
import json
import google.generativeai as genai

# Tenta configurar a API key.
# A chave foi carregada no ambiente pelo arquivo __init__.py
try:
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
except AttributeError:
    # Lança um erro claro se a chave não foi encontrada
    raise EnvironmentError("Erro: A variável de ambiente GOOGLE_API_KEY não foi definida. Verifique seu arquivo .env")

# --- Este é o "Prompt de Sistema" ---
# É a instrução mais importante que damos à IA.
# Dizemos a ela quem ela é (especialista em SQL) e quais são as regras.
_SYSTEM_PROMPT = """
Você é um especialista em SQL. Você converte perguntas em linguagem natural 
para SQL (dialeto SQLite) que seja estritamente de LEITURA (read-only).
Nunca, em hipótese alguma, gere comandos INSERT, UPDATE, DELETE, DROP ou 
qualquer outro que modifique os dados ou o esquema.
Retorne APENAS um objeto JSON válido no formato: { "sql": "..." }.
Não inclua nenhuma outra palavra, explicação, ou marcadores de markdown 
(como ```json) antes ou depois do objeto JSON.
"""

# Configura o modelo que vamos usar
model = genai.GenerativeModel(
    # gemini-1.5-flash-latest é mais rápido e econômico
    model_name="gemini-1.5-flash-latest",
    
    # Passa a instrução de sistema
    system_instruction=_SYSTEM_PROMPT,
    
    # Configurações de geração
    generation_config=genai.types.GenerationConfig(
        # Força o modelo a responder em formato JSON
        response_mime_type="application/json",
        
        # 'temperature=0.1' torna a resposta mais determinística 
        # (menos "criativa"), o que é bom para SQL.
        temperature=0.1
    )
)

def text_to_sql(question: str, schema: str) -> str:
    """
    Converte uma pergunta em linguagem natural para SQL usando o Gemini.
    """
    
    # Monta o prompt final para o usuário
    user_prompt = f"schema:\n{schema}\n\nquestion: {question}"
    
    try:
        # Envia o prompt para a API do Gemini
        response = model.generate_content(user_prompt)
        
        # A API já retorna o JSON como texto puro (ex: '{"sql": "..."}')
        # Carregamos esse texto para um dicionário Python
        payload = json.loads(response.text)
        
        # Retornamos apenas o valor da chave "sql"
        return payload["sql"]
    
    except Exception as e:
        # Se o Gemini responder algo que não é o JSON esperado
        # ou a API falhar, nós lançamos um erro.
        print(f"Erro ao chamar a API do Gemini ou analisar a resposta: {e}")
        raise ValueError(f"Falha ao gerar SQL: {e}")
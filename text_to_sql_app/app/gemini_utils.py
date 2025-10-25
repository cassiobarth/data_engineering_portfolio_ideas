import os
import json
import google.generativeai as genai

# Tenta configurar a API key.
try:
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
except AttributeError:
    raise EnvironmentError("Erro: A variável de ambiente GOOGLE_API_KEY não foi definida. Verifique seu arquivo .env")

# --- Este é o "Prompt de Sistema" ---
_SYSTEM_PROMPT = """
Você é um especialista em SQL. Você converte perguntas em linguagem natural 
para SQL (dialeto SQLite) que seja estritamente de LEITURA (read-only).
Nunca, em hipótese alguma, gere comandos INSERT, UPDATE, DELETE, DROP ou 
querer outro que modifique os dados ou o esquema.
Retorne APENAS um objeto JSON válido no formato: { "sql": "..." }.
Não inclua nenhuma outra palavra, explicação, ou marcadores de markdown 
(como ```json) antes ou depois do objeto JSON.
"""

# Configura o modelo que vamos usar
model = genai.GenerativeModel(
    model_name="gemini-2.5-flash", 
    system_instruction=_SYSTEM_PROMPT,
    generation_config=genai.types.GenerationConfig(
        temperature=0.1
    )
)

def text_to_sql(question: str, schema: str) -> str:
    """
    Converte uma pergunta em linguagem natural para SQL usando o Gemini.
    """
    
    user_prompt = f"schema:\n{schema}\n\nquestion: {question}"
    
    # *** A CORREÇÃO ESTÁ AQUI EMBAIXO ***
    
    # Inicializa 'response' como None ANTES do 'try'
    response = None 
    
    try:
        # 1. Tenta chamar a API
        response = model.generate_content(user_prompt)
        
        # 2. Tenta limpar e analisar a resposta
        text_response = response.text.strip()
        
        if text_response.startswith("```json"):
            text_response = text_response[7:]
        if text_response.endswith("```"):
            text_response = text_response[:-3]
            
        text_response = text_response.strip()
        
        payload = json.loads(text_response)
        
        return payload["sql"]
    
    except Exception as e:
        print(f"Erro ao chamar a API do Gemini ou analisar a resposta: {e}")
        
        # 3. Agora, esta verificação é segura
        if response:
            # Se a falha foi no 'json.loads', imprime a resposta problemática
            print(f"Resposta (problemática) recebida da IA: {response.text}")
        else:
            # Se a falha foi na chamada da API, 'response' ainda é None
            print("A falha ocorreu ANTES de receber uma resposta da IA (verifique a API Key, Quota, etc).")
            
        raise ValueError(f"Falha ao gerar ou analisar SQL: {e}")
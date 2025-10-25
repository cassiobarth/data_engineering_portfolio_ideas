import streamlit as st
import requests

# URL da nossa API FastAPI (o nome 'text2sql-api' é o nome do serviço
# que vamos definir no docker-compose.yml)
API_URL = "http://text2sql-api:8000/query"

# --- Configuração da Página ---
st.set_page_config(
    page_title="Chat com Banco de Dados",
    page_icon="💬"
)

st.title("Chat com seu Banco de Dados 💬")
st.write("Faça uma pergunta em português sobre os dados e a IA irá traduzir e executar o SQL.")

# --- Interface ---
with st.form(key="query_form"):
    # Input da pergunta
    question = st.text_input(
        "Sua pergunta:",
        placeholder="Ex: Quantos clientes temos do Brasil?"
    )
    
    # Botão de Enviar
    submit_button = st.form_submit_button(label="Perguntar")

# --- Lógica de Backend ---
if submit_button and question:
    with st.spinner("Pensando... 🧠"):
        try:
            # 1. Envia a pergunta para a API FastAPI
            response = requests.post(API_URL, json={"question": question})

            # 2. Trata a resposta
            if response.status_code == 200:
                data = response.json()
                
                # Exibe a query SQL gerada
                st.subheader("Query SQL Gerada:")
                st.code(data['sql'], language='sql')
                
                # Exibe o resultado (em uma tabela)
                st.subheader("Resultado:")
                st.dataframe(data['result'])
                
            else:
                # Mostra o erro da API (ex: 404, 400, etc.)
                st.error(f"Erro da API (Código {response.status_code}):")
                st.json(response.json())

        except requests.exceptions.ConnectionError:
            st.error("Erro de Conexão: Não foi possível conectar à API.")
            st.write("Verifique se o serviço 'text2sql-api' está rodando.")
        except Exception as e:
            st.error(f"Ocorreu um erro inesperado: {e}")
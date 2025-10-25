import streamlit as st
import requests
import os

# --- AVISO DE INICIALIZAÇÃO (NOVO) ---
# Este comando 'toast' mostra um aviso popup rápido assim que a página carrega.
st.toast("Este é um app gratuito e pode demorar até 60s para 'acordar' no primeiro acesso. Obrigado pela paciência! 🚀", icon="⏱️")
# -------------------------------------

# Procura pela URL online no ambiente, se não achar, usa a URL local
# (Esta é a mudança que fizemos antes para o Render)
API_URL = os.getenv("API_URL", "http://text2sql-api:8000/query")


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
    # Mostra um spinner ENQUANTO a API (que também pode estar "dormindo") acorda
    with st.spinner("Conectando aos servidores... 🧠"):
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
            st.write(f"Verifique se o serviço da API ({API_URL}) está acessível.")
        except Exception as e:
            st.error(f"Ocorreu um erro inesperado: {e}")
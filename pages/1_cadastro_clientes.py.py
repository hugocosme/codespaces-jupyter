import streamlit as st
from supabase import create_client, Client
from postgrest.exceptions import APIError
import datetime

st.set_page_config(page_title="Cadastro de Clientes", layout="centered")

if 'logged_in' not in st.session_state or not st.session_state['logged_in']:
    st.error("⚠️ Você precisa estar logado para acessar esta página.")
    st.info("Por favor, faça o login na página principal.")
    st.stop()

def load_css():
    st.markdown("""
        <style>
            :root {
                --primary-color: #00BFFF; /* DeepSkyBlue */
                --text-color: #E0FFFF; /* LightCyan */
                --bg-color: #1a1a2e;
                --secondary-bg-color: #16213e;
            }
            html, body, [class*="st-"] { color: var(--text-color); background-color: var(--bg-color); }
            h1, h2 { color: var(--primary-color); text-shadow: 0 0 5px var(--primary-color), 0 0 10px var(--primary-color); }
            .stButton > button { color: var(--text-color); background-color: var(--secondary-bg-color); border: 1px solid var(--primary-color); border-radius: 8px; transition: all 0.3s ease-in-out; }
            .stButton > button:hover { box-shadow: 0 0 15px var(--primary-color); color: var(--primary-color); }
            [data-testid="stSidebar"] { background-color: var(--secondary-bg-color); }
        </style>
    """, unsafe_allow_html=True)

load_css()

@st.cache_resource
def init_connection():
    url = st.secrets["supabase"]["url"]
    key = st.secrets["supabase"]["key"]
    return create_client(url, key)

supabase: Client = init_connection()

st.title("Cadastro de Novos Clientes")

with st.form("client_form", clear_on_submit=True):
    st.subheader("Informações Pessoais")
    full_name = st.text_input("Nome Completo", placeholder="Ex: João da Silva")
    birth_date = st.date_input("Data de Nascimento", min_value=datetime.date(1920, 1, 1), value=None)

    st.subheader("Contato")
    phone_number = st.text_input("Número de Telefone", placeholder="(11) 99999-8888")
    is_whatsapp = st.checkbox("Este número é WhatsApp?")

    submitted = st.form_submit_button("Cadastrar Cliente")

if submitted:
    if not full_name:
        st.error("O campo 'Nome Completo' é obrigatório!")
    else:
        try:
            client_data = {
                "full_name": full_name,
                "birth_date": str(birth_date),
                "phone_number": phone_number,
                "is_whatsapp": is_whatsapp
            }
            response = supabase.table("clientes").insert(client_data).execute()
            if response.data:
                st.success(f"Cliente '{full_name}' cadastrado com sucesso!")
            else:
                st.error("Ocorreu um erro ao cadastrar o cliente.")
        except APIError as e:
            st.error(f"Erro na API do Supabase: {e.message}")
        except Exception as e:
            st.error(f"Ocorreu um erro inesperado: {e}")
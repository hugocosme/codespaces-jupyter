import streamlit as st
from supabase import create_client, Client
from postgrest import APIError

st.set_page_config(page_title="Cadastro de Usuário", layout="centered")

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

st.title("Crie sua Conta na Helios Nexus")

with st.form("signup_form"):
    st.subheader("Informe seus dados")
    email = st.text_input("E-mail")
    password = st.text_input("Senha", type="password")
    
    submitted = st.form_submit_button("Cadastrar")

if submitted:
    if not email or not password:
        st.error("Por favor, preencha todos os campos.")
    else:
        try:
            user = supabase.auth.sign_up({
                "email": email,
                "password": password,
            })
            st.success("Cadastro realizado com sucesso! Você já pode fazer o login na página principal.")
        except APIError as e:
            st.error(f"Erro no cadastro: {e.message}")
        except Exception as e:
            st.error(f"Ocorreu um erro inesperado: {e}")
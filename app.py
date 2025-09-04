import streamlit as st
from supabase import create_client, Client
from postgrest import APIError

# Configuração da página principal
st.set_page_config(page_title="Helios Nexus | Login", layout="wide")

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

if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
    st.session_state['user'] = None

def logout():
    st.session_state['logged_in'] = False
    st.session_state['user'] = None
    st.success("Você foi desconectado com sucesso!")

if st.session_state['logged_in']:
    st.sidebar.success(f"Bem-vindo, {st.session_state['user']['email']}!")
    st.sidebar.button("Logout", on_click=logout)
    
    st.title("Helios Nexus")
    st.header("Conectando você ao futuro da energia.")
    st.markdown("Use o menu na barra lateral para navegar pelas funcionalidades do sistema.")
    st.image("https://images.unsplash.com/photo-1508515053969-7b94594e62c1?q=80&w=2070", caption="A energia do sol ao seu alcance.")

else:
    st.title("Bem-vindo à Helios Nexus")
    st.subheader("Por favor, faça o login para continuar")

    with st.form("login_form"):
        email = st.text_input("E-mail")
        password = st.text_input("Senha", type="password")
        submitted = st.form_submit_button("Entrar")

        if submitted:
            try:
                user = supabase.auth.sign_in_with_password({"email": email, "password": password})
                st.session_state['logged_in'] = True
                st.session_state['user'] = user.user.dict()
                st.rerun()
            except (APIError, Exception):
                st.error("E-mail ou senha inválidos. Verifique suas credenciais ou cadastre-se.")
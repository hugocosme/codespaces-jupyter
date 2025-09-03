# app.py
import streamlit as st
from supabase import create_client, Client

# Inicializa a conexão com o Supabase usando os segredos do Streamlit
@st.cache_resource
def init_connection():
    url = st.secrets["supabase"]["url"]
    key = st.secrets["supabase"]["key"]
    return create_client(url, key)

supabase: Client = init_connection()

# app.py
import streamlit as st
from supabase import create_client, Client
import pandas as pd

# Título da Aplicação
st.set_page_config(page_title="Minha Lista de Tarefas", layout="wide")
st.title("✅ Minha Lista de Tarefas com Streamlit e Supabase")

# --- CONEXÃO COM O SUPABASE ---
@st.cache_resource
def init_connection():
    url = st.secrets["supabase"]["url"]
    key = st.secrets["supabase"]["key"]
    return create_client(url, key)

supabase: Client = init_connection()

# --- FUNÇÕES DE CRUD ---

# Função para buscar os dados (READ)
def fetch_all_tasks():
    response = supabase.table("tarefas").select("*").order("id").execute()
    return response.data

# Função para inserir dados (CREATE)
def add_task(task_name):
    if task_name:
        supabase.table("tarefas").insert({"nome_tarefa": task_name, "concluida": False}).execute()
        st.success(f"Tarefa '{task_name}' adicionada com sucesso!")
    else:
        st.warning("O nome da tarefa não pode estar vazio.")

# Função para atualizar o status (UPDATE)
def update_task_status(task_id, new_status):
    supabase.table("tarefas").update({"concluida": new_status}).eq("id", task_id).execute()

# Função para deletar uma tarefa (DELETE)
def delete_task(task_id):
    supabase.table("tarefas").delete().eq("id", task_id).execute()
    st.success(f"Tarefa ID {task_id} deletada!")

# --- INTERFACE DA APLICAÇÃO ---

# Formulário para adicionar nova tarefa
st.header("Adicionar Nova Tarefa")
with st.form("add_task_form", clear_on_submit=True):
    new_task_name = st.text_input("Nome da Tarefa")
    submitted = st.form_submit_button("Adicionar")
    if submitted:
        add_task(new_task_name)

st.divider()

# Exibição das tarefas
st.header("Tarefas Atuais")
tasks = fetch_all_tasks()

if not tasks:
    st.info("Nenhuma tarefa encontrada. Adicione uma nova tarefa acima!")
else:
    # Criando colunas para a tabela
    col1, col2, col3, col4 = st.columns([0.1, 0.5, 0.2, 0.2])

    with col1:
        st.write("**ID**")
    with col2:
        st.write("**Tarefa**")
    with col3:
        st.write("**Status**")
    with col4:
        st.write("**Ações**")
    
    st.divider()

    for task in tasks:
        with st.container():
            col1, col2, col3, col4 = st.columns([0.1, 0.5, 0.2, 0.2])
            with col1:
                st.write(task['id'])
            with col2:
                st.write(task['nome_tarefa'])
            with col3:
                # Checkbox para marcar como concluída
                is_completed = st.checkbox(
                    "Concluída", 
                    value=task['concluida'], 
                    key=f"check_{task['id']}",
                    on_change=update_task_status,
                    args=(task['id'], not task['concluida']) # Passa os argumentos para a função
                )
            with col4:
                # Botão para deletar
                if st.button("Deletar", key=f"del_{task['id']}"):
                    delete_task(task['id'])
                    st.rerun() # Recarrega a página para refletir a exclusão

# Para visualizar os dados brutos (opcional)
if st.checkbox("Mostrar dados brutos"):
    st.dataframe(pd.DataFrame(tasks))
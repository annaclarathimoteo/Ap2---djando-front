import streamlit as st
import requests
import pandas as pd
import altair as alt

# ============================================
# 🔧 CONFIGURAÇÃO GLOBAL
# ============================================
BASE_URL = "http://127.0.0.1:8000/api/cadastro_aluno"

st.set_page_config(
    page_title="AcadManage — Sistema Acadêmico",
    page_icon="🎓",
    layout="wide"
)

# Tema dark customizado
st.markdown("""
<style>

    /* Fundo geral */
    .stApp {
        background-color: #0E1117 !important;
    }

    /* Textos */
    h1, h2, h3, h4, h5, h6, label, p, span, div {
        color: #e6e6e6 !important;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: #111418 !important;
        border-right: 1px solid #2c2f36;
    }

    [data-testid="stSidebar"] * {
        color: #e6e6e6 !important;
    }

    /* Inputs e Select */
    .stTextInput>div>div>input,
    .stNumberInput input,
    .stSelectbox div[data-baseweb="select"] div {
        background-color: #111418 !important;
        color: #fff !important;
        border: 1px solid #2f333a !important;
        border-radius: 8px !important;
    }

    /* Botões */
    .stButton>button {
        background: linear-gradient(135deg, #2563eb, #1d4ed8);
        color: white !important;
        border-radius: 8px;
        border: none;
        padding: 0.6rem 1.2rem;
        font-weight: 600;
        transition: 0.2s;
    }

    .stButton>button:hover {
        background: linear-gradient(135deg, #3b82f6, #2563eb);
        transform: scale(1.03);
    }

    /* Cards */
    .card {
        padding: 20px;
        border-radius: 14px;
        background-color: #111418;
        border: 1px solid #2c2f36;
        margin-bottom: 25px;
    }

    /* Separadores */
    hr {
        border: 1px solid #2c2f36 !important;
    }

</style>
""", unsafe_allow_html=True)

# ============================================
# 🔥 CABEÇALHO PREMIUM
# ============================================
st.markdown("""
<div style="
    padding: 25px;
    background: linear-gradient(90deg, #1f2937, #111827);
    border-radius: 14px;
    margin-bottom: 30px;
    border: 1px solid #2c2f36;
">
    <h1 style="margin:0; text-align:center; font-size:36px;">🎓 AcadManage</h1>
    <p style="text-align:center; font-size:15px; margin-top:6px; color:#b3b3b3;">
        Sistema de Gestão Acadêmica — Administração de Alunos, Endereços, Notas e Disciplinas
    </p>
</div>
""", unsafe_allow_html=True)

# ============================================
# FUNÇÕES AUXILIARES
# ============================================
def safe_json(response):
    try:
        return response.json()
    except ValueError:
        return None

def show_error(response, data):
    if isinstance(data, dict):
        st.error(data.get("erro", f"Erro {response.status_code}: {response.text}"))
    else:
        st.error(f"Erro {response.status_code}: {response.text}")

# ============================================
# 📌 MENU LATERAL
# ============================================
st.sidebar.markdown("## 📋 Navegação")
menu = st.sidebar.radio(
    "",
    [
        "Cadastrar Dados",
        "Consultar Dados",
        "Atualizar Aluno",
        "Atualizar Endereço",
        "Atualizar Nota",
        "Atualizar Disciplina",
        "Boletim do Aluno"
    ]
)

# ============================================
# ✅ CADASTRAR
# ============================================
if menu == "Cadastrar Dados":

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("### 🧾 Cadastrar Informações")

    tipo = st.selectbox("Selecione o tipo de cadastro:", ["Aluno", "Endereço", "Nota", "Disciplina"])

    # --- ALUNO ---
    if tipo == "Aluno":
        nome = st.text_input("Nome completo")
        email = st.text_input("Email institucional")
        matricula = st.text_input("Matrícula")
        endereco_id = st.number_input("ID do Endereço (opcional)", min_value=1, step=1)

        if st.button("Cadastrar Aluno"):
            dados = {"nome": nome, "email": email, "matricula": matricula}
            if endereco_id:
                dados["endereco_id"] = endereco_id

            if not nome or not email or not matricula:
                st.warning("⚠ Preencha todos os campos obrigatórios.")
            else:
                res = requests.post(f"{BASE_URL}/aluno-cadastrado/", json={"dados": dados})
                data = safe_json(res)
                if res.status_code == 200:
                    st.success("✅ Aluno cadastrado com sucesso!")
                else:
                    show_error(res, data)

    # --- ENDEREÇO ---
    elif tipo == "Endereço":
        bairro = st.text_input("Bairro")
        cidade = st.text_input("Cidade")
        estado = st.text_input("Estado")
        cep = st.text_input("CEP")
        regiao = st.text_input("Região")
        endereco = st.text_input("Endereço")

        if st.button("Cadastrar Endereço"):
            dados = {
                "bairro": bairro, "cidade": cidade, "estado": estado,
                "cep": cep, "regiao": regiao, "endereco": endereco,
            }
            if not bairro or not cidade or not estado or not cep:
                st.warning("⚠ Preencha os campos obrigatórios.")
            else:
                res = requests.post(f"{BASE_URL}/endereco-cadastro/", json={"dados": dados})
                data = safe_json(res)
                if res.status_code == 200:
                    st.success("✅ Endereço cadastrado com sucesso!")
                else:
                    show_error(res, data)

    # --- NOTA ---
    elif tipo == "Nota":
        aluno_id = st.number_input("ID do Aluno", min_value=1, step=1)
        disciplina_id = st.number_input("ID da Disciplina", min_value=1, step=1)
        nota = st.number_input("Nota", min_value=0.0, max_value=10.0, step=0.1)

        if st.button("Cadastrar Nota"):
            payload = {
                "aluno_id": int(aluno_id),
                "disciplina_id": int(disciplina_id),
                "nota": float(nota)
            }
            res = requests.post(f"{BASE_URL}/nota-cadastro/", json=payload)
            data = safe_json(res)

            if res.status_code == 200:
                st.success("✅ Nota cadastrada com sucesso!")
            else:
                show_error(res, data)

    # --- DISCIPLINA ---
    elif tipo == "Disciplina":
        nome = st.text_input("Nome da Disciplina")
        codigo = st.text_input("Código")
        carga = st.number_input("Carga Horária (h)", min_value=1, step=1)

        if st.button("Cadastrar Disciplina"):
            dados = {"nome": nome, "carga_horaria": carga}
            if codigo:
                dados["codigo"] = codigo

            res = requests.post(f"{BASE_URL}/disciplina-cadastro/", json={"dados": dados})
            data = safe_json(res)

            if res.status_code == 200:
                st.success("✅ Disciplina cadastrada com sucesso!")
            else:
                show_error(res, data)

    st.markdown("</div>", unsafe_allow_html=True)

# ============================================
# ✅ CONSULTAR
# ============================================
elif menu == "Consultar Dados":

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("### 🔍 Consultar Dados")

    abas = st.tabs(["Consultar Todos", "Consultar por ID"])

    # --- CONSULTAR TODOS ---
    with abas[0]:
        tipo = st.selectbox("Selecione a tabela:", ["Alunos", "Endereços", "Notas", "Disciplinas"])
        endpoints = {
            "Alunos": f"{BASE_URL}/consultar-alunos/",
            "Endereços": f"{BASE_URL}/consultar-enderecos/",
            "Notas": f"{BASE_URL}/consultar-notas/",
            "Disciplinas": f"{BASE_URL}/consultar-disciplinas/",
        }

        if st.button("Consultar"):
            res = requests.get(endpoints[tipo])
            data = safe_json(res)
            if res.status_code == 200:
                st.dataframe(pd.DataFrame(data))
            else:
                show_error(res, data)

    # --- CONSULTAR POR ID ---
    with abas[1]:
        tipo = st.selectbox("Escolha o tipo:", ["Aluno", "Endereço", "Nota", "Disciplina"])
        id = st.number_input("ID:", min_value=1, step=1)

        endpoints = {
            "Aluno": f"{BASE_URL}/aluno-por-id/{id}",
            "Endereço": f"{BASE_URL}/endereco-id/{id}",
            "Nota": f"{BASE_URL}/nota-por-aluno/{id}",
            "Disciplina": f"{BASE_URL}/disciplina-por-id/{id}",
        }

        if st.button("Buscar"):
            res = requests.get(endpoints[tipo])
            data = safe_json(res)
            if res.status_code == 200:
                st.dataframe(pd.DataFrame(data))
            else:
                show_error(res, data)

    st.markdown("</div>", unsafe_allow_html=True)

# ============================================
# ✅ ATUALIZAR ALUNO
# ============================================
elif menu == "Atualizar Aluno":

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("### ✏️ Atualizar Aluno")

    aluno_id = st.number_input("ID do Aluno", min_value=1, step=1)
    nome = st.text_input("Novo nome")
    email = st.text_input("Novo email")
    matricula = st.text_input("Nova matrícula")

    if st.button("Atualizar"):
        dados = {k: v for k, v in {"nome": nome, "email": email, "matricula": matricula}.items() if v}

        res = requests.put(f"{BASE_URL}/alunos-por-id/{aluno_id}", json=dados)
        data = safe_json(res)

        if res.status_code == 200:
            st.success("✅ Aluno atualizado com sucesso!")
        else:
            show_error(res, data)

    st.markdown("</div>", unsafe_allow_html=True)

# ============================================
# ✅ ATUALIZAR ENDEREÇO
# ============================================
elif menu == "Atualizar Endereço":

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("### 🏠 Atualizar Endereço")

    id = st.number_input("ID do Endereço", min_value=1, step=1)
    bairro = st.text_input("Bairro")
    cidade = st.text_input("Cidade")
    estado = st.text_input("Estado")
    cep = st.text_input("CEP")
    regiao = st.text_input("Região")
    endereco = st.text_input("Endereço")

    if st.button("Atualizar"):
        dados = {k: v for k, v in {
            "bairro": bairro,
            "cidade": cidade,
            "estado": estado,
            "cep": cep,
            "regiao": regiao,
            "endereco": endereco,
        }.items() if v}

        res = requests.put(f"{BASE_URL}/endereco-por-id/{id}", json={"dados": dados})
        data = safe_json(res)

        if res.status_code == 200:
            st.success("✅ Endereço atualizado com sucesso!")
        else:
            show_error(res, data)

    st.markdown("</div>", unsafe_allow_html=True)

# ============================================
# ✅ ATUALIZAR NOTA
# ============================================
elif menu == "Atualizar Nota":

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("### 📝 Atualizar Nota")

    id = st.number_input("ID da Nota", min_value=1, step=1)
    aluno_id = st.number_input("Novo ID do Aluno (opcional)", min_value=1, step=1)
    disciplina_id = st.number_input("Novo ID da Disciplina (opcional)", min_value=1, step=1)
    nota = st.number_input("Nova Nota (opcional)", min_value=0.0, max_value=10.0, step=0.1)

    if st.button("Atualizar Nota"):
        dados = {}

        if aluno_id:
            dados["aluno_id"] = int(aluno_id)
        if disciplina_id:
            dados["disciplina_id"] = int(disciplina_id)
        if nota is not None:
            dados["nota"] = float(nota)

        if not dados:
            st.warning("⚠ Você precisa informar ao menos um campo para atualizar.")
        else:
            res = requests.put(f"{BASE_URL}/nota-por-id/{id}", json=dados)
            data = safe_json(res)

            if res.status_code == 200:
                st.success("✅ Nota atualizada com sucesso!")
            else:
                show_error(res, data)

    st.markdown("</div>", unsafe_allow_html=True)

# ============================================
# ✅ ATUALIZAR DISCIPLINA
# ============================================
elif menu == "Atualizar Disciplina":

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("### 📚 Atualizar Disciplina")

    id = st.number_input("ID da Disciplina", min_value=1, step=1)
    nome = st.text_input("Novo Nome da Disciplina")
    codigo = st.text_input("Novo Código")
    carga_horaria = st.number_input("Nova Carga Horária", min_value=0, step=1)

    if st.button("Atualizar Disciplina"):
        dados = {}

        if nome:
            dados["nome"] = nome
        if codigo:
            dados["codigo"] = codigo
        if carga_horaria > 0:
            dados["carga_horaria"] = int(carga_horaria)

        if not dados:
            st.warning("⚠ Você precisa informar ao menos um campo para atualizar.")
        else:
            res = requests.put(f"{BASE_URL}/disciplina-por-id/{id}", json=dados)
            data = safe_json(res)

            if res.status_code == 200:
                st.success("✅ Disciplina atualizada com sucesso!")
            else:
                show_error(res, data)

    st.markdown("</div>", unsafe_allow_html=True)

# ============================================
# ✅ BOLETIM DO ALUNO
# ============================================
elif menu == "Boletim do Aluno":

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("### 📖 Boletim do Aluno")

    aluno_id = st.number_input("Informe o ID do Aluno:", min_value=1, step=1)

    if st.button("Ver Boletim"):
        # Buscar dados do aluno
        aluno_res = requests.get(f"{BASE_URL}/aluno-por-id/{aluno_id}")
        aluno_data = safe_json(aluno_res)

        # Buscar notas e disciplinas
        notas_res = requests.get(f"{BASE_URL}/nota-por-aluno/{aluno_id}")
        notas_data = safe_json(notas_res)

        if aluno_res.status_code == 200 and notas_res.status_code == 200:
            aluno = aluno_data[0] if isinstance(aluno_data, list) else aluno_data
            st.subheader(f"👤 {aluno.get('nome', 'Aluno não encontrado')}")
            st.write(f"**Email:** {aluno.get('email', '—')}")
            st.write(f"**Matrícula:** {aluno.get('matricula', '—')}")
            st.markdown("---")

            df_notas = pd.DataFrame(notas_data)

            if not df_notas.empty:
                st.markdown("### 📊 Notas do Aluno")
                st.dataframe(df_notas)
            else:
                st.warning("⚠️ Nenhuma nota encontrada para este aluno.")
        else:
            show_error(notas_res, notas_data)

    st.markdown("</div>", unsafe_allow_html=True)

# ============================================
# ✅ RODAPÉ PREMIUM
# ============================================
st.markdown("<hr>", unsafe_allow_html=True)
st.caption("📘 AcadManage — Sistema Acadêmico • Desenvolvido por Anna Clara Thimoteo de Melo • 2025")

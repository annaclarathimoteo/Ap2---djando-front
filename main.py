import streamlit as st
import requests
import pandas as pd
import altair as alt

# ==============================
# CONFIGURAÇÃO
# ==============================
BASE_URL = "http://127.0.0.1:8000/api/cadastro_aluno"

st.set_page_config(page_title="Sistema Acadêmico", layout="wide")
st.title("🎓 Sistema de Cadastro Acadêmico - Django Ninja + Streamlit")
st.markdown("---")

menu = st.sidebar.radio(
    "📋 Menu",
    ["Cadastrar Dados", "Consultar Dados", "Atualizar Aluno", "Atualizar Endereço", 
     "Análises e Gráficos", "Relatórios"]
)


def safe_json(response):
    try:
        return response.json()
    except ValueError:
        return None

def show_error(response, data):
    """Evita erro se 'data' for None ou não for dicionário"""
    if isinstance(data, dict):
        st.error(data.get("erro", f"Erro {response.status_code}: {response.text}"))
    else:
        st.error(f"Erro {response.status_code}: {response.text}")

# ==============================
# CADASTRAR DADOS
# ==============================
if menu == "Cadastrar Dados":
    st.subheader("🧾 Cadastrar Dados")

    tipo = st.selectbox("Selecione o tipo de cadastro:", ["Aluno", "Endereço", "Nota", "Disciplina"])

    # -------------------------------
    # CADASTRAR ALUNO
    # -------------------------------
    if tipo == "Aluno":
        nome = st.text_input("Nome")
        email = st.text_input("Email")
        matricula = st.text_input("Matrícula")
        endereco_id = st.number_input("Endereço ID (opcional)", min_value=1, step=1, value=None, placeholder="ID do endereço")

        if st.button("Cadastrar Aluno"):
            dados = {"nome": nome, "email": email, "matricula": matricula}
            if endereco_id:
                dados["endereco_id"] = endereco_id

            if not nome or not email or not matricula:
                st.warning("Preencha todos os campos obrigatórios.")
            else:
                response = requests.post(f"{BASE_URL}/aluno-cadastrado/", json={"dados": dados})
                data = safe_json(response)
                if response.status_code == 200 and isinstance(data, dict):
                    st.success(data.get("mensagem", "Aluno cadastrado com sucesso!"))
                else:
                    show_error(response, data)

    # -------------------------------
    # CADASTRAR ENDEREÇO
    # -------------------------------
    elif tipo == "Endereço":
        bairro = st.text_input("Bairro")
        cidade = st.text_input("Cidade")
        estado = st.text_input("Estado")
        cep = st.text_input("CEP")
        regiao = st.text_input("Região")
        endereco = st.text_input("Endereço")

        if st.button("Cadastrar Endereço"):
            dados = {
                "bairro": bairro,
                "cidade": cidade,
                "estado": estado,
                "cep": cep,
                "regiao": regiao,
                "endereco": endereco,
            }
            if not bairro or not cidade or not estado or not cep:
                st.warning("Preencha todos os campos obrigatórios.")
            else:
                response = requests.post(f"{BASE_URL}/endereco-cadastro/", json={"dados": dados})
                data = safe_json(response)
                if response.status_code == 200 and isinstance(data, dict):
                    st.success(data.get("mensagem", "Endereço cadastrado com sucesso!"))
                else:
                    show_error(response, data)

    # -------------------------------
    # CADASTRAR NOTA
    # -------------------------------
    elif tipo == "Nota":
        aluno_id = st.number_input("ID do Aluno", min_value=1, step=1)
        disciplina_id = st.number_input("ID da Disciplina", min_value=1, step=1)
        nota = st.number_input("Nota", min_value=0.0, max_value=10.0, step=0.1)

        if st.button("Cadastrar Nota"):
            if not aluno_id or not disciplina_id:
                st.warning("Informe os IDs de aluno e disciplina.")
            else:
                payload = {
                    "aluno_id": int(aluno_id),
                    "disciplina_id": int(disciplina_id),
                    "nota": float(nota)
                }
                response = requests.post(f"{BASE_URL}/nota-cadastro/", json=payload)
                data = safe_json(response)
                if response.status_code == 200 and isinstance(data, dict):
                    st.success(data.get("mensagem", "Nota cadastrada com sucesso!"))
                else:
                    show_error(response, data)


    # -------------------------------
    # CADASTRAR DISCIPLINA
    # -------------------------------
    elif tipo == "Disciplina":
        nome = st.text_input("Nome da Disciplina")
        codigo = st.text_input("Código (opcional)")
        carga_horaria = st.number_input("Carga Horária", min_value=1, step=1)

        if st.button("Cadastrar Disciplina"):
            dados = {"nome": nome, "carga_horaria": carga_horaria}
            if codigo:
                dados["codigo"] = codigo

            if not nome or not carga_horaria:
                st.warning("Preencha o nome e a carga horária.")
            else:
                response = requests.post(f"{BASE_URL}/disciplina-cadastro/", json={"dados": dados})
                data = safe_json(response)
                if response.status_code == 200 and isinstance(data, dict):
                    st.success(data.get("mensagem", "Disciplina cadastrada com sucesso!"))
                else:
                    show_error(response, data)

# ==============================
# CONSULTAR DADOS
# ==============================
elif menu == "Consultar Dados":
    st.subheader("🔍 Consultar Dados")

    aba = st.tabs(["Consultar Todos", "Consultar por ID"])

    # Consultar Todos
    with aba[0]:
        opcao = st.selectbox("Selecione a Tabela:", ["Alunos", "Endereços", "Notas", "Disciplinas"])
        endpoints = {
            "Alunos": f"{BASE_URL}/consultar-alunos/",
            "Endereços": f"{BASE_URL}/consultar-enderecos/",
            "Notas": f"{BASE_URL}/consultar-notas/",
            "Disciplinas": f"{BASE_URL}/consultar-disciplinas/",
        }

        if st.button("Consultar Todos"):
            response = requests.get(endpoints[opcao])
            if response.status_code == 200:
                data = safe_json(response)
                if isinstance(data, list):
                    st.dataframe(pd.DataFrame(data))
                else:
                    show_error(response, data)
            else:
                show_error(response, None)

    # Consultar por ID
    with aba[1]:
        opcao = st.selectbox("Selecione o tipo:", ["Aluno", "Endereço", "Nota", "Disciplina"])
        id_input = st.number_input("Digite o ID:", min_value=1, step=1)

        endpoints = {
            "Aluno": f"{BASE_URL}/aluno-por-id/{id_input}",
            "Endereço": f"{BASE_URL}/endereco-id/{id_input}",
            "Nota": f"{BASE_URL}/nota-por-aluno/{id_input}",
            "Disciplina": f"{BASE_URL}/disciplina-por-id/{id_input}",
        }

        if st.button("Buscar"):
            response = requests.get(endpoints[opcao])
            if response.status_code == 200:
                data = safe_json(response)
                if isinstance(data, (list, dict)):
                    st.dataframe(pd.DataFrame(data))
                else:
                    show_error(response, data)
            else:
                show_error(response, None)

# ==============================
# ATUALIZAR ALUNO
# ==============================
elif menu == "Atualizar Aluno":
    st.subheader("✏️ Atualizar Aluno")

    aluno_id = st.number_input("ID do Aluno", min_value=1, step=1)
    nome = st.text_input("Nome")
    email = st.text_input("Email")
    matricula = st.text_input("Matrícula")

    if st.button("Atualizar Aluno"):
        dados = {k: v for k, v in {"nome": nome, "email": email, "matricula": matricula}.items() if v}
        if not dados:
            st.warning("Preencha pelo menos um campo para atualizar.")
        else:
            url = f"{BASE_URL}/alunos-por-id/{aluno_id}"
            response = requests.put(url, json=dados)
            data = safe_json(response)
            if response.status_code == 200:
                if isinstance(data, dict):
                    st.success(data.get("mensagem", "Aluno atualizado com sucesso!"))
                else:
                    st.success("Aluno atualizado com sucesso!")
            else:
                show_error(response, data)

# ==============================
# ATUALIZAR ENDEREÇO
# ==============================
elif menu == "Atualizar Endereço":
    st.subheader("🏠 Atualizar Endereço")

    id = st.number_input("ID do Endereço", min_value=1, step=1)
    bairro = st.text_input("Bairro")
    cidade = st.text_input("Cidade")
    estado = st.text_input("Estado")
    cep = st.text_input("CEP")
    regiao = st.text_input("Região")
    endereco = st.text_input("Endereço")

    if st.button("Atualizar Endereço"):
        dados = {k: v for k, v in {
            "bairro": bairro or endereco,
            "cidade": cidade,
            "estado": estado,
            "cep": cep,
            "regiao": regiao,
        }.items() if v}

        if not dados:
            st.warning("Preencha pelo menos um campo para atualizar.")
        else:
            url = f"{BASE_URL}/endereco-por-id/{id}"
            response = requests.put(url, json={"dados": dados})
            data = safe_json(response)
            if response.status_code == 200 and isinstance(data, dict):
                st.success(data.get("mensagem", "Endereço atualizado com sucesso!"))
            else:
                show_error(response, data)

# ==============================
# ANÁLISES E GRÁFICOS
# ==============================
elif menu == "Análises e Gráficos":
    st.subheader("📊 Análises e Gráficos")

    try:
        alunos = requests.get(f"{BASE_URL}/consultar-alunos/").json()
        enderecos = requests.get(f"{BASE_URL}/consultar-enderecos/").json()
        notas = requests.get(f"{BASE_URL}/consultar-notas/").json()
        disciplinas = requests.get(f"{BASE_URL}/consultar-disciplinas/").json()

        df_alunos = pd.DataFrame(alunos)
        df_end = pd.DataFrame(enderecos)
        df_notas = pd.DataFrame(notas)
        df_disc = pd.DataFrame(disciplinas)

        tab1, tab2 = st.tabs(["🎓 Alunos por Cidade", "📈 Médias de Notas por Disciplina"])

        with tab1:
            if not df_end.empty and "cidade" in df_end.columns:
                graf1 = (
                    alt.Chart(df_end)
                    .mark_bar()
                    .encode(x="cidade:N", y="count():Q", tooltip=["cidade", "count()"])
                    .properties(title="Distribuição de Alunos por Cidade")
                )
                st.altair_chart(graf1, use_container_width=True)
            else:
                st.warning("Dados de cidade não encontrados.")

        with tab2:
            if not df_notas.empty and "nota" in df_notas.columns and "disciplina_id" in df_notas.columns:
                medias = df_notas.groupby("disciplina_id")["nota"].mean().reset_index()
                medias = medias.merge(df_disc, left_on="disciplina_id", right_on="id", how="left")
                graf2 = (
                    alt.Chart(medias)
                    .mark_bar(color="#4e79a7")
                    .encode(x="nome:N", y="nota:Q", tooltip=["nome", "nota"])
                    .properties(title="Média de Notas por Disciplina")
                )
                st.altair_chart(graf2, use_container_width=True)
            else:
                st.warning("Dados insuficientes para gerar gráfico.")
    except Exception as e:
        st.error(f"Erro ao carregar dados: {e}")



elif menu == "Relatórios":
    st.subheader("📄 Relatórios de Notas por Aluno")

    tipo_rel = st.radio("Escolha o tipo de relatório:", ["Todos os Alunos", "Apenas 1 Aluno"])

    try:
        alunos = requests.get(f"{BASE_URL}/consultar-alunos/").json()
        notas = requests.get(f"{BASE_URL}/consultar-notas/").json()
        disciplinas = requests.get(f"{BASE_URL}/consultar-disciplinas/").json()

        df_alunos = pd.DataFrame(alunos)
        df_notas = pd.DataFrame(notas)
        df_disc = pd.DataFrame(disciplinas)

        # Colunas compatíveis com seu modelo Django:
        # aluno -> id do aluno
        # disciplina -> id da disciplina
        # nota -> valor da nota
        
        # Mescla: notas → alunos
        rel = (
            df_notas
            .merge(df_alunos, left_on="aluno", right_on="id", how="left", suffixes=("", "_aluno"))
            .merge(df_disc, left_on="disciplina", right_on="id", how="left", suffixes=("", "_disc"))
        )

        # Seleciona colunas finais
        rel = rel[["nome", "nome_disc", "nota"]]
        rel.columns = ["Aluno", "Disciplina", "Nota"]

        # ==============================
        # RELATÓRIO DE TODOS
        # ==============================
        if tipo_rel == "Todos os Alunos":
            st.write("📘 **Relatório com Todos os Alunos**")
            st.dataframe(rel)

        # ==============================
        # RELATÓRIO DE APENAS UM
        # ==============================
        else:
            lista_nomes = df_alunos["nome"].tolist()
            selecionado = st.selectbox("Selecione o aluno:", lista_nomes)

            rel_individual = rel[rel["Aluno"] == selecionado]

            st.write(f"📗 **Relatório de {selecionado}**")
            st.dataframe(rel_individual)

    except Exception as e:
        st.error(f"Erro ao gerar relatório: {e}")


st.markdown("---")
st.caption("💡 Desenvolvido com Streamlit + Django Ninja 🐍")

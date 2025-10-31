import streamlit as st
import requests

# URLs base da API Django Ninja
BASE_URL = "http://127.0.0.1:8000/api/cadastro_aluno"

st.title("📘 Sistema de Gestão - Alunos, Endereços, Notas e Disciplinas")

menu = ["Cadastrar", "Atualizar", "Deletar"]
choice = st.sidebar.selectbox("Menu", menu)

# Função para tratar resposta JSON
def safe_json(response):
    """Tenta converter a resposta para JSON, retorna dicionário vazio se falhar."""
    try:
        return response.json()
    except ValueError:
        return {}

# -------------------------------------------------
# CADASTRAR
# -------------------------------------------------
if choice == "Cadastrar":
    st.subheader("Cadastrar Novo Registro")

    tipo = st.selectbox("Tipo de Cadastro", ["Aluno", "Endereço", "Nota", "Disciplina"])

    if tipo == "Aluno":
        nome = st.text_input("Nome")
        email = st.text_input("Email")
        matricula = st.text_input("Matrícula")

        if st.button("Cadastrar Aluno"):
            dados = {"nome": nome, "email": email, "matricula": matricula}
            response = requests.post(f"{BASE_URL}/aluno-cadastrado/", json=dados)
            data = safe_json(response)

            if response.status_code == 200:
                st.success(data.get("mensagem", "Aluno cadastrado com sucesso!"))
            else:
                st.error(data.get("erro", f"Erro {response.status_code}: {response.text}"))

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
                "endereco": endereco
            }
            response = requests.post(f"{BASE_URL}/endereco-cadastro/", json=dados)
            data = safe_json(response)

            if response.status_code == 200:
                st.success(data.get("mensagem", "Endereço cadastrado com sucesso!"))
            else:
                st.error(data.get("erro", f"Erro {response.status_code}: {response.text}"))

    elif tipo == "Nota":
        aluno_id = st.number_input("ID do Aluno", min_value=1, step=1)
        disciplina_id = st.number_input("ID da Disciplina", min_value=1, step=1)
        valor = st.number_input("Nota", min_value=0.0, max_value=10.0, step=0.1)

        if st.button("Cadastrar Nota"):
            dados = {"aluno_id": aluno_id, "disciplina_id": disciplina_id, "valor": valor}
            response = requests.post(f"{BASE_URL}/nota-cadastro/", json=dados)
            data = safe_json(response)

            if response.status_code == 200:
                st.success(data.get("mensagem", "Nota cadastrada com sucesso!"))
            else:
                st.error(data.get("erro", f"Erro {response.status_code}: {response.text}"))

    elif tipo == "Disciplina":
        nome = st.text_input("Nome da Disciplina")
        carga_horaria = st.number_input("Carga Horária", min_value=1, step=1)

        if st.button("Cadastrar Disciplina"):
            dados = {"nome": nome, "carga_horaria": carga_horaria}
            response = requests.post(f"{BASE_URL}/disciplina-cadastro/", json=dados)
            data = safe_json(response)

            if response.status_code == 200:
                st.success(data.get("mensagem", "Disciplina cadastrada com sucesso!"))
            else:
                st.error(data.get("erro", f"Erro {response.status_code}: {response.text}"))

# -------------------------------------------------
# ATUALIZAR
# -------------------------------------------------
elif choice == "Atualizar":
    st.subheader("Atualizar Dados Existentes")

    tipo = st.selectbox("Tipo de Atualização", ["Aluno", "Endereço"])

    if tipo == "Aluno":
        aluno_id = st.number_input("ID do Aluno", min_value=1, step=1)
        nome = st.text_input("Nome")
        email = st.text_input("Email")
        matricula = st.text_input("Matrícula")

        if st.button("Atualizar Aluno"):
            dados = {k: v for k, v in {
                "nome": nome, "email": email, "matricula": matricula
            }.items() if v}

            if not dados:
                st.warning("Preencha pelo menos um campo para atualizar.")
            else:
                response = requests.put(f"{BASE_URL}/alunos-por-id/{aluno_id}", json=dados)
                data = safe_json(response)
                if response.status_code == 200:
                    st.success(data.get("mensagem", "Aluno atualizado com sucesso!"))
                else:
                    st.error(data.get("erro", f"Erro {response.status_code}: {response.text}"))

    elif tipo == "Endereço":
        id = st.number_input("ID do Endereço", min_value=1, step=1)
        bairro = st.text_input("Bairro")
        cidade = st.text_input("Cidade")
        estado = st.text_input("Estado")
        cep = st.text_input("CEP")
        regiao = st.text_input("Região")
        endereco = st.text_input("Endereço")

        if st.button("Atualizar Endereço"):
            dados = {k: v for k, v in {
                "bairro": bairro, "cidade": cidade, "estado": estado,
                "cep": cep, "regiao": regiao, "endereco": endereco
            }.items() if v}

            if not dados:
                st.warning("Preencha pelo menos um campo para atualizar.")
            else:
                response = requests.put(f"{BASE_URL}/endereco-por-id/{id}", json=dados)
                data = safe_json(response)
                if response.status_code == 200:
                    st.success(data.get("mensagem", "Endereço atualizado com sucesso!"))
                else:
                    st.error(data.get("erro", f"Erro {response.status_code}: {response.text}"))

# -------------------------------------------------
# DELETAR
# -------------------------------------------------
elif choice == "Deletar":
    st.subheader("Excluir Registros")

    tipo = st.selectbox("Tipo de Registro", ["Aluno", "Endereço", "Nota", "Disciplina"])
    id_item = st.number_input(f"ID do {tipo}", min_value=1, step=1)

    if st.button(f"Deletar {tipo}"):
        endpoint = {
            "Aluno": "aluno-deletar",
            "Endereço": "endereco-deletar",
            "Nota": "nota-deletar",
            "Disciplina": "disciplina-deletar"
        }[tipo]

        response = requests.delete(f"{BASE_URL}/{endpoint}/{id_item}")
        data = safe_json(response)

        if response.status_code == 200:
            st.success(data.get("mensagem", f"{tipo} deletado com sucesso!"))
        else:
            st.error(data.get("erro", f"Erro {response.status_code}: {response.text}"))
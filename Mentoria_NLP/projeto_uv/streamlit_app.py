import streamlit as st
import sys
import os
from datetime import datetime

# Adiciona o diretório raiz ao sistema para importar os módulos corretamente
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

from src.models.fluxo_gerador_receita.grafo import fluxo_resumo
from src.models.fluxo_gerador_receita.estado import EstadoReceita
from src.services.salvar_receita import buscar_receita_por_url
from src.services.salvar_receita import salvar_receita

from src.models.fluxo_gerador_receita.estado import Receita


# -------------------------
# CONFIGURAÇÃO DA PÁGINA
# -------------------------
st.set_page_config(
    page_title="Gerador de Receitas com IA",
    page_icon="🍳",
    layout="wide"
)

st.title("🍳 Gerador de Receitas do YouTube")
st.markdown("""
Transforme vídeos de culinária do YouTube em receitas estruturadas usando IA.  
Basta colar o link do vídeo abaixo!
""")


# -------------------------
# SESSION STATE
# -------------------------
if "receita" not in st.session_state:
    st.session_state.receita = None

if "receita_salva" not in st.session_state:
    st.session_state.receita_salva = False

if "video_url" not in st.session_state:
    st.session_state.video_url = None


# -------------------------
# INPUT
# -------------------------
url_video = st.text_input(
    "Cole a URL do vídeo do YouTube aqui:",
    placeholder="https://www.youtube.com/watch?v=..."
)


# -------------------------
# BOTÃO GERAR RECEITA
# -------------------------
if st.button("Gerar Receita", type="primary"):
    if not url_video:
        st.warning("Por favor, insira uma URL válida.")
    else:
        try:

            # 🔎 verifica no banco primeiro
            receita_existente = buscar_receita_por_url(url_video)

            if receita_existente:

                st.info("Receita já existe no banco. Carregando...")

                receita_existente.pop("_id", None)  # remove id do mongo
    
                receita = Receita(**receita_existente)

                st.session_state.receita = receita

            else:
                with st.spinner("Processando o vídeo... Isso pode levar alguns instantes."):

                    # 1. Inicializa o estado
                    estado_inicial = EstadoReceita(url_video=url_video)

                    # 2. Inicializa o grafo
                    grafo = fluxo_resumo()

                    # 3. Executa o fluxo
                    estado_final = grafo.invoke(estado_inicial)

                    # 4. Recupera a receita
                    receita = getattr(estado_final, "receita_gerada", None)

                    if receita is None and isinstance(estado_final, dict):
                        receita = estado_final.get("receita_gerada")

                # Salva no session_state
                st.session_state.receita = receita
                st.session_state.video_url = url_video
                st.session_state.receita_salva = False

        except Exception as e:
            st.error(f"Ocorreu um erro durante o processamento: {e}")


# ======================================================
# EXIBIÇÃO DA RECEITA (FORA DO BOTÃO!)
# ======================================================
if st.session_state.receita:

    receita = st.session_state.receita
    url_video = st.session_state.video_url

    st.success("Receita gerada com sucesso!", icon="✅")

    st.divider()

    # Cabeçalho
    st.header(receita.nome_receita)
    st.markdown(f"**{receita.descricao}**")

    # Metadados
    m_col1, m_col2 = st.columns(2)
    with m_col1:
        st.metric("Tempo de Preparo", receita.tempo_preparo)
    with m_col2:
        st.metric("Rendimento", receita.rendimento)

    st.divider()

    # Conteúdo principal
    col_ing, col_prep = st.columns([1, 1.5])

    # Ingredientes
    with col_ing:
        st.subheader("📝 Ingredientes")

        with st.container(border=True):
            for item in receita.ingredientes:
                st.write(f"**{item.quantidade}** {item.nome}")

        if receita.observacoes:
            st.info(f"💡 {receita.observacoes}")

    # Modo de preparo
    with col_prep:
        st.subheader("🍳 Modo de Preparo")

        for i, passo in enumerate(receita.modo_preparo):
            with st.expander(f"Passo {i+1}: {passo.passo}", expanded=True):
                st.markdown(passo.instrucoes)

    st.divider()

    # -------------------------
    # BOTÃO SALVAR RECEITA
    # -------------------------
    if st.button("💾 Salvar Receita", disabled=st.session_state.receita_salva):

        receita_dict = receita.model_dump()

        receita_dict["video_url"] = url_video
        receita_dict["created_at"] = datetime.utcnow()

        receita_id = salvar_receita(receita_dict)

        st.success(f"Receita salva com sucesso! ID: {receita_id}")

        st.session_state.receita_salva = True

    # -------------------------
    # VÍDEO ORIGINAL
    # -------------------------
    with st.expander("Ver Vídeo Original"):
        st.video(url_video)
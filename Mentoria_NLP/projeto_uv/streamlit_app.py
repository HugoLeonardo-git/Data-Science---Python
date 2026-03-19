import streamlit as st
import sys
import os
from datetime import datetime

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

from src.models.fluxo_gerador_receita.grafo import fluxo_resumo
from src.models.fluxo_gerador_receita.estado import EstadoReceita
from src.services.salvar_receita import buscar_receita_por_url, salvar_receita

# -------------------------
# CONFIGURAÇÃO
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
                st.session_state.receita = receita_existente

            else:
                with st.spinner("Processando o vídeo..."):

                    estado_inicial = EstadoReceita(url_video=url_video)
                    grafo = fluxo_resumo()
                    estado_final = grafo.invoke(estado_inicial)

                    receita = getattr(estado_final, "receita_gerada", None)

                    if receita is None and isinstance(estado_final, dict):
                        receita = estado_final.get("receita_gerada")

                    st.session_state.receita = receita
                    st.session_state.receita_salva = False

            st.session_state.video_url = url_video

        except Exception as e:
            st.error(f"Ocorreu um erro: {e}")

# ======================================================
# EXIBIÇÃO
# ======================================================
if st.session_state.receita:

    receita = st.session_state.receita
    url_video = st.session_state.video_url

    st.success("Receita pronta!", icon="✅")
    st.divider()

    st.header(receita.nome_receita)
    st.markdown(f"**{receita.descricao}**")

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Tempo de Preparo", receita.tempo_preparo)
    with col2:
        st.metric("Rendimento", receita.rendimento)

    st.divider()

    col_ing, col_prep = st.columns([1, 1.5])

    with col_ing:
        st.subheader("📝 Ingredientes")
        with st.container(border=True):
            for item in receita.ingredientes:
                st.write(f"**{item.quantidade}** {item.nome}")

        if receita.observacoes:
            st.info(receita.observacoes)

    with col_prep:
        st.subheader("🍳 Modo de Preparo")
        for i, passo in enumerate(receita.modo_preparo):
            with st.expander(f"Passo {i+1}: {passo.passo}", expanded=True):
                st.markdown(passo.instrucoes)

    st.divider()

    if st.button("💾 Salvar Receita", disabled=st.session_state.receita_salva):

        receita_dict = receita.model_dump()
        receita_dict["video_url"] = url_video
        receita_dict["created_at"] = datetime.utcnow()

        receita_id = salvar_receita(receita_dict)

        st.success(f"Receita salva! ID: {receita_id}")
        st.session_state.receita_salva = True

    with st.expander("Ver Vídeo Original"):
        st.video(url_video)
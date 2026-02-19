import streamlit as st
import sys
import os

# Adiciona o diretório raiz ao sistema para importar os módulos corretamente
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

from src.models.fluxo_gerador_receita.grafo import fluxo_resumo
from src.models.fluxo_gerador_receita.estado import EstadoReceita

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

url_video = st.text_input("Cole a URL do vídeo do YouTube aqui:", placeholder="https://www.youtube.com/watch?v=...")

if st.button("Gerar Receita", type="primary"):
    if not url_video:
        st.warning("Por favor, insira uma URL válida.")
    else:
        try:
            with st.spinner("Processando o vídeo... Isso pode levar alguns instantes."):
                # 1. Inicializa o estado
                estado_inicial = EstadoReceita(url_video=url_video)
                
                # 2. Inicializa o grafo
                grafo = fluxo_resumo()
                
                # 3. Executa o fluxo
                # invoke processa todo o grafo
                estado_final = grafo.invoke(estado_inicial)
                
                # 4. Recupera a receita
                # Verifica se é objeto ou dict
                receita = getattr(estado_final, "receita_gerada", None)
                if receita is None and isinstance(estado_final, dict):
                    receita = estado_final.get("receita_gerada")
                
                if receita:
                    st.success("Receita gerada com sucesso!", icon="✅")
                    
                    st.divider()

                    # Cabeçalho da Receita
                    st.header(receita.nome_receita)
                    st.markdown(f"**{receita.descricao}**")

                    # Metadados em colunas
                    m_col1, m_col2, m_col3 = st.columns(3)
                    with m_col1:
                        st.metric("Tempo de Preparo", receita.tempo_preparo)
                    with m_col2:
                         st.metric("Rendimento", receita.rendimento)
                    
                    st.divider()

                    # Conteúdo principal
                    col_ing, col_prep = st.columns([1, 1.5])
                    
                    with col_ing:
                        st.subheader("📝 Ingredientes")
                        # Usando container para dar destaque visual
                        with st.container(border=True):
                            for item in receita.ingredientes:
                                # Checkbox para ir marcando o que já separou
                                st.checkbox(f"**{item.quantidade}** {item.nome}")
                            
                        if receita.observacoes:
                            st.info(f"**💡 Observações:** {receita.observacoes}")
                            
                    with col_prep:
                        st.subheader("🍳 Modo de Preparo")
                        for i, passo in enumerate(receita.modo_preparo):
                            with st.expander(f"Passo {i+1}: {passo.passo}", expanded=True):
                                st.markdown(passo.instrucoes)
                        
                    st.divider()
                    
                    with st.expander("Ver Vídeo Original"):
                        st.video(url_video)
                        
                else:
                     st.error("Não foi possível gerar a estrutura da receita. Verifique o log ou tente outro vídeo.")
                     
        except Exception as e:
            st.error(f"Ocorreu um erro durante o processamento: {e}")
            # st.exception(e) # Descomentar para debug detalhado

"""Construtor do grafo para o LangGraph fluxo_resumo"""
 
from langgraph.graph import END, START, StateGraph
 
from .estado import EstadoReceita
from .nos import (
gerar_transcricao,
gerar_receita,
receber_video
)
 
def fluxo_resumo():
 
    # Cria o grafo com tipagem explícita do estado
    workflow = StateGraph(EstadoReceita)
    

    # Nó para geração de relatório inicial
    workflow.add_node("receber_video",receber_video)
    workflow.add_node("gerar_transcricao",gerar_transcricao)
    workflow.add_node("gerar_receita",gerar_receita)
 
    # Conecta os nós em sequência
    workflow.add_edge(START, "receber_video")
    workflow.add_edge("receber_video", "gerar_transcricao")
    workflow.add_edge("gerar_transcricao", "gerar_receita")
    workflow.add_edge("gerar_receita", END)
    # Compila e retorna o grafo
    return workflow.compile()
from typing import List, Optional
from pydantic import BaseModel, Field

# --- Models para Receita ---

class Ingrediente(BaseModel):
    nome: str = Field(..., description="Nome do ingrediente")
    quantidade: str = Field(..., description="Quantidade do ingrediente")

class PassoPreparo(BaseModel):
    passo: str = Field(..., description="Descrição resumida do passo")
    instrucoes: str = Field(..., alias="instruções", description="Instruções detalhadas do passo")

class Receita(BaseModel):
    nome_receita: str = Field(..., description="Nome da receita")
    descricao: str = Field(..., description="Breve descrição da receita")
    ingredientes: List[Ingrediente] = Field(..., description="Lista de ingredientes")
    modo_preparo: List[PassoPreparo] = Field(..., description="Lista de passos de preparo")
    tempo_preparo: str = Field(..., description="Tempo estimado de preparo")
    rendimento: str = Field(..., description="Rendimento da receita (ex: 4 porções)")
    observacoes: str = Field(..., description="Observações adicionais ou dicas")

# --- Models para Podcast ---

class Participante(BaseModel):
    nome: str = Field(..., description="Nome do participante")
    papel: str = Field(..., description="Papel do participante (ex: Host, Convidado)")
    descricao: str = Field(..., description="Breve descrição do participante")

class Topico(BaseModel):
    tema: str = Field(..., description="Tema do tópico discutido")
    descricao: str = Field(..., description="Descrição do que foi discutido sobre o tema")

class Referencia(BaseModel):
    descricao: str = Field(..., description="Descrição da referência citada")
    tipo: str = Field(..., description="Tipo da referência (pesquisa, dado, obra, outro)")

class Podcast(BaseModel):
    expertise_convidado: str = Field(..., description="Expertise do convidado")
    expertise_host: str = Field(..., description="Expertise do host")
    participantes: List[Participante] = Field(..., description="Lista de participantes")
    topicos_discutidos: List[Topico] = Field(..., description="Lista de tópicos discutidos")
    referencias_citadas: List[Referencia] = Field(..., description="Lista de referências citadas")
    momentos_chave: List[str] = Field(..., description="Lista de momentos chave ou insights importantes")
    resumo_geral: str = Field(..., description="Resumo geral do episódio")

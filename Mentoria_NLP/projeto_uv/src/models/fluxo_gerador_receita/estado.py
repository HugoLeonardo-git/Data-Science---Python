"""Definição do estado para o LangGraph."""
 
from typing import Dict, List, Optional
 
from typing import Annotated, Any
from pydantic import BaseModel, Field, BeforeValidator

def extract_text_from_dict(v: Any) -> str:
    """Extrai texto se o valor for um dicionário com chave 'texto' ou converte para string."""
    if isinstance(v, dict):
        return v.get("texto", str(v))
    return v

class Ingrediente(BaseModel):
    nome: str = Field(..., description="Nome do ingrediente")
    quantidade: str = Field(..., description="Quantidade do ingrediente")

class PassoPreparo(BaseModel):
    passo: str = Field(..., description="Descrição resumida do passo")
    instrucoes: Annotated[str, BeforeValidator(extract_text_from_dict)] = Field(..., description="Instruções detalhadas do passo")

class Receita(BaseModel):
    nome_receita: str = Field(..., description="Nome da receita")
    descricao: str = Field(..., description="Breve descrição da receita")
    ingredientes: List[Ingrediente] = Field(..., description="Lista de ingredientes")
    modo_preparo: List[PassoPreparo] = Field(..., description="Lista de passos de preparo")
    tempo_preparo: str = Field(..., description="Tempo estimado de preparo")
    rendimento: str = Field(..., description="Rendimento da receita (ex: 4 porções)")
    observacoes: str = Field(..., description="Observações adicionais ou dicas")
 
class EstadoReceita(BaseModel):
    """
    Representa os campos do dicionário das instruções,
    que está contido no dicionário do paragrafo (EstadoParagrafoSecao)
    da seção (EstadoSecaoResumo) do resumo do processo
 
    Garante os campos:
    - no_gerar_resumo: Prompt específico da seção para orientar o fluxo gerar resumo - string
    - no_transformar_resumo_html: Prompt específico da seção para orientar o fluxo transformar resumo em html - string
    """

    url_video: Optional[str] = Field(
        default=None,
        description="URL do video de receita no Youtube"
        )

    bytes_video: Optional[bytes] = Field(
        default=None,
        description="Bytes do video de receita"
        )
   
    transcricao:  Optional[str] = Field(
        default=None,
        description="Texto da transcrição do video de receita"
        )

    receita_gerada:  Optional[Receita] = Field(
        default=None,
        description="Receita gerada"
        )
 
 
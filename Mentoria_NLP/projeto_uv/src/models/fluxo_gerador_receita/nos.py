from .utils_prompt import render_prompt
from .estado import EstadoReceita, Receita
from groq import Groq
from dotenv import load_dotenv
from pathlib import Path
import os

from .youtube import baixar_audio_youtube
from .transcricao import transcrever_audio_local

# Caminho absoluto até a raiz do projeto
ROOT = Path(__file__).resolve().parents[3]

# Carrega .env
load_dotenv(ROOT / ".env")

import instructor
api_key = os.environ.get("GROQ_API_KEY")
client = instructor.from_groq(Groq(api_key=api_key), mode=instructor.Mode.JSON)


def receber_video(state: EstadoReceita) -> EstadoReceita:
    url = state.url_video
    if not url:
        raise ValueError("URL do vídeo não fornecido")

    audio_path = baixar_audio_youtube(url)

    with open(audio_path, "rb") as f:
        state.bytes_video = f.read()

    os.remove(audio_path)
    return state


def gerar_transcricao(state: EstadoReceita) -> EstadoReceita:
    audio_bytes = state.bytes_video
    if not audio_bytes:
        raise ValueError("Áudio não encontrado no estado")

    temp_path = "data/temp_audio.mp3"

    with open(temp_path, "wb") as f:
        f.write(audio_bytes)

    texto = transcrever_audio_local(temp_path)

    #os.remove(temp_path)

    state.transcricao = texto
    return state


def gerar_receita(estado: EstadoReceita) -> EstadoReceita:
    """
    Converte a transcrição em receita estruturada usando LLM + prompt Jinja.
    """
    transcricao = estado.transcricao
    if not transcricao:
        raise ValueError("Transcrição não encontrada no estado")
    
    # Truncate to avoid rate limits (approx 4k tokens)
    if len(transcricao) > 15000:
        transcricao = transcricao[:15000] + "... [texto truncado]"

    # Renderiza prompts
    prompt_sistema = render_prompt("sistema.jinja2")

    prompt_usuario = render_prompt(
        "usuario.jinja2",
        texto_transcricao=transcricao
    )

    # Chamada LLM
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        response_model=Receita,   # structured output automático
        temperature=0,            # Garante determinismo
        messages=[
            {"role": "system", "content": prompt_sistema},
            {"role": "user", "content": prompt_usuario},
        ],
    )

    estado.receita_gerada = response
    return estado
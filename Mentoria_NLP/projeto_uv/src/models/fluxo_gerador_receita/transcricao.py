import os
from ...utils.extrair_audio import transcrever_arquivo

def transcrever_audio_local(audio_path: str, modelo: str = "small") -> str:
    resultado = transcrever_arquivo(audio_path, modelo)
    return resultado["text"]

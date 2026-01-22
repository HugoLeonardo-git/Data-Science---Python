
import os
import sys
from pydub import AudioSegment

# Ajuste o caminho para o arquivo de podcast
# O script está na raiz do projeto (c:\Users\HugoLeonardo\Documents\GitHub\Data-Science---Python\Mentoria_NLP\projeto_uv)
# O áudio está em data/audio_podcast.mp3
AUDIO_PATH = "data/audio_podcast.mp3"
OUTPUT_DIR = "data/debug_chunks"

def dividir_audio_debug(audio_path, chunk_min=10):
    print(f"Iniciando divisão de: {audio_path}")
    if not os.path.exists(audio_path):
        print("Arquivo não encontrado!")
        return

    try:
        print("Carregando áudio com pydub (isso pode demorar e usar muita RAM)...")
        audio = AudioSegment.from_file(audio_path)
        print(f"Áudio carregado. Duração: {len(audio)/1000/60:.2f} minutos")
        
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        
        chunk_ms = chunk_min * 60 * 1000
        duracao_ms = len(audio)
        
        print(f"Gerando chunks de {chunk_min} minutos...")
        count = 0
        for i in range(0, duracao_ms, chunk_ms):
            chunk = audio[i:i + chunk_ms]
            nome_chunk = f"chunk_{count:03d}.mp3"
            caminho = os.path.join(OUTPUT_DIR, nome_chunk)
            print(f"Exportando {nome_chunk}...")
            chunk.export(caminho, format="mp3")
            count += 1
            
        print(f"Sucesso! {count} chunks gerados em {OUTPUT_DIR}")
        
    except Exception as e:
        print(f"ERRO CRÍTICO durante a divisão: {e}")

if __name__ == "__main__":
    dividir_audio_debug(AUDIO_PATH)

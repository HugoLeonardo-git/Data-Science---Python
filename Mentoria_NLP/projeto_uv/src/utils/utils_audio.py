
import subprocess
import glob
import os
import time
import re
from groq import RateLimitError

def dividir_audio_ffmpeg(audio_path, chunk_min=10, output_dir="chunks_audio"):
    """
    Divide o áudio em chunks usando FFMPEG diretamente (via subprocess).
    Isso é muito mais rápido e eficiente que usar Pydub para arquivos grandes,
    pois não carrega o áudio inteiro na RAM decodificado.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Limpar chunks antigos para evitar misturas
    for f in glob.glob(os.path.join(output_dir, "chunk_*.mp3")):
        try:
            os.remove(f)
        except:
            pass

    # Converter chunk_min para segundos
    segment_time = chunk_min * 60
    
    # Padrão de nome dos arquivos de saída
    output_pattern = os.path.join(output_dir, "chunk_%03d.mp3")
    
    print(f"🔪 Dividindo áudio em chunks de {chunk_min} minutos usando FFMPEG...")
    
    # Comando ffmpeg:
    # -i: entrada
    # -f segment: formato de segmentação
    # -segment_time: tempo de cada segmento
    # -c copy: copia o stream sem re-codificar (MUITO RÁPIDO)
    # -reset_timestamps 1: reseta o tempo de cada chunk para começar em 0
    cmd = [
        "ffmpeg",
        "-i", audio_path,
        "-f", "segment",
        "-segment_time", str(segment_time),
        "-c:a", "libmp3lame",  # Re-codificar para MP3 (garante compatibilidade se a fonte não for MP3 nativo) 
        "-reset_timestamps", "1",
        "-y", # Sobrescrever sem perguntar
        output_pattern
    ]
    
    try:
        # Executar comando ocultando output excessivo mas capturando erro
        subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Listar arquivos criados e ordenar
        chunks = sorted(glob.glob(os.path.join(output_dir, "chunk_*.mp3")))
        print(f"✅ Sucesso! {len(chunks)} chunks criados em '{output_dir}'.")
        return chunks
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao executar FFMPEG: {e}")
        # Tentar imprimir o erro capturado
        if e.stderr:
            print(f"Detalhes: {e.stderr.decode('utf-8')}")
        return []
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        return []

def transcrever_com_retry(client, audio_path, model="whisper-large-v3-turbo", language="pt"):
    """
    Transcreve um arquivo de áudio usando a API Groq com tratamento automático de Rate Limit (HTTP 429).
    """
    while True:
        try:
            with open(audio_path, "rb") as file:
                # Chama a API
                transcription = client.audio.transcriptions.create(
                    file=(os.path.basename(audio_path), file),
                    model=model,
                    response_format="text",
                    language=language
                )
            return transcription
            
        except RateLimitError as e:
            erro_msg = str(e)
            print(f"⚠️ Rate Limit atingido para '{os.path.basename(audio_path)}'.")
            
            # Lógica para extrair o tempo de espera da mensagem de erro
            # Ex: "Please try again in 4m56.5s"
            wait_time = 60 # Tempo padrão de espera
            
            # Tentar encontrar minutos e segundos
            match_min = re.search(r"(\d+)m", erro_msg)
            match_sec = re.search(r"(\d+\.?\d*)s", erro_msg)
            
            mduration = 0
            sduration = 0
            
            if match_min:
                mduration = int(match_min.group(1))
            if match_sec:
                sduration = float(match_sec.group(1))
                
            if mduration > 0 or sduration > 0:
                wait_time = (mduration * 60) + sduration + 5 # Adiciona 5s de segurança
            
            print(f"⏳ Aguardando {wait_time:.1f} segundos para liberar cota da API...")
            time.sleep(wait_time)
            print("🔄 Retomando transcrição...")
            
        except Exception as e:
            print(f"❌ Erro inesperado ao transcrever {audio_path}: {e}")
            raise e

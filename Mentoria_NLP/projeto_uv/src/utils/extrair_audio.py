import os
import yt_dlp
import whisper
from pydub import AudioSegment
from tqdm import tqdm
import tempfile
import time

def baixar_audio_youtube(url: str, output_path: str = "data/audio_temp.mp3", quiet: bool = True) -> str:
    """
    Baixa o áudio de um vídeo do YouTube.
    """
    print("[..] Baixando áudio com yt-dlp...")
    # Garantir que o diretório existe
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': output_path,
        'quiet': quiet,
        'no_warnings': True,
        'noplaylist': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    print(f"[OK] Áudio baixado em: {output_path}")
    return output_path

def transcrever_arquivo(audio_path: str, modelo: str = "small") -> dict:
    """
    Transcreve um arquivo de áudio local usando Whisper.
    Retorna um dicionário com o texto e métricas de tempo.

    Parâmetros:
        audio_path (str): caminho do arquivo de áudio
        modelo (str): modelo Whisper ('tiny', 'base', 'small', 'medium', 'large')
    
    Retorna:
        dict: dicionário com o texto transcrevido e métricas de tempo
        
    """
    # Passo 2: Carregar modelo Whisper
    print(f"[..] Carregando modelo Whisper ({modelo})...")
    start_load = time.time()
    model = whisper.load_model(modelo)
    load_time = time.time() - start_load

    # Passo 3: Transcrever áudio
    print("[..] Transcrevendo áudio...")
    start_transcribe = time.time()
    result = model.transcribe(audio_path, language="pt")
    transcribe_time = time.time() - start_transcribe
    
    texto = result["text"]
    print("[OK] Transcrição concluída.")
    
    return {
        "text": texto,
        "load_time": load_time,
        "transcribe_time": transcribe_time
    }

def transcrever_youtube_yt_dlp(url:str, modelo:str="small", nome_arquivo:str="transcricao_youtube.txt") -> str:
    """
    Faz download do áudio de um vídeo do YouTube e transcreve com Whisper.
    
    Parâmetros:
        url (str): URL do vídeo no YouTube
        modelo (str): modelo Whisper ('tiny', 'base', 'small', 'medium', 'large')
        nome_arquivo (str): nome do arquivo de saída da transcrição

    Retorna:
        str: texto transcrevido
    """
    audio_path = "data/audio_temp.mp3"
    
    try:
        baixar_audio_youtube(url, audio_path)
        
        resultado = transcrever_arquivo(audio_path, modelo)
        texto = resultado["text"]

        # Passo 4: Salvar transcrição
        with open(nome_arquivo, "w", encoding="utf-8") as f:
            f.write(texto)
        print(f"[OK] Transcrição salva em: {nome_arquivo}")

    finally:
        # Remover arquivo temporário
        if os.path.exists(audio_path):
            os.remove(audio_path)

    return texto



def transcrever_youtube_yt_dlp_quebrado(url, modelo="small", chunk_min=30, nome_arquivo="transcricao.txt"):
    """
    Faz download do áudio de um vídeo do YouTube e transcreve com Whisper.
    
    Parâmetros:
        url (str): URL do vídeo no YouTube
        modelo (str): modelo Whisper ('tiny', 'base', 'small', 'medium', 'large')
        chunk_min (int): duração máxima de cada chunk em minutos
        nome_arquivo (str): nome do arquivo de saída da transcrição
    """
    
    # === Passo 1: Criar pasta temporária ===
    temp_dir = tempfile.mkdtemp()
    audio_path = os.path.join(temp_dir, "audio_temp.mp3")
    audio_path = os.path.join('docs/', "audio_temp.mp3")

    print("[..] Baixando áudio com yt-dlp...")
    ydl_opts = {
        'format': 'bestaudio[ext=m4a]/bestaudio/best',
        'outtmpl': audio_path,
        'quiet': False,
        'noplaylist': True,
        'retries': 20,
        'fragment_retries': 20,
        'timeout': 120,
        'continuedl': True,
        'http_chunk_size': 10 * 1024 * 1024,  # 10 MB por fragmento
        'retry_sleep_functions': {'http': lambda n: 5 + n * 2},
    }

    # === Passo 2: Download do áudio ===
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        start_time = time.time()
        try:
            ydl.download([url])
        except Exception as e:
            print(f"[ERRO] Erro ao baixar o áudio: {e}")
            return None
        print(f"[OK] Áudio baixado em {audio_path} ({time.time()-start_time:.1f}s)")

    # === Passo 3: Carregar modelo Whisper ===
    print(f"[..] Carregando modelo Whisper ({modelo})...")
    model = whisper.load_model(modelo)

    # === Passo 4: Dividir áudio em blocos ===
    print("[..] Dividindo áudio em partes menores...")
    audio = AudioSegment.from_file(audio_path)
    duracao_total = len(audio)
    chunk_ms = chunk_min * 60 * 1000
    partes = [(i, audio[i:i+chunk_ms]) for i in range(0, duracao_total, chunk_ms)]
    print(f"[..] Total de partes: {len(partes)} ({chunk_min} min cada aprox.)")

    # === Passo 5: Transcrever cada bloco ===
    transcricao_final = ""
    for idx, (_, chunk) in enumerate(tqdm(partes, desc="Transcrevendo partes", unit="parte")):
        chunk_path = os.path.join(temp_dir, f"parte_{idx+1}.mp3")
        chunk.export(chunk_path, format="mp3")
        try:
            result = model.transcribe(chunk_path, language="pt")
            transcricao_final += result["text"].strip() + "\n"
        except Exception as e:
            print(f"[AVISO] Erro ao transcrever parte {idx+1}: {e}")
            continue

    # === Passo 6: Salvar resultado ===
    with open(nome_arquivo, "w", encoding="utf-8") as f:
        f.write(transcricao_final.strip())

    print(f"[OK] Transcrição completa! Salva em '{nome_arquivo}'")
    print(f"[Tempo] Tempo total: {time.time() - start_time:.1f}s")

    return transcricao_final

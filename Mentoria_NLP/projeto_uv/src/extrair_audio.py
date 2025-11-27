def transcrever_youtube_yt_dlp(url, modelo="small", nome_arquivo="transcricao_youtube.txt"):
    # Passo 1: Baixar áudio com yt-dlp
    print("⏳ Baixando áudio com yt-dlp...")
    audio_path = "data/audio_temp.mp3"
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': audio_path,
        'quiet': True,
        'no_warnings': True,
        'noplaylist': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    print(f"✅ Áudio baixado em: {audio_path}")

    # Passo 2: Carregar modelo Whisper
    print(f"⏳ Carregando modelo Whisper ({modelo})...")
    model = whisper.load_model(modelo)

    # Passo 3: Transcrever áudio
    print("⏳ Transcrevendo áudio...")
    result = model.transcribe(audio_path, language="pt")
    texto = result["text"]
    print("✅ Transcrição concluída.")

    # Passo 4: Salvar transcrição
    with open(nome_arquivo, "w", encoding="utf-8") as f:
        f.write(texto)
    print(f"✅ Transcrição salva em: {nome_arquivo}")

    # Remover arquivo temporário
    os.remove(audio_path)

    return texto

import os
import yt_dlp
import whisper
from pydub import AudioSegment
from tqdm import tqdm
import tempfile
import time

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

    print("🎧 Baixando áudio com yt-dlp...")
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
            print(f"❌ Erro ao baixar o áudio: {e}")
            return None
        print(f"✅ Áudio baixado em {audio_path} ({time.time()-start_time:.1f}s)")

    # === Passo 3: Carregar modelo Whisper ===
    print(f"🧠 Carregando modelo Whisper ({modelo})...")
    model = whisper.load_model(modelo)

    # === Passo 4: Dividir áudio em blocos ===
    print("🔪 Dividindo áudio em partes menores...")
    audio = AudioSegment.from_file(audio_path)
    duracao_total = len(audio)
    chunk_ms = chunk_min * 60 * 1000
    partes = [(i, audio[i:i+chunk_ms]) for i in range(0, duracao_total, chunk_ms)]
    print(f"📦 Total de partes: {len(partes)} ({chunk_min} min cada aprox.)")

    # === Passo 5: Transcrever cada bloco ===
    transcricao_final = ""
    for idx, (_, chunk) in enumerate(tqdm(partes, desc="Transcrevendo partes", unit="parte")):
        chunk_path = os.path.join(temp_dir, f"parte_{idx+1}.mp3")
        chunk.export(chunk_path, format="mp3")
        try:
            result = model.transcribe(chunk_path, language="pt")
            transcricao_final += result["text"].strip() + "\n"
        except Exception as e:
            print(f"⚠️ Erro ao transcrever parte {idx+1}: {e}")
            continue

    # === Passo 6: Salvar resultado ===
    with open(nome_arquivo, "w", encoding="utf-8") as f:
        f.write(transcricao_final.strip())

    print(f"✅ Transcrição completa! Salva em '{nome_arquivo}'")
    print(f"🕒 Tempo total: {time.time() - start_time:.1f}s")

    return transcricao_final

import os
import yt_dlp


def baixar_audio_youtube(url: str, output_path: str = "data/audio_temp.mp3") -> str:
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": output_path,
        "quiet": True,
        "no_warnings": True,
        "noplaylist": True,
        "socket_timeout": 30,
        "retries": 10,
        "force_ipv4": True,  # Fix for some connection issues
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    return output_path

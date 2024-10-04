import os
import time
import threading
from datetime import datetime, timedelta
from dotenv import load_dotenv
from instagrapi import Client

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()
USERNAME = os.getenv('LOGIN')
PASSWORD = os.getenv('SENHA')

LEGENDA_FIXA = """Painel para iniciantes do 7️⃣ na bio! 🐀
.
.
.
.
#marketingdigital #marketingdigitalbrasil
#dropshipping #dropshippingbrasil #dropshippingnacional #ecommerce
#negociosonline #trafegopago
#empreendedorismodigital #rendaextra
#rendaextraemcasa #dinheiro
#dinheiroextra #dinheiroonline #shopify"""

def selecionar_pasta_videos():
    pasta = input("Digite o caminho da pasta com os vídeos: ")
    if os.path.exists(pasta):
        return pasta
    else:
        print("A pasta selecionada não existe.")
        return selecionar_pasta_videos()

def obter_horarios():
    horarios = []
    print("Selecione os horários de postagem (formatar como HH:MM). Digite 'fim' para terminar:")
    while True:
        horario = input("Horário (ou 'fim' para concluir): ")
        if horario.lower() == 'fim':
            break
        if len(horario) == 5 and horario[2] == ':' and horario[:2].isdigit() and horario[3:].isdigit():
            horarios.append(horario)
        else:
            print("Formato inválido. Por favor, use HH:MM.")
    return horarios

def postar_videos_thread(pasta_videos, horarios_selecionados):
    try:
        client = Client()
        client.login(USERNAME, PASSWORD)

        videos = [f for f in os.listdir(pasta_videos) if f.endswith('.mp4')]

        if not videos:
            raise FileNotFoundError("Nenhum vídeo encontrado na pasta selecionada.")

        if not horarios_selecionados:
            raise ValueError("Nenhum horário selecionado.")

        for i, video in enumerate(videos):
            if i >= len(horarios_selecionados):
                break

            horario_postagem = horarios_selecionados[i]
            horario_obj = datetime.strptime(horario_postagem, "%H:%M")
            agora = datetime.now()
            proxima_postagem = agora.replace(hour=horario_obj.hour, minute=horario_obj.minute, second=0, microsecond=0)

            if proxima_postagem < agora:
                proxima_postagem += timedelta(days=1)

            tempo_espera = (proxima_postagem - agora).total_seconds()
            print(f"Aguardando até {horario_postagem} para postar o vídeo {video}...")
            time.sleep(tempo_espera)

            video_path = os.path.join(pasta_videos, video)
            client.video_upload(video_path, caption=LEGENDA_FIXA)
            print(f"Vídeo {video} postado com sucesso!")

        print("Todos os vídeos foram postados com sucesso!")
    except Exception as e:
        print(f"Erro: {str(e)}")

def postar_videos():
    pasta_videos = selecionar_pasta_videos()
    horarios_selecionados = obter_horarios()
    # Inicia o processo de postagem em um thread separado
    threading.Thread(target=postar_videos_thread, args=(pasta_videos, horarios_selecionados)).start()

if __name__ == "__main__":
    postar_videos()

import tkinter as tk
from tkinter import filedialog, messagebox
from instagrapi import Client
import os
import time
import threading
from datetime import datetime, timedelta
from dotenv import load_dotenv

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
    pasta = filedialog.askdirectory(title="Selecione a Pasta com os Vídeos")
    if pasta:
        entry_pasta_videos.delete(0, tk.END)
        entry_pasta_videos.insert(0, pasta)

def postar_videos_thread():
    try:
        client = Client()
        client.login(USERNAME, PASSWORD)

        pasta_videos = entry_pasta_videos.get()
        
        # Obtém os horários selecionados
        horarios_selecionados = [horario for horario, var in checkboxes.items() if var.get() == 1]

        # Verifica se a pasta de vídeos existe
        if not os.path.exists(pasta_videos):
            raise FileNotFoundError("A pasta selecionada não existe.")

        videos = [f for f in os.listdir(pasta_videos) if f.endswith('.mp4')]

        if not videos:
            raise FileNotFoundError("Nenhum vídeo encontrado na pasta selecionada.")

        if not horarios_selecionados:
            raise ValueError("Nenhum horário selecionado.")

        for i, video in enumerate(videos):
            # Verifica se há um horário correspondente para o vídeo
            if i >= len(horarios_selecionados):
                break

            horario_postagem = horarios_selecionados[i]

            # Converte o horário para um objeto datetime
            horario_obj = datetime.strptime(horario_postagem, "%H:%M")

            # Obtém o horário atual
            agora = datetime.now()

            # Ajusta a data do horário de postagem para hoje ou amanhã, se já passou
            proxima_postagem = agora.replace(hour=horario_obj.hour, minute=horario_obj.minute, second=0, microsecond=0)
            if proxima_postagem < agora:
                proxima_postagem += timedelta(days=1)

            # Calcula o tempo até a próxima postagem
            tempo_espera = (proxima_postagem - agora).total_seconds()

            # Espera até o horário de postagem
            log.insert(tk.END, f"Aguardando até {horario_postagem} para postar o vídeo {video}...")
            log.yview(tk.END)
            time.sleep(tempo_espera)

            video_path = os.path.join(pasta_videos, video)
            client.video_upload(video_path, caption=LEGENDA_FIXA)
            log.insert(tk.END, f"Vídeo {video} postado com sucesso!")
            log.yview(tk.END)

        messagebox.showinfo("Sucesso", "Todos os vídeos foram postados com sucesso!")
    except Exception as e:
        messagebox.showerror("Erro", str(e))
        log.insert(tk.END, f"Erro: {str(e)}")
        log.yview(tk.END)

def postar_videos():
    # Inicia o processo de postagem em um thread separado
    threading.Thread(target=postar_videos_thread).start()

# Configuração da interface gráfica
root = tk.Tk()
root.title("Postar Vídeos no Instagram")
root.geometry("700x800")
root.configure(bg='#3a3a3a')

# Estilos
fonte_padrao = ("Helvetica", 12)
fonte_titulo = ("Helvetica", 16, "bold")
cor_fundo = '#3a3a3a'
cor_fonte = '#ffffff'
cor_botao = '#00bfa5'
cor_botao_claro = '#4caf50'

# Título
titulo = tk.Label(root, text="Postar Vídeos no Instagram", font=fonte_titulo, bg=cor_fundo, fg=cor_fonte)
titulo.pack(pady=20)

# Campo para selecionar a pasta de vídeos
frame_pasta_videos = tk.Frame(root, bg=cor_fundo)
frame_pasta_videos.pack(pady=10)
tk.Label(frame_pasta_videos, text="Pasta com Vídeos:", bg=cor_fundo, fg=cor_fonte, font=fonte_padrao).pack(side=tk.LEFT)
entry_pasta_videos = tk.Entry(frame_pasta_videos, width=40, font=fonte_padrao)
entry_pasta_videos.pack(side=tk.LEFT, padx=10)
tk.Button(frame_pasta_videos, text="Selecionar Pasta", command=selecionar_pasta_videos, bg=cor_botao_claro, fg=cor_fonte, font=fonte_padrao).pack(side=tk.LEFT)

# Frame para os horários de postagem
frame_horarios = tk.Frame(root, bg=cor_fundo)
frame_horarios.pack(pady=20)

tk.Label(frame_horarios, text="Selecione os horários de postagem:", bg=cor_fundo, fg=cor_fonte, font=fonte_padrao).pack()

# Criar checkboxes para os horários de 00:00 até 23:00, organizando-os em colunas
checkboxes = {}
horarios_frame = tk.Frame(frame_horarios, bg=cor_fundo)
horarios_frame.pack(pady=10)

for coluna in range(4):
    coluna_frame = tk.Frame(horarios_frame, bg=cor_fundo)
    coluna_frame.pack(side=tk.LEFT, padx=10)

    for hora in range(coluna * 6, (coluna + 1) * 6):
        horario_str = f"{hora:02d}:00"
        var = tk.IntVar()
        checkbox = tk.Checkbutton(coluna_frame, text=horario_str, variable=var, bg=cor_fundo, fg=cor_fonte, font=fonte_padrao, selectcolor=cor_fundo, activebackground=cor_fundo)
        checkboxes[horario_str] = var
        checkbox.pack(anchor='w')

# Botão para postar vídeos
botao_postar = tk.Button(root, text="Postar Vídeos", command=postar_videos, bg=cor_botao, fg=cor_fonte, font=fonte_padrao, width=20)
botao_postar.pack(pady=20)

# Log
log_frame = tk.Frame(root, bg=cor_fundo)
log_frame.pack(pady=20)
tk.Label(log_frame, text="Log de Atividades:", bg=cor_fundo, fg=cor_fonte, font=fonte_padrao).pack()
log = tk.Listbox(log_frame, width=80, height=15, bg='#2e2e2e', fg=cor_fonte, font=fonte_padrao)
log.pack(pady=10)

# Rodapé com o texto "CRIADO POR: @japablackhat"
rodape = tk.Label(root, text="CRIADO POR: @japablackhat", font=("Helvetica", 10), bg=cor_fundo, fg=cor_fonte)
rodape.pack(pady=10)

# Iniciar a interface gráfica
root.mainloop()

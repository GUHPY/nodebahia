import os
import queue
import threading
from datetime import datetime
from flask import Flask, render_template, request, jsonify, Response

# Helper para ler o arquivo
def ler_arquivo(caminho):
    if not os.path.exists(caminho):
        return ""
    with open(caminho, 'r', encoding='utf-8') as f:
        return f.read()

# Helper para escrever no arquivo
def escrever_arquivo(caminho, conteudo):
    with open(caminho, 'w', encoding='utf-8') as f:
        f.write(conteudo)

app = Flask(__name__)

# Fila global para enviar eventos de progresso para o cliente conectado
download_progress_queue = queue.Queue()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/visuals')
def visuals():
    return render_template('visuals.html')

# --- API Links ---
@app.route('/api/links', methods=['GET', 'POST'])
def handle_links():
    if request.method == 'POST':
        data = request.json
        links_content = data.get('content', '')
        escrever_arquivo('links.txt', links_content)
        return jsonify({"status": "success"})
    return jsonify({"content": ler_arquivo('links.txt')})

# --- API Cookies ---
@app.route('/api/cookies', methods=['GET', 'POST'])
def handle_cookies():
    cookie_path = 'cookies/instagram_cookie.txt'
    if request.method == 'POST':
        data = request.json
        cookie_content = data.get('content', '')
        os.makedirs('cookies', exist_ok=True)
        escrever_arquivo(cookie_path, cookie_content)
        return jsonify({"status": "success"})
    return jsonify({"content": ler_arquivo(cookie_path)})

# --- SSE: Progress Streaming ---
@app.route('/stream')
def stream():
    def event_stream():
        # Envia um "olá" inicial
        yield "data: {\"status\": \"connected\"}\n\n"
        while True:
            # Aguarda eventos na fila
            item = download_progress_queue.get()
            if item == "DONE":
                yield "data: {\"status\": \"done\"}\n\n"
                break
            # Envia o JSON do progresso
            import json
            yield f"data: {json.dumps(item)}\n\n"
            
    return Response(event_stream(), content_type='text/event-stream')

# --- API Start Download ---
@app.route('/api/download', methods=['POST'])
def start_download():
    # Isso vai iniciar o processamento em uma thread separada para não travar o servidor
    thread = threading.Thread(target=processar_downloads)
    thread.start()
    return jsonify({"status": "started"})

def processar_downloads():
    from core.downloader import baixar_video, baixar_video_instagram
    from utils.helpers import pausa_randomica
    import time
    
    # 1. Cria uma pasta batch com data/hora
    # Ex: Batch_2023-10-31_14-30-00
    batch_name = "Batch_" + datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    batch_path = os.path.join('downloads', batch_name)
    os.makedirs(batch_path, exist_ok=True)
    
    # Notifica o cliente que começamos
    download_progress_queue.put({"status": "info", "message": f"Iniciando Lote: {batch_name}"})
    
    # 2. Lê os links
    links_brutos = ler_arquivo('links.txt')
    links = [linha.strip() for linha in links_brutos.split('\n') if linha.strip()]
    
    if not links:
        download_progress_queue.put({"status": "error", "message": "Nenhum link encontrado."})
        download_progress_queue.put("DONE")
        return
        
    total_links = len(links)
    
    # Inicia o Loop
    for index, url in enumerate(links, start=1):
        # Avisa a UI de qual vídeo estamos baixando
        download_progress_queue.put({"status": "progress", "video_index": index, "total": total_links, "message": f"Baixando vídeo {index} de {total_links}..."})
        
        try:
            if "tiktok.com" in url:
                baixar_video(url, batch_path, download_progress_queue)
            elif "instagram.com" in url:
                baixar_video_instagram(url, batch_path, download_progress_queue)
            else:
                download_progress_queue.put({"status": "warning", "message": f"Plataforma não suportada: {url}"})
        except Exception as e:
            download_progress_queue.put({"status": "error", "message": f"Erro no link {url}: {str(e)}"})
            
        if index < total_links:
            time.sleep(2) # Pausa leve entre downloads

    # Notifica fim do processo
    download_progress_queue.put({"status": "success", "message": "Lote finalizado com sucesso!", "batch": batch_name})
    download_progress_queue.put("DONE")

if __name__ == '__main__':
    # Cria diretórios padrões se não existirem
    os.makedirs('downloads', exist_ok=True)
    os.makedirs('cookies', exist_ok=True)
    if not os.path.exists('links.txt'):
        escrever_arquivo('links.txt', '')
        
    app.run(debug=True, port=5000)

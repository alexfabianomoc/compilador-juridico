import os

# Determina o diretório base automaticamente baseado na localização do arquivo config.py
# Isso permite que o sistema seja executado de qualquer local sem modificações
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Caminho do diretório de cache
CACHE_DIR = os.path.join(BASE_DIR, "assets", "cache")

# Assegura que o diretório cache existe
os.makedirs(CACHE_DIR, exist_ok=True)

# Arquivos de listas
LISTA_TJ_FILE = os.path.join(CACHE_DIR, "lista_processos_tj.json")
LISTA_TRF_FILE = os.path.join(CACHE_DIR, "lista_processos_trf.json")

# Arquivos de resultados
RESULTADO_TJ_FILE = os.path.join(CACHE_DIR, "resultados_processos_tj.json")
RESULTADO_TRF_FILE = os.path.join(CACHE_DIR, "resultados_processos_trf.json")

# Configurações de API
API_KEY = "ApiKey cDZHYzlZa0JadVREZDJCendQbXY6SkJlTzNjLV9TRENyQk1RdnFKZGRQdw=="
API_TJMG_URL = "https://api-publica.datajud.cnj.jus.br/api_publica_tjmg/_search"
API_TRF6_URL = "https://api-publica.datajud.cnj.jus.br/api_publica_trf6/_search"

# Pausa entre consultas à API (em segundos)
API_DELAY = 0.5

# Função para inicializar os arquivos JSON se eles não existirem
def inicializar_arquivos_json():
    """Cria arquivos JSON vazios se não existirem"""
    arquivos = [LISTA_TJ_FILE, LISTA_TRF_FILE, RESULTADO_TJ_FILE, RESULTADO_TRF_FILE]
    for arquivo in arquivos:
        if not os.path.exists(arquivo):
            with open(arquivo, 'w', encoding='utf-8') as f:
                if arquivo.startswith(LISTA_TJ_FILE) or arquivo.startswith(LISTA_TRF_FILE):
                    # Listas são arrays vazios
                    f.write('[]')
                else:
                    # Resultados são objetos vazios
                    f.write('{}')
            print(f"Arquivo {os.path.basename(arquivo)} criado.")

# Inicializa os arquivos JSON na primeira execução
inicializar_arquivos_json()
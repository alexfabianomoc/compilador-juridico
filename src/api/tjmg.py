import requests
import json
import time
from ..config import API_TJMG_URL, API_KEY, API_DELAY, LISTA_TJ_FILE, RESULTADO_TJ_FILE
from ..utils.file_handler import carregar_arquivo_json, salvar_arquivo_json

def consultar_processo_tjmg(numero_processo):
    """
    Consulta um único processo no TJMG e atualiza o arquivo de resultados.
    
    Args:
        numero_processo: Número do processo a ser consultado
        
    Returns:
        dict: Resultado da consulta
    """
    headers = {
        'Authorization': API_KEY,
        'Content-Type': 'application/json'
    }
    
    payload = json.dumps({
        "query": {
            "match": {
                "numeroProcesso": numero_processo
            }
        }
    })
    
    try:
        # Fazer a requisição à API
        response = requests.request("POST", API_TJMG_URL, headers=headers, data=payload)
        
        # Preparar o resultado da consulta
        if response.status_code == 200:
            resultado = response.json()
        else:
            resultado = {"erro": f"Código de status: {response.status_code}", "mensagem": response.text}
        
        # Carregar o dicionário atual de resultados
        resultados = carregar_arquivo_json(RESULTADO_TJ_FILE)
        if not resultados:
            resultados = {}
        
        # Atualizar o dicionário com o novo resultado
        resultados[numero_processo] = resultado
        
        # Salvar o dicionário atualizado
        salvar_arquivo_json(RESULTADO_TJ_FILE, resultados)
        print(f"Resultado do processo {numero_processo} atualizado no arquivo {RESULTADO_TJ_FILE}")
        
        return resultado
        
    except Exception as e:
        erro = {"erro": str(e)}
        
        # Mesmo em caso de erro, atualizar o arquivo com a informação do erro
        resultados = carregar_arquivo_json(RESULTADO_TJ_FILE)
        if not resultados:
            resultados = {}
            
        resultados[numero_processo] = erro
        salvar_arquivo_json(RESULTADO_TJ_FILE, resultados)
        
        print(f"Erro ao consultar o processo {numero_processo}: {str(e)}")
        return erro

def consultar_todos_processos_tjmg():
    """
    Consulta todos os processos do TJ na lista e retorna um dicionário com os resultados.
    Garante que o arquivo de resultados seja atualizado com todos os processos da lista.
    """
    # Carregar a lista de processos TJ
    lista_processos = carregar_arquivo_json(LISTA_TJ_FILE)
    
    if not lista_processos:
        print(f"Nenhum processo encontrado na lista {LISTA_TJ_FILE}.")
        return {}
    
    print(f"Lista de processos TJ carregada: {len(lista_processos)} processos encontrados.")
    
    # Dicionário para armazenar os resultados da execução atual
    resultados = {}
    
    # Carregar resultados existentes para atualização do arquivo
    arquivo_resultados = carregar_arquivo_json(RESULTADO_TJ_FILE)
    if not arquivo_resultados:
        arquivo_resultados = {}
    
    total = len(lista_processos)
    consultas_feitas = 0
    erros = 0
    
    for i, numero in enumerate(lista_processos, 1):
        try:
            print(f"Consultando processo {i}/{total}: {numero}")
            
            # Fazer a consulta do processo
            headers = {
                'Authorization': API_KEY,
                'Content-Type': 'application/json'
            }
            
            payload = json.dumps({
                "query": {
                    "match": {
                        "numeroProcesso": numero
                    }
                }
            })
            
            # Fazer a requisição à API
            response = requests.request("POST", API_TJMG_URL, headers=headers, data=payload)
            
            # Processar o resultado
            if response.status_code == 200:
                resultado = response.json()
                resultados[numero] = resultado
                consultas_feitas += 1
            else:
                erro = {"erro": f"Código de status: {response.status_code}", "mensagem": response.text}
                resultados[numero] = erro
                erros += 1
                print(f"Erro ao consultar o processo {numero}: Código {response.status_code}")
            
            # Aguardar entre as requisições para evitar sobrecarga na API
            time.sleep(API_DELAY)
            
        except Exception as e:
            # Capturar qualquer erro durante a consulta
            erro = {"erro": str(e)}
            resultados[numero] = erro
            erros += 1
            print(f"Exceção ao consultar o processo {numero}: {str(e)}")
            time.sleep(API_DELAY)  # Mesmo com erro, aguardar antes da próxima requisição
    
    # Atualizar o arquivo de resultados
    try:
        # Atualizar o arquivo com os novos resultados
        for numero, resultado in resultados.items():
            arquivo_resultados[numero] = resultado
            
        # Salvar o arquivo atualizado
        salvar_arquivo_json(RESULTADO_TJ_FILE, arquivo_resultados)
        print(f"Arquivo de resultados {RESULTADO_TJ_FILE} atualizado com sucesso.")
        print(f"Consultas realizadas: {consultas_feitas}, Erros: {erros}")
    except Exception as e:
        print(f"Erro ao salvar o arquivo de resultados: {str(e)}")
    
    # Retorna apenas os resultados das consultas realizadas nesta execução
    return resultados
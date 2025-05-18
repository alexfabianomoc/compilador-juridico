import os
from src.config import LISTA_TJ_FILE, LISTA_TRF_FILE, RESULTADO_TJ_FILE, RESULTADO_TRF_FILE
from src.utils.file_handler import carregar_arquivo_json, salvar_arquivo_json
from src.models.processo import Processo

def excluir_processo(numero_processo, tipo, excluir_resultados=True):
    """
    Exclui um processo da lista correspondente e opcionalmente do arquivo de resultados.
    
    Args:
        numero_processo (str): Número do processo a ser excluído
        tipo (str): Tipo do processo ('TJ' ou 'TRF')
        excluir_resultados (bool): Se True, também remove os resultados do processo
        
    Returns:
        bool: True se o processo foi excluído com sucesso, False caso contrário
    """
    # Validar o número do processo
    try:
        Processo.validar_numero(numero_processo)
    except ValueError as e:
        print(f"Erro: Número de processo inválido - {str(e)}")
        return False
    
    # Normalizar o tipo
    tipo = tipo.upper()
    if tipo not in ["TJ", "TRF"]:
        print("Erro: Tipo de processo inválido. Use 'TJ' ou 'TRF'.")
        return False
    
    # Determinar quais arquivos usar
    arquivo_lista = LISTA_TJ_FILE if tipo == "TJ" else LISTA_TRF_FILE
    arquivo_resultados = RESULTADO_TJ_FILE if tipo == "TJ" else RESULTADO_TRF_FILE
    
    # Excluir da lista
    sucesso_lista = excluir_processo_da_lista(numero_processo, arquivo_lista)
    
    # Excluir dos resultados se solicitado
    sucesso_resultados = True
    if excluir_resultados:
        sucesso_resultados = excluir_processo_dos_resultados(numero_processo, arquivo_resultados)
        
    return sucesso_lista and (not excluir_resultados or sucesso_resultados)

def excluir_processo_da_lista(numero_processo, arquivo_lista):
    """
    Remove um processo do arquivo de lista especificado.
    
    Args:
        numero_processo (str): Número do processo a remover
        arquivo_lista (str): Caminho do arquivo da lista
        
    Returns:
        bool: True se a operação foi bem-sucedida, False caso contrário
    """
    # Carregar a lista atual
    lista = carregar_arquivo_json(arquivo_lista)
    
    # Verificar se o processo existe na lista
    if numero_processo not in lista:
        print(f"Processo {numero_processo} não encontrado na lista.")
        return False
    
    # Remover o processo da lista
    lista.remove(numero_processo)
    
    # Salvar a lista atualizada
    if salvar_arquivo_json(arquivo_lista, lista):
        print(f"Processo {numero_processo} removido da lista com sucesso.")
        return True
    else:
        print(f"Erro ao salvar a lista após remover o processo {numero_processo}.")
        return False

def excluir_processo_dos_resultados(numero_processo, arquivo_resultados):
    """
    Remove um processo do arquivo de resultados especificado.
    
    Args:
        numero_processo (str): Número do processo a remover
        arquivo_resultados (str): Caminho do arquivo de resultados
        
    Returns:
        bool: True se a operação foi bem-sucedida, False caso contrário
    """
    # Verificar se o arquivo de resultados existe
    if not os.path.exists(arquivo_resultados):
        print(f"Arquivo de resultados {arquivo_resultados} não encontrado.")
        return False
    
    # Carregar o dicionário de resultados
    resultados = carregar_arquivo_json(arquivo_resultados)
    
    # Verificar se o processo existe nos resultados
    if numero_processo not in resultados:
        print(f"Processo {numero_processo} não encontrado nos resultados.")
        return False
    
    # Remover o processo dos resultados
    del resultados[numero_processo]
    
    # Salvar o dicionário atualizado
    if salvar_arquivo_json(arquivo_resultados, resultados):
        print(f"Processo {numero_processo} removido dos resultados com sucesso.")
        return True
    else:
        print(f"Erro ao salvar os resultados após remover o processo {numero_processo}.")
        return False

def excluir_todos_processos(tipo, confirmar=True):
    """
    Exclui todos os processos da lista e resultados do tipo especificado.
    
    Args:
        tipo (str): Tipo de processos a excluir ('TJ' ou 'TRF')
        confirmar (bool): Se True, solicita confirmação antes de excluir
        
    Returns:
        bool: True se a operação foi bem-sucedida, False caso contrário
    """
    # Normalizar o tipo
    tipo = tipo.upper()
    if tipo not in ["TJ", "TRF"]:
        print("Erro: Tipo de processo inválido. Use 'TJ' ou 'TRF'.")
        return False
    
    # Determinar quais arquivos usar
    arquivo_lista = LISTA_TJ_FILE if tipo == "TJ" else LISTA_TRF_FILE
    arquivo_resultados = RESULTADO_TJ_FILE if tipo == "TJ" else RESULTADO_TRF_FILE
    
    # Solicitar confirmação se necessário
    if confirmar:
        resposta = input(f"Tem certeza que deseja excluir TODOS os processos {tipo}? (s/n): ").lower()
        if resposta != 's':
            print("Operação cancelada.")
            return False
    
    # Criar listas vazias
    lista_vazia = []
    resultados_vazios = {}
    
    # Salvar arquivos vazios
    sucesso_lista = salvar_arquivo_json(arquivo_lista, lista_vazia)
    sucesso_resultados = True
    
    if os.path.exists(arquivo_resultados):
        sucesso_resultados = salvar_arquivo_json(arquivo_resultados, resultados_vazios)
    
    if sucesso_lista and sucesso_resultados:
        print(f"Todos os processos {tipo} foram excluídos com sucesso.")
        return True
    else:
        print(f"Erro ao excluir todos os processos {tipo}.")
        return False

if __name__ == "__main__":
    # Exemplo de uso do script
    print("===== EXCLUSÃO DE PROCESSOS =====")
    print("1. Excluir um processo específico")
    print("2. Excluir todos os processos de um tipo")
    
    opcao = input("\nEscolha uma opção: ")
    
    if opcao == "1":
        numero = input("Digite o número do processo (20 dígitos): ")
        tipo = input("Digite o tipo do processo (TJ ou TRF): ")
        excluir_resultados = input("Excluir também os resultados? (s/n): ").lower() == 's'
        
        excluir_processo(numero, tipo, excluir_resultados)
        
    elif opcao == "2":
        tipo = input("Digite o tipo de processos a excluir (TJ ou TRF): ")
        excluir_todos_processos(tipo)
        
    else:
        print("Opção inválida.")

from src.config import CACHE_DIR
from src.utils.file_handler import garantir_diretorio_existe, carregar_arquivo_json, salvar_arquivo_json
from src.models.processo import Processo
# Importando as funções de consulta individual e em lote
from src.api.tjmg import consultar_processo_tjmg, consultar_todos_processos_tjmg
from src.api.trf6 import consultar_processo_trf6, consultar_todos_processos_trf6
from src.config import LISTA_TJ_FILE, LISTA_TRF_FILE

def adicionar_processo(numero, tipo):
    """Adiciona um processo à lista correspondente."""
    try:
        # Criar objeto Processo para validação
        processo = Processo(numero, tipo)
        
        # Determinar qual arquivo usar
        arquivo = LISTA_TJ_FILE if processo.tipo == "TJ" else LISTA_TRF_FILE
        
        # Carregar lista atual
        lista = carregar_arquivo_json(arquivo)
        
        # Verificar se já existe
        if numero in lista:
            print(f"Processo {tipo} {numero} já existe na lista.")
            return False
        
        # Adicionar à lista
        lista.append(numero)
        
        # Salvar lista atualizada
        if salvar_arquivo_json(arquivo, lista):
            print(f"Processo {tipo} {numero} adicionado com sucesso.")
            return True
        return False
        
    except ValueError as e:
        print(f"Erro: {str(e)}")
        return False

def exibir_estatisticas():
    """Exibe estatísticas sobre as listas de processos."""
    processos_tj = carregar_arquivo_json(LISTA_TJ_FILE)
    processos_trf = carregar_arquivo_json(LISTA_TRF_FILE)
    
    print("\n----- Estatísticas -----")
    print(f"Total de processos cadastrados: {len(processos_tj) + len(processos_trf)}")
    print(f"Processos TJ: {len(processos_tj)}")
    print(f"Processos TRF: {len(processos_trf)}")
    print("-----------------------\n")

def consultar_unico_processo():
    """Menu para consultar um único processo."""
    print("\n===== CONSULTAR PROCESSO ÚNICO =====")
    print("1. Consultar processo TJ")
    print("2. Consultar processo TRF")
    print("3. Voltar")
    
    opcao = input("\nEscolha uma opção: ")
    
    if opcao == "1":
        numero = input("Digite o número do processo TJ (20 dígitos): ")
        try:
            # Validar o número do processo
            if Processo.validar_numero(numero):
                print(f"Consultando processo TJ {numero}...")
                resultado = consultar_processo_tjmg(numero)
                
                # Verificar se houve erro na consulta
                if "erro" in resultado:
                    print(f"Erro na consulta: {resultado['erro']}")
                else:
                    print("Consulta realizada com sucesso!")
                    # Exibir informações básicas do resultado
                    if "hits" in resultado and "total" in resultado["hits"]:
                        total = resultado["hits"]["total"]["value"]
                        print(f"Total de resultados encontrados: {total}")
                        
                        if total > 0 and "hits" in resultado["hits"]:
                            for i, hit in enumerate(resultado["hits"]["hits"], 1):
                                print(f"\nResultado {i}:")
                                if "_source" in hit:
                                    source = hit["_source"]
                                    campos = ["numeroProcesso", "orgaoJulgador", "dataAjuizamento", "classeProcessual"]
                                    for campo in campos:
                                        if campo in source:
                                            print(f"{campo}: {source[campo]}")
                    else:
                        print("Formato de resposta inesperado.")
            else:
                print("Número de processo inválido. Deve conter exatamente 20 dígitos numéricos.")
        except Exception as e:
            print(f"Erro ao processar a consulta: {str(e)}")
    
    elif opcao == "2":
        numero = input("Digite o número do processo TRF (20 dígitos): ")
        try:
            # Validar o número do processo
            if Processo.validar_numero(numero):
                print(f"Consultando processo TRF {numero}...")
                resultado = consultar_processo_trf6(numero)
                
                # Verificar se houve erro na consulta
                if "erro" in resultado:
                    print(f"Erro na consulta: {resultado['erro']}")
                else:
                    print("Consulta realizada com sucesso!")
                    # Exibir informações básicas do resultado
                    if "hits" in resultado and "total" in resultado["hits"]:
                        total = resultado["hits"]["total"]["value"]
                        print(f"Total de resultados encontrados: {total}")
                        
                        if total > 0 and "hits" in resultado["hits"]:
                            for i, hit in enumerate(resultado["hits"]["hits"], 1):
                                print(f"\nResultado {i}:")
                                if "_source" in hit:
                                    source = hit["_source"]
                                    campos = ["numeroProcesso", "orgaoJulgador", "dataAjuizamento", "classeProcessual"]
                                    for campo in campos:
                                        if campo in source:
                                            print(f"{campo}: {source[campo]}")
                    else:
                        print("Formato de resposta inesperado.")
            else:
                print("Número de processo inválido. Deve conter exatamente 20 dígitos numéricos.")
        except Exception as e:
            print(f"Erro ao processar a consulta: {str(e)}")
    
    elif opcao == "3":
        return
    
    else:
        print("Opção inválida.")

def menu_principal():
    """Exibe o menu principal do programa."""
    garantir_diretorio_existe(CACHE_DIR)
    
    while True:
        print("\n===== COMPILADOR JURÍDICO =====")
        print("1. Gerenciar processos")
        print("2. Consultar processo único")
        print("3. Consultar todos processos TJ")
        print("4. Consultar todos processos TRF")
        print("5. Sair")
        
        opcao = input("\nEscolha uma opção: ")
        
        if opcao == "1":
            menu_gerenciar_processos()
        elif opcao == "2":
            consultar_unico_processo()
        elif opcao == "3":
            consultar_todos_processos_tjmg()
        elif opcao == "4":
            consultar_todos_processos_trf6()
        elif opcao == "5":
            print("Programa encerrado.")
            break
        else:
            print("Opção inválida. Tente novamente.")

def menu_gerenciar_processos():
    """Exibe o menu de gerenciamento de processos."""
    while True:
        print("\n===== GERENCIAR PROCESSOS =====")
        print("1. Adicionar processo TJ")
        print("2. Adicionar processo TRF")
        print("3. Ver estatísticas")
        print("4. Voltar ao menu principal")
        
        opcao = input("\nEscolha uma opção: ")
        
        if opcao == "1":
            numero = input("Digite o número do processo TJ (20 dígitos): ")
            adicionar_processo(numero, "TJ")
        
        elif opcao == "2":
            numero = input("Digite o número do processo TRF (20 dígitos): ")
            adicionar_processo(numero, "TRF")
        
        elif opcao == "3":
            exibir_estatisticas()
        
        elif opcao == "4":
            break
        
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    menu_principal()
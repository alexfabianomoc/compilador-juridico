import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
import requests
import json
from datetime import datetime
import os


from src.config import LISTA_TJ_FILE, LISTA_TRF_FILE
from src.utils.file_handler import carregar_arquivo_json
from src.models.processo import Processo
from src.api.tjmg import consultar_processo_tjmg, consultar_todos_processos_tjmg
from src.api.trf6 import consultar_processo_trf6, consultar_todos_processos_trf6
from src.models.gerador_pdf_file import GeradorPDF
from excluir_processo import excluir_processo, excluir_todos_processos

class CompiladorJuridicoGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Compilador Jurídico")
        self.root.geometry("800x600")
        self.root.minsize(800, 600)

        # Armazenar resultados de consultas para geração de PDF
        self.resultado_consulta_individual_texto = ""
        self.resultado_consulta_individual_numero = ""
        self.resultado_consulta_individual_tipo = ""
        self.resultados_consulta_lote = {}
        self.ultimo_tipo_consulta_lote = ""

        # Criar abas
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Aba de Cadastro
        self.cadastro_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.cadastro_frame, text="Cadastrar Meus Processos")
        self.setup_cadastro_tab()
        
        # Aba de Consulta
        self.consulta_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.consulta_frame, text="Consultar Processos")
        self.setup_consulta_tab()
        
        # Aba de Estatísticas
        self.stats_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.stats_frame, text="Estatísticas Meus Processos")
        self.setup_stats_tab()
        
        # Aba de Exclusão
        self.exclusao_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.exclusao_frame, text="Excluir Meus Processos")
        self.setup_exclusao_tab()
        
        # Barra de status
        self.status_var = tk.StringVar()
        self.status_var.set("Pronto")
        self.status_bar = ttk.Label(root, textvariable=self.status_var, relief="sunken", anchor="w")
        self.status_bar.pack(side="bottom", fill="x")

    def setup_cadastro_tab(self):
        """Configurar a aba de cadastro de processos"""
        frame = ttk.LabelFrame(self.cadastro_frame, text="Adicionar Processo")
        frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Número do processo
        ttk.Label(frame, text="Número do Processo (20 dígitos):").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.processo_entry = ttk.Entry(frame, width=30)
        self.processo_entry.grid(row=0, column=1, sticky="w", padx=5, pady=5)
        
        # Tipo de processo
        ttk.Label(frame, text="Tipo:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.tipo_var = tk.StringVar(value="TJ")
        ttk.Radiobutton(frame, text="TJ", variable=self.tipo_var, value="TJ").grid(row=1, column=1, sticky="w", padx=5, pady=5)
        ttk.Radiobutton(frame, text="TRF", variable=self.tipo_var, value="TRF").grid(row=2, column=1, sticky="w", padx=5, pady=5)
        
        # Botão de adicionar
        self.add_button = ttk.Button(frame, text="Adicionar Processo", command=self.adicionar_processo)
        self.add_button.grid(row=3, column=0, columnspan=2, padx=5, pady=20)
        
        # Log de saída
        ttk.Label(frame, text="Log:").grid(row=4, column=0, sticky="w", padx=5, pady=5)
        self.log_text = scrolledtext.ScrolledText(frame, height=10, width=60, wrap=tk.WORD)
        self.log_text.grid(row=5, column=0, columnspan=3, padx=5, pady=5)
        self.log_text.config(state="disabled")
        
        # Frame para botões adicionais
        button_frame = ttk.Frame(frame)
        button_frame.grid(row=6, column=0, columnspan=3, padx=5, pady=10, sticky="w")
        
        # Botão para abrir o manual do usuário
        self.manual_button = ttk.Button(button_frame, text="Manual do Usuário", command=self.abrir_manual)
        self.manual_button.pack(side="left", padx=5)
        
        # Estilizar o botão do manual para destacá-lo
        style = ttk.Style()
        style.configure("Manual.TButton", foreground="blue")
        self.manual_button.configure(style="Manual.TButton")

    def setup_consulta_tab(self):
        """Configurar a aba de consulta de processos"""
        # Frame de consulta individual
        individual_frame = ttk.LabelFrame(self.consulta_frame, text="Consulta processo - DATAJUD")
        individual_frame.pack(fill="x", padx=10, pady=10)
        
        ttk.Label(individual_frame, text="Número do Processo:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.consulta_entry = ttk.Entry(individual_frame, width=30)
        self.consulta_entry.grid(row=0, column=1, sticky="w", padx=5, pady=5)
        
        ttk.Label(individual_frame, text="Tipo:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.consulta_tipo_var = tk.StringVar(value="TJ")
        ttk.Radiobutton(individual_frame, text="TJ", variable=self.consulta_tipo_var, value="TJ").grid(row=1, column=1, sticky="w", padx=5, pady=5)
        ttk.Radiobutton(individual_frame, text="TRF", variable=self.consulta_tipo_var, value="TRF").grid(row=2, column=1, sticky="w", padx=5, pady=5)
        
        button_frame = ttk.Frame(individual_frame)
        button_frame.grid(row=3, column=0, columnspan=2, padx=5, pady=10)
        
        self.consultar_button = ttk.Button(button_frame, text="Consultar", command=self.consultar_processo)
        self.consultar_button.pack(side="left", padx=5)
        
        # Novo botão para gerar PDF da consulta individual
        self.gerar_pdf_consulta_button = ttk.Button(button_frame, text="Gerar PDF", command=self.gerar_pdf_consulta_individual)
        self.gerar_pdf_consulta_button.pack(side="left", padx=5)
        self.gerar_pdf_consulta_button.config(state="disabled")  # Desabilitado inicialmente
        
        # Frame de consulta em lote
        lote_frame = ttk.LabelFrame(self.consulta_frame, text="Consulta em Lote - MEUS PROCESSOS")
        lote_frame.pack(fill="x", padx=10, pady=10)
        
        button_frame_tj = ttk.Frame(lote_frame)
        button_frame_tj.grid(row=0, column=0, padx=20, pady=10)
        
        self.consultar_tj_button = ttk.Button(button_frame_tj, text="Consultar Todos TJ", command=self.consultar_todos_tj)
        self.consultar_tj_button.pack(side="left", padx=5)
        
        self.gerar_pdf_tj_button = ttk.Button(button_frame_tj, text="Gerar PDF TJ", command=lambda: self.gerar_pdf_consulta_lote("TJ"))
        self.gerar_pdf_tj_button.pack(side="left", padx=5)
        self.gerar_pdf_tj_button.config(state="disabled")  # Desabilitado inicialmente
        
        button_frame_trf = ttk.Frame(lote_frame)
        button_frame_trf.grid(row=0, column=1, padx=20, pady=10)
        
        self.consultar_trf_button = ttk.Button(button_frame_trf, text="Consultar Todos TRF", command=self.consultar_todos_trf)
        self.consultar_trf_button.pack(side="left", padx=5)
        
        self.gerar_pdf_trf_button = ttk.Button(button_frame_trf, text="Gerar PDF TRF", command=lambda: self.gerar_pdf_consulta_lote("TRF"))
        self.gerar_pdf_trf_button.pack(side="left", padx=5)
        self.gerar_pdf_trf_button.config(state="disabled")  # Desabilitado inicialmente
        
        # Frame de resultados
        resultado_frame = ttk.LabelFrame(self.consulta_frame, text="Resultados")
        resultado_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.resultado_text = scrolledtext.ScrolledText(resultado_frame, height=12, width=70, wrap=tk.WORD)
        self.resultado_text.pack(fill="both", expand=True, padx=5, pady=5)
        self.resultado_text.config(state="disabled")

    def setup_stats_tab(self):
        """Configurar a aba de estatísticas"""
        frame = ttk.Frame(self.stats_frame)
        frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        button_frame = ttk.Frame(frame)
        button_frame.pack(pady=10)
        
        self.stats_button = ttk.Button(button_frame, text="Atualizar Estatísticas", command=self.exibir_estatisticas)
        self.stats_button.pack(side="left", padx=5)
        
        # Novo botão para gerar PDF das estatísticas
        self.gerar_pdf_stats_button = ttk.Button(button_frame, text="Gerar PDF", command=self.gerar_pdf_estatisticas)
        self.gerar_pdf_stats_button.pack(side="left", padx=5)
        
        self.stats_text = scrolledtext.ScrolledText(frame, height=15, width=70, wrap=tk.WORD)
        self.stats_text.pack(fill="both", expand=True, padx=5, pady=5)
        self.stats_text.config(state="disabled")
        
        # Inicializar estatísticas
        self.exibir_estatisticas()

    def setup_exclusao_tab(self):
        """Configurar a aba de exclusão de processos"""
        # Frame de exclusão individual
        individual_frame = ttk.LabelFrame(self.exclusao_frame, text="Excluir Processo Individual")
        individual_frame.pack(fill="x", padx=10, pady=10)
        
        ttk.Label(individual_frame, text="Número do Processo:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.excluir_entry = ttk.Entry(individual_frame, width=30)
        self.excluir_entry.grid(row=0, column=1, sticky="w", padx=5, pady=5)
        
        ttk.Label(individual_frame, text="Tipo:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.excluir_tipo_var = tk.StringVar(value="TJ")
        ttk.Radiobutton(individual_frame, text="TJ", variable=self.excluir_tipo_var, value="TJ").grid(row=1, column=1, sticky="w", padx=5, pady=5)
        ttk.Radiobutton(individual_frame, text="TRF", variable=self.excluir_tipo_var, value="TRF").grid(row=2, column=1, sticky="w", padx=5, pady=5)
        
        self.excluir_resultados_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(individual_frame, text="Excluir também o dicionário de processos", variable=self.excluir_resultados_var).grid(row=3, column=0, columnspan=2, sticky="w", padx=5, pady=5)
        
        self.excluir_button = ttk.Button(individual_frame, text="Excluir Processo", command=self.excluir_processo_individual)
        self.excluir_button.grid(row=4, column=0, columnspan=2, padx=5, pady=10)
        
        # Frame de exclusão em lote
        lote_frame = ttk.LabelFrame(self.exclusao_frame, text="Excluir Todos os Processos")
        lote_frame.pack(fill="x", padx=10, pady=10)
        
        ttk.Label(lote_frame, text="Tipo:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.excluir_lote_tipo_var = tk.StringVar(value="TJ")
        ttk.Radiobutton(lote_frame, text="TJ", variable=self.excluir_lote_tipo_var, value="TJ").grid(row=0, column=1, sticky="w", padx=5, pady=5)
        ttk.Radiobutton(lote_frame, text="TRF", variable=self.excluir_lote_tipo_var, value="TRF").grid(row=1, column=1, sticky="w", padx=5, pady=5)
        
        self.excluir_todos_button = ttk.Button(lote_frame, text="Excluir Todos", command=self.excluir_todos_processos)
        self.excluir_todos_button.grid(row=2, column=0, columnspan=2, padx=5, pady=10)
        
        # Log de exclusão
        log_frame = ttk.LabelFrame(self.exclusao_frame, text="Log de Exclusão")
        log_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.exclusao_log = scrolledtext.ScrolledText(log_frame, height=8, width=70, wrap=tk.WORD)
        self.exclusao_log.pack(fill="both", expand=True, padx=5, pady=5)
        self.exclusao_log.config(state="disabled")

    # Funções de callback
    def adicionar_processo(self):
        """Adicionar um processo à lista correspondente"""
        numero = self.processo_entry.get().strip()
        tipo = self.tipo_var.get()
        
        if not numero:
            messagebox.showerror("Erro", "Por favor, digite o número do processo.")
            return
        
        # Validar o número do processo
        if not Processo.validar_numero(numero):
            messagebox.showerror("Erro", "Número de processo inválido. Deve conter exatamente 20 dígitos numéricos.")
            return
        
        try:
            # Criar objeto Processo para validação
            processo = Processo(numero, tipo)
            
            # Determinar qual arquivo usar
            arquivo = LISTA_TJ_FILE if processo.tipo == "TJ" else LISTA_TRF_FILE
            
            # Carregar lista atual
            lista = carregar_arquivo_json(arquivo)
            
            # Verificar se já existe
            if numero in lista:
                self.append_log(f"Processo {tipo} {numero} já existe na lista.")
                return
            
            # Adicionar à lista
            lista.append(numero)
            
            # Importar a função só quando necessário para evitar circular imports
            from src.utils.file_handler import salvar_arquivo_json
            
            # Salvar lista atualizada
            if salvar_arquivo_json(arquivo, lista):
                self.append_log(f"Processo {tipo} {numero} adicionado com sucesso.")
                self.processo_entry.delete(0, tk.END)  # Limpar entrada
                # Atualizar estatísticas
                self.exibir_estatisticas()
            else:
                self.append_log("Erro ao salvar o arquivo.")
                
        except (ValueError, OSError, IOError, json.JSONDecodeError) as e:
            self.append_log(f"Erro: {str(e)}")

    def abrir_manual(self):
        """Abrir o manual do usuário em PDF"""
        import sys
        try:
            from src.config import BASE_DIR
            manual_path = os.path.join(BASE_DIR, "assets", "manual", "Manual_usuario_compilador_juridico.pdf")
            
            # Verifica se o diretório manual existe, senão cria
            manual_dir = os.path.dirname(manual_path)
            if not os.path.exists(manual_dir):
                os.makedirs(manual_dir)
                self.append_log("Diretório do manual criado: " + manual_dir)
            
            # Verifica se o arquivo existe
            if not os.path.exists(manual_path):
                self.append_log("Manual não encontrado em: " + manual_path)
                messagebox.showinfo("Informação", "O manual será aberto no navegador padrão.")
                # Redireciona para um link online do manual (pode ser substituído pelo seu link real)
                import webbrowser
                webbrowser.open("https://github.com/seu-usuario/compilador-juridico/blob/main/docs/manual.pdf")
                return
                
            # Abre o PDF com o visualizador padrão do sistema
            self.append_log("Abrindo manual: " + manual_path)
            if os.name == 'nt':  # Windows
                os.startfile(manual_path)
            elif os.name == 'posix':  # macOS e Linux
                import subprocess
                if sys.platform == 'darwin':  # macOS
                    subprocess.run(['open', manual_path])
                else:  # Linux
                    subprocess.run(['xdg-open', manual_path])
                    
            self.append_log("Manual aberto com sucesso!")
        except Exception as e:
            self.append_log(f"Erro ao abrir manual: {str(e)}")
            messagebox.showerror("Erro", f"Não foi possível abrir o manual: {str(e)}")
    
    def consultar_processo(self):
        """Consultar um processo individual"""
        numero = self.consulta_entry.get().strip()
        tipo = self.consulta_tipo_var.get()
        
        if not numero:
            messagebox.showerror("Erro", "Por favor, digite o número do processo.")
            return
        
        # Validar o número do processo
        if not Processo.validar_numero(numero):
            messagebox.showerror("Erro", "Número de processo inválido. Deve conter exatamente 20 dígitos numéricos.")
            return
        
        # Limpar resultado anterior e desabilitar botão de PDF
        self.resultado_text.config(state="normal")
        self.resultado_text.delete(1.0, tk.END)
        self.resultado_text.config(state="disabled")
        self.gerar_pdf_consulta_button.config(state="disabled")
        
        # Armazenar número e tipo para uso na geração de PDF
        self.resultado_consulta_individual_numero = numero
        self.resultado_consulta_individual_tipo = tipo
        self.resultado_consulta_individual_texto = ""
        
        self.update_resultado_text(f"Consultando processo {tipo} {numero}...\n")
        self.status_var.set(f"Consultando processo {tipo} {numero}...")
        self.root.update_idletasks()
        
        # Usar thread para não bloquear a interface durante a consulta
        threading.Thread(target=self._consultar_processo_thread, args=(numero, tipo)).start()
    
    def _consultar_processo_thread(self, numero, tipo):
        """Thread para consulta de processo"""
        try:
            if tipo == "TJ":
                resultado = consultar_processo_tjmg(numero)
                # Verificar se houve erro na consulta
                if "erro" in resultado:
                    self.update_resultado_text(f"Erro na consulta: {resultado['erro']}\n")
                else:
                    self.update_resultado_text("Consulta realizada com sucesso!\n\n")
                    
                    # Exibir informações específicas para processos TJ no formato solicitado
                    if "hits" in resultado and "total" in resultado["hits"]:
                        total = resultado["hits"]["total"]["value"]
                        
                        # Verificar se foram encontrados resultados
                        if total > 0 and "hits" in resultado["hits"]:
                            hits = resultado["hits"]["hits"]
                            
                            # Cabeçalho
                            self.update_resultado_text("=" * 60 + "\n")
                            self.update_resultado_text(f"PROCESSO TJ {numero}\n")
                            self.update_resultado_text("=" * 60 + "\n\n")
                            
                            # INFORMAÇÕES BÁSICAS
                            self.update_resultado_text("INFORMAÇÕES BÁSICAS\n")
                            self.update_resultado_text("-" * 30 + "\n")
                            
                            # Número do Processo
                            self.update_resultado_text(f"* Número do Processo: {numero}\n")
                            
                            # Tribunal
                            if len(hits) > 0 and "_source" in hits[0] and "tribunal" in hits[0]["_source"]:
                                tribunal = hits[0]["_source"]["tribunal"]
                                self.update_resultado_text(f"* Tribunal: {tribunal}")
                                if tribunal == "TJMG":
                                    self.update_resultado_text(" (Tribunal de Justiça de Minas Gerais)\n")
                                else:
                                    self.update_resultado_text("\n")
                            
                            # Data de Ajuizamento 
                            if len(hits) > 0 and "_source" in hits[0] and "dataAjuizamento" in hits[0]["_source"]:
                                data_str = hits[0]["_source"]["dataAjuizamento"]
                                try:
                                    data = datetime.strptime(data_str.split("T")[0], "%Y-%m-%d")
                                    data_formatada = data.strftime("%d/%m/%Y")
                                    self.update_resultado_text(f"* Data de Ajuizamento: {data_formatada}\n")
                                except (ValueError, TypeError, IndexError):
                                    self.update_resultado_text(f"* Data de Ajuizamento: {data_str}\n")
                            
                            # Classe Original
                            primeira_instancia = None
                            for hit in hits:
                                if "_source" in hit and "grau" in hit["_source"] and hit["_source"]["grau"] == "G1":
                                    primeira_instancia = hit["_source"]
                                    break
                                    
                            if primeira_instancia and "classe" in primeira_instancia and "nome" in primeira_instancia["classe"]:
                                self.update_resultado_text(f"* Classe Original: {primeira_instancia['classe']['nome']} (primeira instância)\n")
                            
                            # Formato
                            formato_convertido = False
                            if primeira_instancia and "movimentos" in primeira_instancia:
                                for mov in primeira_instancia["movimentos"]:
                                    if "codigo" in mov and mov["codigo"] == 14732:  # Conversão de Autos Físicos em Eletrônicos
                                        formato_convertido = True
                                        data_conversao = mov.get("dataHora", "").split("T")[0]
                                        try:
                                            data = datetime.strptime(data_conversao, "%Y-%m-%d")
                                            data_formatada = data.strftime("%d/%m/%Y")
                                            self.update_resultado_text(f"* Formato: Inicialmente Físico, convertido para Eletrônico em {data_formatada}\n")
                                        except (ValueError, TypeError, IndexError):
                                            self.update_resultado_text(f"* Formato: Inicialmente Físico, convertido para Eletrônico em {data_conversao}\n")
                                        break
                                        
                            if not formato_convertido and primeira_instancia and "formato" in primeira_instancia and "nome" in primeira_instancia["formato"]:
                                self.update_resultado_text(f"* Formato: {primeira_instancia['formato']['nome']}\n")
                            
                            # Assunto
                            if primeira_instancia and "assuntos" in primeira_instancia and len(primeira_instancia["assuntos"]) > 0:
                                self.update_resultado_text(f"* Assunto: {primeira_instancia['assuntos'][0]['nome']}\n")
                            
                            # SITUAÇÃO ATUAL
                            self.update_resultado_text("\nSITUAÇÃO ATUAL\n")
                            self.update_resultado_text("-" * 30 + "\n")
                            
                            # Última Atualização
                            if primeira_instancia and "dataHoraUltimaAtualizacao" in primeira_instancia:
                                data_str = primeira_instancia["dataHoraUltimaAtualizacao"]
                                try:
                                    data = datetime.strptime(data_str.split("T")[0], "%Y-%m-%d")
                                    data_formatada = data.strftime("%d/%m/%Y")
                                    self.update_resultado_text(f"* Última Atualização: {data_formatada}\n")
                                except (ValueError, TypeError, IndexError):
                                    self.update_resultado_text(f"* Última Atualização: {data_str}\n")
                            
                            # Status
                            status = "Em andamento"
                            data_baixa = ""
                            if primeira_instancia and "movimentos" in primeira_instancia:
                                try:
                                    movimentos = sorted(primeira_instancia["movimentos"], 
                                                    key=lambda x: x.get("dataHora", ""), 
                                                    reverse=True)
                                except (KeyError, TypeError, ValueError, AttributeError):
                                    movimentos = primeira_instancia["movimentos"]
                                
                                for mov in movimentos:
                                    if "codigo" in mov and mov["codigo"] == 22:  # Baixa Definitiva
                                        status = "Arquivado definitivamente"
                                        data_str = mov.get("dataHora", "").split("T")[0]
                                        try:
                                            data = datetime.strptime(data_str, "%Y-%m-%d")
                                            data_baixa = data.strftime("%d/%m/%Y")
                                        except (ValueError, TypeError, IndexError):
                                            data_baixa = data_str
                                        break
                            
                            if data_baixa:
                                self.update_resultado_text(f"* Status: {status} (Baixa Definitiva em {data_baixa})\n")
                            else:
                                self.update_resultado_text(f"* Status: {status}\n")
                            
                            # Órgão Julgador Original
                            if primeira_instancia and "orgaoJulgador" in primeira_instancia and "nome" in primeira_instancia["orgaoJulgador"]:
                                self.update_resultado_text(f"* Órgão Julgador Original: {primeira_instancia['orgaoJulgador']['nome']}\n")
                            
                            # HISTÓRICO PROCESSUAL
                            self.update_resultado_text("\nHISTÓRICO PROCESSUAL\n")
                            self.update_resultado_text("-" * 30 + "\n")
                            self.update_resultado_text("O processo passou por três instâncias/fases:\n")
                            
                            # Identificar as diferentes instâncias
                            instancias = []
                            for hit in hits:
                                if "_source" in hit:
                                    source = hit["_source"]
                                    if "grau" in source and "classe" in source and "nome" in source["classe"]:
                                        grau = source["grau"]
                                        classe = source["classe"]["nome"]
                                        data_ajuizamento = ""
                                        if "dataAjuizamento" in source:
                                            data_str = source["dataAjuizamento"].split("T")[0]
                                            try:
                                                data = datetime.strptime(data_str, "%Y-%m-%d")
                                                data_ajuizamento = data.strftime("%d/%m/%Y")
                                            except (ValueError, TypeError, IndexError):
                                                data_ajuizamento = data_str
                                        
                                        instancias.append((grau, classe, data_ajuizamento))
                            
                            # Exibir instâncias ordenadas
                            contador = 1
                            for grau, classe, data in instancias:
                                desc = ""
                                if grau == "G1":
                                    desc = "Primeira Instância (G1)"
                                elif grau == "G2":
                                    if "Recurso" in classe or "Agravo" in classe:
                                        desc = "Recurso (G2)"
                                    else:
                                        desc = "Segunda Instância (G2)"
                                
                                if data:
                                    self.update_resultado_text(f"{contador}. **{desc}**: {classe} (iniciada em {data})\n")
                                else:
                                    self.update_resultado_text(f"{contador}. **{desc}**: {classe}\n")
                                contador += 1
                            
                            # MOVIMENTAÇÕES IMPORTANTES
                            self.update_resultado_text("\nMOVIMENTAÇÕES IMPORTANTES\n")
                            self.update_resultado_text("-" * 30 + "\n")
                            
                            # Coletar movimentações importantes
                            movimentacoes = []
                            if primeira_instancia and "movimentos" in primeira_instancia:
                                for mov in primeira_instancia["movimentos"]:
                                    if "codigo" in mov and "dataHora" in mov:
                                        codigo = mov["codigo"]
                                        nome = mov.get("nome", "")
                                        data_str = mov["dataHora"].split("T")[0]
                                        
                                        # Códigos importantes
                                        if codigo in [22, 848, 893, 14732, 246]:  # Baixa, Trânsito em julgado, Desarquivamento, Conversão, Arquivamento Definitivo
                                            try:
                                                data = datetime.strptime(data_str, "%Y-%m-%d")
                                                data_formatada = data.strftime("%d/%m/%Y")
                                            except (ValueError, TypeError, IndexError):
                                                data_formatada = data_str
                                                
                                            movimentacoes.append((data_str, f"* {nome} em {data_formatada}"))
                            
                            # Extrair datas de início e fim
                            data_inicio = ""
                            data_fim = ""
                            if len(instancias) > 0:
                                for grau, classe, data in instancias:
                                    if grau == "G1" and data:
                                        data_inicio = data
                                        break
                            
                            # Encontrar data de trânsito em julgado
                            if primeira_instancia and "movimentos" in primeira_instancia:
                                for mov in primeira_instancia["movimentos"]:
                                    if "codigo" in mov and mov["codigo"] == 848:  # Trânsito em julgado
                                        data_str = mov.get("dataHora", "").split("T")[0]
                                        try:
                                            data = datetime.strptime(data_str, "%Y-%m-%d")
                                            data_fim = data.strftime("%d/%m/%Y")
                                        except (ValueError, TypeError, IndexError):
                                            data_fim = data_str
                                        break
                            
                            if data_inicio and data_fim:
                                self.update_resultado_text(f"* O processo tramitou de {data_inicio} a {data_fim}\n")
                            
                            # Exibir movimentações importantes ordenadas por data
                            try:
                                movimentacoes.sort(key=lambda x: x[0], reverse=False)  # Ordenar por data (mais antiga primeiro)
                            except (KeyError, TypeError, ValueError, AttributeError):
                                # Em caso de erro na ordenação, mantemos a ordem original
                                pass
                                
                            for _, texto in movimentacoes:
                                self.update_resultado_text(f"{texto}\n")
                        else:
                            # Tratamento específico para quando o processo não é encontrado
                            self.update_resultado_text("=" * 60 + "\n")
                            self.update_resultado_text(f"PROCESSO {numero}\n")
                            self.update_resultado_text("=" * 60 + "\n\n")
                            self.update_resultado_text("PROCESSO NÃO ENCONTRADO\n")
                            self.update_resultado_text("-" * 30 + "\n")
                            self.update_resultado_text(f"A consulta foi realizada com sucesso, mas não há informações sobre o processo {numero} no TJMG.\n")
                            self.update_resultado_text("\nPossíveis motivos:\n")
                            self.update_resultado_text("- O número do processo pode estar incorreto\n")
                            self.update_resultado_text("- O processo pode estar em sigilo\n")
                            self.update_resultado_text("- O processo pode não existir na base de dados\n")
                    else:
                        self.update_resultado_text("Formato de resposta inesperado.\n")
            
            else:  # TRF
                resultado = consultar_processo_trf6(numero)
                # Verificar se houve erro na consulta
                if "erro" in resultado:
                    self.update_resultado_text(f"Erro na consulta: {resultado['erro']}\n")
                else:
                    self.update_resultado_text("Consulta realizada com sucesso!\n\n")
                    # Exibir informações para processos TRF com formato específico
                    if "hits" in resultado and "total" in resultado["hits"]:
                        total = resultado["hits"]["total"]["value"]
                        
                        if total > 0 and "hits" in resultado["hits"]:
                            hits = resultado["hits"]["hits"]
                            
                            # Cabeçalho
                            self.update_resultado_text("=" * 50 + "\n")
                            self.update_resultado_text(f"PROCESSO TRF {numero}\n")
                            self.update_resultado_text("=" * 50 + "\n\n")
                            
                            # Informações Básicas
                            self.update_resultado_text("INFORMAÇÕES BÁSICAS:\n")
                            self.update_resultado_text("-" * 30 + "\n")
                            
                            for hit in hits:
                                if "_source" in hit:
                                    source = hit["_source"]
                                    
                                    # Número do Processo
                                    if "numeroProcesso" in source:
                                        self.update_resultado_text(f"Número do Processo: {source['numeroProcesso']}\n")
                                    
                                    # Classe Processual
                                    if "classeProcessual" in source:
                                        self.update_resultado_text(f"Classe Processual: {source['classeProcessual']}\n")
                                    elif "classe" in source and "nome" in source["classe"]:
                                        self.update_resultado_text(f"Classe Processual: {source['classe']['nome']}\n")
                                    
                                    # Data de Ajuizamento
                                    if "dataAjuizamento" in source:
                                        self.update_resultado_text(f"Data de Ajuizamento: {source['dataAjuizamento']}\n")
                                        
                                    # Sistema
                                    if "sistema" in source and "nome" in source["sistema"]:
                                        self.update_resultado_text(f"Sistema: {source['sistema']['nome']}\n")
                                    
                                    # Formato
                                    if "formato" in source and "nome" in source["formato"]:
                                        self.update_resultado_text(f"Formato: {source['formato']['nome']}\n")
                                    
                                    # Assunto
                                    if "assuntos" in source and len(source["assuntos"]) > 0:
                                        self.update_resultado_text("Assuntos:\n")
                                        for i, assunto in enumerate(source["assuntos"]):
                                            if "nome" in assunto:
                                                self.update_resultado_text(f"- {assunto['nome']}\n")
                                    
                                    # Órgão Julgador
                                    if "orgaoJulgador" in source:
                                        if isinstance(source["orgaoJulgador"], dict) and "nome" in source["orgaoJulgador"]:
                                            self.update_resultado_text(f"Órgão Julgador: {source['orgaoJulgador']['nome']}\n")
                                        else:
                                            self.update_resultado_text(f"Órgão Julgador: {source['orgaoJulgador']}\n")
                                    
                                    # Situação Atual
                                    self.update_resultado_text("\nSITUAÇÃO ATUAL:\n")
                                    self.update_resultado_text("-" * 30 + "\n")
                                    
                                    # Última atualização
                                    if "dataHoraUltimaAtualizacao" in source:
                                        self.update_resultado_text(f"Última Atualização: {source['dataHoraUltimaAtualizacao']}\n")
                                    
                                    # Movimentos
                                    if "movimentos" in source and len(source["movimentos"]) > 0:
                                        # Ordenar movimentos por data (mais recente primeiro)
                                        try:
                                            movimentos = sorted(source["movimentos"], 
                                                                key=lambda x: x.get("dataHora", ""), 
                                                                reverse=True)
                                        except (KeyError, TypeError, ValueError, AttributeError):
                                            # Especificamos os tipos de exceção que podem ocorrer ao ordenar
                                            movimentos = source["movimentos"]
                                        
                                        # Último movimento
                                        if movimentos:
                                            ultimo_mov = movimentos[0]
                                            if isinstance(ultimo_mov, dict):
                                                codigo = ultimo_mov.get("codigo", "N/A")
                                                nome = ultimo_mov.get("nome", "Não informado")
                                                data = ultimo_mov.get("dataHora", "Não informada")
                                                self.update_resultado_text(f"Último Movimento: [{codigo}] {nome} ({data})\n")
                                        
                                        # Histórico Recente
                                        self.update_resultado_text("\nHISTÓRICO RECENTE:\n")
                                        self.update_resultado_text("-" * 30 + "\n")
                                        
                                        # Mostrar até 5 movimentos mais recentes
                                        cont = 0
                                        for mov in movimentos:
                                            if isinstance(mov, dict):
                                                cont += 1
                                                codigo = mov.get("codigo", "N/A")
                                                nome = mov.get("nome", "Não informado")
                                                data = mov.get("dataHora", "Não informada")
                                                self.update_resultado_text(f"{cont}. [{codigo}] {nome}\n   Data: {data}\n")
                                                if cont >= 5:
                                                    break
                                    
                                    # Após processar um hit, saímos do loop para evitar repetição
                                    break
                        else:
                            # Tratamento específico para quando o processo não é encontrado
                            self.update_resultado_text("=" * 50 + "\n")
                            self.update_resultado_text(f"PROCESSO TRF {numero}\n")
                            self.update_resultado_text("=" * 50 + "\n\n")
                            self.update_resultado_text("PROCESSO NÃO ENCONTRADO\n")
                            self.update_resultado_text("-" * 30 + "\n")
                            self.update_resultado_text(f"A consulta foi realizada com sucesso, mas não há informações sobre o processo {numero} no TRF.\n")
                            self.update_resultado_text("\nPossíveis motivos:\n")
                            self.update_resultado_text("- O número do processo pode estar incorreto\n")
                            self.update_resultado_text("- O processo pode estar em sigilo\n")
                            self.update_resultado_text("- O processo pode não existir na base de dados\n")
                    else:
                        self.update_resultado_text("Formato de resposta inesperado.\n")
            
            # Agora temos um resultado válido, habilitar o botão de PDF
            self.root.after(0, lambda: self.gerar_pdf_consulta_button.config(state="normal"))
            self.status_var.set("Pronto")
            
        except (KeyError, TypeError, ValueError, AttributeError, requests.RequestException, json.JSONDecodeError) as e:
            self.update_resultado_text(f"Erro ao processar a consulta: {str(e)}\n")
            self.status_var.set("Erro na consulta")
    
    def consultar_todos_tj(self):
        """Consultar todos os processos TJ"""
        self.update_resultado_text("Iniciando consulta de todos os processos TJ...\n")
        self.status_var.set("Consultando processos TJ...")
        self.root.update_idletasks()
        
        # Desabilitar botões durante a consulta
        self.consultar_tj_button.config(state="disabled")
        self.consultar_trf_button.config(state="disabled")
        self.gerar_pdf_tj_button.config(state="disabled")
        self.gerar_pdf_trf_button.config(state="disabled")
        
        # Usar thread para não bloquear a interface durante a consulta
        threading.Thread(target=self._consultar_todos_tj_thread).start()
    
    def _consultar_todos_tj_thread(self):
        """Thread para consulta de todos os processos TJ"""
        try:
            from datetime import datetime
            
            # Manter a chamada da API original
            resultados = consultar_todos_processos_tjmg()
            
            # Criar um dicionário para armazenar os resultados formatados
            processos_formatados = {}
            
            # Para cada processo no resultado da API
            for numero_processo, dados in resultados.items():
                if "hits" in dados and "hits" in dados["hits"] and len(dados["hits"]["hits"]) > 0:
                    hits = dados["hits"]["hits"]
                    
                    # Vamos trabalhar com o primeiro hit (normalmente contém as informações mais relevantes)
                    primeiro_hit = hits[0]
                    
                    if "_source" in primeiro_hit:
                        source = primeiro_hit["_source"]
                        
                        # Extrair dados básicos
                        tribunal = source.get("tribunal", "Não informado")
                        
                        # Formatar data de última atualização
                        data_atualizacao = source.get("dataHoraUltimaAtualizacao", "")
                        if data_atualizacao:
                            try:
                                data_obj = datetime.strptime(data_atualizacao.split("T")[0], "%Y-%m-%d")
                                data_atualizacao = data_obj.strftime("%d/%m/%Y")
                            except (ValueError, TypeError, IndexError):
                                # Manter o valor original se houver erro de formatação
                                pass
                        
                        # Determinar o status com base nos movimentos
                        status = "Em andamento"
                        if "movimentos" in source:
                            movimentos = source["movimentos"]
                            # Ordenar movimentos por data (mais recente primeiro)
                            try:
                                movimentos = sorted(movimentos, key=lambda x: x.get("dataHora", ""), reverse=True)
                            except (KeyError, TypeError, AttributeError):
                                # Em caso de erro na ordenação, manter a ordem original
                                pass
                            
                            # Verificar os códigos de movimento mais importantes para determinar o status
                            for mov in movimentos:
                                codigo = mov.get("codigo", 0)
                                if codigo == 22:  # Baixa Definitiva
                                    status = "Arquivado definitivamente"
                                    break
                                elif codigo == 246:  # Definitivo
                                    status = "Arquivado definitivamente"
                                    break
                                elif codigo == 848:  # Trânsito em julgado
                                    status = "Transitado em julgado"
                                    break
                                elif codigo == 196:  # Extinção da execução
                                    status = "Execução extinta"
                                    break
                                elif codigo == 893:  # Desarquivamento
                                    status = "Desarquivado"
                                    break
                        
                        # Armazenar os dados formatados
                        processos_formatados[numero_processo] = {
                            "numero": numero_processo,
                            "tribunal": tribunal,
                            "ultima_atualizacao": data_atualizacao,
                            "status": status
                        }
            
            # Ordenar os processos por número
            processos_ordenados = dict(sorted(processos_formatados.items()))
            
            # Exibir os resultados
            self.update_resultado_text("\n=== RESULTADO DA CONSULTA DE PROCESSOS TJ ===\n\n")
            self.update_resultado_text(f"Total de processos consultados: {len(processos_ordenados)}\n\n")
            
            for proc in processos_ordenados.values():
                self.update_resultado_text(f"Número: {proc['numero']}\n")
                self.update_resultado_text(f"Tribunal: {proc['tribunal']}\n")
                self.update_resultado_text(f"Última Atualização: {proc['ultima_atualizacao']}\n")
                self.update_resultado_text(f"Status: {proc['status']}\n")
                self.update_resultado_text("-" * 50 + "\n")
            
            # Armazenar resultados para geração de PDF
            self.resultados_consulta_lote = processos_ordenados
            self.ultimo_tipo_consulta_lote = "TJ"
            
            # Habilitar botão de PDF TJ
            self.root.after(0, lambda: self.gerar_pdf_tj_button.config(state="normal"))
            
        except requests.RequestException as e:
            self.update_resultado_text(f"Erro de conexão ao consultar processos: {str(e)}\n")
        except json.JSONDecodeError as e:
            self.update_resultado_text(f"Erro ao processar resposta JSON: {str(e)}\n")
        except (KeyError, ValueError, TypeError) as e:
            self.update_resultado_text(f"Erro ao processar os dados: {str(e)}\n")
        except IOError as e:
            self.update_resultado_text(f"Erro de entrada/saída: {str(e)}\n")
        except Exception as e:
            self.update_resultado_text(f"Erro inesperado: {str(e)}\n")
        finally:
            self.status_var.set("Pronto")
            # Reabilitar botões
            self.root.after(0, lambda: self.consultar_tj_button.config(state="normal"))
            self.root.after(0, lambda: self.consultar_trf_button.config(state="normal"))
    
    def consultar_todos_trf(self):
        """Consultar todos os processos TRF"""
        self.update_resultado_text("Iniciando consulta de todos os processos TRF...\n")
        self.status_var.set("Consultando processos TRF...")
        self.root.update_idletasks()
        
        # Desabilitar botões durante a consulta
        self.consultar_tj_button.config(state="disabled")
        self.consultar_trf_button.config(state="disabled")
        self.gerar_pdf_tj_button.config(state="disabled")
        self.gerar_pdf_trf_button.config(state="disabled")
        
        # Usar thread para não bloquear a interface durante a consulta
        threading.Thread(target=self._consultar_todos_trf_thread).start()
    
    def _consultar_todos_trf_thread(self):
        """Thread para consulta de todos os processos TRF"""
        try:
            from datetime import datetime
            
            # Manter a chamada da API original
            resultados = consultar_todos_processos_trf6()
            
            # Criar um dicionário para armazenar os resultados formatados
            processos_formatados = {}
            
            # Para cada processo no resultado da API
            for numero_processo, dados in resultados.items():
                if "hits" in dados and "hits" in dados["hits"] and len(dados["hits"]["hits"]) > 0:
                    hits = dados["hits"]["hits"]
                    
                    # Vamos trabalhar com o primeiro hit (normalmente contém as informações mais relevantes)
                    primeiro_hit = hits[0]
                    
                    if "_source" in primeiro_hit:
                        source = primeiro_hit["_source"]
                        
                        # Extrair dados básicos
                        orgao_julgador = "Não informado"
                        if "orgaoJulgador" in source:
                            if isinstance(source["orgaoJulgador"], dict) and "nome" in source["orgaoJulgador"]:
                                orgao_julgador = source["orgaoJulgador"]["nome"]
                            elif isinstance(source["orgaoJulgador"], str):
                                orgao_julgador = source["orgaoJulgador"]
                        
                        # Formatar data de última atualização
                        data_atualizacao = source.get("dataHoraUltimaAtualizacao", "")
                        if data_atualizacao:
                            try:
                                data_obj = datetime.strptime(data_atualizacao.split("T")[0], "%Y-%m-%d")
                                data_atualizacao = data_obj.strftime("%d/%m/%Y")
                            except (ValueError, TypeError, IndexError):
                                # Manter o valor original se houver erro de formatação
                                pass
                        
                        # Determinar o último movimento
                        ultimo_movimento = "Não informado"
                        if "movimentos" in source and len(source["movimentos"]) > 0:
                            movimentos = source["movimentos"]
                            # Ordenar movimentos por data (mais recente primeiro)
                            try:
                                movimentos = sorted(movimentos, key=lambda x: x.get("dataHora", ""), reverse=True)
                                
                                # Obter o movimento mais recente
                                if movimentos:
                                    mov = movimentos[0]
                                    codigo = mov.get("codigo", "")
                                    nome = mov.get("nome", "Não especificado")
                                    data_hora = mov.get("dataHora", "")
                                    
                                    # Formatar data se existir
                                    if data_hora:
                                        try:
                                            data_obj = datetime.strptime(data_hora.split("T")[0], "%Y-%m-%d")
                                            data_hora = data_obj.strftime("%d/%m/%Y")
                                        except (ValueError, TypeError, IndexError):
                                            # Manter o valor original se houver erro de formatação
                                            pass
                                    
                                    ultimo_movimento = f"[{codigo}] {nome} ({data_hora})"
                            except (KeyError, TypeError, AttributeError):
                                ultimo_movimento = "Erro ao processar movimentos: dados incompatíveis"
                        
                        # Armazenar os dados formatados
                        processos_formatados[numero_processo] = {
                            "numero": numero_processo,
                            "orgao_julgador": orgao_julgador,
                            "ultima_atualizacao": data_atualizacao,
                            "ultimo_movimento": ultimo_movimento
                        }
            
            # Ordenar os processos por número
            processos_ordenados = dict(sorted(processos_formatados.items()))
            
            # Exibir os resultados
            self.update_resultado_text("\n=== RESULTADO DA CONSULTA DE PROCESSOS TRF ===\n\n")
            self.update_resultado_text(f"Total de processos consultados: {len(processos_ordenados)}\n\n")
            
            for proc in processos_ordenados.values():
                self.update_resultado_text(f"Número: {proc['numero']}\n")
                self.update_resultado_text(f"Órgão Julgador: {proc['orgao_julgador']}\n")
                self.update_resultado_text(f"Última Atualização: {proc['ultima_atualizacao']}\n")
                self.update_resultado_text(f"Último Movimento: {proc['ultimo_movimento']}\n")
                self.update_resultado_text("-" * 50 + "\n")
            
            # Armazenar resultados para geração de PDF
            self.resultados_consulta_lote = processos_ordenados
            self.ultimo_tipo_consulta_lote = "TRF"
            
            # Habilitar botão de PDF TRF
            self.root.after(0, lambda: self.gerar_pdf_trf_button.config(state="normal"))
            
        except requests.RequestException as e:
            self.update_resultado_text(f"Erro de conexão ao consultar processos: {str(e)}\n")
        except json.JSONDecodeError as e:
            self.update_resultado_text(f"Erro ao processar resposta JSON: {str(e)}\n")
        except (KeyError, ValueError, TypeError) as e:
            self.update_resultado_text(f"Erro ao processar os dados: {str(e)}\n")
        except IOError as e:
            self.update_resultado_text(f"Erro de entrada/saída: {str(e)}\n")
        except Exception as e:
            self.update_resultado_text(f"Erro inesperado: {str(e)}\n")
        finally:
            self.status_var.set("Pronto")
            # Reabilitar botões
            self.root.after(0, lambda: self.consultar_tj_button.config(state="normal"))
            self.root.after(0, lambda: self.consultar_trf_button.config(state="normal"))
    
    def exibir_estatisticas(self):
        """Exibir estatísticas sobre as listas de processos"""
        processos_tj = carregar_arquivo_json(LISTA_TJ_FILE)
        processos_trf = carregar_arquivo_json(LISTA_TRF_FILE)
        
        self.stats_text.config(state="normal")
        self.stats_text.delete(1.0, tk.END)
        
        self.stats_text.insert(tk.END, "\n----- ESTATÍSTICAS - MEUS PROCESSOS -----\n\n")
        self.stats_text.insert(tk.END, f"Total de processos cadastrados: {len(processos_tj) + len(processos_trf)}\n")
        self.stats_text.insert(tk.END, f"Processos TJ: {len(processos_tj)}\n")
        self.stats_text.insert(tk.END, f"Processos TRF: {len(processos_trf)}\n")
        self.stats_text.insert(tk.END, "\n-----------------------\n")
        
        # Mostrar os últimos 5 processos de cada tipo se existirem
        if processos_tj:
            self.stats_text.insert(tk.END, "\nÚltimos processos TJ cadastrados:\n")
            for processo in processos_tj[-5:]:
                self.stats_text.insert(tk.END, f"- {processo}\n")
        
        if processos_trf:
            self.stats_text.insert(tk.END, "\nÚltimos processos TRF cadastrados:\n")
            for processo in processos_trf[-5:]:
                self.stats_text.insert(tk.END, f"- {processo}\n")
        
        self.stats_text.config(state="disabled")
    
    def excluir_processo_individual(self):
        """Excluir um processo individual"""
        numero = self.excluir_entry.get().strip()
        tipo = self.excluir_tipo_var.get()
        excluir_resultados = self.excluir_resultados_var.get()
        
        if not numero:
            messagebox.showerror("Erro", "Por favor, digite o número do processo.")
            return
        
        # Confirmar exclusão
        if not messagebox.askyesno("Confirmar Exclusão", f"Tem certeza que deseja excluir o processo {tipo} {numero}?"):
            return
        
        # Excluir processo
        try:
            resultado = excluir_processo(numero, tipo, excluir_resultados)
            if resultado:
                self.append_exclusao_log(f"Processo {tipo} {numero} excluído com sucesso.")
                self.excluir_entry.delete(0, tk.END)  # Limpar entrada
                # Atualizar estatísticas
                self.exibir_estatisticas()
            else:
                self.append_exclusao_log(f"Falha ao excluir o processo {tipo} {numero}.")
        except (ValueError, IOError, FileNotFoundError, json.JSONDecodeError, OSError) as e:
            self.append_exclusao_log(f"Erro ao excluir o processo: {str(e)}")
    
    def excluir_todos_processos(self):
        """Excluir todos os processos de um tipo"""
        tipo = self.excluir_lote_tipo_var.get()
        
        # Confirmar exclusão
        if not messagebox.askyesno("Confirmar Exclusão", f"ATENÇÃO: Tem certeza que deseja excluir TODOS os processos {tipo}?\nEsta ação não pode ser desfeita."):
            return
        # Pedir confirmação novamente
        if not messagebox.askyesno("Confirmar Exclusão", f"ÚLTIMA CHANCE: Confirma a exclusão de TODOS os processos {tipo}?"):
            return
        
        # Excluir todos os processos
        try:
            resultado = excluir_todos_processos(tipo, confirmar=False)  # Não pedir confirmação novamente
            if resultado:
                self.append_exclusao_log(f"Todos os processos {tipo} foram excluídos com sucesso.")
                # Atualizar estatísticas
                self.exibir_estatisticas()
            else:
                self.append_exclusao_log(f"Falha ao excluir todos os processos {tipo}.")
        except (ValueError, IOError, FileNotFoundError, json.JSONDecodeError, OSError) as e:
            self.append_exclusao_log(f"Erro ao excluir os processos: {str(e)}")
    
    # Novas funções para geração de PDF
    def gerar_pdf_estatisticas(self):
        """Gerar um PDF com as estatísticas atuais"""
        try:
            processos_tj = carregar_arquivo_json(LISTA_TJ_FILE)
            processos_trf = carregar_arquivo_json(LISTA_TRF_FILE)
            
            arquivo = GeradorPDF.gerar_pdf_estatisticas(processos_tj, processos_trf)
            
            if arquivo:
                self.status_var.set(f"PDF de estatísticas gerado: {os.path.basename(arquivo)}")
                messagebox.showinfo("PDF Gerado", f"O arquivo PDF foi salvo com sucesso em:\n{arquivo}")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao gerar PDF de estatísticas: {str(e)}")
            self.status_var.set("Erro ao gerar PDF")
    
    def gerar_pdf_consulta_individual(self):
        """Gerar um PDF com o resultado da consulta individual"""
        if not self.resultado_consulta_individual_texto and not self.resultado_text.get(1.0, tk.END).strip():
            messagebox.showwarning("Atenção", "Não há resultado de consulta para gerar o PDF.")
            return
        
        try:
            # Obter o texto atual da área de resultados
            self.resultado_consulta_individual_texto = self.resultado_text.get(1.0, tk.END)
            
            arquivo = GeradorPDF.gerar_pdf_consulta_individual(
                self.resultado_consulta_individual_numero,
                self.resultado_consulta_individual_tipo,
                self.resultado_consulta_individual_texto
            )
            
            if arquivo:
                self.status_var.set(f"PDF de consulta gerado: {os.path.basename(arquivo)}")
                messagebox.showinfo("PDF Gerado", f"O arquivo PDF foi salvo com sucesso em:\n{arquivo}")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao gerar PDF da consulta: {str(e)}")
            self.status_var.set("Erro ao gerar PDF")
    
    def gerar_pdf_consulta_lote(self, tipo):
        """Gerar um PDF com o resultado da consulta em lote"""
        if not self.resultados_consulta_lote or self.ultimo_tipo_consulta_lote != tipo:
            messagebox.showwarning("Atenção", f"Não há resultados de consulta em lote para processos {tipo}.")
            return
        
        try:
            arquivo = GeradorPDF.gerar_pdf_consulta_lote(tipo, self.resultados_consulta_lote)
            
            if arquivo:
                self.status_var.set(f"PDF de consulta em lote {tipo} gerado: {os.path.basename(arquivo)}")
                messagebox.showinfo("PDF Gerado", f"O arquivo PDF foi salvo com sucesso em:\n{arquivo}")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao gerar PDF da consulta em lote: {str(e)}")
            self.status_var.set("Erro ao gerar PDF")
    
    # Funções auxiliares
    def append_log(self, texto):
        """Adicionar texto ao log de cadastro"""
        self.log_text.config(state="normal")
        self.log_text.insert(tk.END, texto + "\n")
        self.log_text.see(tk.END)
        self.log_text.config(state="disabled")
    
    def update_resultado_text(self, texto):
        """Atualizar o texto de resultado (thread-safe)"""
        self.root.after(0, lambda: self._update_resultado_text_impl(texto))
    
    def _update_resultado_text_impl(self, texto):
        """Implementação da atualização do texto de resultado"""
        self.resultado_text.config(state="normal")
        self.resultado_text.insert(tk.END, texto)
        self.resultado_consulta_individual_texto += texto  # Armazenar para PDF
        self.resultado_text.see(tk.END)
        self.resultado_text.config(state="disabled")
    
    def append_exclusao_log(self, texto):
        """Adicionar texto ao log de exclusão"""
        self.exclusao_log.config(state="normal")
        self.exclusao_log.insert(tk.END, texto + "\n")
        self.exclusao_log.see(tk.END)
        self.exclusao_log.config(state="disabled")

if __name__ == "__main__":
    root = tk.Tk()
    app = CompiladorJuridicoGUI(root)
    root.mainloop()
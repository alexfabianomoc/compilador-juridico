import os
import logging
from datetime import datetime, timedelta
from flask import Flask, render_template, request, redirect, url_for, flash, session, send_file
from flask_session import Session
from flask_babel import Babel
from src.config import LISTA_TJ_FILE, LISTA_TRF_FILE, BASE_DIR
from src.utils.file_handler import carregar_arquivo_json, salvar_arquivo_json
from src.models.processo import Processo
from src.api.tjmg import consultar_processo_tjmg, consultar_todos_processos_tjmg
from src.api.trf6 import consultar_processo_trf6, consultar_todos_processos_trf6
from src.models.gerador_pdf_file import GeradorPDF
from excluir_processo import excluir_processo, excluir_todos_processos
import glob

# Configuração básica da aplicação
app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'fallback-key-segura')

# Configuração do Babel
app.config['BABEL_DEFAULT_LOCALE'] = 'pt_BR'
babel = Babel(app)

# Configurações de sessão
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_FILE_DIR'] = os.path.join(BASE_DIR, 'instance', 'flask_session')
app.config['SESSION_PERMANENT'] = False
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=1)

# Configurações de PDF
app.config['PDF_OUTPUT_DIR'] = os.path.join(BASE_DIR, 'instance', 'pdf_output')
app.config['MAX_PDF_AGE_HOURS'] = 24  # Tempo máximo que um PDF fica armazenado

# Inicializa extensões
Session(app)

# Configuração de logging
logging.basicConfig(level=logging.INFO)
app.logger.setLevel(logging.INFO)
handler = logging.FileHandler(os.path.join(BASE_DIR, 'instance', 'app.log'))
handler.setLevel(logging.INFO)
app.logger.addHandler(handler)

# Helpers e Filtros
# ==============================================

def criar_diretorios():
    """Garante que os diretórios necessários existam"""
    os.makedirs(app.config['SESSION_FILE_DIR'], exist_ok=True)
    os.makedirs(app.config['PDF_OUTPUT_DIR'], exist_ok=True)

@app.template_filter('strptime')
def strptime_filter(date_string, format='%Y-%m-%d'):
    """Converte string em objeto datetime"""
    try:
        return datetime.strptime(date_string, format)
    except (ValueError, TypeError):
        return None

@app.template_filter('strftime')
def strftime_filter(date_obj, format='%d/%m/%Y'):
    """Formata objeto datetime como string"""
    try:
        if isinstance(date_obj, str):
            date_obj = datetime.strptime(date_obj.split('T')[0], '%Y-%m-%d')
        return date_obj.strftime(format)
    except (ValueError, TypeError, AttributeError):
        return date_obj

@app.template_filter('format_date')
def format_date_filter(date_string):
    """Formata datas do DataJud"""
    try:
        if 'T' in str(date_string):
            date_string = str(date_string).split('T')[0]
        date_obj = datetime.strptime(date_string, '%Y-%m-%d')
        return date_obj.strftime('%d/%m/%Y')
    except (ValueError, TypeError, AttributeError):
        return date_string

@app.context_processor
def utility_processor():
    """Disponibiliza funções nos templates"""
    return dict(
        datetime=datetime,
        len=len,
        str=str,
        isinstance=isinstance,
        dict=dict,
        list=list
    )

# Rotas Principais
# ==============================================

@app.route('/')
def index():
    """Página inicial"""
    return render_template('index.html')

@app.route('/estatisticas')
def estatisticas():
    """Página de estatísticas"""
    try:
        processos_tj = carregar_arquivo_json(LISTA_TJ_FILE)
        processos_trf = carregar_arquivo_json(LISTA_TRF_FILE)
        return render_template('estatisticas.html', 
                            total=len(processos_tj) + len(processos_trf),
                            tj=processos_tj,
                            trf=processos_trf)
    except Exception as e:
        app.logger.error(f"Erro ao carregar estatísticas: {str(e)}")
        flash("Erro ao carregar estatísticas. Consulte os logs.", "error")
        return render_template('estatisticas.html', total=0, tj=[], trf=[])

@app.route('/manual')
def manual():
    """Página do manual"""
    return render_template('manual.html')

@app.route('/abrir_manual')
def abrir_manual():
    """Download do manual"""
    try:
        manual_path = os.path.join(BASE_DIR, "assets", "manual", "Manual_usuario_compilador_juridico_web.pdf")
        
        if os.path.exists(manual_path):
            return send_file(manual_path, as_attachment=False)
        else:
            flash("Manual local não encontrado. Redirecionando para versão online.", "warning")
            return redirect("https://github.com/alexfabianomoc/compilador-juridico/blob/web/assets/manual/Manual_usuario_compilador_juridico_web.pdf")
    except Exception as e:
        app.logger.error(f"Erro ao acessar manual: {str(e)}")
        flash("Erro ao acessar o manual. Consulte os logs.", "error")
        return redirect(url_for('manual'))

# Rotas de Processos
# ==============================================

@app.route('/cadastrar', methods=['GET', 'POST'])
def cadastrar():
    """Cadastro de processos"""
    if request.method == 'POST':
        numero = request.form.get('numero', '').strip()
        tipo = request.form.get('tipo', 'TJ')

        if not numero:
            flash('Informe o número do processo.', 'error')
            return redirect(url_for('cadastrar'))

        if not Processo.validar_numero(numero):
            flash('Número inválido. Deve conter exatamente 20 dígitos.', 'error')
            return redirect(url_for('cadastrar'))

        try:
            arquivo = LISTA_TJ_FILE if tipo == 'TJ' else LISTA_TRF_FILE
            lista = carregar_arquivo_json(arquivo)

            if numero in lista:
                flash(f"Processo {numero} já cadastrado.", "warning")
            else:
                lista.append(numero)
                if salvar_arquivo_json(arquivo, lista):
                    flash(f"Processo {numero} cadastrado com sucesso.", "success")
                    app.logger.info(f"Processo {numero} cadastrado ({tipo})")
                else:
                    flash("Erro ao salvar o processo.", "error")
        except Exception as e:
            app.logger.error(f"Erro ao cadastrar processo {numero}: {str(e)}")
            flash("Erro ao cadastrar processo. Consulte os logs.", "error")

        return redirect(url_for('cadastrar'))
    
    return render_template('cadastrar.html')

@app.route('/consultar', methods=['GET', 'POST'])
def consultar():
    """Consulta de processos"""
    if request.method == 'POST':
        numero = request.form.get('numero', '').strip()
        tipo = request.form.get('tipo', 'TJ')

        if not numero:
            flash('Informe o número do processo.', 'error')
            return redirect(url_for('consultar'))

        if not Processo.validar_numero(numero):
            flash('Número inválido. Deve conter exatamente 20 dígitos.', 'error')
            return redirect(url_for('consultar'))

        try:
            app.logger.info(f"Consultando processo {tipo} {numero}...")
            
            resultado = consultar_processo_tjmg(numero) if tipo == 'TJ' else consultar_processo_trf6(numero)
            
            if isinstance(resultado, dict) and "erro" in resultado:
                flash(f"Erro na consulta: {resultado['erro']}", "error")
                return redirect(url_for('consultar'))
            
            if not isinstance(resultado, dict) or "hits" not in resultado:
                flash("Formato de resposta inválido da API.", "error")
                return redirect(url_for('consultar'))
            
            # Armazenar resultado na sessão (apenas referência)
            session['ultimo_resultado'] = {
                'numero': numero,
                'tipo': tipo,
                'timestamp': datetime.now().isoformat()
            }
            # Salvar dados completos em cache
            cache_id = f"consulta_{tipo}_{numero}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
            salvar_arquivo_json(os.path.join(app.config['PDF_OUTPUT_DIR'], f"{cache_id}.json"), resultado)

            return redirect(url_for('resultado'))
            
        except Exception as e:
            app.logger.error(f"Erro na consulta do processo {numero}: {str(e)}")
            flash("Erro ao consultar processo. Consulte os logs.", "error")
            return redirect(url_for('consultar'))

    return render_template('consultar.html')

@app.route('/resultado')
def resultado():
    """Resultado de consulta individual"""
    if 'ultimo_resultado' not in session:
        flash("Nenhuma consulta individual realizada.", "warning")
        return redirect(url_for('consultar'))
    
    cache_id = f"consulta_{session['ultimo_resultado']['tipo']}_{session['ultimo_resultado']['numero']}_*"
    cache_files = glob.glob(os.path.join(app.config['PDF_OUTPUT_DIR'], cache_id))
    
    if not cache_files:
        flash("Dados da consulta não encontrados.", "error")
        return redirect(url_for('consultar'))
    
    dados = carregar_arquivo_json(cache_files[0])
    return render_template('resultado.html', 
                         numero=session['ultimo_resultado']['numero'],
                         tipo=session['ultimo_resultado']['tipo'],
                         resultado=dados,
                         todos=False)

@app.route('/consultar_todos/<tipo>')
def consultar_todos(tipo):
    """Consulta em lote de processos"""
    if tipo not in ['TJ', 'TRF']:
        flash('Tipo inválido.', 'error')
        return redirect(url_for('consultar'))

    try:
        app.logger.info(f"Iniciando consulta em lote para processos {tipo}")
        
        resultados = consultar_todos_processos_tjmg() if tipo == 'TJ' else consultar_todos_processos_trf6()
        
        if not isinstance(resultados, dict):
            flash("Formato de resposta inválido da API.", "error")
            return redirect(url_for('consultar'))
        
        if not resultados:
            flash(f"Nenhum processo {tipo} encontrado.", "warning")
            return redirect(url_for('consultar'))

        # Armazenar referência na sessão
        session['ultimo_resultado_lote'] = {
            'tipo': tipo,
            'timestamp': datetime.now().isoformat()
        }
        # Salvar dados completos em cache
        cache_id = f"consulta_lote_{tipo}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        salvar_arquivo_json(os.path.join(app.config['PDF_OUTPUT_DIR'], f"{cache_id}.json"), resultados)

        return redirect(url_for('resultado_lote', tipo=tipo))
        
    except Exception as e:
        app.logger.error(f"Erro na consulta em lote {tipo}: {str(e)}")
        flash("Erro ao consultar processos. Consulte os logs.", "error")
        return redirect(url_for('consultar'))

@app.route('/resultado_lote/<tipo>')
def resultado_lote(tipo):
    """Resultado de consulta em lote"""
    if 'ultimo_resultado_lote' not in session or session['ultimo_resultado_lote']['tipo'] != tipo:
        flash(f"Nenhuma consulta em lote {tipo} realizada.", "warning")
        return redirect(url_for('consultar'))
    
    cache_id = f"consulta_lote_{tipo}_*"
    cache_files = glob.glob(os.path.join(app.config['PDF_OUTPUT_DIR'], cache_id))
    cache_files.sort(reverse=True)  # Pega o mais recente
    
    if not cache_files:
        flash("Dados da consulta não encontrados.", "error")
        return redirect(url_for('consultar'))
    
    dados = carregar_arquivo_json(cache_files[0])
    return render_template('resultado.html',
                         resultados=dados,
                         tipo=tipo,
                         todos=True)

@app.route('/excluir', methods=['GET', 'POST'])
def excluir():
    """Exclusão de processos"""
    if request.method == 'POST':
        numero = request.form.get('numero', '').strip()
        tipo = request.form.get('tipo', 'TJ')
        todos = request.form.get('todos')

        try:
            if todos:
                # Modificado para usar confirmar=False já que temos confirmação via interface web
                if excluir_todos_processos(tipo, confirmar=False):
                    flash(f'Todos os processos {tipo} excluídos.', 'success')
                    app.logger.info(f"Todos os processos {tipo} excluídos")
                else:
                    flash(f'Erro ao excluir processos {tipo}.', 'error')
            elif numero:
                if not Processo.validar_numero(numero):
                    flash('Número inválido.', 'error')
                # Modificado para incluir excluir_resultados=True
                elif excluir_processo(numero, tipo, excluir_resultados=True):
                    flash(f'Processo {numero} ({tipo}) excluído.', 'success')
                    app.logger.info(f"Processo {numero} ({tipo}) excluído")
                else:
                    flash(f'Erro ao excluir processo {numero}.', 'error')
            else:
                flash('Informe o número ou selecione "Excluir todos".', 'warning')
        except Exception as e:
            app.logger.error(f"Erro na exclusão: {str(e)}")
            flash("Erro na exclusão. Consulte os logs.", "error")

        return redirect(url_for('excluir'))
    
    return render_template('excluir.html')

# Rotas de PDF
# ==============================================

@app.route('/pdf/estatisticas')
def gerar_pdf_estatisticas():
    """Gera PDF de estatísticas"""
    try:
        processos_tj = carregar_arquivo_json(LISTA_TJ_FILE)
        processos_trf = carregar_arquivo_json(LISTA_TRF_FILE)
        
        pdf_path = GeradorPDF.gerar_pdf_estatisticas(processos_tj, processos_trf)
        
        if pdf_path:
            flash("PDF gerado com sucesso.", "success")
            return send_file(
                pdf_path,
                as_attachment=True,
                download_name=f"estatisticas_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            )
        flash("Erro ao gerar PDF.", "error")
    except Exception as e:
        app.logger.error(f"Erro ao gerar PDF de estatísticas: {str(e)}")
        flash("Erro ao gerar PDF. Consulte os logs.", "error")
    
    return redirect(url_for('estatisticas'))

@app.route('/pdf/consulta_individual')
def gerar_pdf_consulta_individual():
    """Gera PDF de consulta individual"""
    try:        
        if 'ultimo_resultado' not in session:
            flash("Nenhuma consulta individual encontrada.", "warning")
            return redirect(url_for('consultar'))
        
        cache_id = f"consulta_{session['ultimo_resultado']['tipo']}_{session['ultimo_resultado']['numero']}_*"
        cache_files = glob.glob(os.path.join(app.config['PDF_OUTPUT_DIR'], cache_id))
        
        if not cache_files:
            flash("Dados da consulta não encontrados.", "error")
            return redirect(url_for('consultar'))
        
        dados = carregar_arquivo_json(cache_files[0])
        pdf_path = GeradorPDF.gerar_pdf_consulta_individual(
            session['ultimo_resultado']['numero'],
            session['ultimo_resultado']['tipo'],
            dados
        )
        
        if pdf_path:
            flash("PDF gerado com sucesso.", "success")
            return send_file(
                pdf_path,
                as_attachment=True,
                download_name=f"consulta_{session['ultimo_resultado']['tipo']}_{session['ultimo_resultado']['numero']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            )
        flash("Erro ao gerar PDF.", "error")
    except Exception as e:
        app.logger.error(f"Erro ao gerar PDF de consulta individual: {str(e)}")
        flash("Erro ao gerar PDF. Consulte os logs.", "error")
    
    return redirect(url_for('consultar'))

@app.route('/pdf/consulta_lote/<tipo>')
def gerar_pdf_consulta_lote(tipo):
    """Gera PDF de consulta em lote"""
    try:        
        if 'ultimo_resultado_lote' not in session or session['ultimo_resultado_lote']['tipo'] != tipo:
            flash(f"Nenhuma consulta em lote {tipo} encontrada.", "warning")
            return redirect(url_for('consultar'))
        
        cache_id = f"consulta_lote_{tipo}_*"
        cache_files = glob.glob(os.path.join(app.config['PDF_OUTPUT_DIR'], cache_id))
        cache_files.sort(reverse=True)
        
        if not cache_files:
            flash("Dados da consulta não encontrados.", "error")
            return redirect(url_for('consultar'))
        
        dados = carregar_arquivo_json(cache_files[0])
        pdf_path = GeradorPDF.gerar_pdf_consulta_lote(tipo, dados)
        
        if pdf_path:
            flash(f"PDF da consulta em lote {tipo} gerado.", "success")
            return send_file(
                pdf_path,
                as_attachment=True,
                download_name=f"consulta_lote_{tipo}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            )
        flash("Erro ao gerar PDF.", "error")
    except Exception as e:
        app.logger.error(f"Erro ao gerar PDF de consulta em lote: {str(e)}")
        flash("Erro ao gerar PDF. Consulte os logs.", "error")
    
    return redirect(url_for('consultar'))

# Manutenção
# ==============================================

@app.before_request
def limpar_arquivos_antigos():
    """Limpa arquivos temporários antigos"""
    try:
        agora = datetime.now()
        limite = agora - timedelta(hours=app.config['MAX_PDF_AGE_HOURS'])
        
        # Limpar PDFs antigos
        for pdf in glob.glob(os.path.join(app.config['PDF_OUTPUT_DIR'], '*.pdf')):
            if datetime.fromtimestamp(os.path.getmtime(pdf)) < limite:
                os.remove(pdf)
                
        # Limpar cache de consultas antigas
        for json_file in glob.glob(os.path.join(app.config['PDF_OUTPUT_DIR'], '*.json')):
            if datetime.fromtimestamp(os.path.getmtime(json_file)) < limite:
                os.remove(json_file)
    except Exception as e:
        app.logger.error(f"Erro ao limpar arquivos temporários: {str(e)}")

# Inicialização
# ==============================================

if __name__ == '__main__':
    criar_diretorios()
    app.run(debug=True)
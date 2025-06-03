"""
Módulo para geração de arquivos PDF do Compilador Jurídico - Versão Web
Esta versão foi adaptada para integração com Flask 
"""

import os
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.platypus.flowables import HRFlowable
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER
from flask import current_app
from flask_babel import _

try:
    from flask_babel import _
except ImportError:
    # Fallback para quando o Babel não estiver disponível
    def _(text):
        return text

class GeradorPDF:
    """Classe responsável por gerar relatórios PDF em aplicações Flask"""
    
    @staticmethod
    def _criar_estilos_padrao():
        """Cria e retorna os estilos padrão para os documentos PDF"""
        styles = getSampleStyleSheet()
        
        # Estilos personalizados
        styles.add(ParagraphStyle(
            name='TituloPrincipal',
            parent=styles['Heading1'],
            alignment=TA_CENTER,
            fontSize=16,
            spaceAfter=12,
            fontName='Helvetica-Bold'
        ))
        
        styles.add(ParagraphStyle(
            name='TituloSecao',
            parent=styles['Heading2'],
            fontSize=14,
            spaceAfter=10,
            fontName='Helvetica-Bold',
            textColor=colors.darkblue
        ))
        
        styles.add(ParagraphStyle(
            name='Subtitulo',
            parent=styles['Heading3'],
            fontSize=12,
            spaceAfter=8,
            textColor=colors.darkblue
        ))
        
        styles.add(ParagraphStyle(
            name='ItemLista',
            parent=styles['Normal'],
            fontSize=10,
            leftIndent=20,
            spaceAfter=5,
            bulletIndent=10
        ))
        
        styles.add(ParagraphStyle(
            name='Rodape',
            parent=styles['Normal'],
            fontSize=8,
            alignment=TA_CENTER,
            textColor=colors.grey
        ))
        
        return styles
    
    @staticmethod
    def _configurar_documento(output_path):
        """Configura o documento PDF com metadados e margens"""
        doc = SimpleDocTemplate(
            output_path,
            pagesize=A4,
            rightMargin=36,
            leftMargin=36,
            topMargin=36,
            bottomMargin=36,
            title=_("Relatório do Compilador Jurídico"),
            author="Compilador Jurídico",
            subject=_("Relatório de processos jurídicos")
        )
        return doc
    
    @staticmethod
    def _adicionar_cabecalho(conteudo, titulo):
        """Adiciona cabeçalho padrão ao conteúdo do PDF"""
        styles = GeradorPDF._criar_estilos_padrao()
        
        conteudo.append(Paragraph(_("Compilador Jurídico"), styles['TituloPrincipal']))
        conteudo.append(Paragraph(titulo, styles['TituloSecao']))
        conteudo.append(Paragraph(
            _("Gerado em: {date}").format(date=datetime.now().strftime('%d/%m/%Y às %H:%M:%S')),
            styles['Subtitulo']
        ))
        conteudo.append(HRFlowable(
            width="100%", 
            thickness=1, 
            color=colors.darkblue, 
            spaceBefore=10, 
            spaceAfter=15
        ))
        
        return conteudo
    
    @staticmethod
    def _adicionar_rodape(conteudo, nova_pagina=False):
        """
        Adiciona rodapé padrão ao conteúdo do PDF
        
        Args:
            conteudo: Lista de elementos do PDF
            nova_pagina: Se True, adiciona quebra de página antes do rodapé
        """
        styles = GeradorPDF._criar_estilos_padrao()
        
        if nova_pagina:
            conteudo.append(PageBreak())
        else:
            # Adiciona apenas um espaço antes do rodapé
            conteudo.append(Spacer(1, 0.5*inch))
        
        conteudo.append(HRFlowable(
            width="100%", 
            thickness=0.5, 
            color=colors.lightgrey, 
            spaceBefore=10
        ))
        conteudo.append(Paragraph(
            _("Compilador Jurídico - © {year}").format(year=datetime.now().year),
            styles['Rodape']
        ))
        
        return conteudo
    
    @staticmethod
    def _gerar_nome_arquivo(titulo):
        """Gera um nome de arquivo único baseado no título e timestamp"""
        nome_sanitizado = titulo.lower().replace(" ", "_").replace("/", "-")
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        return f"{nome_sanitizado}_{timestamp}.pdf"
    
    @staticmethod
    def gerar_pdf(conteudo, titulo="Relatório", rodape_nova_pagina=False):
        """
        Gera um arquivo PDF com o conteúdo fornecido
        
        Args:
            conteudo (list): Lista de elementos Flowable do ReportLab
            titulo (str): Título do documento
            rodape_nova_pagina (bool): Se True, coloca rodapé em nova página
            
        Returns:
            str: Caminho para o arquivo PDF gerado ou None em caso de erro
        """
        try:
            # Verificar e criar diretório de saída
            output_dir = os.path.join(current_app.config['PDF_OUTPUT_DIR'])
            os.makedirs(output_dir, exist_ok=True)
            
            # Gerar caminho completo do arquivo
            filename = GeradorPDF._gerar_nome_arquivo(titulo)
            filepath = os.path.join(output_dir, filename)
            
            # Configurar documento
            doc = GeradorPDF._configurar_documento(filepath)
            
            # Adicionar cabeçalho e rodapé
            conteudo_completo = []
            GeradorPDF._adicionar_cabecalho(conteudo_completo, titulo)
            conteudo_completo.extend(conteudo)
            GeradorPDF._adicionar_rodape(conteudo_completo, nova_pagina=rodape_nova_pagina)
            
            # Construir PDF
            doc.build(conteudo_completo)
            
            current_app.logger.info(f"PDF gerado com sucesso: {filepath}")
            return filepath
            
        except Exception as e:
            current_app.logger.error(f"Erro ao gerar PDF: {str(e)}", exc_info=True)
            return None
    
    @staticmethod
    def gerar_pdf_estatisticas(processos_tj, processos_trf):
        """Gera um PDF com as estatísticas dos processos"""
        styles = GeradorPDF._criar_estilos_padrao()
        conteudo = []
        
        # Título da seção
        conteudo.append(Paragraph(_("Estatísticas de Processos"), styles['TituloSecao']))
        conteudo.append(Spacer(1, 0.2*inch))
        
        # Tabela de totais
        dados_tabela = [
            [_("Tipo"), _("Quantidade")],
            [_("Processos TJ"), str(len(processos_tj))],
            [_("Processos TRF"), str(len(processos_trf))],
            [_("Total"), str(len(processos_tj) + len(processos_trf))]
        ]
        
        tabela = Table(dados_tabela, colWidths=[3*inch, 1.5*inch])
        tabela.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#003366")),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, -1), (-1, -1), colors.lightgrey),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('ROWBACKGROUNDS', (0, 1), (-1, -2), [colors.white, colors.whitesmoke])
        ]))
        
        conteudo.append(tabela)
        conteudo.append(Spacer(1, 0.3*inch))
        
        # Últimos processos cadastrados
        if processos_tj:
            conteudo.append(Paragraph(_("Últimos Processos TJ Cadastrados:"), styles['Subtitulo']))
            for processo in processos_tj[-5:]:
                conteudo.append(Paragraph(f"• {processo}", styles['ItemLista']))
            conteudo.append(Spacer(1, 0.2*inch))
        
        if processos_trf:
            conteudo.append(Paragraph(_("Últimos Processos TRF Cadastrados:"), styles['Subtitulo']))
            for processo in processos_trf[-5:]:
                conteudo.append(Paragraph(f"• {processo}", styles['ItemLista']))
        
        return GeradorPDF.gerar_pdf(conteudo, _("Estatísticas de Processos"))
    
    @staticmethod
    def gerar_pdf_consulta_individual(numero, tipo, dados_processo):
        """Gera um PDF com o resultado da consulta individual de um processo"""
        styles = GeradorPDF._criar_estilos_padrao()
        conteudo = []
        
        # Log para debug (opcional - remover em produção)
        if current_app:
            current_app.logger.info(f"Dados recebidos para {tipo} {numero}: {type(dados_processo)}")
        
        # Extrair dados do processo da estrutura da API do DataJud
        processo_data = None
        
        try:
            # Se os dados vieram da API diretamente (estrutura com "hits")
            if isinstance(dados_processo, dict) and "hits" in dados_processo:
                hits = dados_processo.get("hits", {}).get("hits", [])
                if hits:
                    # Pegar o primeiro resultado (processo mais relevante)
                    processo_data = hits[0].get("_source", {})
                else:
                    # Nenhum processo encontrado
                    conteudo.append(Paragraph(_("Processo não encontrado nas consultas."), styles['Normal']))
                    return GeradorPDF.gerar_pdf(conteudo, 
                        _("Consulta Individual {tipo} {numero}").format(tipo=tipo, numero=numero))
            else:
                # Dados já processados
                processo_data = dados_processo
                
        except Exception as e:
            if current_app:
                current_app.logger.error(f"Erro ao extrair dados do processo: {str(e)}")
            processo_data = {}
        
        if not processo_data:
            conteudo.append(Paragraph(_("Nenhum dado do processo disponível."), styles['Normal']))
            return GeradorPDF.gerar_pdf(conteudo, 
                _("Consulta Individual {tipo} {numero}").format(tipo=tipo, numero=numero))
        
        # Título do documento
        conteudo.append(Paragraph(
            _("Consulta Individual - Processo {tipo} {numero}").format(tipo=tipo, numero=numero),
            styles['TituloSecao']
        ))
        conteudo.append(Spacer(1, 0.2*inch))
        
        # Função auxiliar para extrair valor com múltiplas tentativas
        def extrair_valor(dados, *chaves_possiveis):
            """Tenta extrair valor usando diferentes chaves possíveis"""
            if not dados:
                return _("Não informado")
            
            for chave in chaves_possiveis:
                if isinstance(chave, str):
                    if chave in dados:
                        valor = dados[chave]
                        if isinstance(valor, dict) and 'nome' in valor:
                            return valor['nome']
                        elif valor:
                            return str(valor)
                elif isinstance(chave, tuple):  # Para navegação aninhada como ('classe', 'nome')
                    try:
                        valor = dados
                        for sub_chave in chave:
                            valor = valor[sub_chave]
                        return str(valor) if valor else _("Não informado")
                    except (KeyError, TypeError):
                        continue
            
            return _("Não informado")
        
        # Função auxiliar para extrair lista de assuntos
        def extrair_assuntos(dados):
            """Extrai assuntos de diferentes estruturas possíveis"""
            assuntos_possiveis = ['assuntos', 'assunto', 'assuntoPrincipal']
            for campo in assuntos_possiveis:
                if campo in dados:
                    assunto_data = dados[campo]
                    if isinstance(assunto_data, list) and assunto_data:
                        primeiro = assunto_data[0]
                        if isinstance(primeiro, dict):
                            return primeiro.get('nome', str(primeiro))
                        return str(primeiro)
                    elif isinstance(assunto_data, dict):
                        return assunto_data.get('nome', str(assunto_data))
                    elif assunto_data:
                        return str(assunto_data)
            return _("Não informado")
        
        # Informações básicas
        conteudo.append(Paragraph(_("Informações Básicas"), styles['Subtitulo']))
        
        if tipo == "TJ":
            info_items = [
                (_("Número do Processo"), numero),
                (_("Tribunal"), extrair_valor(processo_data, 'tribunal', 'tribunalNome')),
                (_("Data de Ajuizamento"), extrair_valor(processo_data, 'dataAjuizamento', 'dataDistribuicao', 'dataAutuacao')),
                (_("Classe"), extrair_valor(processo_data, ('classe', 'nome'), 'classeProcessual')),
                (_("Assunto"), extrair_assuntos(processo_data)),
                (_("Formato"), extrair_valor(processo_data, ('formato', 'nome'), 'tipoProcesso')),
                (_("Vara/Órgão"), extrair_valor(processo_data, ('orgaoJulgador', 'nome'), 'vara', 'orgaoJulgador')),
                (_("Sistema"), extrair_valor(processo_data, ('sistema', 'nome'), 'sistema')),
                (_("Grau"), extrair_valor(processo_data, 'grau', 'instancia')),
                (_("Nível de Sigilo"), extrair_valor(processo_data, 'nivelSigilo')),
            ]
        else:  # TRF
            info_items = [
                (_("Número do Processo"), numero),
                (_("Classe Processual"), extrair_valor(processo_data, ('classe', 'nome'), 'classeProcessual')),
                (_("Data de Ajuizamento"), extrair_valor(processo_data, 'dataAjuizamento', 'dataDistribuicao', 'dataAutuacao')),
                (_("Assunto"), extrair_assuntos(processo_data)),
                (_("Formato"), extrair_valor(processo_data, ('formato', 'nome'), 'tipoProcesso')),
                (_("Órgão Julgador"), extrair_valor(processo_data, ('orgaoJulgador', 'nome'), 'vara', 'secaoJudiciaria')),
                (_("Tribunal"), extrair_valor(processo_data, 'tribunal', 'tribunalNome')),
                (_("Sistema"), extrair_valor(processo_data, ('sistema', 'nome'), 'sistema')),
                (_("Grau"), extrair_valor(processo_data, 'grau', 'instancia')),
                (_("Nível de Sigilo"), extrair_valor(processo_data, 'nivelSigilo')),
            ]
        
        # Remover itens com "Não informado"
        info_items = [(label, valor) for label, valor in info_items 
                    if valor and valor != _("Não informado") and str(valor).strip()]
        
        # Criar tabela de informações básicas
        if info_items:
            dados_tabela = [[_("Campo"), _("Valor")]]
            for item in info_items:
                dados_tabela.append([item[0], str(item[1])])
            
            tabela = Table(dados_tabela, colWidths=[2.5*inch, 3.5*inch])
            tabela.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#003366")),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('ALIGN', (0, 0), (0, -1), 'LEFT'),
                ('ALIGN', (1, 0), (1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
                ('GRID', (0, 0), (-1, -1), 1, colors.lightgrey),
                ('ROWBACKGROUNDS', (1, 1), (-1, -1), [colors.white, colors.whitesmoke])
            ]))
            
            conteudo.append(tabela)
            conteudo.append(Spacer(1, 0.3*inch))
        
        # Situação atual (baseada na última atualização)
        conteudo.append(Paragraph(_("Situação Atual"), styles['Subtitulo']))
        
        # Extrair data da última atualização
        ultima_atualizacao = extrair_valor(processo_data, 'dataHoraUltimaAtualizacao', 'ultimaAtualizacao')
        if ultima_atualizacao != _("Não informado"):
            try:
                # Formatear data se necessário
                if 'T' in str(ultima_atualizacao):
                    data_obj = datetime.strptime(ultima_atualizacao.split('T')[0], '%Y-%m-%d')
                    ultima_atualizacao = data_obj.strftime('%d/%m/%Y')
            except (ValueError, TypeError, AttributeError):
                pass
        
        situacao_items = [
            (_("Última Atualização"), ultima_atualizacao),
            (_("ID do Processo"), extrair_valor(processo_data, 'id')),
        ]
        
        # Remover itens vazios
        situacao_items = [(label, valor) for label, valor in situacao_items 
                        if valor and valor != _("Não informado") and str(valor).strip()]
        
        if situacao_items:
            dados_situacao = [[_("Campo"), _("Valor")]]
            for item in situacao_items:
                dados_situacao.append([item[0], str(item[1])])
            
            tabela_situacao = Table(dados_situacao, colWidths=[2.5*inch, 3.5*inch])
            tabela_situacao.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#006600")),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('ALIGN', (0, 0), (0, -1), 'LEFT'),
                ('ALIGN', (1, 0), (1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
                ('GRID', (0, 0), (-1, -1), 1, colors.lightgrey),
                ('ROWBACKGROUNDS', (1, 1), (-1, -1), [colors.white, colors.whitesmoke])
            ]))
            
            conteudo.append(tabela_situacao)
            conteudo.append(Spacer(1, 0.3*inch))
        
        # Movimentações (se disponíveis)
        movimentos = processo_data.get('movimentos', [])
        if movimentos and isinstance(movimentos, list):
            conteudo.append(Paragraph(_("Movimentações Recentes"), styles['Subtitulo']))
            
            # Tentar ordenar movimentações por data (mais recente primeiro)
            try:
                movimentos = sorted(
                    movimentos, 
                    key=lambda x: x.get("dataHora", x.get("data", x.get("timestamp", ""))), 
                    reverse=True
                )
            except (ValueError, TypeError, KeyError, AttributeError):
                pass  # Se não conseguir ordenar, manter ordem original
            
            # Limitar às 20 mais recentes e criar tabela
            movimentos_recentes = movimentos[:20]
            
            dados_mov = [[_("Data"), _("Movimento")]]
            for mov in movimentos_recentes:
                if isinstance(mov, dict):
                    data = mov.get("dataHora", mov.get("data", mov.get("timestamp", _("Data desconhecida"))))
                    nome = mov.get("nome", mov.get("descricao", mov.get("movimento", _("Movimento sem descrição"))))
                    codigo = mov.get("codigo", "")
                    
                    # Formatar data
                    if data and data != _("Data desconhecida"):
                        try:
                            if 'T' in str(data):
                                data_formatada = datetime.strptime(data.split('T')[0], '%Y-%m-%d').strftime('%d/%m/%Y')
                            else:
                                data_formatada = str(data)
                        except (ValueError, TypeError, KeyError, AttributeError):
                            data_formatada = str(data)
                    else:
                        data_formatada = _("Data desconhecida")
                    
                    # Formatar movimento
                    if codigo:
                        movimento_formatado = f"[{codigo}] {nome}"
                    else:
                        movimento_formatado = nome
                    
                    dados_mov.append([data_formatada, movimento_formatado])
            
            if len(dados_mov) > 1:  # Tem dados além do cabeçalho
                tabela_mov = Table(dados_mov, colWidths=[1.5*inch, 4.5*inch])
                tabela_mov.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#333366")),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                    ('ALIGN', (0, 0), (0, -1), 'LEFT'),
                    ('ALIGN', (1, 0), (1, -1), 'LEFT'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, -1), 8),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
                    ('GRID', (0, 0), (-1, -1), 1, colors.lightgrey),
                    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.whitesmoke]),
                    ('VALIGN', (0, 0), (-1, -1), 'TOP')
                ]))
                
                conteudo.append(tabela_mov)
                conteudo.append(Spacer(1, 0.2*inch))
        
        # Informações complementares se disponíveis
        outros_campos = [
            ('complementosTabelados', _("Complementos Tabelados")),
            ('observacoes', _("Observações")),
            ('recursos', _("Recursos")),
            ('incidentes', _("Incidentes"))
        ]
        
        for campo, titulo in outros_campos:
            if campo in processo_data and processo_data[campo]:
                conteudo.append(Paragraph(titulo, styles['Subtitulo']))
                
                dados_campo = processo_data[campo]
                if isinstance(dados_campo, list):
                    for item in dados_campo[:5]:  # Limitar a 5 itens
                        if isinstance(item, dict):
                            descricao = item.get("descricao", item.get("nome", item.get("valor", str(item))))
                        else:
                            descricao = str(item)
                        conteudo.append(Paragraph(f"• {descricao}", styles['ItemLista']))
                elif isinstance(dados_campo, str):
                    conteudo.append(Paragraph(dados_campo, styles['Normal']))
                
                conteudo.append(Spacer(1, 0.2*inch))
        
        # Adicionar resumo final
        conteudo.append(Paragraph(_("Resumo"), styles['Subtitulo']))
        total_movimentos = len(movimentos) if movimentos else 0
        conteudo.append(Paragraph(
            _("Este processo possui {total} movimentações registradas.").format(total=total_movimentos),
            styles['Normal']
        ))
        
        if total_movimentos > 20:
            conteudo.append(Paragraph(
                _("Apenas as 20 movimentações mais recentes são exibidas neste relatório."),
                styles['ItemLista']
            ))
        
        return GeradorPDF.gerar_pdf(
            conteudo, 
            _("Consulta Individual {tipo} {numero}").format(tipo=tipo, numero=numero)
        )
    
    @staticmethod
    def gerar_pdf_consulta_lote(tipo, resultados):
        """Gera um PDF com o resultado da consulta em lote de processos"""
        styles = GeradorPDF._criar_estilos_padrao()
        conteudo = []
        
        # Título do documento
        conteudo.append(Paragraph(
            _("Consulta em Lote - Processos {tipo}").format(tipo=tipo),
            styles['TituloSecao']
        ))
        conteudo.append(Spacer(1, 0.2*inch))
        
        # Resumo da consulta
        conteudo.append(Paragraph(
            _("Total de processos consultados: {total}").format(total=len(resultados)),
            styles['Normal']
        ))
        conteudo.append(Spacer(1, 0.3*inch))
        
        # Configurar colunas baseadas no tipo
        if tipo == "TJ":
            colunas = [
                (_("Número"), 2.5*inch),
                (_("Tribunal"), 1*inch),
                (_("Última Atualização"), 1.2*inch),
                (_("Status"), 1.3*inch)
            ]
        else:  # TRF
            colunas = [
                (_("Número"), 2.2*inch),
                (_("Órgão Julgador"), 2*inch),
                (_("Última Atualização"), 1.2*inch),
                (_("Último Movimento"), 2.1*inch)
            ]
        
        # Criar cabeçalho da tabela
        dados_tabela = [[col[0] for col in colunas]]
        larguras_colunas = [col[1] for col in colunas]
        
        # Contadores para estatísticas
        encontrados = 0
        nao_encontrados = 0
        com_erro = 0
        
        # Preencher dados da tabela
        for numero, dados_api in resultados.items():
            linha = [numero]  # Primeira coluna sempre é o número
            
            try:
                # Verificar se há erro na consulta
                if isinstance(dados_api, dict) and "erro" in dados_api:
                    com_erro += 1
                    if tipo == "TJ":
                        linha.extend([_("Erro"), _("Erro"), _("Erro na consulta")])
                    else:
                        linha.extend([_("Erro"), _("Erro"), _("Erro na consulta")])
                
                # Verificar se há hits na resposta
                elif (isinstance(dados_api, dict) and 
                    'hits' in dados_api and 
                    isinstance(dados_api['hits'], dict) and
                    'hits' in dados_api['hits'] and 
                    isinstance(dados_api['hits']['hits'], list) and
                    len(dados_api['hits']['hits']) > 0):
                    
                    encontrados += 1
                    source = dados_api['hits']['hits'][0].get('_source', {})
                    
                    if tipo == "TJ":
                        # Tribunal
                        tribunal = source.get('tribunal', _("Não informado"))
                        
                        # Última atualização
                        ultima_atualizacao = _("Não informado")
                        if 'dataHoraUltimaAtualizacao' in source:
                            try:
                                data_str = source['dataHoraUltimaAtualizacao']
                                if 'T' in str(data_str):
                                    data_obj = datetime.strptime(data_str.split('T')[0], '%Y-%m-%d')
                                    ultima_atualizacao = data_obj.strftime('%d/%m/%Y')
                                else:
                                    ultima_atualizacao = str(data_str)
                            except (ValueError, TypeError, KeyError, AttributeError):
                                ultima_atualizacao = str(data_str)
                        
                        # Status baseado nos movimentos
                        status = _("Em andamento")
                        if 'movimentos' in source and isinstance(source['movimentos'], list):
                            movimentos = source['movimentos']
                            try:
                                movimentos_ordenados = sorted(movimentos, key=lambda x: x.get('dataHora', '1900-01-01'), reverse=True)
                                for mov in movimentos_ordenados:
                                    codigo_mov = mov.get('codigo')
                                    if codigo_mov == 22:
                                        status = _("Arquivado definitivamente")
                                        break
                                    elif codigo_mov == 848:
                                        status = _("Transitado em julgado")
                                        break
                                    elif codigo_mov == 246:
                                        status = _("Arquivado definitivamente")
                                        break
                            except (ValueError, TypeError, KeyError, AttributeError):
                                pass
                        
                        linha.extend([tribunal, ultima_atualizacao, status])
                    
                    else:  # TRF
                        # Órgão julgador
                        orgao_julgador = _("Não informado")
                        if 'orgaoJulgador' in source:
                            orgao = source['orgaoJulgador']
                            if isinstance(orgao, dict):
                                nome_orgao = orgao.get('nome', '')
                                if len(nome_orgao) > 40:
                                    orgao_julgador = nome_orgao[:37] + "..."
                                else:
                                    orgao_julgador = nome_orgao
                            elif isinstance(orgao, str):
                                orgao_julgador = orgao
                        
                        # Última atualização
                        ultima_atualizacao = _("Não informado")
                        if 'dataHoraUltimaAtualizacao' in source:
                            try:
                                data_str = source['dataHoraUltimaAtualizacao']
                                if 'T' in str(data_str):
                                    data_obj = datetime.strptime(data_str.split('T')[0], '%Y-%m-%d')
                                    ultima_atualizacao = data_obj.strftime('%d/%m/%Y')
                                else:
                                    ultima_atualizacao = str(data_str)
                            except (ValueError, TypeError, KeyError, AttributeError):
                                ultima_atualizacao = str(data_str)
                        
                        # Último movimento
                        ultimo_movimento = _("Não informado")
                        if 'movimentos' in source and isinstance(source['movimentos'], list) and source['movimentos']:
                            try:
                                movimentos_ordenados = sorted(source['movimentos'], key=lambda x: x.get('dataHora', '1900-01-01'), reverse=True)
                                ultimo_mov = movimentos_ordenados[0]
                                codigo = ultimo_mov.get('codigo', '')
                                nome = ultimo_mov.get('nome', '')
                                
                                if codigo and nome:
                                    movimento_texto = f"[{codigo}] {nome}"
                                    if len(movimento_texto) > 35:
                                        ultimo_movimento = movimento_texto[:32] + "..."
                                    else:
                                        ultimo_movimento = movimento_texto
                                elif nome:
                                    if len(nome) > 35:
                                        ultimo_movimento = nome[:32] + "..."
                                    else:
                                        ultimo_movimento = nome
                            except (ValueError, TypeError, KeyError, AttributeError):
                                pass
                        
                        linha.extend([orgao_julgador, ultima_atualizacao, ultimo_movimento])
                
                else:
                    # Processo não encontrado
                    nao_encontrados += 1
                    if tipo == "TJ":
                        linha.extend([_("Não informado"), _("Não informado"), _("Não encontrado")])
                    else:
                        linha.extend([_("Não informado"), _("Não informado"), _("Não encontrado")])
                    
            except Exception as e:
                com_erro += 1
                if current_app:
                    current_app.logger.error(f"Erro ao processar dados do processo {numero}: {str(e)}")
                if tipo == "TJ":
                    linha.extend([_("Erro"), _("Erro"), _("Erro de processamento")])
                else:
                    linha.extend([_("Erro"), _("Erro"), _("Erro de processamento")])
            
            dados_tabela.append(linha)
        
        # Criar tabela
        tabela = Table(dados_tabela, colWidths=larguras_colunas)
        tabela.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#003366")),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('ALIGN', (0, 1), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
            ('GRID', (0, 0), (-1, -1), 1, colors.lightgrey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.whitesmoke]),
            ('VALIGN', (0, 0), (-1, -1), 'TOP')
        ]))
        
        conteudo.append(tabela)
        conteudo.append(Spacer(1, 0.3*inch))
        
        # Resumo dos resultados
        conteudo.append(Paragraph(_("Resumo dos Resultados"), styles['Subtitulo']))
        conteudo.append(Paragraph(f"• {_('Processos encontrados')}: {encontrados}", styles['ItemLista']))
        conteudo.append(Paragraph(f"• {_('Processos não encontrados')}: {nao_encontrados}", styles['ItemLista']))
        if com_erro > 0:
            conteudo.append(Paragraph(f"• {_('Erros de consulta')}: {com_erro}", styles['ItemLista']))
        conteudo.append(Spacer(1, 0.2*inch))
        
        # Observações
        conteudo.append(Paragraph(_("Observações"), styles['Subtitulo']))
        
        if tipo == "TJ":
            obs = [
                _("Processos arquivados não terão novas movimentações."),
                _("Processos transitados em julgado têm decisão final."),
                _("Processos não encontrados podem estar em sigilo ou não mais existir na base de dados."),
                _("Para detalhes completos, consulte individualmente cada processo.")
            ]
        else:
            obs = [
                _("O último movimento indica a situação mais recente do processo."),
                _("Para histórico completo de movimentações, consulte o processo individualmente."),
                _("Processos não encontrados podem estar em sigilo ou não mais existir na base de dados."),
                _("Consulte o sistema oficial para informações sempre atualizadas.")
            ]
        
        for item in obs:
            conteudo.append(Paragraph(f"• {item}", styles['ItemLista']))
        
        return GeradorPDF.gerar_pdf(
            conteudo, _("Consulta em Lote {tipo}").format(tipo=tipo)
        )
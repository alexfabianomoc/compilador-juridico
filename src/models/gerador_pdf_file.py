"""
Módulo para geração de arquivos PDF do Compilador Jurídico.
Este módulo implementa a classe GeradorPDF que é responsável por transformar
os dados do sistema em arquivos PDF formatados.
"""

from tkinter import filedialog, messagebox
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle#, Image
from reportlab.platypus.flowables import HRFlowable
from reportlab.lib.units import inch#, cm
from reportlab.lib.enums import TA_CENTER##, TA_LEFT
from datetime import datetime

class GeradorPDF:
    """Classe responsável por gerar relatórios PDF"""
    
    @staticmethod
    def salvar_arquivo_pdf(conteudo, titulo_padrao="Relatório"):
        """Exibe diálogo para salvar arquivo PDF e cria o documento"""
        # Diálogo para salvar arquivo
        arquivo = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("Arquivos PDF", "*.pdf")],
            title="Salvar PDF",
            initialfile=f"{titulo_padrao}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        )
        
        if not arquivo:
            return None  # Usuário cancelou
        
        try:
            # Criar documento PDF
            doc = SimpleDocTemplate(
                arquivo,
                pagesize=A4,
                rightMargin=72,
                leftMargin=72,
                topMargin=72,
                bottomMargin=72
            )
            
            # Definir estilos
            styles = getSampleStyleSheet()
            styles.add(ParagraphStyle(
                name='TituloPrincipal',
                parent=styles['Heading1'],
                alignment=TA_CENTER,
                fontSize=16,
                spaceAfter=12
            ))
            styles.add(ParagraphStyle(
                name='Titulo',
                parent=styles['Heading2'],
                fontSize=14,
                spaceAfter=10
            ))
            styles.add(ParagraphStyle(
                name='Subtitulo',
                parent=styles['Heading3'],
                fontSize=12,
                spaceAfter=8
            ))
            styles.add(ParagraphStyle(
                name='Item',
                parent=styles['Normal'],
                fontSize=10,
                leftIndent=20,
                spaceAfter=3
            ))
            
            # Adicionar metadados
            conteudo.insert(0, Paragraph(f"Compilador Jurídico - {titulo_padrao}", styles['TituloPrincipal']))
            conteudo.insert(1, Paragraph(f"Gerado em: {datetime.now().strftime('%d/%m/%Y às %H:%M:%S')}", styles['Normal']))
            conteudo.insert(2, HRFlowable(width="100%", thickness=1, color=colors.black, spaceBefore=10, spaceAfter=10))
            
            # Rodapé
            conteudo.append(Spacer(1, 0.5*inch))
            conteudo.append(HRFlowable(width="100%", thickness=1, color=colors.black))
            conteudo.append(Paragraph("Compilador Jurídico - © 2025", styles['Normal']))
            
            # Criar PDF
            doc.build(conteudo)
            return arquivo
        
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao gerar PDF: {str(e)}")
            return None
    
    @staticmethod
    def gerar_pdf_estatisticas(processos_tj, processos_trf):
        """Gera um PDF com as estatísticas dos processos"""
        styles = getSampleStyleSheet()
        
        # Personalizar estilos
        styles.add(ParagraphStyle(name='Titulo', parent=styles['Heading2'], fontSize=14, spaceAfter=10))
        styles.add(ParagraphStyle(name='Subtitulo', parent=styles['Heading3'], fontSize=12, spaceAfter=8))
        styles.add(ParagraphStyle(name='Item', parent=styles['Normal'], fontSize=10, leftIndent=20, spaceAfter=3))
        
        # Conteúdo do PDF
        conteudo = [] 
        
        # Título da seção
        conteudo.append(Paragraph("Estatísticas de Processos", styles['Titulo']))
        conteudo.append(Spacer(1, 0.2*inch))
        
        # Tabela de totais
        dados_tabela = [
            ["Tipo", "Quantidade"],
            ["Processos TJ", str(len(processos_tj))],
            ["Processos TRF", str(len(processos_trf))],
            ["Total", str(len(processos_tj) + len(processos_trf))]
        ]
        
        tabela = Table(dados_tabela, colWidths=[3*inch, 1.5*inch])
        tabela.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, -1), (-1, -1), colors.lightgrey),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        conteudo.append(tabela)
        conteudo.append(Spacer(1, 0.3*inch))
        
        # Últimos processos TJ
        if processos_tj:
            conteudo.append(Paragraph("Últimos Processos TJ Cadastrados:", styles['Subtitulo']))
            for processo in processos_tj[-5:]:
                conteudo.append(Paragraph(f"• {processo}", styles['Item']))
            conteudo.append(Spacer(1, 0.2*inch))
        
        # Últimos processos TRF
        if processos_trf:
            conteudo.append(Paragraph("Últimos Processos TRF Cadastrados:", styles['Subtitulo']))
            for processo in processos_trf[-5:]:
                conteudo.append(Paragraph(f"• {processo}", styles['Item']))
        
        # Criar e salvar o PDF
        return GeradorPDF.salvar_arquivo_pdf(conteudo, "Estatísticas")
    
    @staticmethod
    def gerar_pdf_consulta_individual(numero, tipo, resultado_texto):
        """Gera um PDF com o resultado da consulta individual de um processo"""
        styles = getSampleStyleSheet()

         # Personalizar estilos
        styles.add(ParagraphStyle(name='Titulo', parent=styles['Heading2'], fontSize=14, spaceAfter=10))
        #styles.add(ParagraphStyle(name='Subtitulo', parent=styles['Heading3'], fontSize=12, spaceAfter=8))
        styles.add(ParagraphStyle(name='Item', parent=styles['Normal'], fontSize=10, leftIndent=20, spaceAfter=3))
        
        # Conteúdo do PDF
        conteudo = []
        
        # Título do documento
        #conteudo.append(Paragraph(f"Consulta de Processo {tipo} {numero}", styles['Titulo']))
        #conteudo.append(Spacer(1, 0.2*inch))
        
        # Converter o texto bruto em parágrafos formatados
        linhas = resultado_texto.split('\n')
        
        # Variáveis para controlar o estilo
        estilo_atual = 'Normal'
        for linha in linhas:
            # Pular linhas vazias
            if not linha.strip():
                conteudo.append(Spacer(1, 6))
                continue
            
            # Detectar títulos e subtítulos
            if '=' * 10 in linha:
                # Linhas de separação
                conteudo.append(HRFlowable(width="100%", thickness=1, color=colors.black, spaceBefore=5, spaceAfter=5))
                continue
            elif '-' * 10 in linha:
                # Linhas de separação menores
                conteudo.append(HRFlowable(width="80%", thickness=0.5, color=colors.grey, spaceBefore=3, spaceAfter=3))
                continue
            
            # Detectar cabeçalhos baseados em padrões comuns
            if linha.strip().isupper() and len(linha.strip()) > 5:
                estilo_atual = 'Titulo'
                conteudo.append(Paragraph(linha, styles[estilo_atual]))
            elif linha.startswith('*') or linha.startswith('-'):
                estilo_atual = 'Item'
                conteudo.append(Paragraph(linha.replace('*', '•').replace('-', '•'), styles[estilo_atual]))
            elif linha.startswith('PROCESSO'):
                estilo_atual = 'Titulo'
                conteudo.append(Paragraph(linha, styles[estilo_atual]))
            else:
                estilo_atual = 'Normal'
                conteudo.append(Paragraph(linha, styles[estilo_atual]))
        
        # Criar e salvar o PDF
        return GeradorPDF.salvar_arquivo_pdf(conteudo)
    
    @staticmethod
    def gerar_pdf_consulta_lote(tipo, resultados):
        """Gera um PDF com o resultado da consulta em lote de processos"""
        styles = getSampleStyleSheet()

        # Personalizar estilos
        styles.add(ParagraphStyle(name='Titulo', parent=styles['Heading2'], fontSize=14, spaceAfter=10))
        styles.add(ParagraphStyle(name='Subtitulo', parent=styles['Heading3'], fontSize=12, spaceAfter=8))
        styles.add(ParagraphStyle(name='Item', parent=styles['Normal'], fontSize=10, leftIndent=20, spaceAfter=3))
        styles.add(ParagraphStyle(name='Celula', parent=styles['Normal'], fontSize=9, spaceAfter=3))
        
        # Conteúdo do PDF
        conteudo = []
        
        # Título do documento
        conteudo.append(Paragraph(f"Consulta em Lote - Meus Processos {tipo}", styles['Titulo']))
        conteudo.append(Spacer(1, 0.2*inch))
        
        # Resumo da consulta
        conteudo.append(Paragraph(f"Total de processos consultados: {len(resultados)}", styles['Normal']))
        conteudo.append(Spacer(1, 0.3*inch))
        
        # Criar tabela de resultados com cabeçalho específico para cada tipo
        if tipo == "TJ":
            dados_tabela = [["Número do Processo", "Tribunal", "Última Atualização", "Status"]]
            
            for numero, info in resultados.items():
                if isinstance(info, dict):
                    dados_tabela.append([
                        info.get("numero", numero),
                        info.get("tribunal", "Não informado"),
                        info.get("ultima_atualizacao", "Não informado"),
                        info.get("status", "Não informado")
                    ])
            
            # Definir larguras de colunas para TJ
            larguras_colunas = [2*inch, 1.5*inch, 1.5*inch, 2*inch]
        
        elif tipo == "TRF":
            dados_tabela = [["Número do Processo", "Última Atualização", "Último Movimento"]]
            
            for numero, info in resultados.items():
                if isinstance(info, dict):
                    # Último movimento pode ser muito longo, vamos limitá-lo
                    ultimo_mov = info.get("ultimo_movimento", "Não informado")
                    if len(ultimo_mov) > 50:  # Limitar tamanho para caber na tabela
                        ultimo_mov = ultimo_mov[:47] + "..."
                    
                    dados_tabela.append([
                        info.get("numero", numero),
                        info.get("ultima_atualizacao", "Não informado"),
                        ultimo_mov
                    ])
            
            # Definir larguras de colunas para TRF
            larguras_colunas = [2*inch, 1.5*inch, 1.5*inch, 2*inch]
        
        else:
            # Caso genérico
            dados_tabela = [["Número do Processo", "Informações"]]
            
            for numero, info in resultados.items():
                if isinstance(info, dict):
                    # Converter o dicionário em string formatada
                    info_str = ", ".join([f"{k}: {v}" for k, v in info.items()])
                    dados_tabela.append([numero, info_str])
            
            # Definir larguras de colunas para caso genérico
            larguras_colunas = [2*inch, 5*inch]
        
        if len(dados_tabela) > 1:  # Se tiver dados além do cabeçalho
            tabela = Table(dados_tabela, colWidths=larguras_colunas)
            tabela.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('WORDWRAP', (0, 0), (-1, -1), True)
            ]))
            
            conteudo.append(tabela)
        else:
            conteudo.append(Paragraph("Nenhum processo foi consultado.", styles['Normal']))
        
        # Adicionar informações extras
        conteudo.append(Spacer(1, 0.3*inch))
        conteudo.append(Paragraph("Observações:", styles['Subtitulo']))
        
        if tipo == "TJ":
            conteudo.append(Paragraph("• Os processos com status 'Arquivado definitivamente' foram encerrados e não terão mais movimentações.", styles['Item']))
            conteudo.append(Paragraph("• Os processos com status 'Transitado em julgado' tiveram decisão final proferida.", styles['Item']))
        elif tipo == "TRF":
            conteudo.append(Paragraph("• O último movimento indica a situação processual mais recente registrada no sistema.", styles['Item']))
            conteudo.append(Paragraph("• Caso deseje informações mais detalhadas, realize uma consulta individual do processo.", styles['Item']))
        
        # Criar e salvar o PDF
        return GeradorPDF.salvar_arquivo_pdf(conteudo, f"Consulta_Lote_{tipo}")
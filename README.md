# Compilador Jurídico

Um sistema para consulta e gerenciamento de processos judiciais do TJ e TRF, integrando-se às APIs públicas do DataJud (CNJ).

## 📋 Funcionalidades

- Cadastro de processos judiciais com validação de numeração única (20 dígitos)
- Consulta de processos individuais no TJMG e TRF6
- Consulta em lote de todos os processos cadastrados
- Armazenamento de resultados em cache local
- Exclusão de processos individuais ou em lote
- Interface gráfica completa desenvolvida com Tkinter
- Geração de relatórios em PDF

## 🔧 Requisitos

- Python 3.7+
- Pacotes Python (listados em requirements.txt):
  - certifi
  - chardet
  - charset-normalizer
  - idna
  - pillow
  - reportlab
  - requests
  - urllib3

## ⚙️ Instalação

1. Clone o repositório:
```bash
git clone https://github.com/alexfabianomoc/compilador_juridico.git
cd compilador_juridico
```

2. Crie e ative um ambiente virtual:
```bash
python -m venv compilador_juridico
# No Windows
compilador_juridico\Scripts\activate
# No Linux/Mac
source compilador_juridico/bin/activate
```

3. Instale as dependências usando o arquivo requirements.txt:
```bash
pip install -r requirements.txt
```

## 🚀 Como usar

1. Inicie o programa com interface gráfica:
```bash
python gui.py
```

2. Ou execute o programa principal para a versão de linha de comando:
```bash
python main.py
```

3. A interface é dividida em quatro abas principais:
   - **Cadastrar Meus Processos**: Adicionar novos processos ao sistema
   - **Consultar Processos**: Consultar processos individuais ou em lote
   - **Estatísticas Meus Processos**: Visualizar dados estatísticos sobre seus processos
   - **Excluir Meus Processos**: Remover processos individuais ou em lote

4. Para cada consulta, você pode gerar um PDF com os resultados usando o botão "Gerar PDF"

## 📁 Estrutura do Projeto

```
EXPLORADOR: COMPILADOR_JURIDICO/
├── _pycache_/
├── assets/
│   ├── cache/
│   │   ├── lista_processos_tj.json
│   │   ├── lista_processos_trf.json
│   │   ├── resultados_processos_tj.json
│   │   └── resultados_processos_trf.json
│   └── images/
│       ├── background/
│       └── lady_justice.png
├── manual/
│   └── Manual_usuario_compilador_juridico.pdf
├── compilador_juridico/ (ambiente virtual)
├── src/
│   ├── api/
│   │   ├── __init__.py
│   │   ├── tjmg.py
│   │   └── trf6.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── gerador_pdf_file.py
│   │   └── processo.py
│   └── utils/
│       ├── __init__.py
│       ├── file_handler.py
│       └── config.py
├── config.py
├── excluir_processo.py
├── gui.py
├── main.py
├── manual-instalacao.md
├── README.txt
└── requirements.txt
```

## 🔍 Uso da API

O sistema utiliza as seguintes APIs do DataJud:
- `https://api-publica.datajud.cnj.jus.br/api_publica_tjmg/_search` - Para processos do TJMG
- `https://api-publica.datajud.cnj.jus.br/api_publica_trf6/_search` - Para processos do TRF6

As consultas são realizadas utilizando a numeração única CNJ (20 dígitos) e os resultados são armazenados localmente para acesso futuro.

## 💡 Funcionalidades Principais

### Interface Gráfica
- Interface intuitiva com abas para diferentes funcionalidades
- Visualização detalhada de processos e resultados
- Geração de relatórios em PDF

### Gerenciamento de Processos
- Cadastro de processos com validação de formato
- Visualização de estatísticas dos processos cadastrados
- Exclusão seletiva de processos

### Consultas
- Consulta de processo individual com detalhamento
- Consulta em lote de todos os processos cadastrados
- Armazenamento de resultados para consultas offline

## 🧪 Desenvolvimento Futuro

Possibilidades para expansão:
- Suporte a outros tribunais (STJ, STF, outros TJs e TRFs)
- Análise estatística avançada dos processos
- Sistema de notificações para atualizações de processos
- Integração com sistemas de gerenciamento de escritórios de advocacia
- Aplicativo móvel para consultas em trânsito

## 📄 Licença

Este projeto está licenciado sob a [MIT License](LICENSE).

## 👥 Autores

- Alex Fabiano Silva - Desenvolvedor back-end
- Incluir os demais da equipe

---

**Observação**: Este projeto é para fins educacionais e de pesquisa. Não é um produto oficial do CNJ ou de qualquer tribunal.
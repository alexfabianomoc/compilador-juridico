# Manual de Instalação e Configuração - Compilador Jurídico Web

## 📚 Índice
1. [Introdução](#introdução)
2. [Requisitos do Sistema](#requisitos-do-sistema)
3. [Instalação Passo a Passo](#instalação-passo-a-passo)
4. [Configuração e Inicialização](#configuração-e-inicialização)
5. [Verificação da Instalação](#verificação-da-instalação)
6. [Configurações Avançadas](#configurações-avançadas)
7. [Solução de Problemas](#solução-de-problemas)
8. [Deploy em Produção](#deploy-em-produção)

## 🎯 Introdução

O **Compilador Jurídico** é agora uma aplicação web moderna desenvolvida com **Flask**, oferecendo uma interface responsiva e intuitiva para gerenciamento de processos judiciais. Este manual fornece instruções completas para instalação, configuração e execução do sistema.

### 🆕 Novidades da Versão Web
- **Interface Web Responsiva**: Acesso via navegador
- **Design Moderno**: CSS com animações e gradientes
- **Validação em Tempo Real**: Feedback instantâneo
- **Relatórios PDF Aprimorados**: Geração profissional
- **Sistema de Sessões**: Estado persistente entre consultas
- **Cache Inteligente**: Gerenciamento automático de arquivos temporários

## 💻 Requisitos do Sistema

### Hardware Mínimo
- **Processador**: 1.6 GHz dual-core
- **Memória RAM**: 4 GB (8 GB recomendado)
- **Espaço em Disco**: 1 GB disponível
- **Conexão Internet**: Estável para consultas API

### Software Necessário

#### Sistemas Operacionais Suportados
- **Windows**: 10/11 (64-bit)
- **macOS**: 10.15 (Catalina) ou superior
- **Linux**: Ubuntu 20.04+, Debian 11+, CentOS 8+, Fedora 35+

#### Python e Dependências
- **Python**: 3.8 ou superior (3.10+ recomendado)
- **pip**: Gerenciador de pacotes Python
- **Navegador Web**: Chrome 90+, Firefox 88+, Safari 14+, Edge 90+

#### Dependências Python (Automáticas)
```txt
Flask==3.1.1
Flask-Session==0.8.0
Flask-Babel==4.0.0
blinker==1.9.0
reportlab==4.4.1
requests==2.32.3
Pillow==11.2.1
Werkzeug==3.1.3
Jinja2==3.1.6
```

## 🔧 Instalação Passo a Passo

### 1. Instalação do Python

#### Windows
1. Acesse [python.org/downloads](https://www.python.org/downloads/)
2. Baixe Python 3.10+ (recomendado)
3. **IMPORTANTE**: Marque "Add Python to PATH" durante instalação
4. Execute o instalador como administrador
5. Verifique a instalação:
   ```cmd
   python --version
   pip --version
   ```

#### macOS
```bash
# Usando Homebrew (recomendado)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
brew install python@3.10

# Ou download direto do python.org
# Verifique a instalação
python3 --version
pip3 --version
```

#### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install python3.10 python3.10-pip python3.10-venv
sudo apt install python3.10-dev build-essential

# Verifique a instalação
python3.10 --version
pip3 --version
```

#### Linux (CentOS/RHEL/Fedora)
```bash
# CentOS/RHEL
sudo dnf install python3.10 python3.10-pip python3.10-devel

# Fedora
sudo dnf install python3 python3-pip python3-devel

# Verifique a instalação
python3 --version
pip3 --version
```

### 2. Download e Preparação

#### Opção A: Git (Recomendado)
```bash
# Clone o repositório
git clone https://github.com/alexfabianomoc/compilador_juridico.git
cd compilador_juridico

# Verifique se todos os arquivos estão presentes
ls -la
```

#### Opção B: Download ZIP
1. Baixe o arquivo ZIP do repositório
2. Extraia para um diretório de sua escolha
3. Navegue até o diretório extraído

### 3. Configuração do Ambiente Virtual

#### Criação do Ambiente Virtual
```bash
# Navegue até o diretório do projeto
cd compilador_juridico

# Crie o ambiente virtual
python -m venv venv

# Ative o ambiente virtual
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate

# Verifique se está ativo (prompt deve mostrar (venv))
which python
```

#### Instalação das Dependências
```bash
# Atualize pip para a versão mais recente
python -m pip install --upgrade pip

# Instale todas as dependências
pip install -r requirements.txt

# Verifique se tudo foi instalado corretamente
pip list
```

### 4. Verificação da Estrutura

O sistema criará automaticamente todos os diretórios necessários na primeira execução:

```
compilador_juridico/
├── app.py                    # ✅ Aplicação principal Flask
├── requirements.txt          # ✅ Dependências
├── src/                      # ✅ Código fonte
├── templates/                # ✅ Templates HTML
├── static/                   # ✅ CSS e recursos
├── assets/cache/             # 🔄 Criado automaticamente
└── instance/                 # 🔄 Criado automaticamente
    ├── flask_session/        # 🔄 Sessões Flask
    └── pdf_output/           # 🔄 PDFs gerados
```

## 🚀 Configuração e Inicialização

### 1. Configuração de Variáveis de Ambiente (Opcional)

#### Configuração Básica
```bash
# Windows (CMD)
set SECRET_KEY=sua_chave_secreta_muito_longa_e_aleatoria_aqui
set FLASK_ENV=development

# Windows (PowerShell)
$env:SECRET_KEY="sua_chave_secreta_muito_longa_e_aleatoria_aqui"
$env:FLASK_ENV="development"

# macOS/Linux (Bash)
export SECRET_KEY="sua_chave_secreta_muito_longa_e_aleatoria_aqui"
export FLASK_ENV="development"
```

#### Arquivo .env (Opcional)
Crie um arquivo `.env` na raiz do projeto:
```env
SECRET_KEY=sua_chave_secreta_muito_longa_e_aleatoria_aqui
FLASK_ENV=development
FLASK_DEBUG=1
```

### 2. Primeira Execução

```bash
# Certifique-se de que o ambiente virtual está ativo
# O prompt deve mostrar (venv)

# Execute a aplicação
python app.py
```

**Saída esperada:**
```
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://127.0.0.1:5000
 * Press CTRL+C to quit
```

### 3. Acesso ao Sistema

1. Abra seu navegador web
2. Acesse: `http://localhost:5000` ou `http://127.0.0.1:5000`
3. A página inicial do Compilador Jurídico deve ser exibida

## ✅ Verificação da Instalação

### 1. Testes de Funcionalidade

#### Teste de Interface
- [ ] Página inicial carrega sem erros
- [ ] Menu de navegação funciona
- [ ] Páginas de cadastro, consulta, estatísticas são acessíveis
- [ ] Design responsivo funciona (redimensione a janela)

#### Teste de Validação
1. Acesse `/cadastrar`
2. Digite um número com menos de 20 dígitos
3. Verifique se a validação em tempo real funciona
4. Teste com um número válido (20 dígitos)

#### Teste de Diretórios
Após a primeira execução, verifique se foram criados:
```
instance/
├── flask_session/           # Sessões do Flask
└── pdf_output/             # PDFs gerados

assets/cache/
├── lista_processos_tj.json
├── lista_processos_trf.json
├── resultados_processos_tj.json
└── resultados_processos_trf.json
```

### 2. Teste de Geração de PDF

1. Acesse `/estadisticas`
2. Clique em "Gerar PDF Estatísticas"
3. Verifique se o download inicia automaticamente

### 3. Logs do Sistema

Verifique se os logs estão sendo gerados corretamente:
```bash
# Verifique o arquivo de log
cat instance/app.log

# Ou no Windows
type instance\app.log
```

## ⚙️ Configurações Avançadas

### 1. Configuração de Porta Personalizada

```python
# Edite app.py (final do arquivo)
if __name__ == '__main__':
    criar_diretorios()
    app.run(debug=True, host='0.0.0.0', port=8080)
```

### 2. Configuração de Memória para PDFs

```python
# Em src/config.py, ajuste se necessário
MAX_PDF_AGE_HOURS = 48  # Manter PDFs por 48 horas
```

### 3. Configuração de Logs

```python
# Em app.py, ajuste o nível de logging
logging.basicConfig(level=logging.DEBUG)  # Mais detalhado
```

### 4. Acesso em Rede Local

Para permitir acesso de outros computadores na rede:

```python
# app.py (final do arquivo)
if __name__ == '__main__':
    criar_diretorios()
    app.run(debug=True, host='0.0.0.0', port=5000)
```

Depois acesse via: `http://SEU_IP:5000`

## 🔧 Solução de Problemas

### Problemas Comuns de Instalação

#### Erro: "ModuleNotFoundError: No module named 'flask'"
```bash
# Verifique se o ambiente virtual está ativo
# Instale as dependências novamente
pip install -r requirements.txt
```

#### Erro: "Permission denied" ao criar diretórios
```bash
# Linux/macOS - Ajuste permissões
chmod 755 .
chmod -R 755 assets/

# Windows - Execute como administrador
```

#### Erro: "Port 5000 is already in use"
```bash
# Mude a porta em app.py ou mate o processo
# Windows
netstat -ano | findstr :5000
taskkill /PID [PID_NUMBER] /F

# Linux/macOS
lsof -i :5000
kill -9 [PID_NUMBER]
```

### Problemas de Performance

#### PDFs não estão sendo gerados
```bash
# Verifique permissões do diretório
ls -la instance/pdf_output/

# Teste manual de geração
python -c "from reportlab.pdfgen import canvas; print('ReportLab OK')"
```

#### Interface lenta para carregar
1. Verifique conexão com internet
2. Desative modo debug em produção
3. Verifique logs de erro em `instance/app.log`

### Problemas de Conectividade

#### Erro ao consultar APIs
1. Verifique conexão com internet
2. Teste conectividade:
   ```bash
   ping api-publica.datajud.cnj.jus.br
   ```
3. Verifique se não há firewall bloqueando

#### Sessões perdidas constantemente
1. Verifique se o diretório `instance/flask_session/` tem permissões de escrita
2. Defina uma SECRET_KEY fixa
3. Aumente o tempo de sessão em app.py

### Debug Avançado

#### Modo Debug Detalhado
```bash
export FLASK_DEBUG=1
export FLASK_ENV=development
python app.py
```

#### Logs Detalhados
```python
# Adicione ao início de app.py
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 🚀 Deploy em Produção

### 1. Configuração para Produção

#### Variáveis de Ambiente Seguras
```bash
export SECRET_KEY="chave_super_secreta_de_pelo_menos_32_caracteres"
export FLASK_ENV="production"
export FLASK_DEBUG="0"
```

#### Arquivo de Configuração Produção
```python
# config.py
import os

class ProductionConfig:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    DEBUG = False
    TESTING = False
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    PERMANENT_SESSION_LIFETIME = 1800  # 30 minutos
```

### 2. Servidor Web Produção

#### Gunicorn (Recomendado)
```bash
# Instale Gunicorn
pip install gunicorn

# Execute em produção
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```

#### uWSGI
```bash
# Instale uWSGI
pip install uwsgi

# Crie arquivo uwsgi.ini
[uwsgi]
module = app:app
master = true
processes = 4
socket = compilador.sock
chmod-socket = 666
vacuum = true
die-on-term = true
```

### 3. Proxy Reverso (Nginx)

```nginx
server {
    listen 80;
    server_name seu-dominio.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /static {
        alias /caminho/para/compilador_juridico/static;
    }
}
```

### 4. SSL/HTTPS

```bash
# Certbot (Let's Encrypt)
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d seu-dominio.com
```

## 🔄 Atualizações e Manutenção

### 1. Atualização do Sistema

```bash
# Backup dos dados
cp -r assets/cache/ backup_cache_$(date +%Y%m%d)/

# Atualize o código
git pull origin main

# Atualize dependências
pip install -r requirements.txt --upgrade

# Reinicie o serviço
```

### 2. Manutenção Regular

#### Limpeza de Cache (Automática)
O sistema limpa automaticamente arquivos antigos a cada requisição.

#### Backup Manual
```bash
# Backup completo
tar -czf backup_compilador_$(date +%Y%m%d).tar.gz assets/ instance/
```

#### Monitoramento de Logs
```bash
# Acompanhe logs em tempo real
tail -f instance/app.log
```

## 📞 Suporte e Recursos

### Documentação
- **Manual Online**: Acesse `/manual` na aplicação
- **API DataJud**: [Documentação CNJ](https://datajud.cnj.jus.br)
- **Flask**: [Documentação Flask](https://flask.palletsprojects.com)

### Comunidade
- **Issues**: [GitHub Issues](https://github.com/alexfabianomoc/compilador_juridico/issues)
- **Discussões**: [GitHub Discussions](https://github.com/alexfabianomoc/compilador_juridico/discussions)

### Logs e Debugging
```bash
# Verificar logs de erro
grep ERROR instance/app.log

# Verificar logs de acesso
grep "GET\|POST" instance/app.log

# Monitorar performance
grep "slow" instance/app.log
```

---

**🎉 Parabéns!** Seu Compilador Jurídico Web está pronto para uso. A aplicação oferece uma interface moderna e intuitiva para gerenciamento eficiente de processos judiciais.

**💡 Dica**: Marque esta página nos favoritos para referência rápida durante atualizações e manutenção do sistema.
# Compilador Jurídico

Um sistema web para consulta e gerenciamento de processos judiciais do TJMG e TRF6, integrando-se às APIs públicas do DataJud (CNJ). Interface moderna e responsiva desenvolvida com Flask.

## 📋 Funcionalidades

- **Gestão de Processos**: Cadastro com validação automática CNJ (20 dígitos)
- **Consultas Individuais**: Busca detalhada de processos específicos no TJMG e TRF6
- **Consultas em Lote**: Verificação simultânea de todos os processos cadastrados
- **Relatórios PDF**: Geração profissional de estatísticas e resultados
- **Interface Web Moderna**: Design responsivo com validação em tempo real
- **Cache Inteligente**: Armazenamento otimizado de resultados
- **Exclusão Flexível**: Remoção individual ou em massa de processos
- **Internacionalização**: Suporte múltiplos idiomas (Flask-Babel)

## 🔧 Requisitos

- Python 3.8+
- Navegador web moderno
- Conexão estável com a Internet

### Dependências Principais
```
Flask==3.1.1
Flask-Session==0.8.0
Flask-Babel==4.0.0
reportlab==4.4.1
requests==2.32.3
Pillow==11.2.1
```

## ⚙️ Instalação

### 1. Clone o repositório
```bash
git clone https://github.com/alexfabianomoc/compilador_juridico.git
cd compilador_juridico
```

### 2. Crie um ambiente virtual
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. Instale as dependências
```bash
pip install -r requirements.txt
```

### 4. Configure as variáveis de ambiente (opcional)
```bash
# Windows
set SECRET_KEY=sua_chave_secreta_aqui
set FLASK_ENV=development

# Linux/Mac
export SECRET_KEY=sua_chave_secreta_aqui
export FLASK_ENV=development
```

## 🚀 Como usar

### Inicialização do Sistema Web

```bash
python app.py
```

O sistema estará disponível em: `http://localhost:5000`

### Navegação Principal

- **Página Inicial** (`/`): Visão geral e acesso rápido
- **Cadastrar** (`/cadastrar`): Adicionar novos processos
- **Consultar** (`/consultar`): Consultas individuais e em lote  
- **Estatísticas** (`/estatisticas`): Relatórios e análises
- **Excluir** (`/excluir`): Gestão de processos cadastrados
- **Manual** (`/manual`): Documentação integrada

### Funcionalidades Web

- **Validação em Tempo Real**: Feedback instantâneo durante digitação
- **Interface Responsiva**: Adaptação automática a diferentes telas
- **Relatórios PDF**: Download direto de relatórios profissionais
- **Sessões Seguras**: Gestão de estado entre consultas
- **Cache Automático**: Limpeza inteligente de arquivos temporários

## 📁 Estrutura do Projeto

```
COMPILADOR_JURIDICO/
├── app.py                 # Aplicação Flask principal
├── excluir_processo.py    # Módulo de exclusão
├── main.py               # Interface linha de comando
├── requirements.txt      # Dependências Python
├── 
├── src/                  # Código fonte
│   ├── api/             # Integração APIs DataJud
│   │   ├── tjmg.py      # Consultas TJMG
│   │   └── trf6.py      # Consultas TRF6
│   ├── models/          # Modelos de dados
│   │   ├── processo.py  # Classe Processo
│   │   └── gerador_pdf_file.py # Geração PDF
│   ├── utils/           # Utilitários
│   │   └── file_handler.py # Manipulação arquivos
│   └── config.py        # Configurações centralizadas
├── 
├── templates/           # Templates HTML
│   ├── layout.html      # Layout base
│   ├── index.html       # Página inicial
│   ├── cadastrar.html   # Cadastro processos
│   ├── consultar.html   # Consultas
│   ├── estatisticas.html # Estatísticas
│   ├── excluir.html     # Exclusão
│   ├── resultado.html   # Resultados consultas
│   └── manual.html      # Manual usuário
├── 
├── static/              # Recursos estáticos
│   └── style.css        # Estilos CSS modernos
├── 
├── assets/              # Assets da aplicação
│   ├── cache/           # Cache JSON local
│   │   ├── lista_processos_tj.json
│   │   ├── lista_processos_trf.json
│   │   ├── resultados_processos_tj.json
│   │   └── resultados_processos_trf.json
│   └── manual/          # Documentação
└── 
└── instance/            # Instância Flask
    ├── flask_session/   # Sessões
    └── pdf_output/      # PDFs gerados
```

## 🔍 Integração APIs

### APIs DataJud Utilizadas
```python
# TJMG - Tribunal de Justiça de Minas Gerais
API_TJMG_URL = "https://api-publica.datajud.cnj.jus.br/api_publica_tjmg/_search"

# TRF6 - Tribunal Regional Federal 6ª Região  
API_TRF6_URL = "https://api-publica.datajud.cnj.jus.br/api_publica_trf6/_search"
```

### Autenticação
```python
API_KEY = "ApiKey cDZHYzlZa0JadVREZDJCendQbXY6SkJlTzNjLV9TRENyQk1RdnFKZGRQdw=="
```

## 💡 Funcionalidades Técnicas

### Sistema de Cache
- **Armazenamento Local**: JSON para listas e resultados
- **Limpeza Automática**: Remoção de arquivos antigos (24h)
- **Gestão de Sessões**: Flask-Session para estado da aplicação

### Validação e Segurança
- **Validação CNJ**: Verificação rigorosa de 20 dígitos
- **Sanitização**: Limpeza de inputs do usuário
- **CSRF Protection**: Proteção contra ataques
- **Session Security**: Cookies seguros

### Geração de PDFs
- **ReportLab**: Relatórios profissionais
- **Templates Dinâmicos**: Formatação baseada em dados
- **Metadados**: Informações estruturadas nos PDFs

## 🌐 Recursos Web

### Interface Responsiva
```css
/* Design moderno com gradientes */
background: linear-gradient(135deg, #dc2626 0%, #b91c1c 100%);

/* Animações suaves */
transition: all 0.3s ease;
transform: translateY(-2px);
```

### Validação JavaScript
```javascript
// Validação em tempo real
numeroInput.addEventListener('input', function() {
    const valor = this.value.replace(/\D/g, '');
    // Feedback visual instantâneo
});
```

### Internacionalização
- **Flask-Babel**: Suporte múltiplos idiomas
- **Português Brasil**: Idioma padrão
- **Mensagens Traduzíveis**: Sistema `_()` integrado

## 🧪 Desenvolvimento e Testes

### Ambiente de Desenvolvimento
```bash
# Modo debug
export FLASK_ENV=development
export FLASK_DEBUG=1
python app.py
```

### Logs
- **Arquivo**: `instance/app.log`
- **Níveis**: INFO, ERROR, DEBUG
- **Rotação**: Automática por tamanho

### Estrutura Modular
- **Blueprints**: Organização por funcionalidade
- **Helpers**: Filtros e funções de template
- **Error Handling**: Tratamento elegante de erros

## 🚀 Deploy em Produção

### Configurações Recomendadas
```python
# Produção
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True
```

### Servidores Web
- **Gunicorn**: `gunicorn -w 4 app:app`
- **uWSGI**: Configuração via INI
- **Apache/Nginx**: Proxy reverso

## 📊 Funcionalidades Avançadas

### Relatórios Estatísticos
- **Distribuição**: Análise TJ vs TRF
- **Histórico**: Últimos processos cadastrados
- **Métricas**: Contadores e percentuais

### Consultas Inteligentes
- **Cache de Resultados**: Evita consultas duplicadas
- **Retry Logic**: Tentativas automáticas em falhas
- **Rate Limiting**: Respeito aos limites da API

### Gestão de Arquivos
- **PDF Output**: Diretório específico para relatórios
- **Session Files**: Armazenamento de sessões Flask
- **Cache Management**: Limpeza automática de temporários

## 🔮 Roadmap Futuro

### Funcionalidades Planejadas
- [ ] **Dashboard Analytics**: Gráficos interativos
- [ ] **API REST**: Endpoints para integração
- [ ] **Autenticação**: Sistema de usuários
- [ ] **Notificações**: Alertas de atualizações
- [ ] **Mobile App**: Versão mobile nativa
- [ ] **Mais Tribunais**: Expansão para outros TJs/TRFs

### Melhorias Técnicas
- [ ] **Banco de Dados**: Migração para PostgreSQL
- [ ] **Cache Redis**: Cache distribuído
- [ ] **Testes Automatizados**: Cobertura completa
- [ ] **CI/CD**: Pipeline DevOps
- [ ] **Docker**: Containerização
- [ ] **Monitoramento**: Métricas e logs centralizados

## 📄 Licença

Este projeto está licenciado sob a [MIT License](LICENSE).

## 👥 Contribuidores

- **Alex Fabiano Silva** - Desenvolvedor Principal
- **Equipe de Desenvolvimento** - Contribuidores

## 🤝 Contribuindo

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📞 Suporte

- **Issues**: [GitHub Issues](https://github.com/alexfabianomoc/compilador_juridico/issues)
- **Documentação**: Manual integrado em `/manual`
- **API DataJud**: [Documentação Oficial CNJ](https://datajud.cnj.jus.br)

---

**⚠️ Aviso Legal**: Este projeto é para fins educacionais e de pesquisa. Não é um produto oficial do CNJ ou de qualquer tribunal. Use os dados obtidos de acordo com os termos de uso das APIs públicas do DataJud.

**🏛️ DataJud**: Sistema oficial do Conselho Nacional de Justiça para disponibilização de dados processuais.
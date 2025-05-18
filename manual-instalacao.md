# Manual de Instalação e Inicialização - Compilador Jurídico

## Índice
1. [Introdução](#introdução)
2. [Requisitos do Sistema](#requisitos-do-sistema)
3. [Instalação Passo a Passo](#instalação-passo-a-passo)
4. [Inicialização do Sistema](#inicialização-do-sistema)
5. [Verificação da Instalação](#verificação-da-instalação)
6. [Solução de Problemas](#solução-de-problemas)
7. [Atualizações](#atualizações)

## Introdução

Este manual fornece instruções detalhadas para a instalação e inicialização do **Compilador Jurídico**, uma ferramenta para gerenciamento e consulta de processos judiciais. Siga cuidadosamente estas instruções para garantir uma configuração adequada do sistema.

## Requisitos do Sistema

Antes de iniciar a instalação, certifique-se de que seu sistema atende aos seguintes requisitos:

### Hardware Recomendado
- Processador: 1.6 GHz ou superior
- Memória RAM: Mínimo 4 GB
- Espaço em disco: 500 MB disponíveis
- Resolução de tela: 1280 x 720 ou superior

### Software Necessário
- Sistema Operacional:
  * Windows 10/11
  * macOS 10.14 ou superior
  * Linux (Ubuntu 20.04+, Debian 10+, Fedora 34+)
- Python 3.8 ou superior
- Conexão estável com a Internet

### Dependências Python
O Compilador Jurídico requer as seguintes bibliotecas Python:
- certifi==2025.4.26
- chardet==5.2.0
- charset-normalizer==3.4.2
- idna==3.10
- pillow==11.2.1
- reportlab==4.4.1
- requests==2.32.3
- urllib3==2.4.0
- tkinter (normalmente incluído na instalação padrão do Python)

## Instalação Passo a Passo

### 1. Instalação do Python

**Windows:**
1. Acesse [python.org](https://www.python.org/downloads/)
2. Baixe a versão mais recente do Python 3.8+
3. Execute o instalador e marque a opção "Add Python to PATH"
4. Clique em "Install Now" e aguarde a conclusão

**macOS:**
1. Acesse [python.org](https://www.python.org/downloads/)
2. Baixe a versão mais recente do Python 3.8+
3. Execute o instalador e siga as instruções
4. Verifique a instalação abrindo o Terminal e digitando `python3 --version`

**Linux:**
```bash
sudo apt update
sudo apt install python3 python3-pip python3-tk
```

### 2. Download do Compilador Jurídico

1. Baixe o arquivo compactado do Compilador Jurídico do repositório oficial
2. Extraia o conteúdo para um diretório de sua preferência
3. Anote o caminho completo para este diretório

### 3. Instalação das Dependências

1. Abra o terminal ou prompt de comando
2. Navegue até o diretório onde você extraiu o Compilador Jurídico
   ```bash
   cd caminho/para/compilador-juridico
   ```
3. Instale as dependências necessárias usando o arquivo requirements.txt:
   ```bash
   pip install -r requirements.txt
   ```

Para usuários do Windows, pode ser necessário usar:
```bash
python -m pip install -r requirements.txt
```

Para usuários do macOS/Linux, pode ser necessário usar:
```bash
python3 -m pip install -r requirements.txt
```

### 4. Verificação da Estrutura de Diretórios

O Compilador Jurídico está configurado para detectar automaticamente a localização de instalação e criar os diretórios necessários na primeira execução. A estrutura padrão é:

```
compilador-juridico/
├── assets/
│   └── cache/        # Criado automaticamente na primeira execução
├── src/
│   ├── api/
│   ├── config.py     # Configuração com detecção automática de caminho
│   ├── models/
│   └── utils/
├── gui.py
└── requirements.txt
```

Não é necessário modificar manualmente o arquivo `config.py`. O sistema:
- Detecta automaticamente o diretório de instalação
- Cria o diretório de cache se não existir
- Inicializa arquivos de dados vazios na primeira execução

## Inicialização do Sistema

### Inicialização Padrão

1. Abra o terminal ou prompt de comando
2. Navegue até o diretório principal do Compilador Jurídico
3. Execute o programa com o comando:

**Windows:**
```bash
python gui.py
```

**macOS/Linux:**
```bash
python3 gui.py
```

### Criação de Atalho (Opcional)

**Windows:**
1. Clique com o botão direito na área de trabalho
2. Selecione "Novo > Atalho"
3. Em "Localização do item", digite:
   ```
   pythonw.exe "caminho/completo/para/gui.py"
   ```
4. Clique em "Avançar" e dê um nome ao atalho (ex: "Compilador Jurídico")
5. Clique em "Concluir"

**macOS:**
1. Abra o TextEdit e crie um novo arquivo
2. Digite:
   ```bash
   #!/bin/bash
   cd /caminho/completo/para/compilador-juridico
   python3 gui.py
   ```
3. Salve o arquivo como "iniciar_compilador.command"
4. Abra o Terminal e torne o arquivo executável:
   ```bash
   chmod +x /caminho/para/iniciar_compilador.command
   ```
5. Agora você pode iniciar o programa com um duplo clique no arquivo

**Linux:**
1. Crie um arquivo de texto chamado "compilador-juridico.desktop" em ~/.local/share/applications/
2. Adicione o seguinte conteúdo:
   ```
   [Desktop Entry]
   Type=Application
   Name=Compilador Jurídico
   Comment=Sistema de gerenciamento de processos jurídicos
   Exec=python3 /caminho/completo/para/gui.py
   Icon=/caminho/para/icone.png
   Terminal=false
   Categories=Office;Legal;
   ```
3. Torne o arquivo executável:
   ```bash
   chmod +x ~/.local/share/applications/compilador-juridico.desktop
   ```

## Verificação da Instalação

Para verificar se a instalação foi concluída com sucesso:

1. Inicie o sistema conforme as instruções acima
2. A interface gráfica do Compilador Jurídico deve ser exibida sem erros
3. Na primeira execução, o sistema criará automaticamente:
   - O diretório `assets/cache`
   - Arquivos JSON vazios para armazenamento de dados
4. Verifique a barra de status na parte inferior da janela - deve exibir "Pronto"

### Testes Recomendados

1. **Verificação de diretórios**: Após a primeira execução, verifique se o diretório `assets/cache` foi criado automaticamente
2. **Teste de conexão**: Tente consultar um processo existente
3. **Teste de salvamento**: Adicione um processo de teste à sua lista
4. **Teste de geração de PDF**: Gere um relatório PDF de estatísticas

O sistema é configurado para criar automaticamente todos os arquivos e diretórios necessários na primeira execução, não sendo necessária qualquer configuração manual de caminhos.

## Solução de Problemas

### Problemas com Dependências

**Problema**: Erro "No module named X" ao iniciar o programa.

**Solução**:
1. Verifique se você instalou todas as dependências:
   ```bash
   pip list
   ```
2. Instale manualmente a biblioteca faltante:
   ```bash
   pip install nome_da_biblioteca
   ```

### Problemas com o tkinter

**Problema**: "ModuleNotFoundError: No module named 'tkinter'"

**Solução**:
- **Windows/macOS**: Reinstale o Python e certifique-se de selecionar a opção "tcl/tk e IDLE"
- **Linux**: Instale o pacote python3-tk:
  ```bash
  sudo apt install python3-tk
  ```

### Erros de Permissão

**Problema**: Erros relacionados a permissões de arquivos ao salvar dados.

**Solução**:
1. Verifique se você tem permissão de escrita no diretório do programa
2. Execute o programa como administrador (Windows) ou use sudo (Linux/macOS)
3. Verifique se o diretório `assets/cache` tem permissões de escrita

### Erro na Criação de Diretórios

**Problema**: Mensagens de erro indicando falha na criação automática de diretórios ou arquivos.

**Solução**:
1. Verifique as permissões da pasta onde o sistema está instalado
2. Mantenha a estrutura de pastas original (não renomeie ou mova pastas)
3. Crie manualmente o diretório `assets/cache` se necessário
4. Verifique se há espaço disponível em disco

### Problemas de Interface Gráfica

**Problema**: A interface gráfica não é exibida corretamente.

**Solução**:
1. Verifique a versão do Python e atualize se necessário
2. Reinstale a biblioteca tkinter
3. Em sistemas Linux, certifique-se de ter um ambiente de desktop instalado

## Atualizações

### Verificação de Atualizações

É recomendável verificar periodicamente se há atualizações disponíveis para o Compilador Jurídico. Para atualizar:

1. Baixe a versão mais recente do repositório oficial
2. Faça backup dos seus arquivos de dados (normalmente na pasta `data`)
3. Substitua os arquivos antigos pelos novos
4. Execute o comando de instalação de dependências novamente para garantir que todas estejam atualizadas:
   ```bash
   pip install -r requirements.txt --upgrade
   ```

### Migração de Dados

Se você estiver atualizando de uma versão anterior, pode ser necessário migrar seus dados:

1. Copie os arquivos da pasta `data` da instalação antiga
2. Cole-os na pasta `data` da nova instalação
3. Inicie o programa e verifique se todos os seus dados estão presentes

---

© 2025 Compilador Jurídico. Todos os direitos reservados.
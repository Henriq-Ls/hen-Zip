# _CONFIGURA_/__init__.py
"""
Fonte única de verdade para TODOS os valores fixos do projeto.
Nenhum outro arquivo pode ter cores, atalhos, tamanhos ou qualquer
valor fixo — tudo vem daqui.

SEÇÕES:
    APPDATA
    APLICAÇÃO
    FONTES
    JANELA PRINCIPAL
    ATALHOS
    CORES — paleta base
    CORES — UI escuro
    ESTILOS QSS prontos
"""

import os

# ══════════════════════════════════════════════════════════════════════════════
# MODO DE EXECUÇÃO
# ══════════════════════════════════════════════════════════════════════════════
# True  → desenvolvimento: log em nível DEBUG, erros detalhados
# False → produção: log em nível ERROR apenas, sem stack traces no terminal
MODO_DEV = True

# ══════════════════════════════════════════════════════════════════════════════
# APPDATA — pasta do usuário no sistema operacional
# ══════════════════════════════════════════════════════════════════════════════
# Windows: %APPDATA%\hen-zip
# Linux/Mac: ~/hen-zip
PASTA_APPDATA = os.path.join(
    os.environ.get("APPDATA", os.path.expanduser("~")),
    "hen-zip"
)
ID_APP = "hen-zip"

# ══════════════════════════════════════════════════════════════════════════════
# APLICAÇÃO
# ══════════════════════════════════════════════════════════════════════════════
VERSAO_APP  = "v1.0.0"
TITULO_APP  = "hen-Zip"
TEMA_QT     = "Fusion"             # tema base do Qt

# Caminhos absolutos — independentes do CWD de execução
_PROJETO_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMAGEM_ICO   = os.path.join(_PROJETO_DIR, "IMAGENS", "icon.ico")
LOGO_MARCA   = os.path.join(_PROJETO_DIR, "IMAGENS", "logo_nome.png")
LOGO_SIMB    = os.path.join(_PROJETO_DIR, "IMAGENS", "logo.png")

# ══════════════════════════════════════════════════════════════════════════════
# FONTES
# ══════════════════════════════════════════════════════════════════════════════
FONTE_NOME_UI       = "Segoe UI"
FONTE_TAMANHO_BASE  = 10     # pontos — fonte padrão da QApplication

FONTE_TAMANHO_TITULO  = 22   # px (CSS/QSS)
FONTE_TAMANHO_INFO    = 12
FONTE_TAMANHO_LABEL   = 11
FONTE_TAMANHO_DETALHE = 10
FONTE_TAMANHO_SUTIL   = 9
FONTE_TAMANHO_MARCA   = 18

# ══════════════════════════════════════════════════════════════════════════════
# JANELA PRINCIPAL
# ══════════════════════════════════════════════════════════════════════════════
LARGURA_PADRAO = 1240
ALTURA_PADRAO  = 820
LARGURA_MIN    = 940
ALTURA_MIN     = 640
MARGEM_LAYOUT = 28
ESPACO_LAYOUT = 16
ESPACO_INTERNO = 10
ALTURA_CAMPO = 42
ALTURA_BOTAO = 42
ALTURA_LINHA_OPERACAO = 82
LARGURA_CAMPO_CAMINHO_MIN = 120
LARGURA_BOTAO_PROCURAR = 78
LARGURA_BOTAO_EXECUTAR = 104
LARGURA_BOTAO_REMOVER = 40
MARGEM_CARD = 18
ALTURA_MARCA = 48
LIMITE_DIALOGO_CONFLITOS = 560
ALTURA_DIALOGO_CONFLITOS = 460
NIVEL_COMPRESSAO_ZIP = 6
INTERVALO_SALVAR_OPERACOES_MS = 400
CHAVE_CONFIG_OPERACOES = "operacoes"
CHAVE_OPERACAO_MODO = "modo"
CHAVE_OPERACAO_ORIGEM = "origem"
CHAVE_OPERACAO_DESTINO = "destino"
CHAVE_OPERACAO_APAGAR_ZIP = "apagar_zip_apos_extrair"
CHAVE_OPERACAO_EXTRAIR_JUNTO_ZIP = "extrair_junto_ao_zip"

# ══════════════════════════════════════════════════════════════════════════════
# ATALHOS
# ══════════════════════════════════════════════════════════════════════════════
ATALHO_SAIR           = "Alt+F4"
ATALHO_SALVAR         = "Ctrl+S"
ATALHO_ABRIR          = "Ctrl+O"
ATALHO_NOVO           = "Ctrl+N"

# ══════════════════════════════════════════════════════════════════════════════
# TEXTOS DA INTERFACE
# ══════════════════════════════════════════════════════════════════════════════
TXT_MENU_ARQUIVO = "&Arquivo"
TXT_MENU_AJUDA = "&Ajuda"
TXT_MENU_NOVA_OPERACAO = "Nova operação"
TXT_MENU_SAIR = "Sair"
TXT_MENU_SOBRE = "Sobre o hen-Zip"
TXT_HERO_TITULO = "Compacte e extraia sem etapas repetitivas"
TXT_HERO_SUBTITULO = "Organize seus arquivos ZIP em poucos cliques."
TXT_HERO_MARCA = "ZIP"
TXT_BOTAO_NOVA_OPERACAO = "+ Nova operação"
TXT_BOTAO_ABRIR_LOGS = "Abrir logs"
TXT_SECAO_OPERACOES = "Operações"
TXT_SECAO_DESCRICAO = "Configure a origem, o destino e escolha o que fazer."
TXT_COLUNA_ORIGEM = "ORIGEM"
TXT_COLUNA_DESTINO = "DESTINO"
TXT_COLUNA_ACAO = "AÇÃO"
TXT_MODO_COMPACTAR = "Compactar"
TXT_MODO_EXTRAIR = "Extrair"
TXT_ROTULO_ORIGEM = "Pasta para compactar"
TXT_ROTULO_ZIP_ORIGEM = "Arquivo ZIP"
TXT_ROTULO_DESTINO_ZIP = "Salvar arquivo ZIP como"
TXT_ROTULO_DESTINO_PASTA = "Extrair para esta pasta"
TXT_PLACEHOLDER_ORIGEM_PASTA = "Pasta de origem"
TXT_PLACEHOLDER_ORIGEM_ZIP = "Arquivo ZIP de origem"
TXT_PLACEHOLDER_DESTINO_ZIP = "Salvar arquivo ZIP em..."
TXT_PLACEHOLDER_DESTINO_PASTA = "Pasta de destino"
TXT_BOTAO_PROCURAR = "Procurar"
TXT_BOTAO_COMPACTAR = "Zipar"
TXT_BOTAO_EXTRAIR = "Extrair"
TXT_CHECKBOX_APAGAR_ZIP = "Apagar ZIP após extrair"
TXT_TOOLTIP_APAGAR_ZIP = (
    "Apaga o ZIP de origem somente após uma extração concluída. "
    "O caminho continua salvo."
)
TXT_CHECKBOX_EXTRAIR_JUNTO_ZIP = "Também ao lado do ZIP"
TXT_TOOLTIP_EXTRAIR_JUNTO_ZIP = (
    "Além da pasta de destino, extrai os arquivos na pasta onde o ZIP está."
)
TXT_BOTAO_REMOVER = "Remover esta operação"
TXT_ICON_REMOVER = "×"
TXT_SELECIONAR_PASTA_ORIGEM = "Selecione a pasta para compactar"
TXT_SELECIONAR_ZIP_ORIGEM = "Selecione um arquivo ZIP"
TXT_SELECIONAR_DESTINO_ZIP = "Salvar arquivo ZIP"
TXT_SELECIONAR_DESTINO_PASTA = "Selecione a pasta de destino"
TXT_FILTRO_ARQUIVO_ZIP = "Arquivos ZIP (*.zip)"
TXT_STATUS_PRONTO = "Pronto para compactar ou extrair arquivos."
TXT_STATUS_PROCESSANDO = "Processando..."
TXT_STATUS_CANCELADO = "Operação cancelada."
TXT_STATUS_SUCESSO = "Operação concluída com sucesso."
TXT_STATUS_ERRO = "A operação não foi concluída."
TXT_PROGRESS_COMPACTAR = "Compactando: {nome}"
TXT_PROGRESS_EXTRAIR = "Extraindo: {nome}"
TXT_SUCESSO_COMPACTAR = "Arquivo ZIP criado com sucesso:\n{destino}"
TXT_SUCESSO_EXTRAIR = "Arquivos extraídos com sucesso em:\n{destino}"
TXT_SUCESSO_EXTRAIR_JUNTO_ZIP = (
    "\n\nTambém extraídos ao lado do ZIP:\n{destino}"
)
TXT_MENSAGEM_ZIP_APAGADO = "\n\nZIP de origem apagado:\n{arquivo}"
TXT_AVISO_ZIP_NAO_APAGADO = (
    "\n\nA extração foi concluída, mas não foi possível apagar o ZIP:\n"
    "{arquivo}\n\nDetalhes: {erro}"
)
TXT_LOG_ZIP_APAGADO = "ZIP de origem apagado após extração: {arquivo}"
TXT_LOG_FALHA_APAGAR_ZIP = (
    "A extração terminou, mas não foi possível apagar o ZIP {arquivo}: {erro}"
)
TXT_TITULO_SUCESSO = "Operação concluída"
TXT_TITULO_ERRO = "Não foi possível concluir"
TXT_TITULO_CONFLITOS = "Arquivos já existentes"
TXT_TITULO_SUBSTITUIR_ZIP = "Substituir arquivo ZIP?"
TXT_TITULO_AGUARDAR = "Operação em andamento"
TXT_MENSAGEM_CONFLITOS = (
    "Selecione quais arquivos existentes no destino podem ser substituídos. "
    "Os demais serão mantidos."
)
TXT_BOTAO_MARCAR_TODOS = "Marcar todos"
TXT_BOTAO_DESMARCAR_TODOS = "Desmarcar todos"
TXT_BOTAO_APLICAR_SELECAO = "Extrair seleção"
TXT_BOTAO_CANCELAR = "Cancelar"
TXT_CONFIRMAR_SUBSTITUIR_ZIP = (
    "O arquivo de destino já existe:\n{destino}\n\nDeseja substituí-lo?"
)
TXT_CONFIRMAR_SAIR_PROCESSANDO = (
    "Uma operação ainda está em andamento. Aguarde a conclusão antes de fechar."
)
TXT_SOBRE = (
    "hen-Zip {versao}\n\n"
    "Compacte pastas e extraia arquivos ZIP com controle sobre substituições."
)
TXT_ERRO_CAMINHO_VAZIO = "Informe os caminhos de origem e destino."
TXT_ERRO_ORIGEM_PASTA_INVALIDA = "A origem precisa ser uma pasta existente."
TXT_ERRO_ORIGEM_ZIP_INVALIDA = "A origem precisa ser um arquivo ZIP existente."
TXT_ERRO_DESTINO_PASTA_INVALIDO = "O destino informado precisa ser uma pasta."
TXT_ERRO_DESTINO_ZIP_INVALIDO = (
    "O destino do ZIP precisa apontar para um arquivo, não para uma pasta."
)
TXT_ERRO_ARQUIVO_ZIP_INVALIDO = "O arquivo selecionado não é um ZIP válido."
TXT_ERRO_CAMINHO_ZIP_INSEGURO = "O ZIP contém um caminho inválido ou inseguro: {nome}"
TXT_ERRO_DESTINO_INCOMPATIVEL = (
    "O caminho do ZIP não pode ser criado porque já existe um arquivo no caminho: {nome}"
)
TXT_ERRO_DESTINO_E_PASTA = (
    "Não é possível substituir o arquivo '{nome}' porque já existe uma pasta com esse nome."
)
TXT_ERRO_DESTINO_FORA_DA_PASTA = (
    "Um caminho do ZIP aponta para fora da pasta de destino: {nome}"
)
TXT_ERRO_PASTA_ORIGEM_VAZIA = "Escolha uma pasta de origem."
TXT_ERRO_PASTA_DESTINO_VAZIA = "Escolha uma pasta de destino."
TXT_ERRO_ARQUIVO_DESTINO_VAZIO = "Escolha o caminho do arquivo ZIP."
TXT_ERRO_ACAO_ZIP_INVALIDA = "Ação de compactação ou extração desconhecida."
TXT_ERRO_ABRIR_LOGS = "Não foi possível abrir o arquivo de log:\n{caminho}"
TXT_LOG_PASTA_RAIZ_REMOVIDA = "Pasta raiz correspondente ao destino removida: {nome}"
TXT_LOG_RESULTADO_EXTRAIR = (
    "Extração concluída: {destino} | {extraidos} arquivo(s) extraído(s), "
    "{mantidos} arquivo(s) mantido(s)."
)

# ══════════════════════════════════════════════════════════════════════════════
# CORES — paleta base (nomes semânticos)
# ══════════════════════════════════════════════════════════════════════════════
PRETO          = "#020202"
PRETO_FOSCO    = "#070706"
CINZA_ESCURO   = "#0F1210"
BRANCO         = "#EDEEF0"
AMARELO        = "#FFC107"
AMBAR          = "#E0A800"
VERDE          = "#4ec994"
TURQUESA       = "#00C2A8"
AZUL_CLARO     = "#2196F3"
AZUL           = "#0057FF"
AZUL_ESCURO    = "#1FB8D0"
CORAL          = "#FF6B6B"
VERMELHO       = "#A10510"
LARANJA_ESCURO = "#9E3B02"

# ══════════════════════════════════════════════════════════════════════════════
# CORES — UI escuro (usadas nos estilos QSS abaixo)
# ══════════════════════════════════════════════════════════════════════════════
COR_BG_APP           = "#100D16"
COR_BG_SECUNDARIO    = "#191420"
COR_BG_TERCIARIO     = "#221B2A"
COR_BG_CAMPO         = "#15111B"
COR_BG_ESCURO        = "#0C0A10"
COR_BORDA            = "#33283E"
COR_BORDA_CLARA      = "#493954"
COR_TEXTO            = "#F5F0FA"
COR_TEXTO_SECUNDARIO = "#B7AABE"
COR_TEXTO_SUTIL      = "#81748B"
COR_TEXTO_INATIVO    = "#6B6074"
COR_ACENTO           = "#A855F7"
COR_ACENTO_HOVER     = "#9333EA"
COR_ACENTO_ATIVO     = "#4C1D65"
COR_ACENTO_BORDA     = "#C084FC"
COR_SUCESSO          = "#E34D73"
COR_SUCESSO_HOVER    = "#F06483"
COR_PERIGO           = "#F43F5E"
COR_VERMELHO_ESCURO  = "#8A183D"
COR_MAGENTA          = "#D946EF"
COR_ROXO_CLARO       = "#C084FC"

# ══════════════════════════════════════════════════════════════════════════════
# ESTILOS QSS — prontos para uso direto
# ══════════════════════════════════════════════════════════════════════════════

ESTILO_ESCURO_GLOBAL = f"""
QMainWindow, QWidget {{
    background: {COR_BG_APP};
    color: {COR_TEXTO};
    font-family: "{FONTE_NOME_UI}", Arial, sans-serif;
    font-size: {FONTE_TAMANHO_LABEL}px;
}}
QSplitter::handle {{ background: {COR_BORDA}; }}
QMenuBar {{
    background: {COR_BG_SECUNDARIO};
    color: {COR_TEXTO};
    border-bottom: 1px solid {COR_BORDA};
}}
QMenuBar::item:selected {{ background: {COR_ACENTO}; }}
QMenu {{
    background: {COR_BG_TERCIARIO};
    color: {COR_TEXTO};
    border: 1px solid {COR_BORDA_CLARA};
}}
QMenu::item:selected {{ background: {COR_ACENTO}; }}
QToolBar {{
    background: {COR_BG_SECUNDARIO};
    border-bottom: 1px solid {COR_BORDA};
    spacing: 4px;
    padding: 2px;
}}
QToolButton {{
    background: transparent;
    color: {COR_TEXTO};
    border: none;
    padding: 4px 8px;
    border-radius: 3px;
}}
QToolButton:hover   {{ background: {COR_BG_TERCIARIO}; }}
QToolButton:pressed {{ background: {COR_BG_TERCIARIO}; }}
QStatusBar {{
    background: {COR_BG_SECUNDARIO};
    color: {COR_TEXTO_SECUNDARIO};
    border-top: 1px solid {COR_BORDA};
    font-size: {FONTE_TAMANHO_DETALHE}px;
}}
QScrollBar:vertical {{
    background: {COR_BG_ESCURO}; width: 10px; border: none;
}}
QScrollBar::handle:vertical {{
    background: {COR_BORDA_CLARA}; border-radius: 5px; min-height: 20px;
}}
QScrollBar::add-line:vertical,
QScrollBar::sub-line:vertical {{ height: 0; }}
QScrollBar:horizontal {{
    background: {COR_BG_ESCURO}; height: 10px; border: none;
}}
QScrollBar::handle:horizontal {{
    background: {COR_BORDA_CLARA}; border-radius: 5px; min-width: 20px;
}}
QScrollBar::add-line:horizontal,
QScrollBar::sub-line:horizontal {{ width: 0; }}
QFrame#heroCard {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
        stop:0 {COR_ACENTO_ATIVO}, stop:0.52 {COR_VERMELHO_ESCURO},
        stop:1 {COR_BG_SECUNDARIO});
    border: 1px solid {COR_BORDA};
    border-radius: 16px;
}}
QLabel#brandMark {{
    background: {COR_BG_APP};
    color: {COR_ROXO_CLARO};
    border: 1px solid {COR_ACENTO_BORDA};
    border-radius: 12px;
    font-size: {FONTE_TAMANHO_MARCA}px;
    font-weight: bold;
}}
QLabel#heroTitle {{
    color: {COR_TEXTO};
    font-size: {FONTE_TAMANHO_TITULO}px;
    font-weight: bold;
}}
QLabel#heroSubtitle, QLabel#mutedLabel {{ color: {COR_TEXTO_SECUNDARIO}; }}
QLabel#sectionTitle {{
    color: {COR_TEXTO};
    font-size: {FONTE_TAMANHO_INFO}px;
    font-weight: bold;
}}
QLabel#columnHeader {{
    color: {COR_TEXTO_SUTIL};
    font-size: {FONTE_TAMANHO_SUTIL}px;
    font-weight: bold;
}}
QFrame#sectionCard {{
    background: {COR_BG_SECUNDARIO};
    border: 1px solid {COR_BORDA};
    border-radius: 14px;
}}
QFrame#tableHeader {{
    background: {COR_BG_APP};
    border-radius: 8px;
}}
QWidget#operationRow {{
    background: {COR_BG_TERCIARIO};
    border: 1px solid {COR_BORDA};
    border-radius: 10px;
}}
QLineEdit, QComboBox {{
    background: {COR_BG_CAMPO};
    color: {COR_TEXTO};
    border: 1px solid {COR_BORDA_CLARA};
    border-radius: 8px;
    padding: 6px 10px;
    min-height: {ALTURA_CAMPO}px;
    selection-background-color: {COR_ACENTO};
}}
QLineEdit:focus, QComboBox:focus {{ border: 1px solid {COR_ACENTO_BORDA}; }}
QComboBox::drop-down {{ border: none; width: 26px; }}
QCheckBox#deleteArchiveCheck {{
    color: {COR_TEXTO};
    spacing: 7px;
}}
QCheckBox#deleteArchiveCheck::indicator {{
    width: 18px;
    height: 18px;
    border: 1px solid {COR_BORDA_CLARA};
    border-radius: 4px;
    background: {COR_BG_CAMPO};
}}
QCheckBox#deleteArchiveCheck::indicator:hover {{
    border-color: {COR_ACENTO_BORDA};
}}
QCheckBox#deleteArchiveCheck::indicator:checked {{
    background: {COR_ACENTO};
    border-color: {COR_ACENTO};
}}
QComboBox QAbstractItemView {{
    background: {COR_BG_TERCIARIO};
    color: {COR_TEXTO};
    selection-background-color: {COR_ACENTO_ATIVO};
    border: 1px solid {COR_BORDA_CLARA};
}}
QPushButton {{
    background: {COR_BG_TERCIARIO};
    color: {COR_TEXTO};
    border: 1px solid {COR_BORDA_CLARA};
    border-radius: 8px;
    padding: 7px 12px;
    min-height: {ALTURA_BOTAO}px;
}}
QPushButton:hover {{ border-color: {COR_ACENTO_BORDA}; }}
QPushButton:disabled {{
    background: {COR_BG_CAMPO};
    color: {COR_TEXTO_INATIVO};
    border-color: {COR_BORDA};
}}
QPushButton#primaryButton {{
    background: {COR_ACENTO};
    color: #FFFFFF;
    border: none;
    font-weight: bold;
}}
QPushButton#primaryButton:hover {{ background: {COR_ACENTO_HOVER}; }}
QToolButton#primaryButton {{
    background: {COR_ACENTO};
    color: #FFFFFF;
    border: none;
    border-radius: 8px;
    padding: 7px 12px;
    min-height: {ALTURA_BOTAO}px;
    font-weight: bold;
}}
QToolButton#primaryButton:hover {{ background: {COR_ACENTO_HOVER}; }}
QToolButton#primaryButton::menu-button {{
    border-left: 1px solid {COR_ACENTO_BORDA};
    width: 20px;
}}
QPushButton#secondaryButton {{
    background: {COR_BG_TERCIARIO};
    border: 1px solid {COR_ACENTO_BORDA};
    color: {COR_ROXO_CLARO};
    font-weight: bold;
}}
QPushButton#browseButton {{ min-height: {ALTURA_CAMPO}px; }}
QPushButton#removeButton {{
    color: {COR_PERIGO};
    font-weight: bold;
    min-width: {LARGURA_BOTAO_REMOVER}px;
}}
QProgressBar {{
    background: {COR_BG_CAMPO};
    color: {COR_TEXTO};
    border: 1px solid {COR_BORDA_CLARA};
    border-radius: 6px;
    min-height: 12px;
    text-align: center;
}}
QProgressBar::chunk {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 {COR_ACENTO}, stop:1 {COR_PERIGO});
    border-radius: 5px;
}}
QListWidget#conflictList {{
    background: {COR_BG_CAMPO};
    border: 1px solid {COR_BORDA};
    border-radius: 8px;
    padding: 6px;
}}
"""

ESTILO_DIALOGO_ESCURO = f"""
QDialog    {{ background: {COR_BG_CAMPO}; color: {COR_TEXTO}; }}
QLabel     {{ color: {COR_TEXTO_SECUNDARIO}; }}
QGroupBox  {{
    color: #bbbbbb;
    border: 1px solid {COR_BORDA};
    border-radius: 4px;
    margin-top: 8px;
    font-size: {FONTE_TAMANHO_LABEL}px;
}}
QGroupBox::title {{ subcontrol-origin: margin; left: 8px; padding: 0 4px; }}
QComboBox, QSpinBox, QLineEdit, QDoubleSpinBox {{
    background: {COR_BG_TERCIARIO};
    color: {COR_TEXTO};
    border: 1px solid {COR_BORDA_CLARA};
    border-radius: 3px;
    padding: 3px;
}}
"""

ESTILO_BTN_PRIMARIO = f"""
QPushButton {{
    background: {COR_ACENTO};
    color: #ffffff;
    border: none;
    padding: 8px 20px;
    border-radius: 4px;
    font-size: {FONTE_TAMANHO_INFO}px;
    font-weight: bold;
}}
QPushButton:hover    {{ background: {COR_ACENTO_HOVER}; }}
QPushButton:disabled {{ background: {COR_BG_TERCIARIO}; color: {COR_TEXTO_INATIVO}; }}
"""

ESTILO_BTN_CANCELAR = f"""
QPushButton {{
    background: {COR_BORDA_CLARA};
    color: {COR_TEXTO_SECUNDARIO};
    border: none;
    padding: 8px 16px;
    border-radius: 4px;
}}
QPushButton:hover {{ background: {COR_TEXTO_SUTIL}; }}
"""

ESTILO_LIST_WIDGET = f"""
QListWidget {{
    background: {COR_BG_APP};
    border: none;
    color: {COR_TEXTO};
}}
QListWidget::item {{ padding: 4px; border-bottom: 1px solid {COR_BORDA}; }}
QListWidget::item:selected {{ background: {COR_ACENTO_ATIVO}; }}
QListWidget::item:hover    {{ background: {COR_BG_TERCIARIO}; }}
"""

ESTILO_PROGRESSBAR = f"""
QProgressBar {{
    background: {COR_BG_TERCIARIO};
    border: 1px solid {COR_BORDA_CLARA};
    border-radius: 3px;
}}
QProgressBar::chunk {{
    background: {COR_ACENTO};
    border-radius: 2px;
}}
"""

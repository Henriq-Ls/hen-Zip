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
IMAGEM_ICO   = os.path.join(_PROJETO_DIR, "midias", "icone.ico")
LOGO_MARCA   = os.path.join(_PROJETO_DIR, "midias", "logo_horizontal.png")
LOGO_SIMB    = os.path.join(_PROJETO_DIR, "midias", "logo.png")

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
ALTURA_LINHA_OPERACAO = 64
ALTURA_DIVISORIA_OPERACAO = 56
LARGURA_CAMPO_CAMINHO_MIN = 80
LARGURA_CAMPO_SENHA = 110
LARGURA_BOTAO_PROCURAR = 68
LARGURA_BOTAO_EXECUTAR = 104
LARGURA_BOTAO_REMOVER = 40
MARGEM_CARD = 18
ALTURA_MARCA = 70
LARGURA_MARCA = 250
LIMITE_DIALOGO_CONFLITOS = 560
ALTURA_DIALOGO_CONFLITOS = 460
LARGURA_DIALOGO_AJUDA = 900
ALTURA_DIALOGO_AJUDA = 650
LARGURA_MIN_DIALOGO_AJUDA = 680
ALTURA_MIN_DIALOGO_AJUDA = 480
NIVEL_COMPRESSAO_ZIP = 6
INTERVALO_SALVAR_OPERACOES_MS = 400
CHAVE_CONFIG_OPERACOES = "operacoes"
CHAVE_OPERACAO_MODO = "modo"
CHAVE_OPERACAO_ORIGEM = "origem"
CHAVE_OPERACAO_DESTINO = "destino"
CHAVE_OPERACAO_APAGAR_ZIP = "apagar_zip_apos_extrair"
CHAVE_OPERACAO_EXTRAIR_JUNTO_ZIP = "extrair_junto_ao_zip"
CHAVE_OPERACAO_REMOVER_PASTA_RAIZ = "remover_pasta_raiz_diferente"
CHAVE_ITEM_TIPO = "tipo"
VALOR_ITEM_DIVISORIA = "divisoria"
MIME_REORDENAR_OPERACAO = "application/x-hen-zip-operation"

# ══════════════════════════════════════════════════════════════════════════════
# EXPLORER — dimensões, colunas e limites de pré-visualização
# ══════════════════════════════════════════════════════════════════════════════
EXPLORER_LARGURA_PADRAO = 1180
EXPLORER_ALTURA_PADRAO = 760
EXPLORER_LARGURA_MIN = 920
EXPLORER_ALTURA_MIN = 520
EXPLORER_MARGEM = 12
EXPLORER_ESPACAMENTO = 8
EXPLORER_LARGURA_LOCAIS = 160
EXPLORER_PREVIEW_TAMANHO = 240
EXPLORER_PREVIEW_ALTURA = 180
EXPLORER_LARGURA_COLUNA_TAMANHO = 100
EXPLORER_LARGURA_COLUNA_TIPO = 110
EXPLORER_LARGURA_COLUNA_DATA = 150
EXPLORER_TAMANHO_ICONE = 20
EXPLORER_PREVIEW_DEBOUNCE_MS = 180
EXPLORER_PREVIEW_MAX_BYTES = 20 * 1024 * 1024
EXPLORER_PREVIEW_MAX_ITEMS = 10000
EXPLORER_PREVIEW_MAX_PIXELS = 40_000_000
EXPLORER_PREVIEW_MAX_SECONDS = 3
EXPLORER_CABECALHOS = ("Nome", "Tamanho", "Tipo", "Modificado")
EXPLORER_FILTROS = (("Todos os arquivos (*)", ("*",)),)

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
TXT_MENU_AJUDA_GUIA = "Como usar"
TXT_MENU_NOVA_OPERACAO = "Nova operação"
TXT_MENU_SAIR = "Sair"
TXT_MENU_SOBRE = "Sobre o hen-Zip"
TXT_HERO_TITULO = "Compacte e extraia sem etapas repetitivas"
TXT_HERO_SUBTITULO = "Compacte pastas e extraia arquivos ZIP e RAR."
TXT_HERO_MARCA = "ZIP"
TXT_BOTAO_NOVA_OPERACAO = "+ Nova operação"
TXT_BOTAO_NOVO_SEPARADOR = "+ Separador"
TXT_BOTAO_AJUDA = "Ajuda"
TXT_BOTAO_FECHAR_AJUDA = "Fechar"
TXT_BOTAO_ABRIR_LOGS = "Abrir logs"
TXT_TITULO_DIALOGO_AJUDA = "Ajuda do hen-Zip"
TXT_AJUDA_CONTEUDO = (
    "<h1>Como usar o hen-Zip</h1>"
    "<p>Configure cada linha com uma origem, um destino e a ação desejada. "
    "Use <b>Procurar</b> para escolher os caminhos e clique em "
    "<b>Extrair</b> ou <b>Zipar</b>. Os campos ficam recolhidos por padrão; "
    "use o botão ao lado das setas de ordem para expandir e editar. Cada linha "
    "guarda suas próprias opções.</p>"
    "<p>A seta do botão de ação permite trocar entre extrair e compactar. "
    "<b>Nova operação</b> adiciona uma linha; o botão <b>×</b> remove apenas "
    "a linha e suas opções salvas, sem apagar arquivos. <b>Abrir logs</b> "
    "mostra o registro das operações e dos erros.</p>"
    "<p>Arraste pelo puxador ou use as setas <b>↑</b> e <b>↓</b> ao lado de "
    "uma linha para mudar sua ordem. <b>Separador</b> insere uma linha "
    "horizontal; mova-a para dividir as operações em grupos. O separador "
    "também pode ser removido.</p>"
     "<h2>Extrair ZIP ou RAR</h2>"
    "<ol>"
     "<li>Na origem, escolha um arquivo ZIP ou RAR existente. No seletor, "
     "use o filtro para mostrar somente ZIP ou somente RAR; as pastas continuam "
     "visíveis para navegação.</li>"
     "<li>No destino, escolha a pasta que receberá os arquivos. Se marcar "
     "<b>Ao lado do arquivo</b> e deixar o destino vazio, os arquivos serão "
     "extraídos na pasta do ZIP ou RAR.</li>"
     "<li>Clique em <b>Extrair</b>. Se o arquivo não existir ou não puder ser lido, "
    "o hen-Zip mostra um erro e não informa uma conclusão bem-sucedida.</li>"
    "</ol>"
    "<h2>Opções da linha</h2>"
    "<ul>"
     "<li><b>Apagar arquivo:</b> remove somente o ZIP ou RAR de origem depois que "
    "todas as extrações solicitadas terminarem com sucesso. Os arquivos "
     "extraídos permanecem no destino. Se uma etapa falhar, o arquivo é mantido.</li>"
    "<li><b>Ao lado do arquivo:</b> com o destino vazio, extrai na pasta onde "
    "o ZIP ou RAR está. Com um destino preenchido, também extrai uma cópia "
    "ao lado do arquivo. Essa cópia mantém a pasta-raiz interna e mescla os "
    "arquivos nela se a pasta já existir. Se os dois caminhos forem a mesma "
    "pasta, extrai apenas uma vez. As substituições são escolhidas "
     "separadamente em cada destino. A marcação <b>Remover raiz</b> não altera "
     "essa cópia ao lado.</li>"
    "<li><b>Remover raiz:</b> afeta somente o destino informado. Quando todo "
    "o conteúdo está dentro de uma única pasta cujo nome é diferente do "
    "destino, marcado remove essa pasta e coloca o conteúdo direto no destino; "
    "desmarcado mantém a pasta. Se os nomes coincidirem, a pasta é removida "
    "automaticamente nesse destino. A cópia ao lado do ZIP/RAR sempre mantém "
    "a pasta-raiz, independentemente desta marcação. Arquivos com vários itens "
    "na raiz mantêm sua estrutura.</li>"
    "</ul>"
    "<h2>Arquivos que já existem</h2>"
     "<p>Quando um arquivo compactado já existe no destino, o hen-Zip mostra uma "
    "lista antes de substituir. Os itens começam marcados: deixe marcado o "
    "que pode ser substituído e desmarque o que deve ser preservado. "
    "<b>Marcar todos</b> e <b>Desmarcar todos</b> ajudam a ajustar a lista. "
     "Ao extrair também ao lado do arquivo, cada destino tem sua própria lista.</p>"
    "<h2>Compactar uma pasta</h2>"
    "<p>Escolha uma pasta de origem e onde salvar o ZIP. O hen-Zip coloca o "
    "conteúdo da pasta na raiz do arquivo ZIP. Compactar não move nem apaga "
    "a pasta ou os arquivos originais. O campo <b>Senha</b> é opcional e "
    "mascarado: "
    "preenchido, cria um ZIP protegido com criptografia AES-256; vazio, cria "
    "um ZIP sem senha.</p>"
     "<p>Na extração, digite no mesmo campo a senha do ZIP ou RAR, se ele estiver "
    "protegido. A senha não é salva nas configurações e precisa ser informada "
    "novamente quando o aplicativo for reaberto. Para abrir ZIPs AES-256, use "
    "um programa compatível, como 7-Zip ou WinRAR; o extrator padrão do "
     "Windows pode não abrir esse formato. A extração de RAR precisa do "
     "UnRAR, Unar ou bsdtar instalado e disponível no PATH.</p>"
    "<h2>Segurança e limites</h2>"
    "<ul>"
     "<li>Extrair grava arquivos nas pastas escolhidas; não recorta nem move "
     "os arquivos do ZIP ou RAR. A única remoção opcional é a do arquivo de "
     "origem, depois "
    "do sucesso completo.</li>"
     "<li>Os caminhos dentro dos arquivos compactados são verificados. Caminhos que tentem "
     "escrever fora do destino são rejeitados. Links simbólicos em RAR são "
     "rejeitados. Antes de substituir, cada "
    "arquivo é gravado temporariamente para reduzir o risco de ficar "
    "incompleto.</li>"
    "<li>Nenhum programa pode garantir que nunca haverá falha: ZIP danificado, "
    "falta de espaço ou falta de permissão podem impedir a operação. O "
    "hen-Zip informa o erro. Se o primeiro destino já foi extraído e uma "
    "segunda extração falhar, os arquivos já gravados no primeiro destino "
    "podem permanecer; o ZIP de origem não é apagado.</li>"
    "</ul>"
    "<h2>Quando terminar</h2>"
    "<p>O hen-Zip emite um alerta sonoro e mostra a confirmação. Você pode "
    "clicar em <b>Fechar</b> ou fora da janela para dispensá-la.</p>"
)
TXT_SECAO_OPERACOES = "Operações"
TXT_SECAO_DESCRICAO = "Configure a origem, o destino e escolha o que fazer."
TXT_COLUNA_ORIGEM = "ORIGEM"
TXT_COLUNA_DESTINO = "DESTINO"
TXT_COLUNA_ACAO = "AÇÃO"
TXT_MODO_COMPACTAR = "Compactar"
TXT_MODO_EXTRAIR = "Extrair"
TXT_ROTULO_ORIGEM = "Pasta para compactar"
TXT_ROTULO_ZIP_ORIGEM = "Arquivo compactado"
TXT_ROTULO_DESTINO_ZIP = "Salvar arquivo ZIP como"
TXT_ROTULO_DESTINO_PASTA = "Extrair para esta pasta"
TXT_PLACEHOLDER_ORIGEM_PASTA = "Pasta de origem"
TXT_PLACEHOLDER_ORIGEM_ZIP = "Arquivo ZIP ou RAR de origem"
TXT_PLACEHOLDER_DESTINO_ZIP = "Salvar arquivo ZIP em..."
TXT_PLACEHOLDER_DESTINO_PASTA = "Pasta de destino"
TXT_BOTAO_PROCURAR = "Procurar"
TXT_BOTAO_COMPACTAR = "Zipar"
TXT_BOTAO_EXTRAIR = "Extrair"
TXT_CHECKBOX_APAGAR_ZIP = "Apagar arquivo"
TXT_TOOLTIP_APAGAR_ZIP = (
    "Apaga o arquivo de origem somente após a extração terminar com sucesso. "
    "O caminho continua salvo."
)
TXT_CHECKBOX_EXTRAIR_JUNTO_ZIP = "Ao lado do arquivo"
TXT_TOOLTIP_EXTRAIR_JUNTO_ZIP = (
    "Com o destino vazio, extrai na pasta onde o ZIP ou RAR está. "
    "Com um destino preenchido, também extrai uma cópia ao lado do arquivo, "
    "mantendo a pasta-raiz interna mesmo quando ela já existe."
)
TXT_CHECKBOX_REMOVER_PASTA_RAIZ = "Remover raiz"
TXT_TOOLTIP_REMOVER_PASTA_RAIZ = (
    "Afeta somente o destino informado: marcado, remove a pasta-raiz mesmo "
    "quando o nome é diferente; desmarcado, mantém a pasta. Se os nomes "
    "coincidirem, ela é removida automaticamente no destino. A cópia ao lado "
    "do ZIP/RAR sempre mantém a pasta-raiz."
)
TXT_PLACEHOLDER_SENHA_ZIP = "Senha do arquivo"
TXT_TOOLTIP_SENHA_ZIP = (
    "Ao compactar, uma senha cria um ZIP com criptografia AES-256. "
    "Ao extrair, informe a senha do ZIP ou RAR. A senha não é salva."
)
TXT_ERRO_SENHA_ZIP_NECESSARIA = (
    "Este ZIP está protegido por senha. Digite a senha no campo da linha."
)
TXT_ERRO_SENHA_ZIP_INVALIDA = (
    "Não foi possível abrir o ZIP protegido. Confira a senha ou verifique "
    "se o arquivo está danificado."
)
TXT_BOTAO_REMOVER = "Remover esta operação"
TXT_ICON_REMOVER = "×"
TXT_ICON_MOVER_CIMA = "↑"
TXT_ICON_MOVER_BAIXO = "↓"
TXT_ICON_PUXADOR_REORDENAR = "⋮"
TXT_ICON_EXPANDIR_OPERACAO = "▸"
TXT_ICON_RECOLHER_OPERACAO = "▾"
TXT_TOOLTIP_PUXADOR_REORDENAR = "Segure e arraste para reorganizar esta linha"
TXT_TOOLTIP_MOVER_CIMA = "Mover esta linha para cima"
TXT_TOOLTIP_MOVER_BAIXO = "Mover esta linha para baixo"
TXT_TOOLTIP_EXPANDIR_OPERACAO = "Expandir os campos desta operação"
TXT_TOOLTIP_RECOLHER_OPERACAO = "Recolher os campos desta operação"
TXT_OPERACAO_SEM_NOME = "Operação sem nome"
TXT_TOOLTIP_REMOVER_DIVISORIA = "Remover este separador"
TXT_SELECIONAR_PASTA_ORIGEM = "Selecione a pasta para compactar"
TXT_SELECIONAR_ZIP_ORIGEM = "Selecione um arquivo ZIP ou RAR"
TXT_SELECIONAR_DESTINO_ZIP = "Salvar arquivo ZIP"
TXT_SELECIONAR_DESTINO_PASTA = "Selecione a pasta de destino"
TXT_FILTRO_ARQUIVO_ZIP = "Arquivos ZIP (*.zip)"
TXT_FILTRO_ARQUIVO_RAR = "Arquivos RAR (*.rar)"
TXT_FILTRO_TODOS_COMPACTADOS = "Todos os arquivos compactados (*.zip *.rar)"
FILTROS_ARQUIVO_COMPACTADO = (
    TXT_FILTRO_ARQUIVO_ZIP,
    TXT_FILTRO_ARQUIVO_RAR,
    TXT_FILTRO_TODOS_COMPACTADOS,
)
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
    "\n\nTambém extraídos ao lado do arquivo:\n{destino}"
)
TXT_MENSAGEM_ZIP_APAGADO = "\n\nArquivo de origem apagado:\n{arquivo}"
TXT_AVISO_ZIP_NAO_APAGADO = (
    "\n\nA extração foi concluída, mas não foi possível apagar o arquivo:\n"
    "{arquivo}\n\nDetalhes: {erro}"
)
TXT_LOG_ZIP_APAGADO = "Arquivo de origem apagado após extração: {arquivo}"
TXT_LOG_FALHA_APAGAR_ZIP = (
    "A extração terminou, mas não foi possível apagar o arquivo {arquivo}: {erro}"
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
    "Compacte pastas em ZIP e extraia ZIPs e RARs com controle sobre substituições."
)
TXT_ERRO_CAMINHO_VAZIO = "Informe os caminhos de origem e destino."
TXT_ERRO_ORIGEM_PASTA_INVALIDA = "A origem precisa ser uma pasta existente."
TXT_ERRO_ORIGEM_ZIP_INVALIDA = (
    "A origem precisa ser um arquivo ZIP ou RAR existente."
)
TXT_ERRO_DESTINO_PASTA_INVALIDO = "O destino informado precisa ser uma pasta."
TXT_ERRO_DESTINO_ZIP_INVALIDO = (
    "O destino do ZIP precisa apontar para um arquivo, não para uma pasta."
)
TXT_ERRO_ARQUIVO_ZIP_INVALIDO = (
    "O arquivo selecionado não é um ZIP ou RAR válido."
)
TXT_ERRO_RAR_INVALIDO = (
    "O arquivo selecionado não é um RAR válido ou está danificado."
)
TXT_ERRO_CAMINHO_ZIP_INSEGURO = (
    "O arquivo compactado contém um caminho inválido ou inseguro: {nome}"
)
TXT_ERRO_RAR_FERRAMENTA_AUSENTE = (
    "Para extrair RAR, instale o UnRAR, o Unar ou o bsdtar e deixe o executável "
    "disponível no PATH do sistema."
)
TXT_ERRO_RAR_VOLUME_INICIAL = (
    "Este RAR faz parte de um arquivo dividido. Selecione o primeiro volume "
    "do conjunto."
)
TXT_ERRO_RAR_SENHA_NECESSARIA = (
    "Este RAR está protegido por senha. Digite a senha no campo da linha."
)
TXT_ERRO_RAR_SENHA_INVALIDA = (
    "Não foi possível abrir o RAR protegido. Confira a senha ou verifique "
    "se o arquivo está danificado."
)
TXT_ERRO_RAR_CABECALHO_PROTEGIDO = (
    "Os cabeçalhos deste RAR estão criptografados, mas não há suporte de "
    "criptografia disponível para lê-los. Confira se a dependência de "
    "criptografia necessária está instalada."
)
TXT_ERRO_RAR_LINK = (
    "O RAR contém um link ou item especial, que não é extraído por segurança: {nome}"
)
TXT_ERRO_DESTINO_INCOMPATIVEL = (
    "O caminho do arquivo compactado não pode ser criado porque já existe um arquivo no caminho: {nome}"
)
TXT_ERRO_DESTINO_E_PASTA = (
    "Não é possível substituir o arquivo '{nome}' porque já existe uma pasta com esse nome."
)
TXT_ERRO_DESTINO_FORA_DA_PASTA = (
    "Um caminho do arquivo compactado aponta para fora da pasta de destino: {nome}"
)
TXT_ERRO_PASTA_ORIGEM_VAZIA = "Escolha uma pasta de origem."
TXT_ERRO_PASTA_DESTINO_VAZIA = "Escolha uma pasta de destino."
TXT_ERRO_ARQUIVO_DESTINO_VAZIO = "Escolha o caminho do arquivo ZIP."
TXT_ERRO_ACAO_ZIP_INVALIDA = "Ação de compactação ou extração desconhecida."
TXT_ERRO_ABRIR_LOGS = "Não foi possível abrir o arquivo de log:\n{caminho}"
TXT_LOG_PASTA_RAIZ_REMOVIDA = "Pasta raiz removida durante a extração: {nome}"
TXT_LOG_RESULTADO_EXTRAIR = (
    "Extração concluída: {destino} | {extraidos} arquivo(s) extraído(s), "
    "{mantidos} arquivo(s) mantido(s)."
)

# ══════════════════════════════════════════════════════════════════════════════
# TEXTOS DO EXPLORER
# ══════════════════════════════════════════════════════════════════════════════
EXPLORER_TEXTOS = {
    "title_open_file": "Abrir arquivo",
    "title_open_files": "Abrir arquivos",
    "title_select_folder": "Selecionar pasta",
    "title_save_file": "Salvar arquivo",
    "title_manage": "Gerenciar arquivos",
    "tooltip_back": "Voltar",
    "tooltip_forward": "Avançar",
    "tooltip_up": "Subir uma pasta",
    "tooltip_home": "Ir para a pasta pessoal",
    "tooltip_refresh": "Atualizar",
    "location": "Local:",
    "path_placeholder": "Digite ou escolha um caminho",
    "organize": "Organizar",
    "search_placeholder": "Pesquisar nesta pasta",
    "filename": "Nome do arquivo:",
    "file_type": "Tipo de arquivo:",
    "show_hidden": "Mostrar arquivos ocultos",
    "ready": "Pronto",
    "close": "Fechar",
    "cancel": "Cancelar",
    "select_folder": "Selecionar pasta",
    "save": "Salvar",
    "open": "Abrir",
    "copy_path": "Copiar caminho",
    "new_folder": "Nova pasta",
    "rename": "Renomear",
    "move_to_trash": "Mover para a lixeira",
    "sort_name": "Ordenar por nome",
    "sort_size": "Ordenar por tamanho",
    "sort_type": "Ordenar por tipo",
    "sort_modified": "Ordenar por data de modificação",
    "sort_descending": "Ordem decrescente",
    "place_home": "Pessoal",
    "place_desktop": "Área de Trabalho",
    "place_documents": "Documentos",
    "place_downloads": "Downloads",
    "place_pictures": "Imagens",
    "place_music": "Músicas",
    "place_videos": "Vídeos",
    "place_computer": "Computador",
    "preview_title": "Pré-visualização",
    "preview_image_placeholder": "Selecione um item para visualizar",
    "preview_empty": "Nenhum item selecionado",
    "preview_selected_count": "{count} itens selecionados",
    "preview_loading": "Carregando pré-visualização...",
    "preview_folder_details": (
        "{name}\nPasta\nTamanho: {size}\nArquivos: {files}\n"
        "Subpastas: {folders}\nModificado: {modified}\n{path}"
    ),
    "preview_partial": "Resumo parcial: alguns itens não foram contabilizados.",
    "preview_link": "Link simbólico",
    "preview_unavailable": "Pré-visualização indisponível",
    "preview_image_too_large": "Imagem excede o limite de pré-visualização",
    "preview_image_unreadable": "Não foi possível ler esta imagem",
    "preview_video_unavailable": "Pré-visualização de vídeo indisponível",
    "preview_file_details": (
        "{name}\n{kind}\nTipo: {file_type}\nTamanho: {size}\n"
        "Modificado: {modified}\n{path}"
    ),
    "preview_kind_image": "Imagem",
    "preview_kind_video": "Vídeo",
    "preview_kind_file": "Arquivo",
    "preview_kind_unknown": "Desconhecido",
    "items_selected": "{count} item(ns) selecionado(s)",
    "items_count": "{count} item(ns)",
    "error_title": "Erro",
    "invalid_location": "A pasta informada não existe ou não está disponível.",
    "new_folder_title": "Criar pasta",
    "new_folder_prompt": "Nome da nova pasta:",
    "invalid_name": "Informe um nome de arquivo ou pasta válido.",
    "new_folder_error": "Não foi possível criar a pasta.",
    "rename_title": "Renomear",
    "rename_prompt": "Novo nome:",
    "rename_error": "Não foi possível renomear o item.",
    "trash_confirm_title": "Mover para a lixeira?",
    "trash_confirm_message": (
        "O item selecionado será movido para a lixeira do sistema."
    ),
    "trash_error": "Não foi possível mover o item para a lixeira.",
    "empty_filename": "Informe o nome do arquivo.",
    "save_folder_error": "O caminho de destino é uma pasta.",
    "overwrite_title": "Substituir arquivo?",
    "overwrite_message": "Já existe um arquivo com esse nome. Deseja substituí-lo?",
    "file_required": "Selecione um arquivo para continuar.",
}

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
    background: {COR_TEXTO};
    color: {COR_ACENTO};
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
QLabel#operationSummary {{
    color: {COR_TEXTO};
    font-size: {FONTE_TAMANHO_INFO}px;
    font-weight: bold;
    padding-left: 8px;
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
QCheckBox#operationOptionCheck {{
    color: {COR_TEXTO};
    spacing: 7px;
}}
QLineEdit#operationPassword {{
    min-height: 30px;
    max-height: 34px;
    padding: 4px 10px;
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
QPushButton#browseButton {{
    min-height: {ALTURA_CAMPO}px;
    padding: 4px 5px;
}}
QPushButton#removeButton {{
    color: {COR_PERIGO};
    font-weight: bold;
    min-width: {LARGURA_BOTAO_REMOVER}px;
}}
QToolButton#orderButton {{
    background: transparent;
    border: none;
    color: {COR_TEXTO_SECUNDARIO};
    padding: 0;
    min-width: 24px;
    max-width: 24px;
    min-height: 18px;
    max-height: 18px;
}}
QToolButton#orderButton:hover {{
    background: {COR_BG_CAMPO};
    color: {COR_ACENTO_BORDA};
}}
QToolButton#reorderHandle {{
    background: transparent;
    border: none;
    color: {COR_TEXTO_SUTIL};
    padding: 0;
    min-width: 24px;
    max-width: 24px;
    min-height: 18px;
    max-height: 18px;
}}
QToolButton#reorderHandle:hover {{
    color: {COR_ACENTO_BORDA};
}}
QWidget#operationDivider {{ background: transparent; }}
QFrame#operationDividerLine {{
    background: transparent;
    border: none;
    border-top: 2px solid {COR_BORDA_CLARA};
}}
QFrame#operationDropIndicator {{
    background: {COR_ACENTO_BORDA};
    border: none;
}}
QPushButton#dividerRemoveButton {{
    min-width: 28px;
    max-width: 28px;
    min-height: 26px;
    max-height: 26px;
    padding: 0;
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
QTextBrowser#helpContent {{
    background: {COR_BG_CAMPO};
    color: {COR_TEXTO};
    border: 1px solid {COR_BORDA_CLARA};
    border-radius: 8px;
    padding: 10px;
}}
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

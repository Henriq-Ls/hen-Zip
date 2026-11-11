# _APP_/main_window.py
"""
MainWindow — Janela principal do projeto.

Responsabilidades:
  - Aplicar tema e estilo global (de _CONFIGURA_)
  - Restaurar e salvar geometria/estado via appdata
  - Conectar shutdown ao thread_manager
  - Montar a estrutura de painéis e widgets

Expanda este arquivo conforme o projeto crescer.
Painéis grandes devem ir para subpastas dentro de _APP_/.
"""

from _CONFIGURA_ import (
    TITULO_APP, VERSAO_APP,
    LARGURA_PADRAO, ALTURA_PADRAO,
    LARGURA_MIN, ALTURA_MIN,
    ALTURA_MARCA,
    LARGURA_MARCA,
    ATALHO_NOVO,
    ATALHO_SAIR,
    CHAVE_CONFIG_OPERACOES,
    CHAVE_ITEM_TIPO,
    ESPACO_INTERNO,
    ESPACO_LAYOUT,
    IMAGEM_ICO,
    LOGO_MARCA,
    INTERVALO_SALVAR_OPERACOES_MS,
    MARGEM_CARD,
    MARGEM_LAYOUT,
    ESTILO_ESCURO_GLOBAL,
    TXT_BOTAO_NOVA_OPERACAO,
    TXT_BOTAO_NOVO_SEPARADOR,
    TXT_BOTAO_AJUDA,
    TXT_BOTAO_ABRIR_LOGS,
    TXT_AVISO_ZIP_NAO_APAGADO,
    TXT_CONFIRMAR_SAIR_PROCESSANDO,
    TXT_CONFIRMAR_SUBSTITUIR_ZIP,
    TXT_ERRO_ABRIR_LOGS,
    TXT_ERRO_ARQUIVO_DESTINO_VAZIO,
    TXT_ERRO_CAMINHO_VAZIO,
    TXT_ERRO_ACAO_ZIP_INVALIDA,
    TXT_ERRO_DESTINO_PASTA_INVALIDO,
    TXT_ERRO_DESTINO_ZIP_INVALIDO,
    TXT_ERRO_ORIGEM_PASTA_INVALIDA,
    TXT_ERRO_ORIGEM_ZIP_INVALIDA,
    TXT_LOG_FALHA_APAGAR_ZIP,
    TXT_LOG_ZIP_APAGADO,
    TXT_MENSAGEM_ZIP_APAGADO,
    TXT_HERO_MARCA,
    TXT_HERO_SUBTITULO,
    TXT_HERO_TITULO,
    TXT_MENU_ARQUIVO,
    TXT_MENU_AJUDA,
    TXT_MENU_AJUDA_GUIA,
    TXT_MENU_NOVA_OPERACAO,
    TXT_MENU_SAIR,
    TXT_MENU_SOBRE,
    TXT_SECAO_DESCRICAO,
    TXT_SECAO_OPERACOES,
    TXT_STATUS_CANCELADO,
    TXT_STATUS_ERRO,
    TXT_STATUS_PRONTO,
    TXT_STATUS_PROCESSANDO,
    TXT_STATUS_SUCESSO,
    TXT_TITULO_AGUARDAR,
    TXT_TITULO_ERRO,
    TXT_TITULO_SUBSTITUIR_ZIP,
    TXT_TITULO_SUCESSO,
    TXT_SOBRE,
    VALOR_ITEM_DIVISORIA,
)
from _LOGS_ import log
from _APPDATA_ import appdata
from _THREADS_ import thread_manager

from PySide6.QtCore import Qt, QByteArray, QTimer, QUrl
from PySide6.QtGui import QAction, QDesktopServices, QPixmap
from PySide6.QtWidgets import (
    QApplication,
    QDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QProgressBar,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from _APP_.Painel_operacoes import DivisoriaOperacao, LinhaOperacao
from _APP_.Painel_operacoes.movimento_operacoes import AreaOperacoes
from _APP_.Painel_operacoes.dialogo_ajuda import DialogoAjuda
from _APP_.Painel_operacoes.dialogo_conflitos import DialogoConflitos
from _ULTILIDADES_.popups import (
    popup_aviso,
    popup_confirmar_perigo,
    popup_erro,
    popup_info,
)
from _ZIP_.operacoes import listar_conflitos
from _ZIP_.thread_zip import ThreadOperacaoZip

import os
import uuid


class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)
        log.info("MainWindow", "__init__", "inicializando janela principal...")
        self._linhas: list[LinhaOperacao] = []
        self._itens: list[LinhaOperacao | DivisoriaOperacao] = []
        self._threads: dict[str, ThreadOperacaoZip] = {}
        self._processando = False
        self._restaurando_operacoes = True
        self._timer_salvar_operacoes = QTimer(self)
        self._timer_salvar_operacoes.setSingleShot(True)
        self._timer_salvar_operacoes.setInterval(INTERVALO_SALVAR_OPERACOES_MS)
        self._timer_salvar_operacoes.timeout.connect(self._salvar_operacoes)

        self._configurar_janela()
        self._aplicar_estilo()
        self._montar_ui()
        self._restaurar_operacoes()
        self._montar_menu()
        self._restaurar_sessao()
        self._conectar_shutdown()

        log.ok("MainWindow", "__init__", "janela principal pronta")

    # ── Configuração ─────────────────────────────────────────────────────────

    def _configurar_janela(self):
        self.setWindowTitle(f"{TITULO_APP} {VERSAO_APP}")
        self.setMinimumSize(LARGURA_MIN, ALTURA_MIN)
        self.resize(LARGURA_PADRAO, ALTURA_PADRAO)

        # Ícone da janela
        import os
        if os.path.isfile(IMAGEM_ICO):
            from PySide6.QtGui import QIcon
            self.setWindowIcon(QIcon(IMAGEM_ICO))

    def _aplicar_estilo(self):
        self.setStyleSheet(ESTILO_ESCURO_GLOBAL)

    # ── UI ───────────────────────────────────────────────────────────────────

    def _montar_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setContentsMargins(
            MARGEM_LAYOUT, MARGEM_LAYOUT, MARGEM_LAYOUT, MARGEM_LAYOUT
        )
        layout.setSpacing(ESPACO_LAYOUT)

        hero = QFrame()
        hero.setObjectName("heroCard")
        hero_layout = QHBoxLayout(hero)
        hero_layout.setContentsMargins(
            MARGEM_CARD, MARGEM_CARD, MARGEM_CARD, MARGEM_CARD
        )
        hero_layout.setSpacing(ESPACO_LAYOUT)

        marca = QLabel(TXT_HERO_MARCA)
        marca.setObjectName("brandMark")
        marca.setAlignment(Qt.AlignmentFlag.AlignCenter)
        marca.setFixedSize(LARGURA_MARCA, ALTURA_MARCA)
        if os.path.isfile(LOGO_MARCA):
            logo = QPixmap(LOGO_MARCA)
            if not logo.isNull():
                marca.setPixmap(
                    logo.scaled(
                        LARGURA_MARCA - 18,
                        ALTURA_MARCA - 12,
                        Qt.AspectRatioMode.KeepAspectRatio,
                        Qt.TransformationMode.SmoothTransformation,
                    )
                )
                marca.setAccessibleName(TITULO_APP)
        hero_layout.addWidget(marca)

        textos_hero = QVBoxLayout()
        titulo = QLabel(TXT_HERO_TITULO)
        titulo.setObjectName("heroTitle")
        subtitulo = QLabel(TXT_HERO_SUBTITULO)
        subtitulo.setObjectName("heroSubtitle")
        textos_hero.addWidget(titulo)
        textos_hero.addWidget(subtitulo)
        hero_layout.addLayout(textos_hero, 1)

        self._botao_ajuda = QPushButton(TXT_BOTAO_AJUDA)
        self._botao_ajuda.setObjectName("secondaryButton")
        self._botao_ajuda.clicked.connect(self._abrir_ajuda)
        hero_layout.addWidget(self._botao_ajuda)

        self._botao_logs = QPushButton(TXT_BOTAO_ABRIR_LOGS)
        self._botao_logs.setObjectName("secondaryButton")
        self._botao_logs.clicked.connect(self._abrir_logs)
        hero_layout.addWidget(self._botao_logs)
        layout.addWidget(hero)

        painel = QFrame()
        painel.setObjectName("sectionCard")
        painel_layout = QVBoxLayout(painel)
        painel_layout.setContentsMargins(
            MARGEM_CARD, MARGEM_CARD, MARGEM_CARD, MARGEM_CARD
        )
        painel_layout.setSpacing(ESPACO_LAYOUT)

        cabecalho_painel = QHBoxLayout()
        textos_painel = QVBoxLayout()
        titulo_painel = QLabel(TXT_SECAO_OPERACOES)
        titulo_painel.setObjectName("sectionTitle")
        descricao = QLabel(TXT_SECAO_DESCRICAO)
        descricao.setObjectName("mutedLabel")
        textos_painel.addWidget(titulo_painel)
        textos_painel.addWidget(descricao)
        cabecalho_painel.addLayout(textos_painel, 1)

        self._botao_nova = QPushButton(TXT_BOTAO_NOVA_OPERACAO)
        self._botao_nova.setObjectName("secondaryButton")
        self._botao_nova.clicked.connect(self._ao_acao_nova)
        cabecalho_painel.addWidget(self._botao_nova)

        self._botao_nova_divisoria = QPushButton(TXT_BOTAO_NOVO_SEPARADOR)
        self._botao_nova_divisoria.setObjectName("secondaryButton")
        self._botao_nova_divisoria.clicked.connect(self._adicionar_divisoria)
        cabecalho_painel.addWidget(self._botao_nova_divisoria)

        painel_layout.addLayout(cabecalho_painel)

        self._area_linhas = AreaOperacoes()
        self._area_linhas.item_solto.connect(self._ao_soltar_item)
        self._layout_linhas = QVBoxLayout(self._area_linhas)
        self._layout_linhas.setContentsMargins(0, 0, 0, 0)
        self._layout_linhas.setSpacing(ESPACO_INTERNO)
        self._layout_linhas.addStretch(1)

        rolagem = QScrollArea()
        rolagem.setWidgetResizable(True)
        rolagem.setFrameShape(QFrame.Shape.NoFrame)
        rolagem.setWidget(self._area_linhas)
        painel_layout.addWidget(rolagem, 1)

        self._progresso = QProgressBar()
        self._progresso.setRange(0, 100)
        self._progresso.setValue(0)
        self._progresso.setTextVisible(False)
        self._progresso.setVisible(False)
        painel_layout.addWidget(self._progresso)
        layout.addWidget(painel, 1)

        self.statusBar().showMessage(TXT_STATUS_PRONTO)

        log.ok("MainWindow", "_montar_ui", "UI montada")

    def _montar_menu(self):
        menu_arquivo = self.menuBar().addMenu(TXT_MENU_ARQUIVO)
        acao_nova = QAction(TXT_MENU_NOVA_OPERACAO, self)
        acao_nova.setShortcut(ATALHO_NOVO)
        acao_nova.triggered.connect(self._ao_acao_nova)
        menu_arquivo.addAction(acao_nova)

        acao_sair = QAction(TXT_MENU_SAIR, self)
        acao_sair.setShortcut(ATALHO_SAIR)
        acao_sair.triggered.connect(self._ao_acao_sair)
        menu_arquivo.addAction(acao_sair)

        menu_ajuda = self.menuBar().addMenu(TXT_MENU_AJUDA)
        acao_guia = QAction(TXT_MENU_AJUDA_GUIA, self)
        acao_guia.triggered.connect(self._abrir_ajuda)
        menu_ajuda.addAction(acao_guia)
        menu_ajuda.addSeparator()
        acao_sobre = QAction(TXT_MENU_SOBRE, self)
        acao_sobre.triggered.connect(self._ao_acao_sobre)
        menu_ajuda.addAction(acao_sobre)

    def _ao_acao_nova(self, marcado: bool = False):
        self._adicionar_linha()

    def _ao_acao_sair(self, marcado: bool = False):
        self.close()

    def _abrir_ajuda(self, marcado: bool = False):
        DialogoAjuda(self).exec()

    def _ao_acao_sobre(self, marcado: bool = False):
        popup_info(
            TXT_MENU_SOBRE,
            TXT_SOBRE.format(versao=VERSAO_APP),
            self,
        )

    def _abrir_logs(self):
        caminho = log.caminho_geral
        if not os.path.isfile(caminho) or not QDesktopServices.openUrl(
            QUrl.fromLocalFile(caminho)
        ):
            popup_erro(
                TXT_TITULO_ERRO,
                TXT_ERRO_ABRIR_LOGS.format(caminho=caminho),
                self,
            )

    def _adicionar_linha(self):
        self._inserir_linha()
        self._agendar_salvamento_operacoes()

    def _adicionar_divisoria(self):
        if self._processando:
            return
        self._inserir_divisoria()
        self._agendar_salvamento_operacoes()

    def _inserir_linha(self, dados: dict | None = None):
        linha = LinhaOperacao(self._area_linhas)
        if dados is not None:
            linha.restaurar_dados(dados)
        linha.solicitar_operacao.connect(self._executar_operacao)
        linha.solicitar_remocao.connect(self._remover_item)
        linha.solicitar_mover.connect(self._mover_item)
        linha.operacao_alterada.connect(self._agendar_salvamento_operacoes)
        self._linhas.append(linha)
        self._itens.append(linha)
        indice = max(self._layout_linhas.count() - 1, 0)
        self._layout_linhas.insertWidget(indice, linha)
        linha.definir_ocupado(self._processando)
        self._botao_nova.setEnabled(not self._processando)
        self._botao_nova_divisoria.setEnabled(not self._processando)
        self._atualizar_controles_ordenacao()

    def _inserir_divisoria(self):
        divisoria = DivisoriaOperacao(self._area_linhas)
        divisoria.solicitar_remocao.connect(self._remover_item)
        divisoria.solicitar_mover.connect(self._mover_item)
        self._itens.append(divisoria)
        indice = max(self._layout_linhas.count() - 1, 0)
        self._layout_linhas.insertWidget(indice, divisoria)
        divisoria.definir_ocupado(self._processando)
        self._botao_nova_divisoria.setEnabled(not self._processando)
        self._atualizar_controles_ordenacao()

    def _remover_linha(self, linha: LinhaOperacao):
        self._remover_item(linha)

    def _remover_item(self, item: QWidget):
        if item not in self._itens:
            return
        self._itens.remove(item)
        if isinstance(item, LinhaOperacao):
            self._linhas.remove(item)
            try:
                item.solicitar_operacao.disconnect(self._executar_operacao)
            except (RuntimeError, TypeError):
                pass
            try:
                item.operacao_alterada.disconnect(self._agendar_salvamento_operacoes)
            except (RuntimeError, TypeError):
                pass
        try:
            item.solicitar_remocao.disconnect(self._remover_item)
            item.solicitar_mover.disconnect(self._mover_item)
        except (RuntimeError, TypeError):
            pass
        self._layout_linhas.removeWidget(item)
        item.setParent(None)
        item.deleteLater()
        self._atualizar_controles_ordenacao()
        self._agendar_salvamento_operacoes()

    def _mover_item(self, item: QWidget, direcao: int):
        if self._processando or item not in self._itens or direcao not in (-1, 1):
            return
        indice = self._itens.index(item)
        novo_indice = indice + direcao
        if not 0 <= novo_indice < len(self._itens):
            return
        self._reposicionar_item(item, novo_indice)

    def _ao_soltar_item(self, identificador: str, indice: int):
        if self._processando:
            return
        item = next(
            (atual for atual in self._itens if str(id(atual)) == identificador),
            None,
        )
        if item is not None:
            self._reposicionar_item(item, indice)

    def _reposicionar_item(self, item: QWidget, novo_indice: int):
        if self._processando or item not in self._itens:
            return
        indice = self._itens.index(item)
        novo_indice = max(0, min(novo_indice, len(self._itens) - 1))
        if indice == novo_indice:
            return
        self._itens.pop(indice)
        self._itens.insert(novo_indice, item)
        self._layout_linhas.removeWidget(item)
        self._layout_linhas.insertWidget(novo_indice, item)
        self._linhas = [
            atual for atual in self._itens if isinstance(atual, LinhaOperacao)
        ]
        self._atualizar_controles_ordenacao()
        self._agendar_salvamento_operacoes()

    def _atualizar_controles_ordenacao(self):
        self._area_linhas.definir_itens(self._itens)
        total = len(self._itens)
        for indice, item in enumerate(self._itens):
            item.definir_movimentos(indice > 0, indice < total - 1)

    def _restaurar_operacoes(self):
        """Carrega as linhas salvas no arquivo de configuração do usuário."""
        try:
            configuracao = appdata.ler_config()
            salvas = configuracao.get(CHAVE_CONFIG_OPERACOES)
            if isinstance(salvas, list):
                for dados in salvas:
                    if isinstance(dados, dict):
                        if dados.get(CHAVE_ITEM_TIPO) == VALOR_ITEM_DIVISORIA:
                            self._inserir_divisoria()
                        else:
                            self._inserir_linha(dados)
                if not salvas:
                    log.info(
                        "MainWindow",
                        "_restaurar_operacoes",
                        "nenhuma linha salva; mantendo a lista vazia",
                    )
            else:
                self._inserir_linha()
            log.ok(
                "MainWindow",
                "_restaurar_operacoes",
                f"{len(self._linhas)} linha(s) restaurada(s)",
            )
        except Exception as erro:
            log.erro("MainWindow", "_restaurar_operacoes", str(erro))
            if not self._linhas:
                self._inserir_linha()
        finally:
            self._restaurando_operacoes = False

    def _agendar_salvamento_operacoes(self):
        if not self._restaurando_operacoes:
            self._timer_salvar_operacoes.start()

    def _salvar_operacoes(self):
        """Persiste modo e caminhos das linhas no config.json do AppData."""
        try:
            configuracao = appdata.ler_config()
            configuracao[CHAVE_CONFIG_OPERACOES] = [
                item.exportar_dados() for item in self._itens
            ]
            appdata.salvar_config(configuracao)
            log.ok(
                "MainWindow",
                "_salvar_operacoes",
                f"{len(self._itens)} item(ns) salvo(s)",
            )
        except Exception as erro:
            log.erro("MainWindow", "_salvar_operacoes", str(erro))

    def _executar_operacao(
        self,
        acao: str,
        origem: str,
        destino: str,
        apagar_zip_apos_extrair: bool = False,
        extrair_junto_zip: bool = False,
        remover_pasta_raiz_diferente: bool = False,
        senha: str = "",
    ):
        if self._processando:
            return
        origem = os.path.expandvars(os.path.expanduser(origem))
        destino = os.path.expandvars(os.path.expanduser(destino))
        if not origem or (
            not destino
            and not (acao == "extrair" and extrair_junto_zip)
        ):
            popup_aviso(TITULO_APP, TXT_ERRO_CAMINHO_VAZIO, self)
            return

        substituir: set[str] = set()
        substituir_junto_zip: set[str] = set()
        extrair_na_pasta_do_zip = False
        preservar_pasta_raiz_destino = False
        try:
            if acao == "compactar":
                if not os.path.isdir(origem):
                    raise ValueError(TXT_ERRO_ORIGEM_PASTA_INVALIDA)
                if os.path.isdir(destino):
                    raise ValueError(TXT_ERRO_DESTINO_ZIP_INVALIDO)
                if not destino.lower().endswith(".zip"):
                    destino += ".zip"
                    emissor = self.sender()
                    if isinstance(emissor, LinhaOperacao):
                        emissor.definir_destino(destino)
                if os.path.exists(destino) and not popup_confirmar_perigo(
                    TXT_TITULO_SUBSTITUIR_ZIP,
                    TXT_CONFIRMAR_SUBSTITUIR_ZIP.format(destino=destino),
                    self,
                ):
                    self.statusBar().showMessage(TXT_STATUS_CANCELADO)
                    return
            elif acao == "extrair":
                if not os.path.isfile(origem):
                    raise ValueError(TXT_ERRO_ORIGEM_ZIP_INVALIDA)
                if not destino and extrair_junto_zip:
                    destino = os.path.dirname(os.path.abspath(origem))
                if os.path.exists(destino) and not os.path.isdir(destino):
                    raise ValueError(TXT_ERRO_DESTINO_PASTA_INVALIDO)

                pasta_zip = os.path.dirname(os.path.abspath(origem))
                identidade_pasta_zip = os.path.normcase(
                    os.path.realpath(pasta_zip)
                )
                identidade_destino = os.path.normcase(
                    os.path.realpath(os.path.abspath(destino))
                )
                destino_e_pasta_zip = (
                    extrair_junto_zip
                    and identidade_destino == identidade_pasta_zip
                )
                preservar_pasta_raiz_destino = destino_e_pasta_zip
                destinos_extracao = [
                    (
                        destino,
                        remover_pasta_raiz_diferente
                        and not destino_e_pasta_zip,
                        destino_e_pasta_zip,
                    )
                ]
                if extrair_junto_zip:
                    if not destino_e_pasta_zip:
                        destinos_extracao.append((pasta_zip, False, True))
                        extrair_na_pasta_do_zip = True

                for indice, (
                    destino_extracao,
                    remover_raiz_destino,
                    preservar_raiz_destino,
                ) in enumerate(destinos_extracao):
                    conflitos = listar_conflitos(
                        origem,
                        destino_extracao,
                        remover_raiz_destino,
                        senha=senha,
                        preservar_pasta_raiz=preservar_raiz_destino,
                    )
                    if not conflitos:
                        continue
                    dialogo = DialogoConflitos(
                        conflitos,
                        self,
                        destino_extracao,
                    )
                    if dialogo.exec() != QDialog.DialogCode.Accepted:
                        self.statusBar().showMessage(TXT_STATUS_CANCELADO)
                        return
                    if indice == 0:
                        substituir = dialogo.arquivos_selecionados()
                    else:
                        substituir_junto_zip = dialogo.arquivos_selecionados()
            else:
                raise ValueError(TXT_ERRO_ACAO_ZIP_INVALIDA)
        except Exception as erro:
            log.erro("MainWindow", "_executar_operacao", str(erro))
            popup_erro(TXT_TITULO_ERRO, str(erro), self)
            return

        nome_thread = f"operacao_zip_{uuid.uuid4().hex}"
        worker = ThreadOperacaoZip(
            nome=nome_thread,
            acao=acao,
            origem=origem,
            destino=destino,
            substituir=substituir,
            apagar_zip_apos_extrair=(
                acao == "extrair" and apagar_zip_apos_extrair
            ),
            extrair_junto_zip=(
                acao == "extrair" and extrair_na_pasta_do_zip
            ),
            substituir_junto_zip=substituir_junto_zip,
            remover_pasta_raiz_diferente=(
                acao == "extrair"
                and remover_pasta_raiz_diferente
                and not preservar_pasta_raiz_destino
            ),
            senha=senha,
            parent=self,
            preservar_pasta_raiz_destino=(
                acao == "extrair" and preservar_pasta_raiz_destino
            ),
        )
        worker.progresso.connect(self._ao_progresso)
        worker.concluido.connect(self._ao_operacao_concluida)
        worker.falhou.connect(self._ao_operacao_falhou)
        worker.finished.connect(self._limpar_threads_concluidas)
        self._threads[nome_thread] = worker
        self._definir_processando(True)
        self.statusBar().showMessage(TXT_STATUS_PROCESSANDO)
        worker.start()

    def _definir_processando(self, processando: bool):
        self._processando = processando
        for item in self._itens:
            item.definir_ocupado(processando)
        self._botao_nova.setEnabled(not processando)
        self._botao_nova_divisoria.setEnabled(not processando)
        self._progresso.setVisible(processando)
        if not processando:
            self._progresso.setValue(0)

    def _ao_progresso(self, nome: str, percentual: int, mensagem: str):
        self._progresso.setValue(percentual)
        self.statusBar().showMessage(mensagem)

    def _ao_operacao_concluida(
        self,
        nome: str,
        mensagem: str,
        origem: str = "",
        apagar_zip_apos_extrair: bool = False,
    ):
        self._definir_processando(False)
        self.statusBar().showMessage(TXT_STATUS_SUCESSO)
        QApplication.beep()
        if apagar_zip_apos_extrair:
            try:
                os.remove(origem)
                mensagem += TXT_MENSAGEM_ZIP_APAGADO.format(arquivo=origem)
                log.ok(
                    "MainWindow",
                    "_ao_operacao_concluida",
                    TXT_LOG_ZIP_APAGADO.format(arquivo=origem),
                )
            except OSError as erro:
                mensagem += TXT_AVISO_ZIP_NAO_APAGADO.format(
                    arquivo=origem,
                    erro=erro,
                )
                log.aviso(
                    "MainWindow",
                    "_ao_operacao_concluida",
                    TXT_LOG_FALHA_APAGAR_ZIP.format(arquivo=origem, erro=erro),
                )
                popup_aviso(TXT_TITULO_SUCESSO, mensagem, self)
                return
        popup_info(
            TXT_TITULO_SUCESSO,
            mensagem,
            self,
            fechar_ao_clicar_fora=True,
        )

    def _ao_operacao_falhou(self, nome: str, mensagem: str):
        self._definir_processando(False)
        self.statusBar().showMessage(TXT_STATUS_ERRO)
        popup_erro(TXT_TITULO_ERRO, mensagem, self)

    def _limpar_threads_concluidas(self):
        for nome, thread in list(self._threads.items()):
            if not thread.isRunning():
                self._threads.pop(nome, None)
                thread.deleteLater()

    # ── Sessão ───────────────────────────────────────────────────────────────

    def _restaurar_sessao(self):
        """Restaura geometria e estado salvos na sessão anterior."""
        sessao = appdata.ler_sessao()
        try:
            if "geometria" in sessao:
                self.restoreGeometry(QByteArray.fromBase64(
                    sessao["geometria"].encode()
                ))
            if "estado" in sessao:
                self.restoreState(QByteArray.fromBase64(
                    sessao["estado"].encode()
                ))
            log.ok("MainWindow", "_restaurar_sessao", "sessão restaurada")
        except Exception as e:
            log.aviso("MainWindow", "_restaurar_sessao", f"falha ao restaurar sessão: {e}")

    def _salvar_sessao(self):
        """Salva geometria e estado atual para a próxima sessão."""
        try:
            sessao = {
                "geometria": self.saveGeometry().toBase64().data().decode(),
                "estado":    self.saveState().toBase64().data().decode(),
            }
            appdata.salvar_sessao(sessao)
        except Exception as e:
            log.erro("MainWindow", "_salvar_sessao", f"falha ao salvar sessão: {e}")

    # ── Shutdown ─────────────────────────────────────────────────────────────

    def _conectar_shutdown(self):
        """Conecta encerramento ordenado ao sinal aboutToQuit."""
        from PySide6.QtWidgets import QApplication
        app = QApplication.instance()
        if app:
            app.aboutToQuit.connect(self._ao_encerrar)

    def _ao_encerrar(self):
        log.info("MainWindow", "_ao_encerrar", "encerrando aplicação...")
        if self._timer_salvar_operacoes.isActive():
            self._timer_salvar_operacoes.stop()
            self._salvar_operacoes()
        thread_manager.encerrar_todas()
        log.info("MainWindow", "_ao_encerrar", "shutdown concluído")

    def closeEvent(self, event):
        log.info("MainWindow", "closeEvent", "janela fechando...")
        if self._processando:
            popup_aviso(TXT_TITULO_AGUARDAR, TXT_CONFIRMAR_SAIR_PROCESSANDO, self)
            event.ignore()
            return
        self._timer_salvar_operacoes.stop()
        self._salvar_operacoes()
        self._salvar_sessao()
        super().closeEvent(event)

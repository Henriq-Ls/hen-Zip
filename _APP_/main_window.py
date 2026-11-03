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
    ATALHO_NOVO,
    ATALHO_SAIR,
    ESPACO_INTERNO,
    ESPACO_LAYOUT,
    IMAGEM_ICO,
    MARGEM_CARD,
    MARGEM_LAYOUT,
    ESTILO_ESCURO_GLOBAL,
    TXT_BOTAO_NOVA_OPERACAO,
    TXT_COLUNA_ACAO,
    TXT_COLUNA_DESTINO,
    TXT_COLUNA_ORIGEM,
    TXT_CONFIRMAR_SAIR_PROCESSANDO,
    TXT_CONFIRMAR_SUBSTITUIR_ZIP,
    TXT_ERRO_ARQUIVO_DESTINO_VAZIO,
    TXT_ERRO_CAMINHO_VAZIO,
    TXT_ERRO_ACAO_ZIP_INVALIDA,
    TXT_ERRO_DESTINO_PASTA_INVALIDO,
    TXT_ERRO_DESTINO_ZIP_INVALIDO,
    TXT_ERRO_ORIGEM_PASTA_INVALIDA,
    TXT_ERRO_ORIGEM_ZIP_INVALIDA,
    TXT_HERO_MARCA,
    TXT_HERO_SUBTITULO,
    TXT_HERO_TITULO,
    TXT_MENU_ARQUIVO,
    TXT_MENU_AJUDA,
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
)
from _LOGS_ import log
from _APPDATA_ import appdata
from _THREADS_ import thread_manager

from PySide6.QtCore import Qt, QByteArray
from PySide6.QtGui import QAction
from PySide6.QtWidgets import (
    QDialog,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QProgressBar,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from _APP_.Painel_operacoes import LinhaOperacao
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
        self._threads: dict[str, ThreadOperacaoZip] = {}
        self._processando = False

        self._configurar_janela()
        self._aplicar_estilo()
        self._montar_ui()
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
        marca.setFixedSize(ALTURA_MARCA, ALTURA_MARCA)
        hero_layout.addWidget(marca)

        textos_hero = QVBoxLayout()
        titulo = QLabel(TXT_HERO_TITULO)
        titulo.setObjectName("heroTitle")
        subtitulo = QLabel(TXT_HERO_SUBTITULO)
        subtitulo.setObjectName("heroSubtitle")
        textos_hero.addWidget(titulo)
        textos_hero.addWidget(subtitulo)
        hero_layout.addLayout(textos_hero, 1)
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
        painel_layout.addLayout(cabecalho_painel)

        cabecalho_colunas = QFrame()
        cabecalho_colunas.setObjectName("tableHeader")
        grade_cabecalho = QGridLayout(cabecalho_colunas)
        grade_cabecalho.setContentsMargins(MARGEM_CARD, 0, MARGEM_CARD, 0)
        grade_cabecalho.setHorizontalSpacing(ESPACO_LAYOUT)
        grade_cabecalho.setColumnStretch(0, 5)
        grade_cabecalho.setColumnStretch(1, 5)
        grade_cabecalho.setColumnStretch(2, 2)
        for coluna, texto in enumerate(
            (TXT_COLUNA_ORIGEM, TXT_COLUNA_DESTINO, TXT_COLUNA_ACAO)
        ):
            rotulo = QLabel(texto)
            rotulo.setObjectName("columnHeader")
            grade_cabecalho.addWidget(rotulo, 0, coluna)
        painel_layout.addWidget(cabecalho_colunas)

        self._area_linhas = QWidget()
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

        self._adicionar_linha()
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
        acao_sobre = QAction(TXT_MENU_SOBRE, self)
        acao_sobre.triggered.connect(self._ao_acao_sobre)
        menu_ajuda.addAction(acao_sobre)

    def _ao_acao_nova(self, marcado: bool = False):
        self._adicionar_linha()

    def _ao_acao_sair(self, marcado: bool = False):
        self.close()

    def _ao_acao_sobre(self, marcado: bool = False):
        popup_info(
            TXT_MENU_SOBRE,
            TXT_SOBRE.format(versao=VERSAO_APP),
            self,
        )

    def _adicionar_linha(self):
        linha = LinhaOperacao(self._area_linhas)
        linha.solicitar_operacao.connect(self._executar_operacao)
        linha.solicitar_remocao.connect(self._remover_linha)
        self._linhas.append(linha)
        indice = max(self._layout_linhas.count() - 1, 0)
        self._layout_linhas.insertWidget(indice, linha)
        linha.definir_ocupado(self._processando)
        self._botao_nova.setEnabled(not self._processando)

    def _remover_linha(self, linha: LinhaOperacao):
        if linha not in self._linhas:
            return
        self._linhas.remove(linha)
        self._layout_linhas.removeWidget(linha)
        try:
            linha.solicitar_operacao.disconnect(self._executar_operacao)
        except (RuntimeError, TypeError):
            pass
        try:
            linha.solicitar_remocao.disconnect(self._remover_linha)
        except (RuntimeError, TypeError):
            pass
        linha.setParent(None)
        linha.deleteLater()

    def _executar_operacao(self, acao: str, origem: str, destino: str):
        if self._processando:
            return
        origem = os.path.expandvars(os.path.expanduser(origem))
        destino = os.path.expandvars(os.path.expanduser(destino))
        if not origem or not destino:
            popup_aviso(TITULO_APP, TXT_ERRO_CAMINHO_VAZIO, self)
            return

        substituir: set[str] = set()
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
                if os.path.exists(destino) and not os.path.isdir(destino):
                    raise ValueError(TXT_ERRO_DESTINO_PASTA_INVALIDO)
                conflitos = listar_conflitos(origem, destino)
                if conflitos:
                    dialogo = DialogoConflitos(conflitos, self)
                    if dialogo.exec() != QDialog.DialogCode.Accepted:
                        self.statusBar().showMessage(TXT_STATUS_CANCELADO)
                        return
                    substituir = dialogo.arquivos_selecionados()
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
            parent=self,
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
        for linha in self._linhas:
            linha.definir_ocupado(processando)
        self._botao_nova.setEnabled(not processando)
        self._progresso.setVisible(processando)
        if not processando:
            self._progresso.setValue(0)

    def _ao_progresso(self, nome: str, percentual: int, mensagem: str):
        self._progresso.setValue(percentual)
        self.statusBar().showMessage(mensagem)

    def _ao_operacao_concluida(self, nome: str, mensagem: str):
        self._definir_processando(False)
        self.statusBar().showMessage(TXT_STATUS_SUCESSO)
        popup_info(TXT_TITULO_SUCESSO, mensagem, self)

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
        thread_manager.encerrar_todas()
        log.info("MainWindow", "_ao_encerrar", "shutdown concluído")

    def closeEvent(self, event):
        log.info("MainWindow", "closeEvent", "janela fechando...")
        if self._processando:
            popup_aviso(TXT_TITULO_AGUARDAR, TXT_CONFIRMAR_SAIR_PROCESSANDO, self)
            event.ignore()
            return
        self._salvar_sessao()
        super().closeEvent(event)

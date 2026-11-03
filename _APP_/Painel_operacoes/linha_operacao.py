"""Linha editável de compactação ou extração."""

from _CONFIGURA_ import (
    ALTURA_BOTAO,
    ALTURA_LINHA_OPERACAO,
    CHAVE_OPERACAO_DESTINO,
    CHAVE_OPERACAO_MODO,
    CHAVE_OPERACAO_ORIGEM,
    CHAVE_OPERACAO_APAGAR_ZIP,
    CHAVE_OPERACAO_EXTRAIR_JUNTO_ZIP,
    ESPACO_INTERNO,
    LARGURA_BOTAO_EXECUTAR,
    LARGURA_BOTAO_PROCURAR,
    LARGURA_BOTAO_REMOVER,
    LARGURA_CAMPO_CAMINHO_MIN,
    MARGEM_CARD,
    TXT_BOTAO_COMPACTAR,
    TXT_BOTAO_EXTRAIR,
    TXT_BOTAO_PROCURAR,
    TXT_BOTAO_REMOVER,
    TXT_CHECKBOX_APAGAR_ZIP,
    TXT_CHECKBOX_EXTRAIR_JUNTO_ZIP,
    TXT_FILTRO_ARQUIVO_ZIP,
    TXT_ICON_REMOVER,
    TXT_MODO_COMPACTAR,
    TXT_MODO_EXTRAIR,
    TXT_PLACEHOLDER_DESTINO_PASTA,
    TXT_PLACEHOLDER_DESTINO_ZIP,
    TXT_PLACEHOLDER_ORIGEM_PASTA,
    TXT_PLACEHOLDER_ORIGEM_ZIP,
    TXT_ROTULO_DESTINO_PASTA,
    TXT_ROTULO_DESTINO_ZIP,
    TXT_ROTULO_ORIGEM,
    TXT_ROTULO_ZIP_ORIGEM,
    TXT_SELECIONAR_DESTINO_PASTA,
    TXT_SELECIONAR_DESTINO_ZIP,
    TXT_SELECIONAR_PASTA_ORIGEM,
    TXT_SELECIONAR_ZIP_ORIGEM,
    TXT_TOOLTIP_APAGAR_ZIP,
    TXT_TOOLTIP_EXTRAIR_JUNTO_ZIP,
)

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QAction
from PySide6.QtWidgets import (
    QFileDialog,
    QCheckBox,
    QHBoxLayout,
    QLineEdit,
    QMenu,
    QPushButton,
    QToolButton,
    QWidget,
)

import os


class LinhaOperacao(QWidget):
    solicitar_operacao = Signal(str, str, str, bool, bool)
    solicitar_remocao = Signal(object)
    operacao_alterada = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("operationRow")
        self._montar_ui()
        self._conectar_sinais()
        self._definir_modo("extrair")

    def _montar_ui(self):
        self.setMinimumHeight(ALTURA_LINHA_OPERACAO)
        linha = QHBoxLayout(self)
        linha.setContentsMargins(
            MARGEM_CARD, ESPACO_INTERNO, MARGEM_CARD, ESPACO_INTERNO
        )
        linha.setSpacing(8)

        self._modo_atual = "extrair"

        self._origem = QLineEdit()
        self._origem.setMinimumWidth(LARGURA_CAMPO_CAMINHO_MIN)
        self._origem.setClearButtonEnabled(True)
        self._botao_origem = QPushButton(TXT_BOTAO_PROCURAR)
        self._botao_origem.setObjectName("browseButton")
        self._botao_origem.setFixedWidth(LARGURA_BOTAO_PROCURAR)

        self._destino = QLineEdit()
        self._destino.setMinimumWidth(LARGURA_CAMPO_CAMINHO_MIN)
        self._destino.setClearButtonEnabled(True)
        self._botao_destino = QPushButton(TXT_BOTAO_PROCURAR)
        self._botao_destino.setObjectName("browseButton")
        self._botao_destino.setFixedWidth(LARGURA_BOTAO_PROCURAR)

        self._checkbox_apagar_zip = QCheckBox(TXT_CHECKBOX_APAGAR_ZIP)
        self._checkbox_apagar_zip.setObjectName("deleteArchiveCheck")
        self._checkbox_apagar_zip.setToolTip(TXT_TOOLTIP_APAGAR_ZIP)

        self._checkbox_extrair_junto_zip = QCheckBox(
            TXT_CHECKBOX_EXTRAIR_JUNTO_ZIP
        )
        self._checkbox_extrair_junto_zip.setObjectName("extractBesideArchiveCheck")
        self._checkbox_extrair_junto_zip.setToolTip(
            TXT_TOOLTIP_EXTRAIR_JUNTO_ZIP
        )

        self._botao_executar = QToolButton()
        self._botao_executar.setObjectName("primaryButton")
        self._botao_executar.setToolButtonStyle(
            Qt.ToolButtonStyle.ToolButtonTextOnly
        )
        self._botao_executar.setPopupMode(
            QToolButton.ToolButtonPopupMode.MenuButtonPopup
        )
        self._botao_executar.setFixedWidth(LARGURA_BOTAO_EXECUTAR)
        self._botao_executar.setMinimumHeight(ALTURA_BOTAO)
        menu_modo = QMenu(self._botao_executar)
        self._acao_modo_extrair = QAction(TXT_MODO_EXTRAIR, menu_modo)
        self._acao_modo_compactar = QAction(TXT_MODO_COMPACTAR, menu_modo)
        menu_modo.addAction(self._acao_modo_extrair)
        menu_modo.addAction(self._acao_modo_compactar)
        self._botao_executar.setMenu(menu_modo)

        self._botao_remover = QPushButton(TXT_ICON_REMOVER)
        self._botao_remover.setObjectName("removeButton")
        self._botao_remover.setFixedWidth(LARGURA_BOTAO_REMOVER)
        self._botao_remover.setToolTip(TXT_BOTAO_REMOVER)

        linha.addWidget(self._origem, 1)
        linha.addWidget(self._botao_origem)
        linha.addWidget(self._destino, 1)
        linha.addWidget(self._botao_destino)
        linha.addWidget(self._checkbox_apagar_zip)
        linha.addWidget(self._checkbox_extrair_junto_zip)
        linha.addWidget(self._botao_executar)
        linha.addWidget(self._botao_remover)

    def _conectar_sinais(self):
        self._origem.textChanged.connect(self._ao_editar_caminho)
        self._destino.textChanged.connect(self._ao_editar_caminho)
        self._botao_origem.clicked.connect(self._procurar_origem)
        self._botao_destino.clicked.connect(self._procurar_destino)
        self._botao_executar.clicked.connect(self._emitir_operacao)
        self._botao_remover.clicked.connect(self._emitir_remocao)
        self._checkbox_apagar_zip.toggled.connect(self._ao_editar_apagar_zip)
        self._checkbox_extrair_junto_zip.toggled.connect(
            self._ao_editar_extrair_junto_zip
        )
        self._acao_modo_extrair.triggered.connect(self._selecionar_extracao)
        self._acao_modo_compactar.triggered.connect(self._selecionar_compactacao)

    def _definir_modo(self, modo: str):
        self._modo_atual = modo
        compactar = modo == "compactar"
        self._origem.setPlaceholderText(
            TXT_PLACEHOLDER_ORIGEM_PASTA if compactar else TXT_PLACEHOLDER_ORIGEM_ZIP
        )
        self._destino.setPlaceholderText(
            TXT_PLACEHOLDER_DESTINO_ZIP if compactar else TXT_PLACEHOLDER_DESTINO_PASTA
        )
        self._botao_executar.setText(
            TXT_BOTAO_COMPACTAR if compactar else TXT_BOTAO_EXTRAIR
        )
        self._checkbox_apagar_zip.setVisible(not compactar)
        self._checkbox_extrair_junto_zip.setVisible(not compactar)
        self.operacao_alterada.emit()

    def _selecionar_extracao(self, marcado: bool = False):
        self._definir_modo("extrair")

    def _selecionar_compactacao(self, marcado: bool = False):
        self._definir_modo("compactar")

    def _ao_editar_caminho(self, texto: str):
        self.operacao_alterada.emit()

    def _ao_editar_apagar_zip(self, marcado: bool):
        self.operacao_alterada.emit()

    def _ao_editar_extrair_junto_zip(self, marcado: bool):
        self.operacao_alterada.emit()

    def _procurar_origem(self):
        if self._modo_atual == "compactar":
            selecionado = QFileDialog.getExistingDirectory(
                self,
                TXT_SELECIONAR_PASTA_ORIGEM,
                self._diretorio_inicial(self._origem.text()),
            )
        else:
            selecionado, _ = QFileDialog.getOpenFileName(
                self,
                TXT_SELECIONAR_ZIP_ORIGEM,
                self._diretorio_inicial(self._origem.text()),
                TXT_FILTRO_ARQUIVO_ZIP,
            )
        if selecionado:
            self._origem.setText(selecionado)

    def _procurar_destino(self):
        if self._modo_atual == "compactar":
            selecionado, _ = QFileDialog.getSaveFileName(
                self,
                TXT_SELECIONAR_DESTINO_ZIP,
                self._diretorio_inicial(self._destino.text()),
                TXT_FILTRO_ARQUIVO_ZIP,
            )
        else:
            selecionado = QFileDialog.getExistingDirectory(
                self,
                TXT_SELECIONAR_DESTINO_PASTA,
                self._diretorio_inicial(self._destino.text()),
            )
        if selecionado:
            self._destino.setText(selecionado)

    def _diretorio_inicial(self, texto: str) -> str:
        caminho = os.path.expanduser(texto.strip())
        if os.path.isdir(caminho):
            return caminho
        if os.path.isfile(caminho):
            return os.path.dirname(caminho)
        pasta = os.path.dirname(caminho)
        if pasta and os.path.isdir(pasta):
            return pasta
        return os.path.expanduser("~")

    def _emitir_operacao(self, marcado: bool = False):
        self.solicitar_operacao.emit(
            self._modo_atual,
            self._origem.text().strip(),
            self._destino.text().strip(),
            self._checkbox_apagar_zip.isChecked(),
            self._checkbox_extrair_junto_zip.isChecked(),
        )

    def _emitir_remocao(self):
        self.solicitar_remocao.emit(self)

    def definir_destino(self, caminho: str):
        self._destino.setText(caminho)

    def restaurar_dados(self, dados: dict):
        modo = dados.get(CHAVE_OPERACAO_MODO)
        if modo in ("extrair", "compactar"):
            self._definir_modo(modo)
        origem = dados.get(CHAVE_OPERACAO_ORIGEM, "")
        destino = dados.get(CHAVE_OPERACAO_DESTINO, "")
        apagar_zip = dados.get(CHAVE_OPERACAO_APAGAR_ZIP, False)
        extrair_junto_zip = dados.get(CHAVE_OPERACAO_EXTRAIR_JUNTO_ZIP, False)
        self._origem.setText(origem if isinstance(origem, str) else "")
        self._destino.setText(destino if isinstance(destino, str) else "")
        self._checkbox_apagar_zip.setChecked(apagar_zip is True)
        self._checkbox_extrair_junto_zip.setChecked(extrair_junto_zip is True)

    def exportar_dados(self) -> dict[str, str | bool]:
        return {
            CHAVE_OPERACAO_MODO: self._modo_atual,
            CHAVE_OPERACAO_ORIGEM: self._origem.text(),
            CHAVE_OPERACAO_DESTINO: self._destino.text(),
            CHAVE_OPERACAO_APAGAR_ZIP: self._checkbox_apagar_zip.isChecked(),
            CHAVE_OPERACAO_EXTRAIR_JUNTO_ZIP: (
                self._checkbox_extrair_junto_zip.isChecked()
            ),
        }

    def definir_ocupado(self, ocupado: bool):
        self._origem.setEnabled(not ocupado)
        self._destino.setEnabled(not ocupado)
        self._botao_origem.setEnabled(not ocupado)
        self._botao_destino.setEnabled(not ocupado)
        self._checkbox_apagar_zip.setEnabled(not ocupado)
        self._checkbox_extrair_junto_zip.setEnabled(not ocupado)
        self._botao_executar.setEnabled(not ocupado)
        self._botao_remover.setEnabled(not ocupado)

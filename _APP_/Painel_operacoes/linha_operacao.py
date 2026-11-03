"""Linha editável de compactação ou extração."""

from _CONFIGURA_ import (
    ALTURA_BOTAO,
    ALTURA_LINHA_OPERACAO,
    ESPACO_INTERNO,
    ESPACO_LAYOUT,
    LARGURA_BOTAO_EXECUTAR,
    LARGURA_BOTAO_REMOVER,
    MARGEM_CARD,
    TXT_BOTAO_COMPACTAR,
    TXT_BOTAO_EXTRAIR,
    TXT_BOTAO_PROCURAR,
    TXT_BOTAO_REMOVER,
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
)

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QFileDialog,
    QComboBox,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

import os


class LinhaOperacao(QWidget):
    solicitar_operacao = Signal(str, str, str)
    solicitar_remocao = Signal(object)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("operationRow")
        self._montar_ui()
        self._conectar_sinais()
        self._ao_mudar_modo()

    def _montar_ui(self):
        self.setMinimumHeight(ALTURA_LINHA_OPERACAO)
        grade = QGridLayout(self)
        grade.setContentsMargins(MARGEM_CARD, MARGEM_CARD, MARGEM_CARD, MARGEM_CARD)
        grade.setHorizontalSpacing(ESPACO_LAYOUT)
        grade.setVerticalSpacing(ESPACO_INTERNO)
        grade.setColumnStretch(0, 5)
        grade.setColumnStretch(1, 5)
        grade.setColumnStretch(2, 2)

        self._modo = QComboBox()
        self._modo.addItem(TXT_MODO_EXTRAIR, "extrair")
        self._modo.addItem(TXT_MODO_COMPACTAR, "compactar")

        self._rotulo_origem = QLabel()
        self._origem = QLineEdit()
        self._botao_origem = QPushButton(TXT_BOTAO_PROCURAR)
        self._botao_origem.setObjectName("browseButton")

        caixa_origem = QWidget()
        layout_origem = QVBoxLayout(caixa_origem)
        layout_origem.setContentsMargins(0, 0, 0, 0)
        layout_origem.setSpacing(ESPACO_INTERNO)
        linha_origem = QHBoxLayout()
        linha_origem.setContentsMargins(0, 0, 0, 0)
        linha_origem.setSpacing(ESPACO_INTERNO)
        linha_origem.addWidget(self._origem, 1)
        linha_origem.addWidget(self._botao_origem)
        layout_origem.addWidget(self._modo)
        layout_origem.addWidget(self._rotulo_origem)
        layout_origem.addLayout(linha_origem)

        self._rotulo_destino = QLabel()
        self._destino = QLineEdit()
        self._botao_destino = QPushButton(TXT_BOTAO_PROCURAR)
        self._botao_destino.setObjectName("browseButton")

        caixa_destino = QWidget()
        layout_destino = QVBoxLayout(caixa_destino)
        layout_destino.setContentsMargins(0, 0, 0, 0)
        layout_destino.setSpacing(ESPACO_INTERNO)
        linha_destino = QHBoxLayout()
        linha_destino.setContentsMargins(0, 0, 0, 0)
        linha_destino.setSpacing(ESPACO_INTERNO)
        linha_destino.addWidget(self._destino, 1)
        linha_destino.addWidget(self._botao_destino)
        layout_destino.addWidget(self._rotulo_destino)
        layout_destino.addLayout(linha_destino)

        self._botao_executar = QPushButton()
        self._botao_executar.setObjectName("primaryButton")
        self._botao_executar.setMinimumWidth(LARGURA_BOTAO_EXECUTAR)
        self._botao_executar.setMinimumHeight(ALTURA_BOTAO)
        self._botao_remover = QPushButton(TXT_ICON_REMOVER)
        self._botao_remover.setObjectName("removeButton")
        self._botao_remover.setFixedWidth(LARGURA_BOTAO_REMOVER)
        self._botao_remover.setToolTip(TXT_BOTAO_REMOVER)

        caixa_acoes = QWidget()
        layout_acoes = QVBoxLayout(caixa_acoes)
        layout_acoes.setContentsMargins(0, 0, 0, 0)
        layout_acoes.setSpacing(ESPACO_INTERNO)
        layout_acoes.addStretch(1)
        layout_acoes.addWidget(self._botao_executar)
        layout_acoes.addWidget(self._botao_remover)
        layout_acoes.addStretch(1)

        grade.addWidget(caixa_origem, 0, 0)
        grade.addWidget(caixa_destino, 0, 1)
        grade.addWidget(caixa_acoes, 0, 2, Qt.AlignmentFlag.AlignCenter)

    def _conectar_sinais(self):
        self._modo.currentIndexChanged.connect(self._ao_mudar_modo)
        self._botao_origem.clicked.connect(self._procurar_origem)
        self._botao_destino.clicked.connect(self._procurar_destino)
        self._botao_executar.clicked.connect(self._emitir_operacao)
        self._botao_remover.clicked.connect(self._emitir_remocao)

    def _ao_mudar_modo(self, indice: int = 0):
        compactar = self._modo.currentData() == "compactar"
        self._rotulo_origem.setText(
            TXT_ROTULO_ORIGEM if compactar else TXT_ROTULO_ZIP_ORIGEM
        )
        self._rotulo_destino.setText(
            TXT_ROTULO_DESTINO_ZIP if compactar else TXT_ROTULO_DESTINO_PASTA
        )
        self._origem.setPlaceholderText(
            TXT_PLACEHOLDER_ORIGEM_PASTA if compactar else TXT_PLACEHOLDER_ORIGEM_ZIP
        )
        self._destino.setPlaceholderText(
            TXT_PLACEHOLDER_DESTINO_ZIP if compactar else TXT_PLACEHOLDER_DESTINO_PASTA
        )
        self._botao_executar.setText(
            TXT_BOTAO_COMPACTAR if compactar else TXT_BOTAO_EXTRAIR
        )

    def _procurar_origem(self):
        if self._modo.currentData() == "compactar":
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
        if self._modo.currentData() == "compactar":
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
        return os.path.expanduser("~")

    def _emitir_operacao(self):
        self.solicitar_operacao.emit(
            self._modo.currentData(),
            self._origem.text().strip(),
            self._destino.text().strip(),
        )

    def _emitir_remocao(self):
        self.solicitar_remocao.emit(self)

    def definir_destino(self, caminho: str):
        self._destino.setText(caminho)

    def definir_ocupado(self, ocupado: bool):
        self._modo.setEnabled(not ocupado)
        self._origem.setEnabled(not ocupado)
        self._destino.setEnabled(not ocupado)
        self._botao_origem.setEnabled(not ocupado)
        self._botao_destino.setEnabled(not ocupado)
        self._botao_executar.setEnabled(not ocupado)
        self._botao_remover.setEnabled(not ocupado)

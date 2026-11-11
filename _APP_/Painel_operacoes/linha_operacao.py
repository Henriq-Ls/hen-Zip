"""Linha editável de compactação ou extração."""

from _CONFIGURA_ import (
    ALTURA_BOTAO,
    ALTURA_LINHA_OPERACAO,
    CHAVE_OPERACAO_DESTINO,
    CHAVE_OPERACAO_MODO,
    CHAVE_OPERACAO_ORIGEM,
    CHAVE_OPERACAO_APAGAR_ZIP,
    CHAVE_OPERACAO_EXTRAIR_JUNTO_ZIP,
    CHAVE_OPERACAO_REMOVER_PASTA_RAIZ,
    ESPACO_INTERNO,
    FILTROS_ARQUIVO_COMPACTADO,
    LARGURA_BOTAO_EXECUTAR,
    LARGURA_BOTAO_PROCURAR,
    LARGURA_BOTAO_REMOVER,
    LARGURA_CAMPO_CAMINHO_MIN,
    MARGEM_CARD,
    LARGURA_CAMPO_SENHA,
    TXT_BOTAO_COMPACTAR,
    TXT_BOTAO_EXTRAIR,
    TXT_BOTAO_PROCURAR,
    TXT_BOTAO_REMOVER,
    TXT_CHECKBOX_APAGAR_ZIP,
    TXT_CHECKBOX_EXTRAIR_JUNTO_ZIP,
    TXT_CHECKBOX_REMOVER_PASTA_RAIZ,
    TXT_FILTRO_ARQUIVO_ZIP,
    TXT_FILTRO_ARQUIVO_RAR,
    TXT_FILTRO_TODOS_COMPACTADOS,
    TXT_ICON_REMOVER,
    TXT_ICON_MOVER_CIMA,
    TXT_ICON_MOVER_BAIXO,
    TXT_ICON_EXPANDIR_OPERACAO,
    TXT_ICON_RECOLHER_OPERACAO,
    TXT_MODO_COMPACTAR,
    TXT_MODO_EXTRAIR,
    TXT_PLACEHOLDER_SENHA_ZIP,
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
    TXT_TOOLTIP_REMOVER_PASTA_RAIZ,
    TXT_TOOLTIP_SENHA_ZIP,
    TXT_TOOLTIP_MOVER_CIMA,
    TXT_TOOLTIP_MOVER_BAIXO,
    TXT_TOOLTIP_EXPANDIR_OPERACAO,
    TXT_TOOLTIP_RECOLHER_OPERACAO,
    TXT_OPERACAO_SEM_NOME,
)

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QAction
from PySide6.QtWidgets import (
    QCheckBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMenu,
    QPushButton,
    QToolButton,
    QWidget,
    QVBoxLayout,
)

from _APP_.Painel_operacoes.movimento_operacoes import PuxadorReordenacao
from _ULTILIDADES_.explorer import Explorer

import os


class LinhaOperacao(QWidget):
    solicitar_operacao = Signal(str, str, str, bool, bool, bool, str)
    solicitar_remocao = Signal(object)
    solicitar_mover = Signal(object, int)
    operacao_alterada = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("operationRow")
        self._expandida = False
        self._montar_ui()
        self._conectar_sinais()
        self._definir_modo("extrair")

    def _montar_ui(self):
        self.setMinimumHeight(ALTURA_LINHA_OPERACAO)
        layout_principal = QVBoxLayout(self)
        layout_principal.setContentsMargins(
            MARGEM_CARD, ESPACO_INTERNO, MARGEM_CARD, ESPACO_INTERNO
        )
        layout_principal.setSpacing(6)

        linha = QHBoxLayout()
        linha.setSpacing(4)

        self._modo_atual = "extrair"
        self._ocupado = False
        self._pode_mover_cima = False
        self._pode_mover_baixo = False

        self._botao_mover_cima = QToolButton()
        self._botao_mover_cima.setObjectName("orderButton")
        self._botao_mover_cima.setText(TXT_ICON_MOVER_CIMA)
        self._botao_mover_cima.setToolTip(TXT_TOOLTIP_MOVER_CIMA)
        self._botao_mover_cima.setFixedSize(24, 18)

        self._botao_mover_baixo = QToolButton()
        self._botao_mover_baixo.setObjectName("orderButton")
        self._botao_mover_baixo.setText(TXT_ICON_MOVER_BAIXO)
        self._botao_mover_baixo.setToolTip(TXT_TOOLTIP_MOVER_BAIXO)
        self._botao_mover_baixo.setFixedSize(24, 18)

        self._botao_expandir = QToolButton()
        self._botao_expandir.setObjectName("orderButton")
        self._botao_expandir.setFixedSize(24, 18)
        self._botao_expandir.setToolTip(TXT_TOOLTIP_EXPANDIR_OPERACAO)

        self._puxador_reordenar = PuxadorReordenacao(self, self)

        controles_ordem = QHBoxLayout()
        controles_ordem.setContentsMargins(0, 0, 0, 0)
        controles_ordem.setSpacing(2)
        controles_ordem.addWidget(self._puxador_reordenar)
        controles_ordem.addWidget(self._botao_mover_cima)
        controles_ordem.addWidget(self._botao_mover_baixo)
        controles_ordem.addWidget(self._botao_expandir)

        self._resumo = QLabel(TXT_OPERACAO_SEM_NOME)
        self._resumo.setObjectName("operationSummary")
        self._resumo.setMinimumWidth(0)

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
        self._checkbox_apagar_zip.setObjectName("operationOptionCheck")
        self._checkbox_apagar_zip.setToolTip(TXT_TOOLTIP_APAGAR_ZIP)

        self._checkbox_extrair_junto_zip = QCheckBox(
            TXT_CHECKBOX_EXTRAIR_JUNTO_ZIP
        )
        self._checkbox_extrair_junto_zip.setObjectName("operationOptionCheck")
        self._checkbox_extrair_junto_zip.setToolTip(
            TXT_TOOLTIP_EXTRAIR_JUNTO_ZIP
        )

        self._checkbox_remover_pasta_raiz = QCheckBox(
            TXT_CHECKBOX_REMOVER_PASTA_RAIZ
        )
        self._checkbox_remover_pasta_raiz.setObjectName("operationOptionCheck")
        self._checkbox_remover_pasta_raiz.setToolTip(
            TXT_TOOLTIP_REMOVER_PASTA_RAIZ
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

        self._senha = QLineEdit()
        self._senha.setObjectName("operationPassword")
        self._senha.setPlaceholderText(TXT_PLACEHOLDER_SENHA_ZIP)
        self._senha.setToolTip(TXT_TOOLTIP_SENHA_ZIP)
        self._senha.setEchoMode(QLineEdit.EchoMode.Password)
        self._senha.setClearButtonEnabled(True)
        self._senha.setFixedHeight(34)
        self._senha.setFixedWidth(LARGURA_CAMPO_SENHA)

        linha.addLayout(controles_ordem)
        linha.addWidget(self._resumo, 1)
        linha.addWidget(self._origem, 3)
        linha.addWidget(self._botao_origem)
        linha.addWidget(self._destino, 3)
        linha.addWidget(self._botao_destino)
        linha.addWidget(self._senha)
        linha.addWidget(self._checkbox_apagar_zip)
        linha.addWidget(self._checkbox_extrair_junto_zip)
        linha.addWidget(self._checkbox_remover_pasta_raiz)
        linha.addWidget(self._botao_executar)
        linha.addWidget(self._botao_remover)
        layout_principal.addLayout(linha)
        self._definir_expansao(False)

    def _conectar_sinais(self):
        self._origem.textChanged.connect(self._ao_editar_caminho)
        self._destino.textChanged.connect(self._ao_editar_caminho)
        self._botao_origem.clicked.connect(self._procurar_origem)
        self._botao_destino.clicked.connect(self._procurar_destino)
        self._botao_executar.clicked.connect(self._emitir_operacao)
        self._botao_expandir.clicked.connect(self._alternar_expansao)
        self._botao_remover.clicked.connect(self._emitir_remocao)
        self._checkbox_apagar_zip.toggled.connect(self._ao_editar_apagar_zip)
        self._checkbox_extrair_junto_zip.toggled.connect(
            self._ao_editar_extrair_junto_zip
        )
        self._checkbox_remover_pasta_raiz.toggled.connect(
            self._ao_editar_remover_pasta_raiz
        )
        self._acao_modo_extrair.triggered.connect(self._selecionar_extracao)
        self._acao_modo_compactar.triggered.connect(self._selecionar_compactacao)
        self._botao_mover_cima.clicked.connect(
            lambda: self.solicitar_mover.emit(self, -1)
        )
        self._botao_mover_baixo.clicked.connect(
            lambda: self.solicitar_mover.emit(self, 1)
        )

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
        self._checkbox_remover_pasta_raiz.setVisible(not compactar)
        self._atualizar_resumo()
        self.operacao_alterada.emit()

    def _alternar_expansao(self):
        self._definir_expansao(not self._expandida)

    def _definir_expansao(self, expandida: bool):
        self._expandida = bool(expandida)
        self._resumo.setVisible(not self._expandida)
        for controle in (
            self._origem,
            self._botao_origem,
            self._destino,
            self._botao_destino,
            self._senha,
        ):
            controle.setVisible(self._expandida)
        self._botao_expandir.setText(
            TXT_ICON_RECOLHER_OPERACAO
            if self._expandida
            else TXT_ICON_EXPANDIR_OPERACAO
        )
        self._botao_expandir.setToolTip(
            TXT_TOOLTIP_RECOLHER_OPERACAO
            if self._expandida
            else TXT_TOOLTIP_EXPANDIR_OPERACAO
        )
        self.updateGeometry()

    def _atualizar_resumo(self):
        caminho = self._origem.text().strip()
        if self._modo_atual == "compactar" and self._destino.text().strip():
            caminho = self._destino.text().strip()
        nome = caminho.replace("\\", "/").rstrip("/").rsplit("/", 1)[-1]
        nome_sem_extensao, extensao = os.path.splitext(nome)
        if extensao.casefold() in {".zip", ".rar"}:
            nome = nome_sem_extensao
        self._resumo.setText(nome or TXT_OPERACAO_SEM_NOME)
        self._resumo.setToolTip(nome)

    def _selecionar_extracao(self, marcado: bool = False):
        self._definir_modo("extrair")

    def _selecionar_compactacao(self, marcado: bool = False):
        self._definir_modo("compactar")

    def _ao_editar_caminho(self, texto: str):
        self._atualizar_resumo()
        self.operacao_alterada.emit()

    def _ao_editar_apagar_zip(self, marcado: bool):
        self.operacao_alterada.emit()

    def _ao_editar_extrair_junto_zip(self, marcado: bool):
        self.operacao_alterada.emit()

    def _ao_editar_remover_pasta_raiz(self, marcado: bool):
        self.operacao_alterada.emit()

    def _procurar_origem(self):
        if self._modo_atual == "compactar":
            selecionado = Explorer.get_existing_directory(
                self,
                TXT_SELECIONAR_PASTA_ORIGEM,
                self._diretorio_inicial(self._origem.text()),
            )
        else:
            filtros = FILTROS_ARQUIVO_COMPACTADO
            if os.path.splitext(self._origem.text().strip())[1].casefold() == ".rar":
                filtros = (
                    TXT_FILTRO_ARQUIVO_RAR,
                    TXT_FILTRO_ARQUIVO_ZIP,
                    TXT_FILTRO_TODOS_COMPACTADOS,
                )
            selecionado = Explorer.get_open_file_name(
                self,
                TXT_SELECIONAR_ZIP_ORIGEM,
                self._diretorio_inicial(self._origem.text()),
                filtros,
            )
        if selecionado:
            self._origem.setText(selecionado)

    def _procurar_destino(self):
        if self._modo_atual == "compactar":
            selecionado = Explorer.get_save_file_name(
                self,
                TXT_SELECIONAR_DESTINO_ZIP,
                self._diretorio_inicial(self._destino.text()),
                TXT_FILTRO_ARQUIVO_ZIP,
            )
        else:
            selecionado = Explorer.get_existing_directory(
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
            self._checkbox_remover_pasta_raiz.isChecked(),
            self._senha.text(),
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
        remover_pasta_raiz = dados.get(CHAVE_OPERACAO_REMOVER_PASTA_RAIZ, False)
        self._origem.setText(origem if isinstance(origem, str) else "")
        self._destino.setText(destino if isinstance(destino, str) else "")
        self._checkbox_apagar_zip.setChecked(apagar_zip is True)
        self._checkbox_extrair_junto_zip.setChecked(extrair_junto_zip is True)
        self._checkbox_remover_pasta_raiz.setChecked(remover_pasta_raiz is True)

    def exportar_dados(self) -> dict[str, str | bool]:
        return {
            CHAVE_OPERACAO_MODO: self._modo_atual,
            CHAVE_OPERACAO_ORIGEM: self._origem.text(),
            CHAVE_OPERACAO_DESTINO: self._destino.text(),
            CHAVE_OPERACAO_APAGAR_ZIP: self._checkbox_apagar_zip.isChecked(),
            CHAVE_OPERACAO_EXTRAIR_JUNTO_ZIP: (
                self._checkbox_extrair_junto_zip.isChecked()
            ),
            CHAVE_OPERACAO_REMOVER_PASTA_RAIZ: (
                self._checkbox_remover_pasta_raiz.isChecked()
            ),
        }

    def definir_ocupado(self, ocupado: bool):
        self._ocupado = ocupado
        self._origem.setEnabled(not ocupado)
        self._destino.setEnabled(not ocupado)
        self._botao_origem.setEnabled(not ocupado)
        self._botao_destino.setEnabled(not ocupado)
        self._checkbox_apagar_zip.setEnabled(not ocupado)
        self._checkbox_extrair_junto_zip.setEnabled(not ocupado)
        self._checkbox_remover_pasta_raiz.setEnabled(not ocupado)
        self._senha.setEnabled(not ocupado)
        self._botao_expandir.setEnabled(not ocupado)
        self._botao_executar.setEnabled(not ocupado)
        self._botao_remover.setEnabled(not ocupado)
        self._atualizar_botoes_movimento()

    def definir_movimentos(self, pode_mover_cima: bool, pode_mover_baixo: bool):
        self._pode_mover_cima = pode_mover_cima
        self._pode_mover_baixo = pode_mover_baixo
        self._atualizar_botoes_movimento()

    def _atualizar_botoes_movimento(self):
        self._botao_mover_cima.setEnabled(
            not self._ocupado and self._pode_mover_cima
        )
        self._botao_mover_baixo.setEnabled(
            not self._ocupado and self._pode_mover_baixo
        )

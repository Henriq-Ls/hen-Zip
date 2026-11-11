"""Divisória horizontal que pode ser reposicionada entre operações."""

from _CONFIGURA_ import (
    ALTURA_DIVISORIA_OPERACAO,
    CHAVE_ITEM_TIPO,
    MARGEM_CARD,
    TXT_ICON_MOVER_BAIXO,
    TXT_ICON_MOVER_CIMA,
    TXT_ICON_REMOVER,
    TXT_TOOLTIP_MOVER_BAIXO,
    TXT_TOOLTIP_MOVER_CIMA,
    TXT_TOOLTIP_REMOVER_DIVISORIA,
    VALOR_ITEM_DIVISORIA,
)

from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QPushButton,
    QToolButton,
    QVBoxLayout,
    QWidget,
)

from _APP_.Painel_operacoes.movimento_operacoes import PuxadorReordenacao


class DivisoriaOperacao(QWidget):
    solicitar_mover = Signal(object, int)
    solicitar_remocao = Signal(object)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("operationDivider")
        self.setMinimumHeight(ALTURA_DIVISORIA_OPERACAO)
        self._ocupado = False
        self._pode_mover_cima = False
        self._pode_mover_baixo = False

        layout = QHBoxLayout(self)
        layout.setContentsMargins(MARGEM_CARD, 0, MARGEM_CARD, 0)
        layout.setSpacing(10)

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

        self._puxador_reordenar = PuxadorReordenacao(self, self)

        controles_ordem = QVBoxLayout()
        controles_ordem.setContentsMargins(0, 0, 0, 0)
        controles_ordem.setSpacing(0)
        controles_ordem.addWidget(self._puxador_reordenar)
        controles_ordem.addWidget(self._botao_mover_cima)
        controles_ordem.addWidget(self._botao_mover_baixo)
        layout.addLayout(controles_ordem)

        self._linha = QFrame()
        self._linha.setObjectName("operationDividerLine")
        self._linha.setFixedHeight(2)
        layout.addWidget(self._linha, 1)

        self._botao_remover = QPushButton(TXT_ICON_REMOVER)
        self._botao_remover.setObjectName("dividerRemoveButton")
        self._botao_remover.setToolTip(TXT_TOOLTIP_REMOVER_DIVISORIA)
        self._botao_remover.setFixedSize(28, 26)
        layout.addWidget(self._botao_remover)

        self._botao_mover_cima.clicked.connect(
            lambda: self.solicitar_mover.emit(self, -1)
        )
        self._botao_mover_baixo.clicked.connect(
            lambda: self.solicitar_mover.emit(self, 1)
        )
        self._botao_remover.clicked.connect(
            lambda: self.solicitar_remocao.emit(self)
        )
        self.definir_movimentos(False, False)

    def exportar_dados(self) -> dict[str, str]:
        return {CHAVE_ITEM_TIPO: VALOR_ITEM_DIVISORIA}

    def definir_ocupado(self, ocupado: bool):
        self._ocupado = ocupado
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

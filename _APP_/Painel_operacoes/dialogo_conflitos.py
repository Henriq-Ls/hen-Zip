"""Diálogo para escolher individualmente quais arquivos existentes substituir."""

from _CONFIGURA_ import (
    ALTURA_DIALOGO_CONFLITOS,
    ESPACO_INTERNO,
    LIMITE_DIALOGO_CONFLITOS,
    MARGEM_CARD,
    TXT_BOTAO_APLICAR_SELECAO,
    TXT_BOTAO_CANCELAR,
    TXT_BOTAO_DESMARCAR_TODOS,
    TXT_BOTAO_MARCAR_TODOS,
    TXT_MENSAGEM_CONFLITOS,
    TXT_TITULO_CONFLITOS,
)

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QVBoxLayout,
)


class DialogoConflitos(QDialog):
    def __init__(
        self,
        conflitos: list[str],
        parent=None,
        destino: str | None = None,
    ):
        super().__init__(parent)
        self.setWindowTitle(TXT_TITULO_CONFLITOS)
        self.resize(LIMITE_DIALOGO_CONFLITOS, ALTURA_DIALOGO_CONFLITOS)
        self._montar_ui(conflitos, destino)
        self._conectar_sinais()

    def _montar_ui(self, conflitos: list[str], destino: str | None = None):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(MARGEM_CARD, MARGEM_CARD, MARGEM_CARD, MARGEM_CARD)
        layout.setSpacing(ESPACO_INTERNO)

        texto_explicacao = TXT_MENSAGEM_CONFLITOS
        if destino:
            texto_explicacao += f"\n\nPasta: {destino}"
        explicacao = QLabel(texto_explicacao)
        explicacao.setWordWrap(True)
        explicacao.setObjectName("mutedLabel")
        layout.addWidget(explicacao)

        controles = QHBoxLayout()
        self._marcar_todos = QPushButton(TXT_BOTAO_MARCAR_TODOS)
        self._desmarcar_todos = QPushButton(TXT_BOTAO_DESMARCAR_TODOS)
        controles.addWidget(self._marcar_todos)
        controles.addWidget(self._desmarcar_todos)
        controles.addStretch(1)
        layout.addLayout(controles)

        self._lista = QListWidget()
        self._lista.setObjectName("conflictList")
        for caminho in conflitos:
            item = QListWidgetItem(caminho)
            item.setFlags(
                item.flags()
                | Qt.ItemFlag.ItemIsUserCheckable
                | Qt.ItemFlag.ItemIsEnabled
                | Qt.ItemFlag.ItemIsSelectable
            )
            item.setCheckState(Qt.CheckState.Checked)
            item.setData(Qt.ItemDataRole.UserRole, caminho)
            self._lista.addItem(item)
        layout.addWidget(self._lista, 1)

        self._botoes = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok
            | QDialogButtonBox.StandardButton.Cancel
        )
        self._botoes.button(QDialogButtonBox.StandardButton.Ok).setText(
            TXT_BOTAO_APLICAR_SELECAO
        )
        self._botoes.button(QDialogButtonBox.StandardButton.Cancel).setText(
            TXT_BOTAO_CANCELAR
        )
        layout.addWidget(self._botoes)

    def _conectar_sinais(self):
        self._marcar_todos.clicked.connect(self._selecionar_todos)
        self._desmarcar_todos.clicked.connect(self._limpar_selecao)
        self._botoes.accepted.connect(self.accept)
        self._botoes.rejected.connect(self.reject)

    def _selecionar_todos(self):
        for indice in range(self._lista.count()):
            self._lista.item(indice).setCheckState(Qt.CheckState.Checked)

    def _limpar_selecao(self):
        for indice in range(self._lista.count()):
            self._lista.item(indice).setCheckState(Qt.CheckState.Unchecked)

    def arquivos_selecionados(self) -> set[str]:
        return {
            self._lista.item(indice).data(Qt.ItemDataRole.UserRole)
            for indice in range(self._lista.count())
            if self._lista.item(indice).checkState() == Qt.CheckState.Checked
        }

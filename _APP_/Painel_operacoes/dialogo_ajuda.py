"""Guia de uso do hen-Zip."""

from _CONFIGURA_ import (
    ALTURA_DIALOGO_AJUDA,
    ALTURA_MIN_DIALOGO_AJUDA,
    ESPACO_INTERNO,
    LARGURA_DIALOGO_AJUDA,
    LARGURA_MIN_DIALOGO_AJUDA,
    MARGEM_CARD,
    TXT_AJUDA_CONTEUDO,
    TXT_BOTAO_FECHAR_AJUDA,
    TXT_TITULO_DIALOGO_AJUDA,
)

from PySide6.QtGui import QGuiApplication
from PySide6.QtWidgets import (
    QDialog,
    QHBoxLayout,
    QPushButton,
    QTextBrowser,
    QVBoxLayout,
)


class DialogoAjuda(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(TXT_TITULO_DIALOGO_AJUDA)
        largura = LARGURA_DIALOGO_AJUDA
        altura = ALTURA_DIALOGO_AJUDA
        tela = QGuiApplication.primaryScreen()
        if tela is not None:
            area = tela.availableGeometry()
            largura = min(largura, area.width())
            altura = min(altura, area.height())
        self.setMinimumSize(
            min(LARGURA_MIN_DIALOGO_AJUDA, largura),
            min(ALTURA_MIN_DIALOGO_AJUDA, altura),
        )
        self.resize(largura, altura)
        self.setAccessibleName(TXT_TITULO_DIALOGO_AJUDA)
        self._montar_ui()

    def _montar_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(
            MARGEM_CARD, MARGEM_CARD, MARGEM_CARD, MARGEM_CARD
        )
        layout.setSpacing(ESPACO_INTERNO)

        self._conteudo = QTextBrowser()
        self._conteudo.setObjectName("helpContent")
        self._conteudo.setAccessibleName(TXT_TITULO_DIALOGO_AJUDA)
        self._conteudo.setOpenExternalLinks(False)
        self._conteudo.setHtml(TXT_AJUDA_CONTEUDO)
        layout.addWidget(self._conteudo, 1)

        botoes = QHBoxLayout()
        botoes.addStretch(1)
        self._botao_fechar = QPushButton(TXT_BOTAO_FECHAR_AJUDA)
        self._botao_fechar.setObjectName("secondaryButton")
        self._botao_fechar.clicked.connect(self.accept)
        botoes.addWidget(self._botao_fechar)
        layout.addLayout(botoes)

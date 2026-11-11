"""Controles de arraste para reorganizar operações e divisórias."""

from _CONFIGURA_ import (
    MIME_REORDENAR_OPERACAO,
    TXT_ICON_PUXADOR_REORDENAR,
    TXT_TOOLTIP_PUXADOR_REORDENAR,
)

from PySide6.QtCore import Qt, QMimeData, Signal
from PySide6.QtGui import QDrag
from PySide6.QtWidgets import QApplication, QFrame, QToolButton, QWidget


class PuxadorReordenacao(QToolButton):
    def __init__(self, item, parent=None):
        super().__init__(parent)
        self._item = item
        self._posicao_inicio = None
        self.setObjectName("reorderHandle")
        self.setText(TXT_ICON_PUXADOR_REORDENAR)
        self.setToolTip(TXT_TOOLTIP_PUXADOR_REORDENAR)
        self.setFixedSize(24, 18)
        self.setCursor(Qt.CursorShape.OpenHandCursor)

    def mousePressEvent(self, evento):
        if evento.button() == Qt.MouseButton.LeftButton:
            self._posicao_inicio = evento.position().toPoint()
        super().mousePressEvent(evento)

    def mouseMoveEvent(self, evento):
        if (
            self._posicao_inicio is not None
            and evento.buttons() & Qt.MouseButton.LeftButton
            and (evento.position().toPoint() - self._posicao_inicio).manhattanLength()
            >= QApplication.startDragDistance()
        ):
            self._iniciar_arraste()
            return
        super().mouseMoveEvent(evento)

    def mouseReleaseEvent(self, evento):
        self._posicao_inicio = None
        self.setCursor(Qt.CursorShape.OpenHandCursor)
        super().mouseReleaseEvent(evento)

    def _iniciar_arraste(self):
        self._posicao_inicio = None
        self.setDown(False)
        self.setCursor(Qt.CursorShape.ClosedHandCursor)

        dados = QMimeData()
        dados.setData(MIME_REORDENAR_OPERACAO, str(id(self._item)).encode("ascii"))
        arraste = QDrag(self)
        arraste.setMimeData(dados)
        arraste.setPixmap(self.grab())
        arraste.setHotSpot(self.rect().center())

        self._item.setVisible(False)
        arraste.exec(Qt.DropAction.MoveAction)
        self._item.setVisible(True)
        self.setCursor(Qt.CursorShape.OpenHandCursor)


class AreaOperacoes(QWidget):
    item_solto = Signal(str, int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._itens = []
        self.setAcceptDrops(True)
        self._indicador_soltar = QFrame(self)
        self._indicador_soltar.setObjectName("operationDropIndicator")
        self._indicador_soltar.setFixedHeight(3)
        self._indicador_soltar.setAttribute(
            Qt.WidgetAttribute.WA_TransparentForMouseEvents
        )
        self._indicador_soltar.hide()

    def definir_itens(self, itens):
        self._itens = list(itens)

    def dragEnterEvent(self, evento):
        if evento.mimeData().hasFormat(MIME_REORDENAR_OPERACAO):
            evento.acceptProposedAction()
            return
        evento.ignore()

    def dragMoveEvent(self, evento):
        if not evento.mimeData().hasFormat(MIME_REORDENAR_OPERACAO):
            evento.ignore()
            return
        identificador = bytes(
            evento.mimeData().data(MIME_REORDENAR_OPERACAO)
        ).decode("ascii")
        _, y = self._calcular_insercao(
            identificador,
            evento.position().toPoint().y(),
        )
        self._indicador_soltar.setGeometry(
            12,
            y - 1,
            max(self.width() - 24, 1),
            3,
        )
        self._indicador_soltar.show()
        self._indicador_soltar.raise_()
        evento.acceptProposedAction()

    def dragLeaveEvent(self, evento):
        self._indicador_soltar.hide()
        evento.accept()

    def dropEvent(self, evento):
        self._indicador_soltar.hide()
        if not evento.mimeData().hasFormat(MIME_REORDENAR_OPERACAO):
            evento.ignore()
            return
        identificador = bytes(
            evento.mimeData().data(MIME_REORDENAR_OPERACAO)
        ).decode("ascii")
        indice, _ = self._calcular_insercao(
            identificador,
            evento.position().toPoint().y(),
        )
        self.item_solto.emit(identificador, indice)
        evento.acceptProposedAction()

    def _calcular_insercao(self, identificador: str, y: int) -> tuple[int, int]:
        restantes = [
            item for item in self._itens if str(id(item)) != identificador
        ]
        for indice, item in enumerate(restantes):
            geometria = item.geometry()
            if y < geometria.center().y():
                return indice, geometria.top()
        if restantes:
            return len(restantes), restantes[-1].geometry().bottom()
        return 0, 0

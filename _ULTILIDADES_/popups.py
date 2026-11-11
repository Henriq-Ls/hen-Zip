# _ULTILIDADES_/popups.py
"""
Diálogos padronizados do projeto.

Todos usam o estilo escuro definido em _CONFIGURA_.

Uso:
    from _ULTILIDADES_.popups import popup_erro, popup_aviso, popup_confirmar, popup_info

    popup_erro("Título", "Mensagem de erro detalhada.")
    popup_aviso("Atenção", "Algo suspeito aconteceu.")
    popup_info("Info", "Operação concluída.")

    if popup_confirmar("Confirmar", "Deseja realmente excluir?"):
        fazer_exclusao()
"""

from PySide6.QtCore import QEvent, QObject, Qt
from PySide6.QtWidgets import QApplication, QMessageBox, QWidget
from _CONFIGURA_ import ESTILO_DIALOGO_ESCURO, TITULO_APP

_DIALOGOS_INFO_ATIVOS = set()


def _aplicar_estilo(dialogo: QMessageBox):
    dialogo.setStyleSheet(ESTILO_DIALOGO_ESCURO)


class _FecharAoClicarFora(QObject):
    def __init__(self, dialogo: QMessageBox):
        super().__init__(dialogo)
        self._dialogo = dialogo

    def eventFilter(self, objeto, evento):
        if evento.type() == QEvent.Type.MouseButtonPress:
            posicao = evento.globalPosition().toPoint()
            if not self._dialogo.geometry().contains(posicao):
                self._dialogo.close()
        elif evento.type() == QEvent.Type.ApplicationDeactivate:
            self._dialogo.close()
        return False


def popup_erro(titulo: str, mensagem: str, parent: QWidget = None):
    """Exibe diálogo de erro modal."""
    dlg = QMessageBox(parent)
    dlg.setWindowTitle(titulo)
    dlg.setText(mensagem)
    dlg.setIcon(QMessageBox.Icon.Critical)
    dlg.setStandardButtons(QMessageBox.StandardButton.Ok)
    _aplicar_estilo(dlg)
    dlg.exec()


def popup_aviso(titulo: str, mensagem: str, parent: QWidget = None):
    """Exibe diálogo de aviso modal."""
    dlg = QMessageBox(parent)
    dlg.setWindowTitle(titulo)
    dlg.setText(mensagem)
    dlg.setIcon(QMessageBox.Icon.Warning)
    dlg.setStandardButtons(QMessageBox.StandardButton.Ok)
    _aplicar_estilo(dlg)
    dlg.exec()


def popup_info(
    titulo: str,
    mensagem: str,
    parent: QWidget = None,
    fechar_ao_clicar_fora: bool = False,
):
    """Exibe informação; opcionalmente fecha ao clicar fora sem bloquear a janela."""
    dlg = QMessageBox(parent)
    dlg.setWindowTitle(titulo)
    dlg.setText(mensagem)
    dlg.setIcon(QMessageBox.Icon.Information)
    dlg.setStandardButtons(QMessageBox.StandardButton.Ok)
    _aplicar_estilo(dlg)
    if fechar_ao_clicar_fora:
        aplicativo = QApplication.instance()
        if aplicativo is None:
            dlg.exec()
            return

        dlg.setModal(False)
        dlg.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
        filtro = _FecharAoClicarFora(dlg)
        aplicativo.installEventFilter(filtro)
        _DIALOGOS_INFO_ATIVOS.add(dlg)

        def ao_finalizar(_resultado):
            aplicativo.removeEventFilter(filtro)
            _DIALOGOS_INFO_ATIVOS.discard(dlg)

        dlg.finished.connect(ao_finalizar)
        dlg.show()
        return dlg

    dlg.exec()


def popup_confirmar(
    titulo: str,
    mensagem: str,
    parent: QWidget = None,
    btn_ok: str = "Confirmar",
    btn_cancelar: str = "Cancelar"
) -> bool:
    """
    Exibe diálogo de confirmação.
    Retorna True se o usuário confirmou, False se cancelou.
    """
    dlg = QMessageBox(parent)
    dlg.setWindowTitle(titulo)
    dlg.setText(mensagem)
    dlg.setIcon(QMessageBox.Icon.Question)

    btn_sim = dlg.addButton(btn_ok,      QMessageBox.ButtonRole.AcceptRole)
    dlg.addButton(btn_cancelar, QMessageBox.ButtonRole.RejectRole)
    dlg.setDefaultButton(btn_sim)

    _aplicar_estilo(dlg)
    dlg.exec()

    return dlg.clickedButton() == btn_sim


def popup_confirmar_perigo(
    titulo: str,
    mensagem: str,
    parent: QWidget = None
) -> bool:
    """
    Diálogo de confirmação para ações destrutivas (excluir, apagar, resetar).
    Botão de confirmação em vermelho.
    """
    from _CONFIGURA_ import COR_PERIGO
    dlg = QMessageBox(parent)
    dlg.setWindowTitle(titulo)
    dlg.setText(mensagem)
    dlg.setIcon(QMessageBox.Icon.Warning)

    btn_sim = dlg.addButton("Confirmar", QMessageBox.ButtonRole.AcceptRole)
    btn_sim.setStyleSheet(
        f"QPushButton {{ background: {COR_PERIGO}; color: white; "
        f"border: none; padding: 6px 16px; border-radius: 4px; font-weight: bold; }}"
    )
    dlg.addButton("Cancelar", QMessageBox.ButtonRole.RejectRole)

    _aplicar_estilo(dlg)
    dlg.exec()

    return dlg.clickedButton() == btn_sim

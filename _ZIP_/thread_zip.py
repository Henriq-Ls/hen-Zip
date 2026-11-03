"""Worker de compactação e extração para manter a interface responsiva."""

from _CONFIGURA_ import (
    TXT_ERRO_ACAO_ZIP_INVALIDA,
    TXT_SUCESSO_COMPACTAR,
    TXT_SUCESSO_EXTRAIR,
)
from _LOGS_ import log
from _THREADS_.thread_segura import ThreadSegura

from PySide6.QtCore import Signal

from _ZIP_.operacoes import compactar_pasta, extrair_zip


class ThreadOperacaoZip(ThreadSegura):
    progresso = Signal(str, int, str)
    concluido = Signal(str, str)
    falhou = Signal(str, str)

    def __init__(
        self,
        nome: str,
        acao: str,
        origem: str,
        destino: str,
        substituir: set[str] | None = None,
        parent=None,
    ):
        super().__init__(nome=nome, parent=parent)
        self._acao = acao
        self._origem = origem
        self._destino = destino
        self._substituir = substituir or set()

    def run(self):
        try:
            if self._acao == "compactar":
                destino = compactar_pasta(
                    self._origem,
                    self._destino,
                    self._reportar_progresso,
                )
                mensagem = TXT_SUCESSO_COMPACTAR.format(destino=destino)
            elif self._acao == "extrair":
                destino = extrair_zip(
                    self._origem,
                    self._destino,
                    self._substituir,
                    self._reportar_progresso,
                )
                mensagem = TXT_SUCESSO_EXTRAIR.format(destino=destino)
            else:
                raise ValueError(TXT_ERRO_ACAO_ZIP_INVALIDA)

            self.concluido.emit(self.nome, mensagem)
        except Exception as erro:
            log.erro("ThreadOperacaoZip", "run", f"{self.nome}: {erro}")
            self.falhou.emit(self.nome, str(erro))

    def _reportar_progresso(self, percentual: int, mensagem: str):
        self.progresso.emit(self.nome, percentual, mensagem)

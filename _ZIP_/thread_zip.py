"""Worker de compactação e extração para manter a interface responsiva."""

import os

from _CONFIGURA_ import (
    TXT_ERRO_ACAO_ZIP_INVALIDA,
    TXT_SUCESSO_COMPACTAR,
    TXT_SUCESSO_EXTRAIR,
    TXT_SUCESSO_EXTRAIR_JUNTO_ZIP,
)
from _LOGS_ import log
from _THREADS_.thread_segura import ThreadSegura

from PySide6.QtCore import Signal

from _ZIP_.operacoes import compactar_pasta, extrair_zip


class ThreadOperacaoZip(ThreadSegura):
    progresso = Signal(str, int, str)
    concluido = Signal(str, str, str, bool)
    falhou = Signal(str, str)

    def __init__(
        self,
        nome: str,
        acao: str,
        origem: str,
        destino: str,
        substituir: set[str] | None = None,
        apagar_zip_apos_extrair: bool = False,
        extrair_junto_zip: bool = False,
        substituir_junto_zip: set[str] | None = None,
        remover_pasta_raiz_diferente: bool = False,
        senha: str = "",
        parent=None,
        preservar_pasta_raiz_destino: bool = False,
    ):
        super().__init__(nome=nome, parent=parent)
        self._acao = acao
        self._origem = origem
        self._destino = destino
        self._substituir = substituir or set()
        self._apagar_zip_apos_extrair = apagar_zip_apos_extrair
        self._extrair_junto_zip = extrair_junto_zip
        self._substituir_junto_zip = substituir_junto_zip or set()
        self._remover_pasta_raiz_diferente = remover_pasta_raiz_diferente
        self._senha = senha
        self._preservar_pasta_raiz_destino = preservar_pasta_raiz_destino

    def run(self):
        try:
            if self._acao == "compactar":
                destino = compactar_pasta(
                    self._origem,
                    self._destino,
                    self._reportar_progresso,
                    senha=self._senha,
                )
                mensagem = TXT_SUCESSO_COMPACTAR.format(destino=destino)
            elif self._acao == "extrair":
                destino = extrair_zip(
                    self._origem,
                    self._destino,
                    self._substituir,
                    self._reportar_progresso,
                    remover_pasta_raiz_diferente=(
                        self._remover_pasta_raiz_diferente
                    ),
                    senha=self._senha,
                    preservar_pasta_raiz=self._preservar_pasta_raiz_destino,
                )
                mensagem = TXT_SUCESSO_EXTRAIR.format(destino=destino)
                if self._extrair_junto_zip:
                    pasta_zip = os.path.dirname(
                        os.path.abspath(os.path.expanduser(self._origem))
                    )
                    identidade_destino = os.path.normcase(
                        os.path.realpath(os.path.abspath(destino))
                    )
                    identidade_pasta_zip = os.path.normcase(
                        os.path.realpath(pasta_zip)
                    )
                    if identidade_destino != identidade_pasta_zip:
                        extrair_zip(
                            self._origem,
                            pasta_zip,
                            self._substituir_junto_zip,
                            self._reportar_progresso,
                            remover_pasta_raiz_diferente=(
                                False
                            ),
                            senha=self._senha,
                            preservar_pasta_raiz=True,
                        )
                        mensagem += TXT_SUCESSO_EXTRAIR_JUNTO_ZIP.format(
                            destino=pasta_zip
                        )
            else:
                raise ValueError(TXT_ERRO_ACAO_ZIP_INVALIDA)

            self.concluido.emit(
                self.nome,
                mensagem,
                self._origem,
                self._acao == "extrair" and self._apagar_zip_apos_extrair,
            )
        except Exception as erro:
            log.erro("ThreadOperacaoZip", "run", f"{self.nome}: {erro}")
            self.falhou.emit(self.nome, str(erro))

    def _reportar_progresso(self, percentual: int, mensagem: str):
        self.progresso.emit(self.nome, percentual, mensagem)

"""Operações ZIP sem dependência da interface gráfica."""

from _CONFIGURA_ import (
    NIVEL_COMPRESSAO_ZIP,
    TXT_ERRO_ARQUIVO_ZIP_INVALIDO,
    TXT_ERRO_CAMINHO_ZIP_INSEGURO,
    TXT_ERRO_DESTINO_E_PASTA,
    TXT_ERRO_DESTINO_FORA_DA_PASTA,
    TXT_ERRO_DESTINO_INCOMPATIVEL,
    TXT_ERRO_DESTINO_PASTA_INVALIDO,
    TXT_ERRO_DESTINO_ZIP_INVALIDO,
    TXT_ERRO_ORIGEM_PASTA_INVALIDA,
    TXT_ERRO_ORIGEM_ZIP_INVALIDA,
    TXT_PROGRESS_COMPACTAR,
    TXT_PROGRESS_EXTRAIR,
)
from _LOGS_ import log

import os
import re
import shutil
import tempfile
import zipfile
from pathlib import PurePosixPath
from typing import Callable


CallbackProgresso = Callable[[int, str], None]


def _notificar(callback: CallbackProgresso | None, percentual: int, mensagem: str):
    if callback is not None:
        callback(percentual, mensagem)


def _coletar_arquivos(origem: str, destino_zip: str):
    """Lista arquivos e pastas vazias, sem seguir links simbólicos."""
    itens: list[tuple[str | None, str, bool]] = []
    destino_real = os.path.realpath(destino_zip)

    for pasta_atual, diretorios, arquivos in os.walk(origem, followlinks=False):
        diretorios[:] = sorted(
            nome for nome in diretorios
            if not os.path.islink(os.path.join(pasta_atual, nome))
        )
        arquivos = sorted(arquivos)

        arquivos_validos = []
        for nome in arquivos:
            caminho = os.path.join(pasta_atual, nome)
            if os.path.islink(caminho) or os.path.realpath(caminho) == destino_real:
                continue
            arquivos_validos.append(nome)
            relativo = os.path.relpath(caminho, origem).replace(os.sep, "/")
            itens.append((caminho, relativo, False))

        if not diretorios and not arquivos_validos:
            relativo = os.path.relpath(pasta_atual, origem)
            if relativo != ".":
                itens.append((None, relativo.replace(os.sep, "/") + "/", True))

    return itens


def compactar_pasta(
    origem: str,
    destino_zip: str,
    progresso: CallbackProgresso | None = None,
) -> str:
    """Cria um ZIP com o conteúdo da pasta de origem."""
    origem = os.path.abspath(os.path.expanduser(origem))
    destino_zip = os.path.abspath(os.path.expanduser(destino_zip))

    if not os.path.isdir(origem):
        raise ValueError(TXT_ERRO_ORIGEM_PASTA_INVALIDA)
    if os.path.isdir(destino_zip):
        raise ValueError(TXT_ERRO_DESTINO_ZIP_INVALIDO)

    pasta_destino = os.path.dirname(destino_zip)
    os.makedirs(pasta_destino, exist_ok=True)
    itens = _coletar_arquivos(origem, destino_zip)
    descritor, temporario = tempfile.mkstemp(
        prefix=f".{os.path.basename(destino_zip)}.",
        suffix=".tmp",
        dir=pasta_destino,
    )
    os.close(descritor)

    try:
        total = max(len(itens), 1)
        with zipfile.ZipFile(
            temporario,
            mode="w",
            compression=zipfile.ZIP_DEFLATED,
            compresslevel=NIVEL_COMPRESSAO_ZIP,
        ) as arquivo_zip:
            for indice, (caminho, nome_relativo, eh_pasta) in enumerate(itens, 1):
                if eh_pasta:
                    arquivo_zip.writestr(nome_relativo, "")
                else:
                    arquivo_zip.write(caminho, nome_relativo)
                _notificar(
                    progresso,
                    int(indice * 100 / total),
                    TXT_PROGRESS_COMPACTAR.format(nome=nome_relativo),
                )

        os.replace(temporario, destino_zip)
    except Exception:
        if os.path.exists(temporario):
            os.remove(temporario)
        raise

    if not itens:
        _notificar(progresso, 100, TXT_PROGRESS_COMPACTAR.format(nome=""))
    log.ok("OperacoesZIP", "compactar_pasta", f"ZIP criado: {destino_zip}")
    return destino_zip


def _nome_membro_seguro(nome: str) -> str | None:
    """Normaliza um caminho ZIP e rejeita caminhos absolutos ou ascendentes."""
    normalizado = nome.replace("\\", "/")
    if (
        not normalizado
        or "\x00" in normalizado
        or normalizado.startswith("/")
        or re.match(r"^[A-Za-z]:", normalizado)
    ):
        raise ValueError(TXT_ERRO_CAMINHO_ZIP_INSEGURO.format(nome=nome))

    partes = PurePosixPath(normalizado).parts
    if not partes or any(parte in ("..", "") for parte in partes):
        raise ValueError(TXT_ERRO_CAMINHO_ZIP_INSEGURO.format(nome=nome))
    if partes == (".",):
        return None

    return PurePosixPath(*partes).as_posix()


def _caminho_destino_seguro(raiz_absoluta: str, raiz_real: str, relativo: str) -> str:
    partes = PurePosixPath(relativo).parts
    destino = os.path.abspath(os.path.join(raiz_absoluta, *partes))
    try:
        if os.path.commonpath((raiz_absoluta, destino)) != raiz_absoluta:
            raise ValueError
        pasta_real = os.path.realpath(os.path.dirname(destino))
        if os.path.commonpath((raiz_real, pasta_real)) != raiz_real:
            raise ValueError
    except ValueError as erro:
        raise ValueError(
            TXT_ERRO_DESTINO_FORA_DA_PASTA.format(nome=relativo)
        ) from erro
    return destino


def _ler_membros(arquivo_zip: str, destino: str):
    if not os.path.isfile(arquivo_zip):
        raise ValueError(TXT_ERRO_ORIGEM_ZIP_INVALIDA)
    if os.path.exists(destino) and not os.path.isdir(destino):
        raise ValueError(TXT_ERRO_DESTINO_PASTA_INVALIDO)

    raiz_absoluta = os.path.abspath(destino)
    raiz_real = os.path.realpath(destino)
    try:
        with zipfile.ZipFile(arquivo_zip, "r") as zip_aberto:
            membros = []
            for info in zip_aberto.infolist():
                relativo = _nome_membro_seguro(info.filename)
                if relativo is None:
                    continue
                caminho = _caminho_destino_seguro(
                    raiz_absoluta, raiz_real, relativo
                )

                partes = PurePosixPath(relativo).parts
                for indice in range(1, len(partes)):
                    pasta_pai = os.path.join(raiz_absoluta, *partes[:indice])
                    if os.path.lexists(pasta_pai) and not os.path.isdir(pasta_pai):
                        raise ValueError(
                            TXT_ERRO_DESTINO_INCOMPATIVEL.format(nome=partes[indice - 1])
                        )

                if info.is_dir():
                    if os.path.lexists(caminho) and not os.path.isdir(caminho):
                        raise ValueError(
                            TXT_ERRO_DESTINO_INCOMPATIVEL.format(nome=relativo)
                        )
                    if os.path.lexists(caminho):
                        caminho_real = os.path.realpath(caminho)
                        try:
                            dentro_da_raiz = os.path.commonpath(
                                (raiz_real, caminho_real)
                            ) == raiz_real
                        except ValueError:
                            dentro_da_raiz = False
                        if not dentro_da_raiz:
                            raise ValueError(
                                TXT_ERRO_DESTINO_FORA_DA_PASTA.format(nome=relativo)
                            )
                elif os.path.isdir(caminho) and not os.path.islink(caminho):
                    raise ValueError(TXT_ERRO_DESTINO_E_PASTA.format(nome=relativo))

                membros.append((info, relativo, caminho))
            return membros
    except zipfile.BadZipFile as erro:
        raise ValueError(TXT_ERRO_ARQUIVO_ZIP_INVALIDO) from erro


def listar_conflitos(arquivo_zip: str, destino: str) -> list[str]:
    """Valida o ZIP e retorna os arquivos que já existem no destino."""
    membros = _ler_membros(arquivo_zip, destino)
    conflitos = {
        relativo
        for info, relativo, caminho in membros
        if not info.is_dir() and os.path.lexists(caminho)
    }
    return sorted(conflitos)


def extrair_zip(
    arquivo_zip: str,
    destino: str,
    substituir: set[str] | None = None,
    progresso: CallbackProgresso | None = None,
) -> str:
    """Extrai o ZIP dentro do destino, com substituição controlada por arquivo."""
    arquivo_zip = os.path.abspath(os.path.expanduser(arquivo_zip))
    destino = os.path.abspath(os.path.expanduser(destino))
    substituir = substituir or set()
    os.makedirs(destino, exist_ok=True)

    raiz_absoluta = os.path.abspath(destino)
    raiz_real = os.path.realpath(destino)
    membros = _ler_membros(arquivo_zip, destino)
    total = max(sum(not info.is_dir() for info, _, _ in membros), 1)
    processados = 0

    with zipfile.ZipFile(arquivo_zip, "r") as zip_aberto:
        for info, relativo, caminho in membros:
            if info.is_dir():
                caminho = _caminho_destino_seguro(
                    raiz_absoluta, raiz_real, relativo
                )
                if os.path.lexists(caminho) and not os.path.isdir(caminho):
                    raise ValueError(TXT_ERRO_DESTINO_INCOMPATIVEL.format(nome=relativo))
                if os.path.lexists(caminho):
                    caminho_real = os.path.realpath(caminho)
                    try:
                        dentro_da_raiz = os.path.commonpath(
                            (raiz_real, caminho_real)
                        ) == raiz_real
                    except ValueError:
                        dentro_da_raiz = False
                    if not dentro_da_raiz:
                        raise ValueError(
                            TXT_ERRO_DESTINO_FORA_DA_PASTA.format(nome=relativo)
                        )
                os.makedirs(caminho, exist_ok=True)
                continue

            pasta_pai = os.path.dirname(caminho)
            os.makedirs(pasta_pai, exist_ok=True)
            caminho = _caminho_destino_seguro(
                raiz_absoluta, raiz_real, relativo
            )
            if os.path.isdir(caminho) and not os.path.islink(caminho):
                raise ValueError(TXT_ERRO_DESTINO_E_PASTA.format(nome=relativo))

            if not os.path.lexists(caminho) or relativo in substituir:
                descritor, temporario = tempfile.mkstemp(
                    prefix=f".{os.path.basename(caminho)}.",
                    suffix=".tmp",
                    dir=pasta_pai,
                )
                try:
                    with os.fdopen(descritor, "wb") as arquivo_saida:
                        with zip_aberto.open(info, "r") as arquivo_entrada:
                            shutil.copyfileobj(arquivo_entrada, arquivo_saida)
                    os.replace(temporario, caminho)
                except Exception:
                    try:
                        os.close(descritor)
                    except OSError:
                        pass
                    if os.path.exists(temporario):
                        os.remove(temporario)
                    raise

            processados += 1
            _notificar(
                progresso,
                int(processados * 100 / total),
                TXT_PROGRESS_EXTRAIR.format(nome=relativo),
            )

    if processados == 0:
        _notificar(progresso, 100, TXT_PROGRESS_EXTRAIR.format(nome=""))
    log.ok("OperacoesZIP", "extrair_zip", f"Extração concluída: {destino}")
    return destino

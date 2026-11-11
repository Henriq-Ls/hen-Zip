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
    TXT_ERRO_RAR_FERRAMENTA_AUSENTE,
    TXT_ERRO_RAR_INVALIDO,
    TXT_ERRO_RAR_LINK,
    TXT_ERRO_RAR_CABECALHO_PROTEGIDO,
    TXT_ERRO_RAR_SENHA_INVALIDA,
    TXT_ERRO_RAR_SENHA_NECESSARIA,
    TXT_ERRO_RAR_VOLUME_INICIAL,
    TXT_ERRO_SENHA_ZIP_INVALIDA,
    TXT_ERRO_SENHA_ZIP_NECESSARIA,
    TXT_LOG_PASTA_RAIZ_REMOVIDA,
    TXT_LOG_RESULTADO_EXTRAIR,
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

import pyzipper
import rarfile


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
    senha: str = "",
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
        with pyzipper.AESZipFile(
            temporario,
            mode="w",
            compression=zipfile.ZIP_DEFLATED,
            compresslevel=NIVEL_COMPRESSAO_ZIP,
        ) as arquivo_zip:
            if senha:
                arquivo_zip.setpassword(senha.encode("utf-8"))
                arquivo_zip.setencryption(pyzipper.WZ_AES, nbits=256)
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


def _abrir_zip_leitura(arquivo_zip: str, senha: str = ""):
    zip_aberto = pyzipper.AESZipFile(arquivo_zip, mode="r")
    if senha:
        zip_aberto.setpassword(senha.encode("utf-8"))
    return zip_aberto


def _eh_rar(arquivo_compactado: str) -> bool:
    return os.path.splitext(arquivo_compactado)[1].casefold() == ".rar"


def _configurar_ferramenta_rar() -> None:
    if os.name != "nt":
        return
    for pasta_programas in (
        os.environ.get("ProgramFiles"),
        os.environ.get("ProgramFiles(x86)"),
        os.environ.get("ProgramW6432"),
    ):
        if not pasta_programas:
            continue
        executavel = os.path.join(pasta_programas, "WinRAR", "UnRAR.exe")
        if os.path.isfile(executavel):
            rarfile.UNRAR_TOOL = executavel
            return


_configurar_ferramenta_rar()


def _rar_tem_cabecalho_protegido(arquivo_rar) -> bool:
    """Detecta cabeçalhos criptografados, que podem não listar membros sem senha."""
    parser = getattr(arquivo_rar, "_file_parser", None)
    verificar = getattr(parser, "has_header_encryption", None)
    return bool(verificar()) if callable(verificar) else False


def _abrir_arquivo_compactado(arquivo_compactado: str, senha: str = ""):
    extensao = os.path.splitext(arquivo_compactado)[1].casefold()
    if extensao == ".rar":
        arquivo = rarfile.RarFile(arquivo_compactado, errors="strict")
        cabecalho_protegido = _rar_tem_cabecalho_protegido(arquivo)
        senha_requerida = bool(arquivo.needs_password() or cabecalho_protegido)
        if not senha and cabecalho_protegido:
            arquivo.close()
            raise ValueError(TXT_ERRO_RAR_SENHA_NECESSARIA)
        if senha:
            try:
                arquivo.setpassword(senha)
            except rarfile.NoCrypto as erro:
                raise _traduzir_erro_rar(erro) from erro
            except rarfile.Error as erro:
                if senha_requerida:
                    raise ValueError(
                        TXT_ERRO_RAR_SENHA_INVALIDA
                    ) from erro
                raise _traduzir_erro_rar(erro) from erro
        return arquivo
    if extensao == ".zip":
        return _abrir_zip_leitura(arquivo_compactado, senha)
    raise ValueError(TXT_ERRO_ORIGEM_ZIP_INVALIDA)


def _traduzir_erro_rar(erro: Exception) -> ValueError:
    if isinstance(erro, rarfile.RarCannotExec):
        return ValueError(TXT_ERRO_RAR_FERRAMENTA_AUSENTE)
    if isinstance(erro, rarfile.NeedFirstVolume):
        return ValueError(TXT_ERRO_RAR_VOLUME_INICIAL)
    if isinstance(erro, rarfile.NoCrypto):
        return ValueError(TXT_ERRO_RAR_CABECALHO_PROTEGIDO)
    if isinstance(erro, rarfile.PasswordRequired):
        return ValueError(TXT_ERRO_RAR_SENHA_NECESSARIA)
    if isinstance(erro, (rarfile.RarWrongPassword, rarfile.RarCRCError)):
        return ValueError(TXT_ERRO_RAR_SENHA_INVALIDA)
    if isinstance(erro, (rarfile.NotRarFile, rarfile.BadRarFile)):
        return ValueError(TXT_ERRO_RAR_INVALIDO)
    return ValueError(TXT_ERRO_ARQUIVO_ZIP_INVALIDO)


def _validar_senha_zip(zip_aberto, senha: str):
    arquivos_protegidos = [
        info
        for info in zip_aberto.infolist()
        if not info.is_dir() and info.flag_bits & 0x1
    ]
    if arquivos_protegidos and not senha:
        raise ValueError(TXT_ERRO_SENHA_ZIP_NECESSARIA)
    if not arquivos_protegidos:
        return

    try:
        with zip_aberto.open(arquivos_protegidos[0], "r") as entrada:
            entrada.read(1)
    except (RuntimeError, zipfile.BadZipFile, EOFError) as erro:
        raise ValueError(TXT_ERRO_SENHA_ZIP_INVALIDA) from erro


def _validar_senha_arquivo(arquivo_aberto, senha: str, eh_rar: bool):
    if not eh_rar:
        _validar_senha_zip(arquivo_aberto, senha)
        return

    try:
        if not arquivo_aberto.needs_password():
            return
        if not senha:
            raise ValueError(TXT_ERRO_RAR_SENHA_NECESSARIA)
        membros = [
            info for info in arquivo_aberto.infolist() if not info.is_dir()
        ]
        if membros:
            with arquivo_aberto.open(membros[0]) as entrada:
                entrada.read(1)
    except ValueError:
        raise
    except rarfile.Error as erro:
        raise _traduzir_erro_rar(erro) from erro


def _abrir_membro(arquivo_aberto, info, eh_rar: bool):
    return arquivo_aberto.open(info) if eh_rar else arquivo_aberto.open(info, "r")


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


def _prefixo_pasta_raiz_unica(
    membros,
    destino: str,
    remover_pasta_raiz_diferente: bool = False,
    preservar_pasta_raiz: bool = False,
) -> str | None:
    """Detecta uma pasta única que contém todo o conteúdo do ZIP."""
    if preservar_pasta_raiz or not membros:
        return None

    raizes = {
        PurePosixPath(relativo).parts[0]
        for _, relativo in membros
        if PurePosixPath(relativo).parts
    }
    if len(raizes) != 1:
        return None

    raiz = next(iter(raizes))
    nome_destino = os.path.basename(os.path.normpath(destino))
    nomes_coincidem = (
        bool(nome_destino) and raiz.casefold() == nome_destino.casefold()
    )
    if not nomes_coincidem and not remover_pasta_raiz_diferente:
        return None

    for info, relativo in membros:
        partes = PurePosixPath(relativo).parts
        if len(partes) == 1 and not info.is_dir():
            return None
        if relativo != raiz and not relativo.startswith(f"{raiz}/"):
            return None
    return raiz


def _ler_membros(
    arquivo_zip: str,
    destino: str,
    remover_pasta_raiz_diferente: bool = False,
    senha: str = "",
    preservar_pasta_raiz: bool = False,
):
    if (
        not os.path.isfile(arquivo_zip)
        or os.path.splitext(arquivo_zip)[1].casefold() not in {".zip", ".rar"}
    ):
        raise ValueError(TXT_ERRO_ORIGEM_ZIP_INVALIDA)
    if os.path.exists(destino) and not os.path.isdir(destino):
        raise ValueError(TXT_ERRO_DESTINO_PASTA_INVALIDO)

    raiz_absoluta = os.path.abspath(destino)
    raiz_real = os.path.realpath(destino)
    eh_rar = _eh_rar(arquivo_zip)
    try:
        with _abrir_arquivo_compactado(arquivo_zip, senha) as zip_aberto:
            _validar_senha_arquivo(zip_aberto, senha, eh_rar)
            membros_brutos = []
            for info in zip_aberto.infolist():
                if eh_rar and (
                    info.is_symlink()
                    or (not info.is_dir() and not info.is_file())
                ):
                    raise ValueError(
                        TXT_ERRO_RAR_LINK.format(nome=info.filename)
                    )
                relativo = _nome_membro_seguro(info.filename)
                if relativo is not None:
                    membros_brutos.append((info, relativo))

            prefixo = _prefixo_pasta_raiz_unica(
                membros_brutos,
                destino,
                remover_pasta_raiz_diferente,
                preservar_pasta_raiz,
            )
            membros = []
            for info, relativo in membros_brutos:
                if prefixo and relativo == prefixo and info.is_dir():
                    continue
                if prefixo and relativo.startswith(f"{prefixo}/"):
                    relativo = relativo[len(prefixo) + 1:]

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
            return membros, prefixo
    except zipfile.BadZipFile as erro:
        raise ValueError(TXT_ERRO_ARQUIVO_ZIP_INVALIDO) from erro
    except rarfile.Error as erro:
        raise _traduzir_erro_rar(erro) from erro


def listar_conflitos(
    arquivo_zip: str,
    destino: str,
    remover_pasta_raiz_diferente: bool = False,
    senha: str = "",
    preservar_pasta_raiz: bool = False,
) -> list[str]:
    """Valida o ZIP e retorna os arquivos que já existem no destino."""
    membros, _ = _ler_membros(
        arquivo_zip,
        destino,
        remover_pasta_raiz_diferente,
        senha,
        preservar_pasta_raiz,
    )
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
    remover_pasta_raiz_diferente: bool = False,
    senha: str = "",
    preservar_pasta_raiz: bool = False,
) -> str:
    """Extrai ZIP ou RAR dentro do destino, com substituição controlada."""
    arquivo_zip = os.path.abspath(os.path.expanduser(arquivo_zip))
    destino = os.path.abspath(os.path.expanduser(destino))
    substituir = substituir or set()
    os.makedirs(destino, exist_ok=True)

    raiz_absoluta = os.path.abspath(destino)
    raiz_real = os.path.realpath(destino)
    membros, prefixo = _ler_membros(
        arquivo_zip,
        destino,
        remover_pasta_raiz_diferente,
        senha,
        preservar_pasta_raiz,
    )
    total = max(sum(not info.is_dir() for info, _, _ in membros), 1)
    processados = 0
    arquivos_extraidos = 0
    arquivos_mantidos = 0

    if prefixo:
        log.info(
            "OperacoesZIP",
            "extrair_zip",
            TXT_LOG_PASTA_RAIZ_REMOVIDA.format(nome=prefixo),
        )

    eh_rar = _eh_rar(arquivo_zip)
    try:
        with _abrir_arquivo_compactado(arquivo_zip, senha) as zip_aberto:
            _validar_senha_arquivo(zip_aberto, senha, eh_rar)
            for info, relativo, caminho in membros:
                if info.is_dir():
                    caminho = _caminho_destino_seguro(
                        raiz_absoluta, raiz_real, relativo
                    )
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
                                TXT_ERRO_DESTINO_FORA_DA_PASTA.format(
                                    nome=relativo
                                )
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
                            with _abrir_membro(
                                zip_aberto, info, eh_rar
                            ) as arquivo_entrada:
                                shutil.copyfileobj(arquivo_entrada, arquivo_saida)
                        os.replace(temporario, caminho)
                    except Exception as erro:
                        try:
                            os.close(descritor)
                        except OSError:
                            pass
                        if os.path.exists(temporario):
                            os.remove(temporario)
                        if eh_rar and isinstance(erro, rarfile.Error):
                            raise _traduzir_erro_rar(erro) from erro
                        raise
                    arquivos_extraidos += 1
                else:
                    arquivos_mantidos += 1

                processados += 1
                _notificar(
                    progresso,
                    int(processados * 100 / total),
                    TXT_PROGRESS_EXTRAIR.format(nome=relativo),
                )
    except rarfile.Error as erro:
        raise _traduzir_erro_rar(erro) from erro

    if processados == 0:
        _notificar(progresso, 100, TXT_PROGRESS_EXTRAIR.format(nome=""))
    log.ok(
        "OperacoesZIP",
        "extrair_arquivo_compactado",
        TXT_LOG_RESULTADO_EXTRAIR.format(
            destino=destino,
            extraidos=arquivos_extraidos,
            mantidos=arquivos_mantidos,
        ),
    )
    return destino

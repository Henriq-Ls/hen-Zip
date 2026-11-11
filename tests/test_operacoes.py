import io
import os
import tempfile
import unittest
import zipfile
from unittest.mock import patch

import rarfile

from _ZIP_.operacoes import compactar_pasta, extrair_zip, listar_conflitos


class OperacoesZipTest(unittest.TestCase):
    def setUp(self):
        self._temporario = tempfile.TemporaryDirectory()
        self.addCleanup(self._temporario.cleanup)
        self.raiz = self._temporario.name

    def test_compacta_arquivos_e_pastas_vazias(self):
        origem = os.path.join(self.raiz, "origem")
        os.makedirs(os.path.join(origem, "pasta_vazia"))
        with open(os.path.join(origem, "arquivo.txt"), "w", encoding="utf-8") as arq:
            arq.write("conteúdo")
        destino = os.path.join(self.raiz, "resultado.zip")

        compactar_pasta(origem, destino)

        with zipfile.ZipFile(destino) as arquivo_zip:
            self.assertEqual(
                set(arquivo_zip.namelist()),
                {"arquivo.txt", "pasta_vazia/"},
            )
            self.assertEqual(arquivo_zip.read("arquivo.txt"), b"conte\xc3\xbado")

    def test_compacta_e_extrai_zip_com_senha(self):
        origem = os.path.join(self.raiz, "origem")
        destino_zip = os.path.join(self.raiz, "protegido.zip")
        destino = os.path.join(self.raiz, "extraido")
        os.makedirs(origem)
        with open(os.path.join(origem, "arquivo.txt"), "w", encoding="utf-8") as arq:
            arq.write("conteúdo protegido")

        compactar_pasta(origem, destino_zip, senha="senha segura")

        with self.assertRaisesRegex(ValueError, "protegido por senha"):
            listar_conflitos(destino_zip, destino)
        with self.assertRaisesRegex(ValueError, "Confira a senha"):
            listar_conflitos(destino_zip, destino, senha="senha errada")

        extrair_zip(destino_zip, destino, senha="senha segura")

        with open(
            os.path.join(destino, "arquivo.txt"),
            encoding="utf-8",
        ) as arq:
            self.assertEqual(arq.read(), "conteúdo protegido")

    def test_extrai_preservando_e_substituindo_seletivamente(self):
        arquivo_zip = os.path.join(self.raiz, "arquivos.zip")
        destino = os.path.join(self.raiz, "destino")
        os.makedirs(destino)
        with open(os.path.join(destino, "existente.txt"), "w", encoding="utf-8") as arq:
            arq.write("versão atual")
        with zipfile.ZipFile(arquivo_zip, "w") as arquivo:
            arquivo.writestr("existente.txt", "versão do ZIP")
            arquivo.writestr("novo.txt", "novo conteúdo")

        self.assertEqual(listar_conflitos(arquivo_zip, destino), ["existente.txt"])
        extrair_zip(arquivo_zip, destino, set())
        with open(os.path.join(destino, "existente.txt"), encoding="utf-8") as arq:
            self.assertEqual(arq.read(), "versão atual")
        self.assertTrue(os.path.isfile(os.path.join(destino, "novo.txt")))

        extrair_zip(arquivo_zip, destino, {"existente.txt"})
        with open(os.path.join(destino, "existente.txt"), encoding="utf-8") as arq:
            self.assertEqual(arq.read(), "versão do ZIP")

    def test_remove_pasta_raiz_que_tem_o_mesmo_nome_do_destino(self):
        arquivo_zip = os.path.join(self.raiz, "hen-Navi.zip")
        destino = os.path.join(self.raiz, "hen-Navi")
        with zipfile.ZipFile(arquivo_zip, "w") as arquivo:
            arquivo.writestr("hen-Navi/", "")
            arquivo.writestr("hen-Navi/main.py", "conteúdo")
            arquivo.writestr("hen-Navi/nucleo/info.txt", "documentação")

        extrair_zip(arquivo_zip, destino)

        self.assertTrue(os.path.isfile(os.path.join(destino, "main.py")))
        self.assertTrue(
            os.path.isfile(os.path.join(destino, "nucleo", "info.txt"))
        )
        self.assertFalse(os.path.exists(os.path.join(destino, "hen-Navi")))

    def test_preserva_pasta_raiz_unica_se_o_destino_tem_outro_nome_por_padrao(self):
        arquivo_zip = os.path.join(self.raiz, "hen-Navi.zip")
        destino = os.path.join(self.raiz, "projeto-extraido")
        with zipfile.ZipFile(arquivo_zip, "w") as arquivo:
            arquivo.writestr("hen-Navi/", "")
            arquivo.writestr("hen-Navi/main.py", "conteúdo")

        extrair_zip(arquivo_zip, destino)

        self.assertTrue(
            os.path.isfile(os.path.join(destino, "hen-Navi", "main.py"))
        )
        self.assertFalse(os.path.exists(os.path.join(destino, "main.py")))

    def test_remove_pasta_raiz_se_destino_tem_outro_nome_e_opcao_marcada(self):
        arquivo_zip = os.path.join(self.raiz, "hen-Navi.zip")
        destino = os.path.join(self.raiz, "projeto-extraido")
        with zipfile.ZipFile(arquivo_zip, "w") as arquivo:
            arquivo.writestr("hen-Navi/", "")
            arquivo.writestr("hen-Navi/main.py", "conteúdo")

        extrair_zip(
            arquivo_zip,
            destino,
            remover_pasta_raiz_diferente=True,
        )

        self.assertTrue(os.path.isfile(os.path.join(destino, "main.py")))
        self.assertFalse(os.path.exists(os.path.join(destino, "hen-Navi")))

    def test_copia_ao_lado_preserva_e_mescla_raiz_com_checkbox_marcado(self):
        pasta_zip = os.path.join(self.raiz, "Downloads")
        pasta_raiz = os.path.join(pasta_zip, "hen-Navi")
        os.makedirs(pasta_raiz)
        arquivo_zip = os.path.join(pasta_zip, "hen-Navi.zip")
        arquivo_existente = os.path.join(pasta_raiz, "existente.txt")
        with open(arquivo_existente, "w", encoding="utf-8") as arquivo:
            arquivo.write("conteúdo local")
        with zipfile.ZipFile(arquivo_zip, "w") as arquivo:
            arquivo.writestr("hen-Navi/novo.txt", "novo conteúdo")
            arquivo.writestr("hen-Navi/existente.txt", "conteúdo do ZIP")

        self.assertEqual(
            listar_conflitos(
                arquivo_zip,
                pasta_zip,
                remover_pasta_raiz_diferente=True,
                preservar_pasta_raiz=True,
            ),
            ["hen-Navi/existente.txt"],
        )
        extrair_zip(
            arquivo_zip,
            pasta_zip,
            substituir={"hen-Navi/existente.txt"},
            remover_pasta_raiz_diferente=True,
            preservar_pasta_raiz=True,
        )

        self.assertTrue(os.path.isfile(os.path.join(pasta_raiz, "novo.txt")))
        self.assertFalse(os.path.exists(os.path.join(pasta_zip, "novo.txt")))
        with open(arquivo_existente, encoding="utf-8") as arquivo:
            self.assertEqual(arquivo.read(), "conteúdo do ZIP")

    def test_detecta_conflito_e_substitui_arquivo_apos_remover_raiz(self):
        arquivo_zip = os.path.join(self.raiz, "pacote.zip")
        destino = os.path.join(self.raiz, "projeto")
        os.makedirs(destino)
        with open(os.path.join(destino, "arquivo.txt"), "w", encoding="utf-8") as arq:
            arq.write("versão antiga")
        with zipfile.ZipFile(arquivo_zip, "w") as arquivo:
            arquivo.writestr("pasta-do-pacote/arquivo.txt", "versão do ZIP")

        self.assertEqual(
            listar_conflitos(
                arquivo_zip,
                destino,
                remover_pasta_raiz_diferente=True,
            ),
            ["arquivo.txt"],
        )
        extrair_zip(
            arquivo_zip,
            destino,
            {"arquivo.txt"},
            remover_pasta_raiz_diferente=True,
        )

        with open(os.path.join(destino, "arquivo.txt"), encoding="utf-8") as arq:
            self.assertEqual(arq.read(), "versão do ZIP")
        self.assertFalse(os.path.exists(os.path.join(destino, "pasta-do-pacote")))

    def test_preserva_estrutura_se_zip_tambem_tiver_arquivo_na_raiz(self):
        arquivo_zip = os.path.join(self.raiz, "hen-Navi.zip")
        destino = os.path.join(self.raiz, "projeto-extraido")
        with zipfile.ZipFile(arquivo_zip, "w") as arquivo:
            arquivo.writestr("hen-Navi/main.py", "conteúdo")
            arquivo.writestr("LEIA-ME.txt", "instruções")

        extrair_zip(arquivo_zip, destino)

        self.assertTrue(
            os.path.isfile(os.path.join(destino, "hen-Navi", "main.py"))
        )
        self.assertTrue(os.path.isfile(os.path.join(destino, "LEIA-ME.txt")))

    def test_rejeita_caminho_de_travessia(self):
        arquivo_zip = os.path.join(self.raiz, "inseguro.zip")
        destino = os.path.join(self.raiz, "destino")
        with zipfile.ZipFile(arquivo_zip, "w") as arquivo:
            arquivo.writestr("../fora.txt", "não deve ser escrito")

        with self.assertRaisesRegex(ValueError, "caminho inválido ou inseguro"):
            listar_conflitos(arquivo_zip, destino)
        self.assertFalse(os.path.exists(os.path.join(self.raiz, "fora.txt")))

    def test_rejeita_link_de_pasta_que_sai_do_destino(self):
        arquivo_zip = os.path.join(self.raiz, "link.zip")
        destino = os.path.join(self.raiz, "destino")
        fora = os.path.join(self.raiz, "fora")
        os.makedirs(destino)
        os.makedirs(fora)
        os.symlink(fora, os.path.join(destino, "atalho"))
        with zipfile.ZipFile(arquivo_zip, "w") as arquivo:
            arquivo.writestr("atalho/arquivo.txt", "não deve ser escrito")
            arquivo.writestr("outro-arquivo.txt", "preserva a pasta de origem")

        with self.assertRaises(ValueError):
            listar_conflitos(arquivo_zip, destino)
        self.assertFalse(os.path.exists(os.path.join(fora, "arquivo.txt")))

    def test_extrai_rar_com_validacao_de_caminho_e_arquivo_temporario(self):
        arquivo_rar = os.path.join(self.raiz, "pacote.rar")
        destino = os.path.join(self.raiz, "destino-rar")
        os.makedirs(destino)
        with open(arquivo_rar, "wb") as arquivo:
            arquivo.write(b"mock rar")

        class Membro:
            filename = "pasta/arquivo.txt"

            def is_symlink(self):
                return False

            def is_dir(self):
                return False

            def is_file(self):
                return True

        class ArquivoRarFake:
            def __enter__(self):
                return self

            def __exit__(self, *_args):
                return False

            def setpassword(self, _senha):
                pass

            def needs_password(self):
                return False

            def infolist(self):
                return [Membro()]

            def open(self, _membro):
                return io.BytesIO(b"conteudo RAR")

        with patch(
            "_ZIP_.operacoes.rarfile.RarFile",
            return_value=ArquivoRarFake(),
        ):
            conflitos = listar_conflitos(arquivo_rar, destino)
            extrair_zip(arquivo_rar, destino)

        self.assertEqual(conflitos, [])
        with open(
            os.path.join(destino, "pasta", "arquivo.txt"),
            "rb",
        ) as arquivo:
            self.assertEqual(arquivo.read(), b"conteudo RAR")

    def test_rejeita_travessia_de_caminho_em_rar(self):
        arquivo_rar = os.path.join(self.raiz, "inseguro.rar")
        with open(arquivo_rar, "wb") as arquivo:
            arquivo.write(b"mock rar")

        class Membro:
            filename = "../fora.txt"

            def is_symlink(self):
                return False

            def is_dir(self):
                return False

            def is_file(self):
                return True

        class ArquivoRarFake:
            def __enter__(self):
                return self

            def __exit__(self, *_args):
                return False

            def setpassword(self, _senha):
                pass

            def needs_password(self):
                return False

            def infolist(self):
                return [Membro()]

        with patch(
            "_ZIP_.operacoes.rarfile.RarFile",
            return_value=ArquivoRarFake(),
        ):
            with self.assertRaisesRegex(ValueError, "caminho inválido ou inseguro"):
                listar_conflitos(
                    arquivo_rar,
                    os.path.join(self.raiz, "destino"),
                )
        self.assertFalse(os.path.exists(os.path.join(self.raiz, "fora.txt")))

    def test_informa_quando_senha_de_cabecalho_rar_esta_incorreta(self):
        arquivo_rar = os.path.join(self.raiz, "protegido.rar")
        with open(arquivo_rar, "wb") as arquivo:
            arquivo.write(b"mock rar")

        class ParserRar:
            def has_header_encryption(self):
                return True

        class ArquivoRarProtegido:
            _file_parser = ParserRar()

            def needs_password(self):
                return False

            def setpassword(self, _senha):
                raise rarfile.BadRarFile("senha incorreta")

        with patch(
            "_ZIP_.operacoes.rarfile.RarFile",
            return_value=ArquivoRarProtegido(),
        ):
            with self.assertRaisesRegex(ValueError, "Confira a senha"):
                listar_conflitos(
                    arquivo_rar,
                    os.path.join(self.raiz, "destino"),
                    senha="senha errada",
                )

    def test_pede_senha_quando_cabecalho_rar_esta_protegido(self):
        arquivo_rar = os.path.join(self.raiz, "protegido.rar")
        with open(arquivo_rar, "wb") as arquivo:
            arquivo.write(b"mock rar")

        class ParserRar:
            def has_header_encryption(self):
                return True

        class ArquivoRarProtegido:
            _file_parser = ParserRar()

            def needs_password(self):
                return False

            def close(self):
                pass

        with patch(
            "_ZIP_.operacoes.rarfile.RarFile",
            return_value=ArquivoRarProtegido(),
        ):
            with self.assertRaisesRegex(ValueError, "protegido por senha"):
                listar_conflitos(arquivo_rar, os.path.join(self.raiz, "destino"))

    def test_identifica_rar_invalido_sem_chamar_de_zip(self):
        arquivo_rar = os.path.join(self.raiz, "invalido.rar")
        with open(arquivo_rar, "wb") as arquivo:
            arquivo.write(b"conteudo invalido")

        with patch(
            "_ZIP_.operacoes.rarfile.RarFile",
            side_effect=rarfile.NotRarFile("Not a RAR file"),
        ):
            with self.assertRaisesRegex(ValueError, "RAR válido ou está danificado"):
                listar_conflitos(arquivo_rar, os.path.join(self.raiz, "destino"))


if __name__ == "__main__":
    unittest.main()

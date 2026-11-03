import os
import tempfile
import unittest
import zipfile

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

    def test_preserva_pasta_raiz_se_o_destino_tem_outro_nome(self):
        arquivo_zip = os.path.join(self.raiz, "hen-Navi.zip")
        destino = os.path.join(self.raiz, "projeto-extraido")
        with zipfile.ZipFile(arquivo_zip, "w") as arquivo:
            arquivo.writestr("hen-Navi/main.py", "conteúdo")

        extrair_zip(arquivo_zip, destino)

        self.assertTrue(
            os.path.isfile(os.path.join(destino, "hen-Navi", "main.py"))
        )

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

        with self.assertRaises(ValueError):
            listar_conflitos(arquivo_zip, destino)
        self.assertFalse(os.path.exists(os.path.join(fora, "arquivo.txt")))


if __name__ == "__main__":
    unittest.main()

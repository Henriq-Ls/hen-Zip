import os
import tempfile
import unittest
import zipfile
from unittest.mock import patch

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PySide6.QtCore import QEventLoop, QTimer
from PySide6.QtWidgets import QApplication

from _APP_.main_window import MainWindow
from _APPDATA_ import appdata
from _LOGS_ import log
from _ZIP_.thread_zip import ThreadOperacaoZip
from _CONFIGURA_ import (
    CHAVE_CONFIG_OPERACOES,
    CHAVE_OPERACAO_APAGAR_ZIP,
    CHAVE_OPERACAO_DESTINO,
    CHAVE_OPERACAO_EXTRAIR_JUNTO_ZIP,
    CHAVE_OPERACAO_MODO,
    CHAVE_OPERACAO_ORIGEM,
)


class PersistenciaOperacoesTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._app = QApplication.instance() or QApplication([])

    def _criar_janela_mockada(self, configuracao):
        patchers = [
            patch.object(appdata, "ler_config", return_value=configuracao.copy()),
            patch.object(appdata, "salvar_config"),
            patch.object(appdata, "ler_sessao", return_value={}),
            patch.object(appdata, "salvar_sessao"),
        ]
        mocks = []
        for patcher in patchers:
            mocks.append(patcher.start())
            self.addCleanup(patcher.stop)

        janela = MainWindow()
        self.addCleanup(janela.close)
        return janela, mocks[1]

    def test_restaura_e_salva_linhas_e_caminhos(self):
        configuracao = {
            CHAVE_CONFIG_OPERACOES: [
                {
                    CHAVE_OPERACAO_MODO: "compactar",
                    CHAVE_OPERACAO_ORIGEM: "/projetos/um",
                    CHAVE_OPERACAO_DESTINO: "/backups/um.zip",
                    CHAVE_OPERACAO_APAGAR_ZIP: False,
                    CHAVE_OPERACAO_EXTRAIR_JUNTO_ZIP: False,
                },
                {
                    CHAVE_OPERACAO_MODO: "extrair",
                    CHAVE_OPERACAO_ORIGEM: "/downloads/dois.zip",
                    CHAVE_OPERACAO_DESTINO: "/projetos/dois",
                    CHAVE_OPERACAO_APAGAR_ZIP: True,
                    CHAVE_OPERACAO_EXTRAIR_JUNTO_ZIP: True,
                },
            ]
        }

        janela, salvar_config = self._criar_janela_mockada(configuracao)

        self.assertEqual(len(janela._linhas), 2)
        self.assertEqual(janela._linhas[0].layout().count(), 8)
        self.assertEqual(janela._linhas[0]._botao_executar.text(), "Zipar")
        self.assertEqual(janela._linhas[1]._botao_executar.text(), "Extrair")
        self.assertFalse(janela._linhas[0]._checkbox_apagar_zip.isChecked())
        self.assertTrue(janela._linhas[1]._checkbox_apagar_zip.isChecked())
        self.assertFalse(
            janela._linhas[0]._checkbox_extrair_junto_zip.isChecked()
        )
        self.assertTrue(
            janela._linhas[1]._checkbox_extrair_junto_zip.isChecked()
        )
        self.assertEqual(
            janela._linhas[0].exportar_dados(),
            configuracao[CHAVE_CONFIG_OPERACOES][0],
        )
        self.assertEqual(
            janela._linhas[1].exportar_dados(),
            configuracao[CHAVE_CONFIG_OPERACOES][1],
        )

        janela._linhas[0]._origem.setText("/projetos/atualizado")
        self.assertTrue(janela._timer_salvar_operacoes.isActive())
        janela._salvar_operacoes()

        salvo = salvar_config.call_args.args[0]
        self.assertEqual(
            salvo[CHAVE_CONFIG_OPERACOES][0][CHAVE_OPERACAO_ORIGEM],
            "/projetos/atualizado",
        )
        self.assertEqual(
            salvo[CHAVE_CONFIG_OPERACOES][1],
            configuracao[CHAVE_CONFIG_OPERACOES][1],
        )

    def test_menu_do_botao_altera_modo_da_operacao(self):
        janela, _ = self._criar_janela_mockada({})
        linha = janela._linhas[0]

        self.assertEqual(linha._botao_executar.text(), "Extrair")
        linha._acao_modo_compactar.trigger()

        self.assertEqual(linha._botao_executar.text(), "Zipar")
        self.assertEqual(
            linha.exportar_dados()[CHAVE_OPERACAO_MODO],
            "compactar",
        )

    def test_checkbox_apagar_zip_e_salva_e_restaurada(self):
        janela, salvar_config = self._criar_janela_mockada({})
        linha = janela._linhas[0]

        self.assertFalse(linha._checkbox_apagar_zip.isChecked())
        linha._checkbox_apagar_zip.setChecked(True)
        janela._salvar_operacoes()
        configuracao_salva = salvar_config.call_args.args[0]
        self.assertTrue(
            configuracao_salva[CHAVE_CONFIG_OPERACOES][0][
                CHAVE_OPERACAO_APAGAR_ZIP
            ]
        )

        restaurada, _ = self._criar_janela_mockada(configuracao_salva)
        self.assertTrue(restaurada._linhas[0]._checkbox_apagar_zip.isChecked())

    def test_checkbox_extrair_junto_zip_e_salvo_e_restaurado(self):
        janela, salvar_config = self._criar_janela_mockada({})
        linha = janela._linhas[0]

        self.assertFalse(linha._checkbox_extrair_junto_zip.isChecked())
        linha._checkbox_extrair_junto_zip.setChecked(True)
        janela._salvar_operacoes()
        configuracao_salva = salvar_config.call_args.args[0]
        self.assertTrue(
            configuracao_salva[CHAVE_CONFIG_OPERACOES][0][
                CHAVE_OPERACAO_EXTRAIR_JUNTO_ZIP
            ]
        )

        restaurada, _ = self._criar_janela_mockada(configuracao_salva)
        self.assertTrue(
            restaurada._linhas[0]._checkbox_extrair_junto_zip.isChecked()
        )

    def test_extrai_tambem_na_pasta_do_zip(self):
        janela, _ = self._criar_janela_mockada({})
        linha = janela._linhas[0]
        with tempfile.TemporaryDirectory() as temporario:
            pasta_zip = os.path.join(temporario, "downloads")
            os.makedirs(pasta_zip)
            caminho_zip = os.path.join(pasta_zip, "download.zip")
            destino = os.path.join(temporario, "destino")
            with zipfile.ZipFile(caminho_zip, "w") as arquivo:
                arquivo.writestr("subpasta/arquivo.txt", "conteúdo")

            linha._origem.setText(caminho_zip)
            linha._destino.setText(destino)
            linha._checkbox_extrair_junto_zip.setChecked(True)
            loop = QEventLoop()
            iniciar_thread_original = ThreadOperacaoZip.start

            def iniciar_e_aguardar(worker):
                worker.finished.connect(loop.quit)
                iniciar_thread_original(worker)

            with patch.object(
                ThreadOperacaoZip,
                "start",
                new=iniciar_e_aguardar,
            ), patch("_APP_.main_window.popup_info"):
                linha._emitir_operacao()
                QTimer.singleShot(5000, loop.quit)
                loop.exec()
                self._app.processEvents()

            for pasta_extraida in (destino, pasta_zip):
                caminho_extraido = os.path.join(
                    pasta_extraida, "subpasta", "arquivo.txt"
                )
                with open(caminho_extraido, encoding="utf-8") as arquivo:
                    self.assertEqual(arquivo.read(), "conteúdo")
            self.assertTrue(os.path.isfile(caminho_zip))

    def test_zip_so_e_apagado_apos_conclusao_e_caminho_permanece(self):
        janela, _ = self._criar_janela_mockada({})
        linha = janela._linhas[0]
        with tempfile.TemporaryDirectory() as temporario:
            caminho_zip = os.path.join(temporario, "download.zip")
            destino = os.path.join(temporario, "extraido")
            with zipfile.ZipFile(caminho_zip, "w") as arquivo:
                arquivo.writestr("arquivo.txt", "conteúdo")

            linha._origem.setText(caminho_zip)
            linha._destino.setText(destino)
            linha._checkbox_apagar_zip.setChecked(True)
            loop = QEventLoop()
            iniciar_thread_original = ThreadOperacaoZip.start

            def iniciar_e_aguardar(worker):
                worker.finished.connect(loop.quit)
                iniciar_thread_original(worker)

            with patch.object(
                ThreadOperacaoZip,
                "start",
                new=iniciar_e_aguardar,
            ), patch("_APP_.main_window.popup_info"):
                linha._emitir_operacao()
                QTimer.singleShot(5000, loop.quit)
                loop.exec()
                self._app.processEvents()

            self.assertFalse(os.path.exists(caminho_zip))
            with open(os.path.join(destino, "arquivo.txt"), encoding="utf-8") as arq:
                self.assertEqual(arq.read(), "conteúdo")
            self.assertEqual(linha._origem.text(), caminho_zip)

    def test_zip_permanece_se_a_opcao_estiver_desmarcada(self):
        janela, _ = self._criar_janela_mockada({})
        with tempfile.NamedTemporaryFile(suffix=".zip") as arquivo_zip:
            with patch("_APP_.main_window.popup_info"):
                janela._ao_operacao_concluida(
                    "operacao_teste",
                    "Extração concluída.",
                    arquivo_zip.name,
                    False,
                )

            self.assertTrue(os.path.exists(arquivo_zip.name))

    def test_falha_ao_apagar_zip_exibe_aviso(self):
        janela, _ = self._criar_janela_mockada({})
        with patch(
            "_APP_.main_window.os.remove",
            side_effect=PermissionError("sem permissão"),
        ), patch("_APP_.main_window.popup_aviso") as popup:
            janela._ao_operacao_concluida(
                "operacao_teste",
                "Extração concluída.",
                "download.zip",
                True,
            )

        self.assertIn("download.zip", popup.call_args.args[1])
        self.assertIn("sem permissão", popup.call_args.args[1])

    def test_linha_adicionada_e_removida_atualiza_configuracao(self):
        configuracao = {CHAVE_CONFIG_OPERACOES: []}
        janela, salvar_config = self._criar_janela_mockada(configuracao)
        self.assertEqual(janela._linhas, [])

        janela._adicionar_linha()
        self.assertEqual(len(janela._linhas), 1)
        janela._salvar_operacoes()
        self.assertEqual(
            len(salvar_config.call_args.args[0][CHAVE_CONFIG_OPERACOES]),
            1,
        )

        janela._remover_linha(janela._linhas[0])
        janela._salvar_operacoes()
        self.assertEqual(
            salvar_config.call_args.args[0][CHAVE_CONFIG_OPERACOES],
            [],
        )

    def test_botao_abrir_logs_abre_o_log_geral(self):
        janela, _ = self._criar_janela_mockada({})
        with tempfile.NamedTemporaryFile(suffix=".log") as arquivo_log:
            with patch.object(log, "caminho_geral", arquivo_log.name):
                with patch(
                    "_APP_.main_window.QDesktopServices.openUrl",
                    return_value=True,
                ) as abrir_url:
                    janela._botao_logs.click()
                    url = abrir_url.call_args.args[0]

        self.assertEqual(url.toLocalFile(), arquivo_log.name)

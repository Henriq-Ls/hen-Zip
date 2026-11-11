import os
import tempfile
import unittest
import zipfile
from unittest.mock import patch

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PySide6.QtCore import QEventLoop, QPoint, Qt, QTimer
from PySide6.QtTest import QTest
from PySide6.QtWidgets import QApplication, QLineEdit, QWidget

from _APP_.main_window import MainWindow
from _APP_.Painel_operacoes.divisoria_operacao import DivisoriaOperacao
from _APPDATA_ import appdata
from _LOGS_ import log
from _ZIP_.thread_zip import ThreadOperacaoZip
from _ZIP_.operacoes import compactar_pasta
from _ULTILIDADES_.popups import popup_info
from _CONFIGURA_ import (
    CHAVE_CONFIG_OPERACOES,
    CHAVE_OPERACAO_APAGAR_ZIP,
    CHAVE_OPERACAO_DESTINO,
    CHAVE_OPERACAO_EXTRAIR_JUNTO_ZIP,
    CHAVE_OPERACAO_REMOVER_PASTA_RAIZ,
    CHAVE_OPERACAO_MODO,
    CHAVE_OPERACAO_ORIGEM,
    FILTROS_ARQUIVO_COMPACTADO,
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
                    CHAVE_OPERACAO_REMOVER_PASTA_RAIZ: False,
                },
                {
                    CHAVE_OPERACAO_MODO: "extrair",
                    CHAVE_OPERACAO_ORIGEM: "/downloads/dois.zip",
                    CHAVE_OPERACAO_DESTINO: "/projetos/dois",
                    CHAVE_OPERACAO_APAGAR_ZIP: True,
                    CHAVE_OPERACAO_EXTRAIR_JUNTO_ZIP: True,
                    CHAVE_OPERACAO_REMOVER_PASTA_RAIZ: True,
                },
            ]
        }

        janela, salvar_config = self._criar_janela_mockada(configuracao)

        self.assertEqual(len(janela._linhas), 2)
        self.assertEqual(
            janela._linhas[0].layout().itemAt(0).layout().count(),
            10,
        )
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
        self.assertFalse(
            janela._linhas[0]._checkbox_remover_pasta_raiz.isChecked()
        )
        self.assertTrue(
            janela._linhas[1]._checkbox_remover_pasta_raiz.isChecked()
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

    def test_procurar_origem_usa_explorer_com_filtros_zip_e_rar(self):
        janela, _ = self._criar_janela_mockada({})
        linha = janela._linhas[0]
        linha._origem.setText("/arquivos/pacote.rar")

        with patch(
            "_APP_.Painel_operacoes.linha_operacao.Explorer.get_open_file_name",
            return_value="/arquivos/pacote.rar",
        ) as abrir_explorer:
            linha._procurar_origem()

        self.assertEqual(linha._origem.text(), "/arquivos/pacote.rar")
        self.assertEqual(abrir_explorer.call_args.args[0], linha)
        filtros = abrir_explorer.call_args.args[3]
        self.assertEqual(filtros[0], "Arquivos RAR (*.rar)")
        self.assertIn("Arquivos ZIP (*.zip)", filtros)
        self.assertIn("Arquivos RAR (*.rar)", FILTROS_ARQUIVO_COMPACTADO)

    def test_opcoes_tem_marcacao_visual_igual_e_senha_nao_e_salva(self):
        janela, _ = self._criar_janela_mockada({})
        linha = janela._linhas[0]

        checkboxes = (
            linha._checkbox_apagar_zip,
            linha._checkbox_extrair_junto_zip,
            linha._checkbox_remover_pasta_raiz,
        )
        self.assertEqual(
            {checkbox.objectName() for checkbox in checkboxes},
            {"operationOptionCheck"},
        )
        self.assertEqual(linha._senha.echoMode(), QLineEdit.EchoMode.Password)

        linha._senha.setText("senha privada")
        dados = linha.exportar_dados()
        self.assertNotIn("senha", dados)
        restaurada, _ = self._criar_janela_mockada(
            {CHAVE_CONFIG_OPERACOES: [dados]}
        )
        self.assertEqual(restaurada._linhas[0]._senha.text(), "")

    def test_botao_e_menu_ajuda_abrem_o_guia(self):
        janela, _ = self._criar_janela_mockada({})
        with patch("_APP_.main_window.DialogoAjuda") as dialogo_ajuda:
            janela._botao_ajuda.click()

        dialogo_ajuda.assert_called_once_with(janela)
        dialogo_ajuda.return_value.exec.assert_called_once_with()

        menu_ajuda = next(
            acao.menu()
            for acao in janela.menuBar().actions()
            if acao.text().replace("&", "") == "Ajuda"
        )
        self.assertIn(
            "Como usar",
            [acao.text() for acao in menu_ajuda.actions()],
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

    def test_checkbox_remover_pasta_raiz_e_salvo_e_restaurado(self):
        janela, salvar_config = self._criar_janela_mockada({})
        linha = janela._linhas[0]

        self.assertFalse(linha._checkbox_remover_pasta_raiz.isChecked())
        linha._checkbox_remover_pasta_raiz.setChecked(True)
        janela._salvar_operacoes()
        configuracao_salva = salvar_config.call_args.args[0]
        self.assertTrue(
            configuracao_salva[CHAVE_CONFIG_OPERACOES][0][
                CHAVE_OPERACAO_REMOVER_PASTA_RAIZ
            ]
        )

        restaurada, _ = self._criar_janela_mockada(configuracao_salva)
        self.assertTrue(
            restaurada._linhas[0]._checkbox_remover_pasta_raiz.isChecked()
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
                arquivo.writestr("pasta-interna/arquivo.txt", "conteúdo")

            linha._origem.setText(caminho_zip)
            linha._destino.setText(destino)
            linha._checkbox_extrair_junto_zip.setChecked(True)
            linha._checkbox_apagar_zip.setChecked(True)
            linha._checkbox_remover_pasta_raiz.setChecked(True)
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
                caminho_extraido = os.path.join(pasta_extraida, "arquivo.txt")
                with open(caminho_extraido, encoding="utf-8") as arquivo:
                    self.assertEqual(arquivo.read(), "conteúdo")
                self.assertFalse(
                    os.path.exists(os.path.join(pasta_extraida, "pasta-interna"))
                )
            self.assertFalse(os.path.exists(caminho_zip))

    def test_destino_vazio_extrai_ao_lado_do_arquivo_quando_marcado(self):
        janela, _ = self._criar_janela_mockada({})
        linha = janela._linhas[0]

        with tempfile.TemporaryDirectory() as temporario:
            caminho_zip = os.path.join(temporario, "download.zip")
            with zipfile.ZipFile(caminho_zip, "w") as arquivo:
                arquivo.writestr("arquivo.txt", "conteúdo")

            linha._origem.setText(caminho_zip)
            linha._destino.clear()
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
            ), patch("_APP_.main_window.popup_info") as popup_info, patch(
                "_APP_.main_window.popup_erro"
            ) as popup_erro, patch("_APP_.main_window.popup_aviso") as popup_aviso:
                linha._emitir_operacao()
                QTimer.singleShot(5000, loop.quit)
                loop.exec()
                self._app.processEvents()

            with open(
                os.path.join(temporario, "arquivo.txt"),
                encoding="utf-8",
            ) as arquivo:
                self.assertEqual(arquivo.read(), "conteúdo")
            self.assertEqual(linha._destino.text(), "")
            popup_info.assert_called_once()
            popup_erro.assert_not_called()
            popup_aviso.assert_not_called()

    def test_interface_compacta_e_extrai_com_senha(self):
        janela, _ = self._criar_janela_mockada({})
        linha = janela._linhas[0]

        with tempfile.TemporaryDirectory() as temporario:
            origem = os.path.join(temporario, "origem")
            destino_zip = os.path.join(temporario, "protegido.zip")
            destino_extraido = os.path.join(temporario, "extraido")
            os.makedirs(origem)
            with open(
                os.path.join(origem, "arquivo.txt"),
                "w",
                encoding="utf-8",
            ) as arquivo:
                arquivo.write("conteúdo protegido")

            def executar_e_aguardar():
                loop = QEventLoop()
                iniciar_thread_original = ThreadOperacaoZip.start

                def iniciar_e_aguardar_thread(worker):
                    worker.finished.connect(loop.quit)
                    iniciar_thread_original(worker)

                with patch.object(
                    ThreadOperacaoZip,
                    "start",
                    new=iniciar_e_aguardar_thread,
                ), patch("_APP_.main_window.popup_info"):
                    linha._emitir_operacao()
                    QTimer.singleShot(5000, loop.quit)
                    loop.exec()
                    self._app.processEvents()

            linha._acao_modo_compactar.trigger()
            linha._origem.setText(origem)
            linha._destino.setText(destino_zip)
            linha._senha.setText("senha da interface")
            executar_e_aguardar()
            self.assertTrue(os.path.isfile(destino_zip))

            linha._acao_modo_extrair.trigger()
            linha._origem.setText(destino_zip)
            linha._destino.setText(destino_extraido)
            executar_e_aguardar()

            with open(
                os.path.join(destino_extraido, "arquivo.txt"),
                encoding="utf-8",
            ) as arquivo:
                self.assertEqual(arquivo.read(), "conteúdo protegido")

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
            with patch("_APP_.main_window.popup_info") as popup_info, patch(
                "_APP_.main_window.QApplication.beep"
            ) as beep:
                janela._ao_operacao_concluida(
                    "operacao_teste",
                    "Extração concluída.",
                    arquivo_zip.name,
                    False,
                )

            popup_info.assert_called_once_with(
                "Operação concluída",
                "Extração concluída.",
                janela,
                fechar_ao_clicar_fora=True,
            )
            beep.assert_called_once_with()
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

    def test_popup_info_fecha_ao_clicar_fora(self):
        janela = QWidget()
        self.addCleanup(janela.close)
        janela.setGeometry(100, 100, 600, 400)
        janela.show()
        self._app.processEvents()

        dialogo = popup_info(
            "Operação concluída",
            "Extração concluída.",
            janela,
            fechar_ao_clicar_fora=True,
        )
        fechado = []
        dialogo.finished.connect(lambda _: fechado.append(True))
        self._app.processEvents()
        self.assertTrue(dialogo.isVisible())

        QTest.mouseClick(
            janela,
            Qt.MouseButton.LeftButton,
            pos=QPoint(580, 380),
        )
        self._app.processEvents()
        self.assertTrue(fechado)

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

    def test_reordena_operacoes_e_salva_divisorias_entre_grupos(self):
        janela, salvar_config = self._criar_janela_mockada({})
        primeira = janela._linhas[0]
        primeira._origem.setText("primeira.zip")
        janela._adicionar_linha()
        segunda = janela._linhas[1]
        segunda._origem.setText("segunda.zip")
        janela._adicionar_linha()
        terceira = janela._linhas[2]
        terceira._origem.setText("terceira.zip")

        janela._adicionar_divisoria()
        divisoria = janela._itens[-1]
        self.assertIsInstance(divisoria, DivisoriaOperacao)

        terceira._botao_mover_cima.click()
        divisoria._botao_mover_cima.click()

        self.assertEqual(
            janela._itens,
            [primeira, terceira, divisoria, segunda],
        )
        self.assertFalse(primeira._botao_mover_cima.isEnabled())
        self.assertFalse(segunda._botao_mover_baixo.isEnabled())
        self.assertTrue(divisoria._botao_mover_cima.isEnabled())
        self.assertTrue(divisoria._botao_mover_baixo.isEnabled())

        janela._salvar_operacoes()
        salvas = salvar_config.call_args.args[0][CHAVE_CONFIG_OPERACOES]
        self.assertEqual(
            [item.get("tipo", "operacao") for item in salvas],
            ["operacao", "operacao", "divisoria", "operacao"],
        )
        self.assertEqual(
            [item.get(CHAVE_OPERACAO_ORIGEM) for item in salvas],
            ["primeira.zip", "terceira.zip", None, "segunda.zip"],
        )

        restaurada, _ = self._criar_janela_mockada(
            {CHAVE_CONFIG_OPERACOES: salvas}
        )
        self.assertEqual(
            [type(item) for item in restaurada._itens],
            [
                type(primeira),
                type(terceira),
                DivisoriaOperacao,
                type(segunda),
            ],
        )
        self.assertEqual(
            [linha._origem.text() for linha in restaurada._linhas],
            ["primeira.zip", "terceira.zip", "segunda.zip"],
        )

        linha_arrastada = restaurada._linhas[2]
        restaurada._ao_soltar_item(str(id(linha_arrastada)), 0)
        self.assertIs(restaurada._itens[0], linha_arrastada)
        self.assertEqual(
            linha_arrastada._puxador_reordenar.objectName(),
            "reorderHandle",
        )

        divisoria_restaurada = next(
            item
            for item in restaurada._itens
            if isinstance(item, DivisoriaOperacao)
        )
        divisoria_restaurada._botao_remover.click()
        self._app.processEvents()
        self.assertNotIn(divisoria_restaurada, restaurada._itens)

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

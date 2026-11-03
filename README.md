# hen-Zip

Aplicativo desktop em **PySide6** para compactar pastas em arquivos ZIP e extrair
ZIPs diretamente para uma pasta de destino. O hen-Zip permite configurar várias
linhas de operação e escolher individualmente quais arquivos existentes serão
substituídos durante a extração.

## Recursos

- Compacta o conteúdo de uma pasta em um arquivo `.zip`.
- Extrai arquivos para a pasta escolhida, sem apagar os demais arquivos.
- Lista conflitos e deixa selecionar arquivo por arquivo quais serão substituídos.
- Mostra o andamento das operações sem bloquear a interface.
- Rejeita caminhos absolutos e tentativas de sair da pasta de destino pelo ZIP.
- Mantém logs e preferências de janela na pasta de dados do usuário.

## Requisitos

- Python 3.10 ou superior.
- PySide6.

O módulo `zipfile` usado para manipular arquivos ZIP já faz parte da biblioteca
padrão do Python.

## Instalação e execução

Abra um terminal nesta pasta e execute:

```bash
python -m pip install -r requirements.txt
python main.py
```

No Windows, se `python` não estiver disponível no terminal, tente `py`:

```powershell
py -m pip install -r requirements.txt
py main.py
```

## Como usar

1. Escolha **Extrair ZIP para pasta** ou **Compactar pasta em ZIP** na linha.
2. Informe os caminhos de origem e destino ou use **Procurar**.
3. Clique em **Extrair arquivos** ou **Criar ZIP**.
4. Ao extrair, marque os arquivos existentes que podem ser substituídos e
   confirme. Os itens desmarcados e os demais arquivos no destino são mantidos.
5. Use **Nova operação** para adicionar outra linha.

Ao compactar, o conteúdo da pasta é colocado na raiz do ZIP. A pasta de origem
não é incluída como uma pasta extra dentro do arquivo.

## Estrutura

- `_APP_/` — janela e widgets PySide6.
- `_ZIP_/` — compactação, extração segura e execução em thread.
- `_CONFIGURA_/` — textos, cores, atalhos e dimensões da interface.
- `_THREADS_/` — ciclo de vida das threads.
- `_APPDATA_/` — configurações e sessão do aplicativo.
- `_LOGS_/` — registro de erros e operações.
- `nucleo/` — documentação interna do projeto.

## Testes

Os testes das operações de ZIP usam apenas a biblioteca padrão:

```bash
python -m unittest discover -s tests
```

## Licença

Adicione aqui a licença escolhida antes de publicar o projeto no GitHub.

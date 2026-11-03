# hen-Zip

Aplicativo desktop em **PySide6** para compactar pastas em arquivos ZIP e extrair
ZIPs diretamente para uma pasta de destino. O hen-Zip permite configurar várias
linhas de operação e escolher individualmente quais arquivos existentes serão
substituídos durante a extração.

## Recursos

- Compacta o conteúdo de uma pasta em um arquivo `.zip`.
- Extrai arquivos para a pasta escolhida, sem apagar os demais arquivos.
- Opcionalmente, extrai cada ZIP também na pasta onde ele está.
- Lista conflitos e deixa selecionar arquivo por arquivo quais serão substituídos.
- Mostra o andamento das operações sem bloquear a interface.
- Permite apagar o ZIP de origem depois de uma extração concluída, sem limpar o caminho salvo.
- Rejeita caminhos absolutos e tentativas de sair da pasta de destino pelo ZIP.
- Mantém logs e preferências de janela na pasta de dados do usuário.
- Salva automaticamente as linhas e restaura os caminhos na próxima abertura.
- Abre o log atual pela própria interface e registra o resumo da extração.

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

1. Use a seta do botão de ação para escolher **Extrair** ou **Compactar**.
2. Informe os caminhos de origem e destino ou use **Procurar**.
3. Clique em **Extrair** ou **Zipar**.
4. Ao extrair, marque os arquivos existentes que podem ser substituídos e
   confirme. Os itens desmarcados e os demais arquivos no destino são mantidos.
5. Opcionalmente, marque **Apagar ZIP após extrair** para excluir o arquivo ZIP
   somente depois que a extração terminar com sucesso. A linha e o caminho ficam
   salvos para reutilizar quando um novo ZIP for baixado.
6. Opcionalmente, marque **Também ao lado do ZIP** para extrair uma cópia dos
   arquivos na pasta onde o arquivo ZIP está. Se essa pasta já for o destino,
   os arquivos são extraídos apenas uma vez.
7. Use **Nova operação** para adicionar outra linha.

Se houver arquivos existentes nas duas pastas, o aplicativo pergunta
separadamente quais podem ser substituídos em cada uma.

Ao compactar, o conteúdo da pasta é colocado na raiz do ZIP. A pasta de origem
não é incluída como uma pasta extra dentro do arquivo.

Na extração, se o ZIP tiver uma única pasta raiz com o mesmo nome da pasta de
destino, o hen-Zip remove esse nível extra e coloca o conteúdo diretamente no
destino. Em outros casos, preserva a estrutura original do ZIP.

As linhas, os modos escolhidos e os caminhos são guardados no `config.json` do
hen-Zip dentro da pasta de dados do usuário. Você não precisa cadastrá-los de
novo ao reabrir o aplicativo.

## Estrutura

- `_APP_/` — janela e widgets PySide6.
- `_ZIP_/` — compactação, extração segura e execução em thread.
- `_CONFIGURA_/` — textos, cores, atalhos e dimensões da interface.
- `_THREADS_/` — ciclo de vida das threads.
- `_APPDATA_/` — configurações e sessão do aplicativo.
- `_LOGS_/` — registro de erros e operações.
- `nucleo/` — documentação interna do projeto.

## Testes

Os testes de ZIP usam a biblioteca padrão; os testes de persistência da interface
usam o PySide6, incluído em `requirements.txt`:

```bash
python -m unittest discover -s tests
```

## Licença

Adicione aqui a licença escolhida antes de publicar o projeto no GitHub.

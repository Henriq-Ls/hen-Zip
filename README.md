# hen-Zip

Aplicativo desktop em **PySide6** para compactar pastas em arquivos ZIP e extrair
arquivos ZIP e RAR. O hen-Zip permite configurar várias linhas de operação e
escolher individualmente quais arquivos existentes serão substituídos durante
a extração.

## Recursos

- Compacta o conteúdo de uma pasta em um arquivo `.zip`.
- Extrai arquivos `.zip` e `.rar` para a pasta escolhida, sem apagar os demais arquivos.
- O seletor próprio permite filtrar arquivos ZIP ou RAR; as pastas continuam disponíveis para navegação.
- Opcionalmente, extrai cada arquivo também na pasta onde ele está.
- Lista conflitos e deixa selecionar arquivo por arquivo quais serão substituídos.
- Mostra o andamento das operações sem bloquear a interface.
- Permite criar ZIPs com senha e AES-256; a senha digitada para extrair ZIPs protegidos não é salva.
- Permite reordenar operações com as setas e separá-las em grupos com divisórias.
- Permite apagar o arquivo de origem depois de uma extração concluída, sem limpar o caminho salvo.
- Rejeita caminhos absolutos e tentativas de sair da pasta de destino pelo ZIP.
- Mantém logs e preferências de janela na pasta de dados do usuário.
- Salva automaticamente as linhas e restaura os caminhos na próxima abertura.
- Abre o log atual pela própria interface e registra o resumo da extração.

## Requisitos

- Python 3.10 ou superior.
- PySide6.
- pyzipper.
- rarfile.
- cryptography (para ler cabeçalhos RAR protegidos por senha).
- Para extrair RAR, UnRAR, Unar ou bsdtar disponível no `PATH`.

O módulo `zipfile` usado para manipular arquivos ZIP sem senha já faz parte da
biblioteca padrão do Python.

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
2. Informe os caminhos de origem e destino ou use **Procurar**. Na extração,
   escolha o filtro **Arquivos ZIP** ou **Arquivos RAR** no Explorer do hen-Zip.
3. Clique em **Extrair** ou **Zipar**.
4. Ao extrair, marque os arquivos existentes que podem ser substituídos e
   confirme. Os itens desmarcados e os demais arquivos no destino são mantidos.
5. Opcionalmente, marque **Apagar arquivo após extrair** para excluir o ZIP ou
   RAR somente depois que a extração terminar com sucesso. A linha e o caminho ficam
   salvos para reutilizar quando um novo ZIP for baixado.
6. Marque **Ao lado do arquivo** para extrair os arquivos na mesma pasta do ZIP
   ou RAR. Se o destino estiver vazio, essa pasta vira o destino da extração;
   se houver um destino preenchido, o aplicativo também extrai uma cópia ao
   lado do arquivo, preservando a pasta-raiz interna e mesclando nela se já
   existir. **Remover raiz** não altera essa cópia ao lado.
7. **Remover raiz** afeta somente o destino informado: marcado, remove a pasta
   única interna mesmo quando ela tem nome diferente; desmarcado, mantém essa
   pasta. Se os nomes coincidirem, ela é removida automaticamente no destino.
8. Use **Nova operação** para adicionar outra linha.
9. Arraste pelo puxador ou use as setas **↑** e **↓** para mudar a ordem. Use
   **Separador** para inserir uma linha horizontal entre grupos; ela também
   pode ser movida ou removida.
10. As linhas começam recolhidas, mostrando o nome do arquivo sem a extensão.
    Use o botão ao lado das setas de ordem para expandir os campos de origem,
    destino e senha; eles ficam em uma única linha.
11. Use o campo **Senha** para proteger um ZIP ao compactar ou para informar a
    senha de um ZIP/RAR ao extrair. O campo fica mascarado e a senha não é salva
    nas linhas.

Se um RAR tiver cabeçalhos criptografados, o hen-Zip pede a senha antes de listar
seus arquivos. Senha incorreta, RAR inválido e falta de suporte de criptografia
geram avisos diferentes; a mensagem “File is not a zip file”, sozinha, não
confirma que a senha está errada.

O botão **Ajuda** no cabeçalho e a opção **Como usar** no menu **Ajuda** abrem
o guia completo dos campos, das marcações, das substituições e das proteções.
Ao terminar, o aplicativo emite um alerta e mostra a confirmação. Essa janela
não bloqueia o aplicativo e pode ser fechada clicando fora dela.

Se houver arquivos existentes nas duas pastas, o aplicativo pergunta
separadamente quais podem ser substituídos em cada uma.

Ao compactar, o conteúdo da pasta é colocado na raiz do ZIP. A pasta de origem
não é incluída como uma pasta extra dentro do arquivo.

ZIPs criados com senha usam AES-256. Para extraí-los, use um programa compatível,
como 7-Zip ou WinRAR; o extrator padrão do Windows pode não abrir esse formato.
Arquivos RAR podem exigir o executável UnRAR, Unar ou bsdtar instalado e
disponível no `PATH`. O hen-Zip também procura o UnRAR na pasta padrão do
WinRAR no Windows e informa se a ferramenta necessária não estiver disponível.
Cabeçalhos RAR protegidos por senha também precisam do pacote `cryptography`,
incluído em `requirements.txt`.

Na extração, se todo o conteúdo do ZIP estiver dentro de uma única pasta raiz
com nome diferente do destino, a opção **Remover raiz** controla se essa pasta
é removida ou preservada. Se os nomes coincidirem, o hen-Zip remove esse nível
para evitar uma pasta duplicada. ZIPs com mais de um item na raiz mantêm sua
estrutura. Essa regra vale para o destino informado. A cópia feita com
**Ao lado do arquivo** sempre mantém a pasta-raiz interna e grava/mescla os
arquivos dentro dela.

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

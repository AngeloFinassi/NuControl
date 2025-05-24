## NuControl
Um app web feito com Flask que permite que usuários façam upload de extratos bancários para uma visualização dos dados em formato de tabela e vejam gráficos de receitas e despesas categorizadas.

## Funcionalidades
-Registro e login de usuários

-Upload de arquivos de diferentes formatos (csv, xlsx, xls, tsv, json)

-Armazenamento separado por usuário 

-Banco com dados dos usuários e planilhas

-Visualização de dados em tabela

-Dashboard com gráficos sobre a planilha

-Deletar arquivos no sistema

## Formato Esperado da Planilha
A planilha **deve seguir este formato exato**, para que o dasboard funcione adequadamente, pois a interação planilha e backend foi baseada num modelo.

| data       | categoria   | descricao | valor   |
| ---------- | ----------- | --------- | ------- |
| 2025-05-10 | Alimentação | iFood     | -35.90  |
| 2025-05-10 | Salário     | Empresa X | 3000.00 |
| 2025-05-11 | Transporte  | Uber      | -12.50  |

Observações:

Os nomes das colunas devem estar exatamente como mostrado acima (sem acentos).

Os valores negativos representam despesas, e os positivos representam receitas.

**Arquivos diferentes de .csv são lidos e salvos como csv**

## Imagens do Projeto
Tela de Upload:
![image](https://github.com/user-attachments/assets/2c45a314-361b-40ec-88e1-7e0b5e881f10)

Dashboard:
![image](https://github.com/user-attachments/assets/b8dfa355-52d4-4aac-8e1e-e03f4bb137e2)

## Tecnologias Usadas
-Python 3.10+

-Flask

-Flask-Session

-SQLite3

-Pandas / Numpy

-Chart.js

-Jinja2

-HTML/CSS

## Estrutura do Projeto

/project-root
│
├── app.py                # Arquivo principal Flask
├── helpers.py            # Funções auxiliares como leitura de arquivo e categorização
├── db.py                 # Interface com SQLite
├── templates/            # HTML (Jinja2)
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   └── dashboard.html
|   └── ...
├── static/               # CSS
├── users/uploads/user_id # Armazenamento dos arquivos dos usuários
├── databse.db            # banco de dados do projeto
└── README.md             # Este arquivo

## Como Rodar Localmente
Clone o repositório:


`https://github.com/AngeloFinassi/NuControl`
`cd NuControl`

Instale as dependências (use um virtualenv se quiser):
``

`pip install -r requirements.txt`

Inicie o servidor (local do próprio Flask):
`python app.py`

Acesse o app em: http://127.0.0.1:5000

## Requisitos
-Python 3.10+

-Navegador

-Planilha no formato correto!

## Segurança
As senhas são salvas com hash (generate_password_hash).

Uploads são organizados por usuário e salvos com nomes seguros.

Apenas usuários autenticados podem visualizar seus arquivos e dashboard.

Não há SQLinjection nos inputs da aplicação web, todos os Querys são formatados seguindo padrões de segurança.

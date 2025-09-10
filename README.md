# Austay API

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/release/python-390/)

API desenvolvida em FastAPI para a gestão de tutores, pets e estadias do sistema Austay.

## 📜 Estrutura do Projeto - Arquitetura em Camadas (Layered Architecture)

O projeto é organizado para separar as responsabilidades, facilitando a manutenção e o desenvolvimento de novas funcionalidades. 

```
/
├── app/                  # Contém todo o código fonte da aplicação.
│   ├── controllers/      # Define os endpoints da API (rotas).
│   │   ├── auth_controller.py
│   │   ├── tutor_controller.py
│   │   └── user_controller.py
│   ├── models/           # Define os modelos de tabelas do SQLAlchemy.
│   │   ├── pet.py
│   │   ├── tutor.py
│   │   └── user.py
│   ├── schemas/          # Define os schemas Pydantic (validação de dados).
│   │   ├── token.py
│   │   ├── tutor.py
│   │   └── user.py
│   └── templates/        # Módulos de templates de corpo de e-mail's.
│       └── password_reset.html
│   └── utils/            # Módulos utilitários (segurança, dependências, etc.).
│       └── dependencies.py
│       └── security.py
│       └── email_sender.py
│   ├── config.py
│   ├── database.py
│   └── main.py           # Ponto de entrada da aplicação FastAPI.
├── migrations/           # Arquivos de migração gerados pelo Alembic.
│   └── versions/
│   └── env.py
│   └── script.py.mako
├── alembic.ini           # Configuração do Alembic para migrações.
```

## 🚀 Como Configurar e Rodar o Projeto

Configurar o ambiente de desenvolvimento do zero.

### Pré-requisitos
* **Python 3.9 ou superior**
* **Git**
* **PostgreSQL** instalado e rodando na sua máquina.

### Passo a Passo

1.  **Clone o Repositório**
    ```bash
    git clone https://github.com/felipeerocha/austay-backend.git
    cd austay-backend
    ```

2.  **Crie e Ative o Ambiente Virtual (`venv`)**
    Isso cria um ambiente Python isolado para o projeto, evitando conflitos de pacotes.
    ```bash
    # Cria o ambiente virtual
    python3 -m venv venv

    # Ativa o ambiente (Mac/Linux)
    source venv/bin/activate  

    # Ativa o ambiente (Windows)
    .\venv\Scripts\Activate.ps1
    ```
    *O terminal agora deve mostrar `(venv)` no início da linha.*

3.  **Instale as Dependências do Projeto**
    O arquivo `requirements.txt` contém a lista de todos os pacotes Python necessários. Este comando instala todos eles de uma vez.
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure o Banco de Dados**
    - Abra seu cliente PostgreSQL (pgAdmin, DBeaver, etc.).
    - Crie um novo banco de dados para este projeto (ex: `austay_db`).

5.  **Configure as Variáveis de Ambiente (Passo Crucial)**
    As senhas e configurações locais são guardadas em um arquivo `.env`, que não existe no repositório por segurança. Nós usamos um arquivo de exemplo (`.env.example`) como base.

    - **Copie o arquivo de exemplo** para criar seu arquivo de configuração local:
      ```bash
      cp .env.example .env
      ```
    - **Abra o novo arquivo `.env`** com seu editor de texto.
    - **Edite os valores** para que correspondam à sua configuração local do banco de dados (usuário, senha, nome do banco que você criou no passo 4).

6.  **Execute as Migrações do Banco de Dados**
    Com a conexão do banco configurada no `.env`, este comando criará todas as tabelas necessárias.
    ```bash
    alembic upgrade head
    ```

7.  **Rode a Aplicação!**
    Finalmente, inicie o servidor de desenvolvimento.
    ```bash
    uvicorn app.main:app --reload
    ```
    A API estará rodando e acessível em `http://127.0.0.1:8000`.

## 📚 Uso da API

Para explorar e testar todos os endpoints, acesse a documentação interativa gerada automaticamente:

* **Documentação Swagger:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

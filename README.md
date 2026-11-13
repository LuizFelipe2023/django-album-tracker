# 🎸 Rock Album Collection API

API RESTful desenvolvida com **Django** e **Django REST Framework (DRF)** para gerenciamento pessoal de coleções de discos e álbuns de rock. O sistema conta com autenticação via **JWT (JSON Web Tokens)**, rotação e blacklist de tokens para logout seguro, e isolamento rigoroso de dados por usuário.

## 🚀 Funcionalidades

- **Autenticação Segura via E-mail**: Modelo de usuário customizado utilizando `email` como identificador principal de login.
- **JWT & Token Blacklist**: Login, renovação de tokens (*Refresh Token Rotation*) e invalidação imediata no logout.
- **Isolamento de Dados**: Cada colecionador visualiza, edita e gerencia exclusivamente os itens da sua própria coleção (`CollectionItem`).
- **Catálogo Estruturado**: Organização completa de **Gêneros** (`Genre`), **Artistas/Bandas** (`Artist`), **Álbuns** (`Album`) e **Itens da Coleção** (`CollectionItem`).

## ⚙️ Instalação e Configuração Local

```bash
# 1. Crie e ative o ambiente virtual
python -m venv env
# Windows: .\env\Scripts\Activate.ps1
# Linux/Mac: source env/bin/activate

# 2. Instale as dependências
pip install -r requirements.txt

# 3. Execute as migrações
cd collection_albums
python manage.py makemigrations
python manage.py migrate

# 4. Inicie o servidor
python manage.py runserver
```

## 📌 Endpoints Principais

- `POST /api/register/` - Cadastro de novo usuário
- `POST /api/token/` - Login (retorna `access` e `refresh`)
- `POST /api/token/refresh/` - Renova o par de tokens
- `POST /api/logout/` - Invalida o `refresh` token na blacklist
- `GET, POST /api/genres/` - Gêneros musicais
- `GET, POST /api/artists/` - Artistas e bandas
- `GET, POST /api/albums/` - Álbuns
- `GET, POST /api/collection/` - Coleção privada do usuário autenticado

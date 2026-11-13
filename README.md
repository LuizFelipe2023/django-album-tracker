# 🎸 Rock Album Collection API

API RESTful desenvolvida com **Django** e **Django REST Framework (DRF)** para gerenciamento pessoal de coleções de discos e álbuns de rock. O sistema conta com autenticação via **JWT (JSON Web Tokens)**, rotação e blacklist de tokens para logout seguro, e isolamento rigoroso de dados por usuário.

---

## 🚀 Funcionalidades

* **Autenticação Segura via E-mail**: Modelo de usuário customizado utilizando `email` como identificador principal de login.
* **JWT & Token Blacklist**: Login, rotação de tokens (*Refresh Token Rotation*) e invalidação imediata no logout.
* **Isolamento de Dados**: Cada colecionador visualiza, edita e gerencia exclusivamente os itens da sua própria coleção (`CollectionItem`).
* **Catálogo Estruturado**: Organização completa de **Gêneros** (`Genre`), **Artistas/Bandas** (`Artist`), **Álbuns** (`Album`) e **Itens da Coleção** (`CollectionItem`).

---

## ⚙️ Instalação e Configuração Local

Siga os passos abaixo para configurar e rodar o projeto em sua máquina:

### 1. Clonar e acessar o projeto
```bash
git clone https://github.com/seu-usuario/rock-album-api.git
cd albumtracker
```

### 2. Criar e ativar o ambiente virtual
* **Windows (PowerShell):**
  ```powershell
  python -m venv env
  .\env\Scripts\Activate.ps1
  ```
* **Linux / macOS:**
  ```bash
  python3 -m venv env
  source env/bin/activate
  ```

### 3. Instalar as dependências
```bash
pip install -r requirements.txt
```

### 4. Executar as migrações do banco de dados
```bash
cd collection_albums
python manage.py makemigrations
python manage.py migrate
```

### 5. Iniciar o servidor de desenvolvimento
```bash
python manage.py runserver
```
A API estará acessível em `http://localhost:8000/`.

---

## 📌 Endpoints e Exemplos de Uso

Abaixo estão descritos os principais endpoints da API junto com exemplos práticos de requisição via JSON.

### 1. 🔐 Autenticação e Usuários

#### * Registrar Novo Usuário
* **Método:** `POST`
* **Endpoint:** `/api/register/`
* **Acesso:** Público (`AllowAny`)
* **Payload (JSON):**
  ```json
  {
      "email": "colecionador@rock.com",
      "first_name": "Luiz",
      "last_name": "Neves",
      "password": "sua-senha-segura"
  }
  ```

#### * Fazer Login (Obter Tokens)
* **Método:** `POST`
* **Endpoint:** `/api/token/`
* **Acesso:** Público
* **Payload (JSON):**
  ```json
  {
      "email": "colecionador@rock.com",
      "password": "sua-senha-segura"
  }
  ```
> **Nota de Uso:** A resposta trará um `access` token e um `refresh` token. Para acessar as rotas protegidas, envie o cabeçalho HTTP: `Authorization: Bearer <seu_access_token>`.

#### * Renovar Token de Acesso
* **Método:** `POST`
* **Endpoint:** `/api/token/refresh/`
* **Acesso:** Público
* **Payload (JSON):**
  ```json
  {
      "refresh": "seu_refresh_token_aqui"
  }
  ```

#### * Logout (Inativar Token)
* **Método:** `POST`
* **Endpoint:** `/api/logout/`
* **Acesso:** Requer autenticação (`Bearer Token`)
* **Payload (JSON):**
  ```json
  {
      "refresh": "seu_refresh_token_aqui"
  }
  ```

---

### 2. 🎸 Catálogo (Gêneros, Artistas e Álbuns)
*(Todas as rotas abaixo exigem o header de autenticação `Authorization: Bearer <access_token>`)*

#### * Cadastrar Gênero Musical
* **Método:** `POST`
* **Endpoint:** `/api/genres/`
* **Payload (JSON):**
  ```json
  {
      "name": "Heavy Metal",
      "description": "Gênero musical originado no final dos anos 60 e início dos anos 70."
  }
  ```

#### * Cadastrar Artista / Banda
* **Método:** `POST`
* **Endpoint:** `/api/artists/`
* **Payload (JSON):**
  ```json
  {
      "name": "Iron Maiden",
      "country": "Reino Unido",
      "formed_year": 1975
  }
  ```

#### * Cadastrar Álbum
* **Método:** `POST`
* **Endpoint:** `/api/albums/`
* **Payload (JSON):**
  ```json
  {
      "title": "The Number of the Beast",
      "artist": 1,
      "genre": 1,
      "release_year": 1982,
      "cover_url": "https://exemplo.com/capa.jpg"
  }
  ```

---

### 3. 💿 Gerenciamento da Coleção Pessoal
*(Cada usuário gerencia exclusivamente os discos da sua própria estante digital)*

#### * Adicionar Item à Coleção
* **Método:** `POST`
* **Endpoint:** `/api/collection/`
* **Payload (JSON):**
  ```json
  {
      "album": 1,
      "format": "VINYL_12",
      "condition": "NM",
      "notes": "Edição original de época, excelente estado de conservação."
  }
  ```
* **Opções de Formato (`format`):** 
  * `VINYL_12` (Vinil 12" LP)
  * `VINYL_7` (Vinil 7" Compacto)
  * `CD` (CD)
  * `CASSETTE` (Fita K7)
  * `DIGITAL` (Digital / Streaming)

* **Opções de Condição (`condition`):** 
  * `M` (Mint - Perfeito, lacrado)
  * `NM` (Near Mint - Como novo)
  * `VG` (Very Good - Marcas leves de uso)
  * `G` (Good - Desgastado)

#### * Listar / Consultar a Sua Coleção
* **Método:** `GET`
* **Endpoint:** `/api/collection/`
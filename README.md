# Sistema de Gerenciamento de Biblioteca

Sistema completo para gerenciamento de bibliotecas com controle de acervo, membros e empréstimos. Desenvolvido com Python Flask e JavaScript.

## Tecnologias Utilizadas

### Backend
- **Python 3.8+** 
- **Flask** 
- **Flask-SQLAlchemy** 
- **Flask-CORS** 
- **Marshmallow** 
- **SQLite** 
- **pytest** 

### Frontend
- **HTML5** 
- **CSS3** 
- **JavaScript**
- **Fetch API**

## Arquitetura

O projeto segue o padrão **MVC** com **Factory Pattern**:


### Princípios Aplicados

- **MVC Pattern** - Separação de responsabilidades
- **Application Factory** - Configuração flexível
- **Blueprint Pattern** - Modularização de rotas
- **Repository Pattern** - Abstração de dados
- **RESTful API** - Design de endpoints padronizado
- **DRY** - Reutilização de código
- **Validation Layer** - Validação robusta com Marshmallow

## Como Executar

### Instalação

1. **Clone o repositório**
```bash
cd <repositorio>
```

2. **Crie um ambiente virtual**
```bash
python -m venv venv

# Linux/Mac
source venv/bin/activate

# Windows
venv\Scripts\activate
```

3. **Instale as dependências**
```bash
pip install -r requirements.txt
```

4. **Configure as variáveis de ambiente** (opcional)
```bash
cp .env.example .env
# Edite .env conforme necessário
```

5. **Inicialize o banco de dados**
```bash
flask init-db
```

6. **Popule com dados de exemplo** (opcional)
```bash
flask seed-db
```

7. **Inicie o servidor**
```bash
python run.py
```

O servidor estará rodando em `http://localhost:3002`

8. **Abra o frontend**

Abra o arquivo `frontend/index.html` no navegador ou use um servidor local:

```bash
cd frontend
python -m http.server 8000
```

Acesse `http://localhost:8000`

## API Endpoints

### Base URL: `http://localhost:3002/api`

#### Livros

```http
GET    /books              # Listar todos os livros
GET    /books/:id          # Buscar livro por ID
POST   /books              # Criar novo livro
PUT    /books/:id          # Atualizar livro
DELETE /books/:id          # Remover livro
GET    /books/search?q=... # Buscar livros
```

**Exemplo - Criar livro:**
```json
POST /api/books
{
  "title": "Clean Code",
  "author": "Robert C. Martin",
  "isbn": "978-0132350884",
  "publisher": "Prentice Hall",
  "year": 2008,
  "category": "Programming",
  "quantity": 3
}
```

#### Membros

```http
GET    /members           # Listar todos os membros
GET    /members/:id       # Buscar membro por ID
POST   /members           # Criar novo membro
PUT    /members/:id       # Atualizar membro
DELETE /members/:id       # Remover membro
GET    /members/:id/loans # Empréstimos do membro
```

#### Empréstimos

```http
GET    /loans             # Listar todos os empréstimos
GET    /loans/:id         # Buscar empréstimo por ID
POST   /loans             # Criar novo empréstimo
POST   /loans/:id/return  # Registrar devolução
GET    /loans/active      # Empréstimos ativos
GET    /loans/overdue     # Empréstimos atrasados
```

**Exemplo - Criar empréstimo:**
```json
POST /api/loans
{
  "book_id": 1,
  "member_id": 2
}
```

#### Dashboard

```http
GET /dashboard/stats           # Estatísticas gerais
GET /dashboard/recent-activity # Atividades recentes
```

## Testes

### Executar testes
```bash
pytest
```

### Executar testes com coverage
```bash
pytest --cov=app --cov-report=html
```

### Executar testes específicos
```bash
pytest tests/test_books.py
```

## Boas Práticas Implementadas

### Backend
-  Application Factory Pattern
-  Blueprint para modularização
-  SQLAlchemy ORM
-  Validação com Marshmallow
-  Tratamento de erros padronizado
-  Respostas JSON consistentes
-  Relacionamentos de banco de dados
-  Cascade deletes
-  Testes automatizados com pytest
-  Fixtures de teste

### Frontend
-  JavaScript modular (sem frameworks)
-  Separação de responsabilidades
-  Cliente API centralizado
-  Tratamento de erros
-  Feedback visual (toasts)
-  Loading states
-  Modais reutilizáveis
-  Design responsivo
-  CSS puro sem dependências

## Diferenciais do Projeto

### 1. Python Flask 
desenvolvimento backend tradicional.

### 2. JavaScript 
Frontend sem frameworks, domínio de JavaScript puro.

### 3. ORM SQLAlchemy
ORM com relacionamentos e validações.

### 4. Sistema Inteligente
- Cálculo automático de disponibilidade
- Detecção de empréstimos atrasados
- Proteção de integridade referencial

### 5. Interface Rica
Dashboard com estatísticas, busca, filtros e formulários dinâmicos.

### 6. Testes Automatizados
Suite completa de testes com pytest e fixtures.

## Melhorias Futuras

- [ ] Autenticação e autorização (JWT)
- [ ] Reservas de livros
- [ ] Notificações por email
- [ ] Upload de capas de livros
- [ ] Código de barras para ISBN

## Autor
 Thiago Rocha
Desenvolvido como projeto de portfólio demonstrando conhecimentos em desenvolvimento full stack com Python/JS.



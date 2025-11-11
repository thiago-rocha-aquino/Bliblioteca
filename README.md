# Sistema de Gerenciamento de Biblioteca

Sistema completo para gerenciamento de bibliotecas com controle de acervo, membros e empréstimos. Desenvolvido com Python Flask e JavaScript vanilla.

## Tecnologias Utilizadas

### Backend
- **Python 3.8+** - Linguagem de programação
- **Flask** - Framework web minimalista
- **Flask-SQLAlchemy** - ORM para banco de dados
- **Flask-CORS** - Suporte a CORS
- **Marshmallow** - Validação e serialização
- **SQLite** - Banco de dados relacional
- **pytest** - Framework de testes

### Frontend
- **HTML5** - Estrutura semântica
- **CSS3** - Estilização moderna
- **JavaScript (ES6+)** - Lógica e interatividade
- **Fetch API** - Requisições HTTP

## Funcionalidades

### Gerenciamento de Livros
- ✅ Cadastro completo (título, autor, ISBN, editora, ano, categoria)
- ✅ Controle de quantidade e disponibilidade
- ✅ Busca por título, autor ou categoria
- ✅ Edição e remoção de livros
- ✅ Validação de ISBN único

### Gerenciamento de Membros
- ✅ Cadastro de membros (nome, email, telefone, endereço)
- ✅ Status ativo/inativo
- ✅ Validação de email único
- ✅ Histórico de empréstimos
- ✅ Proteção contra remoção com empréstimos ativos

### Sistema de Empréstimos
- ✅ Registro de empréstimos
- ✅ Controle de prazos (14 dias padrão)
- ✅ Identificação de empréstimos atrasados
- ✅ Registro de devoluções
- ✅ Atualização automática de disponibilidade
- ✅ Filtros (todos, ativos, atrasados)

### Dashboard
- ✅ Estatísticas em tempo real
- ✅ Contador de livros, membros e empréstimos
- ✅ Alerta de empréstimos atrasados
- ✅ Atividades recentes
- ✅ Categorias mais populares

## Arquitetura

O projeto segue o padrão **MVC (Model-View-Controller)** com **Application Factory Pattern**:

```
library-management-system/
├── app/
│   ├── __init__.py          # Application Factory
│   ├── models/              # Models (SQLAlchemy)
│   │   ├── book.py
│   │   ├── member.py
│   │   └── loan.py
│   ├── routes/              # Controllers (Blueprints)
│   │   ├── books.py
│   │   ├── members.py
│   │   ├── loans.py
│   │   └── dashboard.py
│   ├── schemas.py           # Validação (Marshmallow)
│   └── utils.py             # Funções utilitárias
├── frontend/                # Interface do usuário
│   ├── index.html
│   ├── css/
│   │   └── style.css
│   └── js/
│       ├── api.js          # Cliente HTTP
│       ├── utils.js        # Utilidades
│       ├── dashboard.js    # Dashboard
│       ├── books.js        # Livros
│       ├── members.js      # Membros
│       ├── loans.js        # Empréstimos
│       └── app.js          # App principal
├── tests/                   # Testes automatizados
├── config.py               # Configurações
└── run.py                  # Ponto de entrada
```

### Princípios Aplicados

- **MVC Pattern** - Separação de responsabilidades
- **Application Factory** - Configuração flexível
- **Blueprint Pattern** - Modularização de rotas
- **Repository Pattern** - Abstração de dados
- **RESTful API** - Design de endpoints padronizado
- **DRY** - Reutilização de código
- **Validation Layer** - Validação robusta com Marshmallow

## Como Executar

### Pré-requisitos
- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

### Instalação

1. **Clone o repositório**
```bash
cd library-management-system
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

## Estrutura do Banco de Dados

### Tabela: books

| Campo      | Tipo    | Descrição               |
|------------|---------|-------------------------|
| id         | INTEGER | Chave primária          |
| title      | STRING  | Título do livro         |
| author     | STRING  | Autor                   |
| isbn       | STRING  | ISBN (único)            |
| publisher  | STRING  | Editora                 |
| year       | INTEGER | Ano de publicação       |
| category   | STRING  | Categoria               |
| quantity   | INTEGER | Quantidade total        |
| available  | INTEGER | Quantidade disponível   |
| created_at | DATETIME| Data de criação         |
| updated_at | DATETIME| Data de atualização     |

### Tabela: members

| Campo      | Tipo    | Descrição               |
|------------|---------|-------------------------|
| id         | INTEGER | Chave primária          |
| name       | STRING  | Nome completo           |
| email      | STRING  | Email (único)           |
| phone      | STRING  | Telefone                |
| address    | STRING  | Endereço                |
| active     | BOOLEAN | Status                  |
| created_at | DATETIME| Data de criação         |
| updated_at | DATETIME| Data de atualização     |

### Tabela: loans

| Campo       | Tipo    | Descrição                |
|-------------|---------|--------------------------|
| id          | INTEGER | Chave primária           |
| book_id     | INTEGER | FK para books            |
| member_id   | INTEGER | FK para members          |
| loan_date   | DATETIME| Data do empréstimo       |
| due_date    | DATETIME| Data de devolução        |
| return_date | DATETIME| Data devolvido (null)    |
| status      | STRING  | active/returned/overdue  |
| created_at  | DATETIME| Data de criação          |
| updated_at  | DATETIME| Data de atualização      |

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
- ✅ Application Factory Pattern
- ✅ Blueprint para modularização
- ✅ SQLAlchemy ORM
- ✅ Validação com Marshmallow
- ✅ Tratamento de erros padronizado
- ✅ Respostas JSON consistentes
- ✅ Relacionamentos de banco de dados
- ✅ Cascade deletes
- ✅ Testes automatizados com pytest
- ✅ Fixtures de teste

### Frontend
- ✅ JavaScript modular (sem frameworks)
- ✅ Separação de responsabilidades
- ✅ Cliente API centralizado
- ✅ Tratamento de erros
- ✅ Feedback visual (toasts)
- ✅ Loading states
- ✅ Modais reutilizáveis
- ✅ Design responsivo
- ✅ CSS puro sem dependências

## Diferenciais do Projeto

### 1. Python Flask sem TypeScript
Demonstra proficiência em Python e desenvolvimento backend tradicional.

### 2. JavaScript Vanilla
Frontend sem frameworks React/Vue, mostrando domínio de JavaScript puro.

### 3. ORM SQLAlchemy
Uso profissional de ORM com relacionamentos e validações.

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
- [ ] Multas por atraso
- [ ] Reservas de livros
- [ ] Notificações por email
- [ ] Relatórios em PDF
- [ ] Gráficos e analytics
- [ ] Upload de capas de livros
- [ ] Código de barras para ISBN
- [ ] API GraphQL
- [ ] Deploy em produção (Heroku/AWS)

## Demonstração de Conhecimentos

Este projeto demonstra:

- 🐍 **Python** - Sintaxe, decorators, list comprehensions
- 🌐 **Flask** - Routes, blueprints, app factory, extensions
- 🗄️ **SQLAlchemy** - Models, relationships, queries, migrations
- ✅ **Marshmallow** - Schemas, validation, serialization
- 🧪 **pytest** - Unit tests, fixtures, test client
- 🎨 **HTML/CSS** - Semântica, flexbox, grid, animações
- ⚡ **JavaScript** - ES6+, async/await, fetch API, DOM manipulation
- 🏗️ **Arquitetura** - MVC, separation of concerns, modularização
- 📊 **Banco de Dados** - Modelagem, relacionamentos, constraints
- 🔒 **Validações** - Server-side e client-side

## Autor

Desenvolvido como projeto de portfólio demonstrando conhecimentos em desenvolvimento full stack com Python.

## Licença

MIT License - Livre para uso em projetos pessoais e comerciais.

"""
Ponto de entrada da aplicação Flask
"""
from app import create_app, db
from app.models import Book, Member, Loan

app = create_app()

@app.shell_context_processor
def make_shell_context():
    """Configuração do shell context para facilitar debugging"""
    return {
        'db': db,
        'Book': Book,
        'Member': Member,
        'Loan': Loan
    }

@app.cli.command()
def init_db():
    """Inicializa o banco de dados"""
    db.create_all()
    print('✓ Database initialized successfully!')

@app.cli.command()
def seed_db():
    """Popula o banco com dados de exemplo"""
    from datetime import datetime, timedelta

    # Criar alguns livros
    books = [
        Book(
            title='Clean Code',
            author='Robert C. Martin',
            isbn='978-0132350884',
            publisher='Prentice Hall',
            year=2008,
            category='Programming',
            quantity=3
        ),
        Book(
            title='The Pragmatic Programmer',
            author='Andrew Hunt',
            isbn='978-0201616224',
            publisher='Addison-Wesley',
            year=1999,
            category='Programming',
            quantity=2
        ),
        Book(
            title='Design Patterns',
            author='Gang of Four',
            isbn='978-0201633610',
            publisher='Addison-Wesley',
            year=1994,
            category='Software Engineering',
            quantity=2
        ),
    ]

    # Criar alguns membros
    members = [
        Member(
            name='João Silva',
            email='joao@example.com',
            phone='(11) 98765-4321',
            address='Rua A, 123'
        ),
        Member(
            name='Maria Santos',
            email='maria@example.com',
            phone='(11) 91234-5678',
            address='Av. B, 456'
        ),
    ]

    db.session.add_all(books + members)
    db.session.commit()

    print('✓ Database seeded with sample data!')

if __name__ == '__main__':
    app.run(debug=True, port=3002)

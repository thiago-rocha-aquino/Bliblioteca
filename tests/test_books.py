"""
Testes para rotas de livros
"""
import pytest
from app import create_app, db
from app.models import Book
from config import TestConfig

@pytest.fixture
def app():
    app = create_app(TestConfig)
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def sample_book(app):
    book = Book(
        title='Test Book',
        author='Test Author',
        isbn='1234567890',
        publisher='Test Publisher',
        year=2020,
        category='Test',
        quantity=5
    )
    db.session.add(book)
    db.session.commit()
    return book

def test_get_books_empty(client):
    response = client.get('/api/books')
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
    assert len(data['data']) == 0

def test_create_book(client):
    book_data = {
        'title': 'New Book',
        'author': 'New Author',
        'isbn': '9876543210',
        'year': 2023,
        'quantity': 3
    }

    response = client.post('/api/books', json=book_data)
    assert response.status_code == 201
    data = response.get_json()
    assert data['success'] is True
    assert data['data']['title'] == 'New Book'
    assert data['data']['available'] == 3

def test_get_book_by_id(client, sample_book):
    response = client.get(f'/api/books/{sample_book.id}')
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
    assert data['data']['title'] == 'Test Book'

def test_get_nonexistent_book(client):
    response = client.get('/api/books/999')
    assert response.status_code == 404

def test_update_book(client, sample_book):
    update_data = {'title': 'Updated Book'}

    response = client.put(f'/api/books/{sample_book.id}', json=update_data)
    assert response.status_code == 200
    data = response.get_json()
    assert data['data']['title'] == 'Updated Book'

def test_delete_book(client, sample_book):
    response = client.delete(f'/api/books/{sample_book.id}')
    assert response.status_code == 200

    # Verificar se foi removido
    response = client.get(f'/api/books/{sample_book.id}')
    assert response.status_code == 404

def test_duplicate_isbn(client, sample_book):
    book_data = {
        'title': 'Another Book',
        'author': 'Another Author',
        'isbn': sample_book.isbn,  # ISBN duplicado
        'quantity': 1
    }

    response = client.post('/api/books', json=book_data)
    assert response.status_code == 409

def test_search_books(client, sample_book):
    response = client.get('/api/books/search?q=Test')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data['data']) > 0
    assert data['data'][0]['title'] == 'Test Book'

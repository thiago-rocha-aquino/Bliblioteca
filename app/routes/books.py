"""
Rotas para gerenciamento de livros
"""
from flask import Blueprint, request
from app import db
from app.models import Book
from app.schemas import BookSchema
from app.utils import success_response, error_response

bp = Blueprint('books', __name__, url_prefix='/api/books')
book_schema = BookSchema()
books_schema = BookSchema(many=True)

@bp.route('', methods=['GET'])#listar todos os livros
def get_books():
    books = Book.query.all()
    return success_response([book.to_dict() for book in books])

@bp.route('/<int:book_id>', methods=['GET']) # listar um livro por id
def get_book(book_id):
    book = Book.query.get(book_id)
    if not book:
        return error_response('Livro não encontrado', 404)
    return success_response(book.to_dict())

@bp.route('', methods=['POST'])# criar um novo livro
def create_book():
    try:
        data = book_schema.load(request.get_json())
    except Exception as e:
        return error_response('Erro de validação', 400, str(e))

    # Verificar se ISBN já existe
    existing_book = Book.query.filter_by(isbn=data['isbn']).first()
    if existing_book:
        return error_response('ISBN já cadastrado', 409)

    book = Book(**data)
    book.available = data.get('quantity', 1)

    db.session.add(book)
    db.session.commit()

    return success_response(book.to_dict(), 'Livro cadastrado com sucesso', 201)

@bp.route('/<int:book_id>', methods=['PUT']) # atualizar um livro
def update_book(book_id):
    book = Book.query.get(book_id)
    if not book:
        return error_response('Livro não encontrado', 404)

    try:
        data = book_schema.load(request.get_json(), partial=True)
    except Exception as e:
        return error_response('Erro de validação', 400, str(e))

    # Se estiver atualizando ISBN, verificar duplicidade
    if 'isbn' in data and data['isbn'] != book.isbn:
        existing = Book.query.filter_by(isbn=data['isbn']).first()
        if existing:
            return error_response('ISBN já cadastrado', 409)

    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at', 'available']:
            setattr(book, key, value)

    db.session.commit()
    return success_response(book.to_dict(), 'Livro atualizado com sucesso')

@bp.route('/<int:book_id>', methods=['DELETE'])# remover um livro
def delete_book(book_id):
    book = Book.query.get(book_id)
    if not book:
        return error_response('Livro não encontrado', 404)

    # Verificar se tem empréstimos ativos
    from app.models import Loan
    active_loans = Loan.query.filter_by(book_id=book_id, status='active').count()
    if active_loans > 0:
        return error_response('Não é possível remover livro com empréstimos ativos', 400)

    db.session.delete(book)
    db.session.commit()

    return success_response(message='Livro removido com sucesso')

@bp.route('/search', methods=['GET']) # buscar livros por título, autor ou categoria
def search_books():
    query = request.args.get('q', '')

    books = Book.query.filter(
        db.or_(
            Book.title.ilike(f'%{query}%'),
            Book.author.ilike(f'%{query}%'),
            Book.category.ilike(f'%{query}%')
        )
    ).all()

    return success_response([book.to_dict() for book in books])

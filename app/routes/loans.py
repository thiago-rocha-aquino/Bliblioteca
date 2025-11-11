"""
Rotas para gerenciamento de empréstimos
"""
from flask import Blueprint, request
from datetime import datetime
from app import db
from app.models import Loan, Book, Member
from app.schemas import LoanSchema
from app.utils import success_response, error_response

bp = Blueprint('loans', __name__, url_prefix='/api/loans')
loan_schema = LoanSchema()
loans_schema = LoanSchema(many=True)

@bp.route('', methods=['GET'])
def get_loans():
    loans = Loan.query.all()
    return success_response([loan.to_dict() for loan in loans])

@bp.route('/<int:loan_id>', methods=['GET'])
def get_loan(loan_id):
    loan = Loan.query.get(loan_id)
    if not loan:
        return error_response('Empréstimo não encontrado', 404)
    return success_response(loan.to_dict())

@bp.route('', methods=['POST'])
def create_loan():
    try:
        data = loan_schema.load(request.get_json())
    except Exception as e:
        return error_response('Erro de validação', 400, str(e))

    # Verificar se livro existe
    book = Book.query.get(data['book_id'])
    if not book:
        return error_response('Livro não encontrado', 404)

    # Verificar se membro existe
    member = Member.query.get(data['member_id'])
    if not member:
        return error_response('Membro não encontrado', 404)

    # Verificar se membro está ativo
    if not member.active:
        return error_response('Membro inativo não pode fazer empréstimos', 400)

    # Verificar disponibilidade do livro
    if book.available <= 0:
        return error_response('Livro indisponível no momento', 400)

    # Criar empréstimo
    loan = Loan(**data)
    book.available -= 1

    db.session.add(loan)
    db.session.commit()

    return success_response(loan.to_dict(), 'Empréstimo registrado com sucesso', 201)

@bp.route('/<int:loan_id>/return', methods=['POST'])
def return_loan(loan_id):
    loan = Loan.query.get(loan_id)
    if not loan:
        return error_response('Empréstimo não encontrado', 404)

    if loan.status == 'returned':
        return error_response('Empréstimo já foi devolvido', 400)

    # Atualizar empréstimo
    loan.return_date = datetime.utcnow()
    loan.status = 'returned'

    # Aumentar disponibilidade do livro
    book = Book.query.get(loan.book_id)
    book.available += 1

    db.session.commit()

    return success_response(loan.to_dict(), 'Devolução registrada com sucesso')

@bp.route('/active', methods=['GET'])
def get_active_loans():
    loans = Loan.query.filter_by(status='active').all()
    return success_response([loan.to_dict() for loan in loans])

@bp.route('/overdue', methods=['GET'])
def get_overdue_loans():
    loans = Loan.query.filter(
        Loan.status == 'active',
        Loan.due_date < datetime.utcnow()
    ).all()
    return success_response([loan.to_dict() for loan in loans])

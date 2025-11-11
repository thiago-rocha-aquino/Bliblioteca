"""
Rotas para gerenciamento de membros
"""
from flask import Blueprint, request
from app import db
from app.models import Member
from app.schemas import MemberSchema
from app.utils import success_response, error_response

bp = Blueprint('members', __name__, url_prefix='/api/members')
member_schema = MemberSchema()
members_schema = MemberSchema(many=True)

@bp.route('', methods=['GET'])
def get_members():
    members = Member.query.all()
    return success_response([member.to_dict() for member in members])

@bp.route('/<int:member_id>', methods=['GET'])
def get_member(member_id):
    member = Member.query.get(member_id)
    if not member:
        return error_response('Membro não encontrado', 404)
    return success_response(member.to_dict())

@bp.route('', methods=['POST'])
def create_member():
    try:
        data = member_schema.load(request.get_json())
    except Exception as e:
        return error_response('Erro de validação', 400, str(e))

    # Verificar se email já existe
    existing = Member.query.filter_by(email=data['email']).first()
    if existing:
        return error_response('Email já cadastrado', 409)

    member = Member(**data)
    db.session.add(member)
    db.session.commit()

    return success_response(member.to_dict(), 'Membro cadastrado com sucesso', 201)

@bp.route('/<int:member_id>', methods=['PUT'])
def update_member(member_id):
    """Atualiza um membro"""
    member = Member.query.get(member_id)
    if not member:
        return error_response('Membro não encontrado', 404)

    try:
        data = member_schema.load(request.get_json(), partial=True)
    except Exception as e:
        return error_response('Erro de validação', 400, str(e))

    # Se estiver atualizando email, verificar duplicidade
    if 'email' in data and data['email'] != member.email:
        existing = Member.query.filter_by(email=data['email']).first()
        if existing:
            return error_response('Email já cadastrado', 409)

    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(member, key, value)

    db.session.commit()
    return success_response(member.to_dict(), 'Membro atualizado com sucesso')

@bp.route('/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):
    member = Member.query.get(member_id)
    if not member:
        return error_response('Membro não encontrado', 404)

    # Verificar se tem empréstimos ativos
    from app.models import Loan
    active_loans = Loan.query.filter_by(member_id=member_id, status='active').count()
    if active_loans > 0:
        return error_response('Não é possível remover membro com empréstimos ativos', 400)

    db.session.delete(member)
    db.session.commit()

    return success_response(message='Membro removido com sucesso')

@bp.route('/<int:member_id>/loans', methods=['GET'])
def get_member_loans(member_id):
    member = Member.query.get(member_id)
    if not member:
        return error_response('Membro não encontrado', 404)

    from app.models import Loan
    loans = Loan.query.filter_by(member_id=member_id).all()
    return success_response([loan.to_dict() for loan in loans])

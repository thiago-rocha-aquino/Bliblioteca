"""
Rotas para dashboard e estatísticas
"""
from flask import Blueprint
from datetime import datetime
from app import db
from app.models import Book, Member, Loan
from app.utils import success_response

bp = Blueprint('dashboard', __name__, url_prefix='/api/dashboard')

@bp.route('/stats', methods=['GET'])
def get_stats():

    # Contadores básicos
    total_books = Book.query.count()
    total_members = Member.query.count()
    active_members = Member.query.filter_by(active=True).count()

    # Estatísticas de livros
    total_copies = db.session.query(db.func.sum(Book.quantity)).scalar() or 0
    available_copies = db.session.query(db.func.sum(Book.available)).scalar() or 0
    loaned_copies = total_copies - available_copies

    # Estatísticas de empréstimos
    total_loans = Loan.query.count()
    active_loans = Loan.query.filter_by(status='active').count()
    returned_loans = Loan.query.filter_by(status='returned').count()
    overdue_loans = Loan.query.filter(
        Loan.status == 'active',
        Loan.due_date < datetime.utcnow()
    ).count()

    # Categorias mais populares
    popular_categories = db.session.query(
        Book.category,
        db.func.count(Loan.id).label('loan_count')
    ).join(Loan).group_by(Book.category).order_by(
        db.desc('loan_count')
    ).limit(5).all()

    stats = {
        'books': {
            'total': total_books,
            'total_copies': total_copies,
            'available': available_copies,
            'loaned': loaned_copies
        },
        'members': {
            'total': total_members,
            'active': active_members,
            'inactive': total_members - active_members
        },
        'loans': {
            'total': total_loans,
            'active': active_loans,
            'returned': returned_loans,
            'overdue': overdue_loans
        },
        'popular_categories': [
            {'category': cat, 'count': count}
            for cat, count in popular_categories
        ]
    }

    return success_response(stats)

@bp.route('/recent-activity', methods=['GET'])
def get_recent_activity():
    recent_loans = Loan.query.order_by(Loan.created_at.desc()).limit(10).all()
    recent_books = Book.query.order_by(Book.created_at.desc()).limit(5).all()
    recent_members = Member.query.order_by(Member.created_at.desc()).limit(5).all()

    activity = {
        'recent_loans': [loan.to_dict() for loan in recent_loans],
        'recent_books': [book.to_dict() for book in recent_books],
        'recent_members': [member.to_dict() for member in recent_members]
    }

    return success_response(activity)

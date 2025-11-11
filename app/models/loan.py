"""
Model de Empréstimo
"""
from datetime import datetime, timedelta
from app import db

class Loan(db.Model):
    __tablename__ = 'loans'

    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)
    member_id = db.Column(db.Integer, db.ForeignKey('members.id'), nullable=False)
    loan_date = db.Column(db.DateTime, default=datetime.utcnow)
    due_date = db.Column(db.DateTime, nullable=False)
    return_date = db.Column(db.DateTime)
    status = db.Column(db.String(20), default='active')  # active, returned, overdue
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, **kwargs):
        super(Loan, self).__init__(**kwargs)
        if not self.due_date:
            # Empréstimo padrão de 14 dias
            self.due_date = datetime.utcnow() + timedelta(days=14)

    @property
    def is_overdue(self):
        if self.status == 'returned':
            return False
        return datetime.utcnow() > self.due_date

    @property
    def days_until_due(self):
        if self.status == 'returned':
            return 0
        delta = self.due_date - datetime.utcnow()
        return delta.days

    def to_dict(self):
        return {
            'id': self.id,
            'book_id': self.book_id,
            'member_id': self.member_id,
            'book': self.book.to_dict() if self.book else None,
            'member': self.member.to_dict() if self.member else None,
            'loan_date': self.loan_date.isoformat(),
            'due_date': self.due_date.isoformat(),
            'return_date': self.return_date.isoformat() if self.return_date else None,
            'status': self.status,
            'is_overdue': self.is_overdue,
            'days_until_due': self.days_until_due,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

    def __repr__(self):
        return f'<Loan {self.id} - Book {self.book_id} to Member {self.member_id}>'

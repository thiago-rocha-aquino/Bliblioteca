"""
Schemas de validação usando Marshmallow
"""
from marshmallow import Schema, fields, validates, ValidationError
import re

class BookSchema(Schema):
    """Schema para validação de livros"""
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True, validate=lambda x: len(x) >= 1)
    author = fields.Str(required=True, validate=lambda x: len(x) >= 1)
    isbn = fields.Str(required=True)
    publisher = fields.Str()
    year = fields.Int()
    category = fields.Str()
    quantity = fields.Int()
    available = fields.Int(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

    @validates('isbn')
    def validate_isbn(self, value):
        # Remove hífens e espaços
        isbn = re.sub(r'[\s-]', '', value)
        if len(isbn) not in [10, 13]:
            raise ValidationError('ISBN deve ter 10 ou 13 dígitos')

    @validates('year')
    def validate_year(self, value):
        from datetime import datetime
        current_year = datetime.now().year
        if value < 1000 or value > current_year + 1:
            raise ValidationError(f'Ano deve estar entre 1000 e {current_year + 1}')

class MemberSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=lambda x: len(x) >= 3)
    email = fields.Email(required=True)
    phone = fields.Str()
    address = fields.Str()
    active = fields.Bool()
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

class LoanSchema(Schema):
    id = fields.Int(dump_only=True)
    book_id = fields.Int(required=True)
    member_id = fields.Int(required=True)
    loan_date = fields.DateTime(dump_only=True)
    due_date = fields.DateTime()
    return_date = fields.DateTime()
    status = fields.Str()
    is_overdue = fields.Bool(dump_only=True)
    days_until_due = fields.Int(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

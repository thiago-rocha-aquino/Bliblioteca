"""
Funções utilitárias
"""
from functools import wraps
from flask import jsonify, request
from marshmallow import ValidationError

def validate_schema(schema):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            try:
                data = schema.load(request.get_json())
                return f(data, *args, **kwargs)
            except ValidationError as err:
                return jsonify({
                    'success': False,
                    'message': 'Erro de validação',
                    'errors': err.messages
                }), 400
        return decorated_function
    return decorator

def success_response(data=None, message=None, status=200):
    response = {'success': True}
    if message:
        response['message'] = message
    if data is not None:
        response['data'] = data
    return jsonify(response), status

def error_response(message, status=400, errors=None):
    response = {
        'success': False,
        'message': message
    }
    if errors:
        response['errors'] = errors
    return jsonify(response), status

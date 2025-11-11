"""
Testes para rotas de membros
"""
import pytest
from app import create_app, db
from app.models import Member
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
def sample_member(app):
    member = Member(
        name='Test Member',
        email='test@example.com',
        phone='(11) 98765-4321',
        address='Test Address'
    )
    db.session.add(member)
    db.session.commit()
    return member

def test_create_member(client):
    member_data = {
        'name': 'John Doe',
        'email': 'john@example.com',
        'phone': '(11) 91234-5678'
    }

    response = client.post('/api/members', json=member_data)
    assert response.status_code == 201
    data = response.get_json()
    assert data['success'] is True
    assert data['data']['name'] == 'John Doe'

def test_get_member(client, sample_member):
    response = client.get(f'/api/members/{sample_member.id}')
    assert response.status_code == 200
    data = response.get_json()
    assert data['data']['email'] == 'test@example.com'

def test_update_member(client, sample_member):
    update_data = {'name': 'Updated Name'}

    response = client.put(f'/api/members/{sample_member.id}', json=update_data)
    assert response.status_code == 200
    data = response.get_json()
    assert data['data']['name'] == 'Updated Name'

def test_duplicate_email(client, sample_member):
    member_data = {
        'name': 'Another Member',
        'email': sample_member.email  # Email duplicado
    }

    response = client.post('/api/members', json=member_data)
    assert response.status_code == 409

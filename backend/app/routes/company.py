from flask import Blueprint, request, jsonify
from sqlalchemy import func
from ..models import Company, Employee, db

bp = Blueprint('company', __name__, url_prefix='/api/companies')

@bp.route('/', methods=['GET'])
def get_companies():
    results = db.session.query(Company).\
        join(Employee, Company.id == Employee.company_id).\
        with_entities(Company.id, Company.name, Company.address, Company.phone,
            Company.url, func.count(Employee.id).label('employee_count')).\
        group_by(Company.id).all()
    
    companies = [{
        'id': c.id,
        'name': c.name,
        'address': c.address,
        'phone': c.phone,
        'url': c.url
    } for c in results]
    
    return jsonify(companies);

@bp.route('/', methods=['POST'])
def create_company():
    data = request.get_json()
    
    company = Company(
        name=data['name'],
        address=data.get('address'),
        phone=data.get('phone'),
        url=data.get('url')
    )
    
    db.session.add(company)
    db.session.commit()
    
    return jsonify({
        'id': company.id,
        'name': company.name,
        'address': company.address,
        'phone': company.phone,
        'url': company.url
    }), 201

@bp.route('/<int:id>', methods=['GET'])
def get_company(id):
    company = Company.query.get_or_404(id)
    return jsonify({
        'id': company.id,
        'name': company.name,
        'address': company.address,
        'phone': company.phone,
        'url': company.url
    })

@bp.route('/<int:id>', methods=['PUT'])
def update_company(id):
    company = Company.query.get_or_404(id)
    data = request.get_json()
    
    company.name = data.get('name', company.name)
    company.address = data.get('address', company.address)
    company.phone = data.get('phone', company.phone)
    company.url = data.get('url', company.url)
    
    db.session.commit()
    
    return jsonify({
        'id': company.id,
        'name': company.name,
        'address': company.address,
        'phone': company.phone,
        'url': company.url
    })

@bp.route('/<int:id>', methods=['DELETE'])
def delete_company(id):
    company = Company.query.get_or_404(id)
    db.session.delete(company)
    db.session.commit()
    
    return '', 204 
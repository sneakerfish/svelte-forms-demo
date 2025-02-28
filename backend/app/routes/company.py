from flask import Blueprint, request, jsonify
from ..models import Company, db

bp = Blueprint('company', __name__, url_prefix='/api/companies')

@bp.route('/', methods=['GET'])
def get_companies():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    pagination = Company.query.paginate(page=page, per_page=per_page)
    
    companies = [{
        'id': c.id,
        'name': c.name,
        'address': c.address,
        'phone': c.phone,
        'url': c.url
    } for c in pagination.items]
    
    return jsonify({
        'companies': companies,
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': page
    })

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
from flask import Blueprint, request, jsonify
from sqlalchemy import func
from ..models import Company, Employee, EmployeeType, db

bp = Blueprint('company', __name__, url_prefix='/api/companies')

def company_to_dict(company):
    """Convert a Company object to a dictionary for JSON serialization"""
    return {
        'id': company.id,
        'name': company.name,
        'address': company.address,
        'phone': company.phone,
        'url': company.url
    }

@bp.route('/', methods=['GET'])
def get_companies():
    results = db.session.query(Company).\
        join(Employee, Company.id == Employee.company_id).\
        with_entities(Company.id, Company.name, Company.address, Company.phone,
            Company.url, func.count(Employee.id).label('employee_count')).\
        group_by(Company.id).all()
    
    companies = [company_to_dict(c) for c in results]
    return jsonify(companies)

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
    
    return jsonify(company_to_dict(company)), 201

@bp.route('/<int:id>', methods=['GET'])
def get_company(id):
    company = Company.query.get_or_404(id)
    return jsonify(company_to_dict(company))

@bp.route('/<int:id>', methods=['PUT'])
def update_company(id):
    company = Company.query.get_or_404(id)
    data = request.get_json()
    
    company.name = data.get('name', company.name)
    company.address = data.get('address', company.address)
    company.phone = data.get('phone', company.phone)
    company.url = data.get('url', company.url)
    
    db.session.commit()
    
    return jsonify(company_to_dict(company))

@bp.route('/<int:id>', methods=['DELETE'])
def delete_company(id):
    company = Company.query.get_or_404(id)
    db.session.delete(company)
    db.session.commit()
    
    return '', 204

@bp.route('/search', methods=['GET'])
def search_companies():
    """Search companies by name"""
    name = request.args.get('name', '').strip()
    if not name:
        return jsonify([])
    
    companies = Company.query.filter(
        Company.name.ilike(f'%{name}%')
    ).all()
    
    return jsonify([company_to_dict(c) for c in companies])

@bp.route('/<int:id>/employees', methods=['GET'])
def get_company_employees(id):
    """Get all employees for a specific company"""
    company = Company.query.get_or_404(id)
    sortorder = [Employee.last_name, Employee.first_name]
    order = request.args.get('sortorder', '')
    if order == "salary":
        sortorder = [Employee.salary.desc(), Employee.last_name]

    # Join with EmployeeType to ensure we have access to employee type information
    employees = Employee.query.\
        filter_by(company_id=id).\
        join(EmployeeType).\
        order_by(*sortorder).all()
    
    from .employee import employee_to_dict
    return jsonify([employee_to_dict(e) for e in employees]) 
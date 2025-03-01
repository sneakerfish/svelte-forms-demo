from flask import Blueprint, request, jsonify
from ..models import Employee, Company, db, EmployeeType
from datetime import datetime
from .company import company_to_dict

bp = Blueprint('employee', __name__, url_prefix='/api/employees')

def employee_to_dict(employee):
    """Convert an Employee object to a dictionary for JSON serialization"""
    return {
        'id': employee.id,
        'company': company_to_dict(employee.company),
        'first_name': employee.first_name,
        'last_name': employee.last_name,
        'type': {
            'id': employee.type.id,
            'name': employee.type.name
        },
        'email': employee.email,
        'phone': employee.phone,
        'salary': float(employee.salary) if employee.salary else None,
        'bio': employee.bio,
        'start_date': employee.start_date.isoformat(),
        'end_date': employee.end_date.isoformat() if employee.end_date else None
    }

@bp.route('/', methods=['GET'])
def get_employees():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    company_id = request.args.get('company_id', type=int)
    
    query = Employee.query.\
        join(Company, Employee.company_id == Company.id).\
        join(EmployeeType, Employee.employee_type_id == EmployeeType.id)
    if company_id:
        query = query.filter_by(company_id=company_id)
    results = query.order_by(Employee.last_name, Employee.first_name).all()

    employees = [employee_to_dict(e) for e in results]
    return jsonify(employees)

@bp.route('/', methods=['POST'])
def create_employee():
    data = request.get_json()
    
    employee = Employee(
        company_id=data['company_id'],
        first_name=data['first_name'],
        last_name=data['last_name'],
        email=data['email'],
        phone=data['phone'],
        employee_type_id=data['employee_type_id'],
        salary=data.get('salary'),
        bio=data.get('bio'),
        start_date=datetime.strptime(data['start_date'], '%Y-%m-%d').date(),
        end_date=datetime.strptime(data['end_date'], '%Y-%m-%d').date() if data.get('end_date') else None
    )
    
    db.session.add(employee)
    db.session.commit()
    
    return jsonify(employee_to_dict(employee)), 201

@bp.route('/<int:id>', methods=['GET'])
def get_employee(id):
    employee = Employee.query.get_or_404(id)
    return jsonify(employee_to_dict(employee))

@bp.route('/<int:id>', methods=['PUT'])
def update_employee(id):
    employee = Employee.query.get_or_404(id)
    data = request.get_json()
    
    employee.company_id = data.get('company_id', employee.company_id)
    employee.first_name = data.get('first_name', employee.first_name)
    employee.last_name = data.get('last_name', employee.last_name)
    employee.email = data.get('email', employee.email)
    employee.phone = data.get('phone', employee.phone)
    employee.employee_type_id = data.get('employee_type_id', employee.employee_type_id)
    employee.salary = data.get('salary', employee.salary)
    employee.bio = data.get('bio', employee.bio)
    
    if 'start_date' in data:
        employee.start_date = datetime.strptime(data['start_date'], '%Y-%m-%d').date()
    if 'end_date' in data:
        employee.end_date = datetime.strptime(data['end_date'], '%Y-%m-%d').date() if data['end_date'] else None
    
    db.session.commit()
    
    return jsonify(employee_to_dict(employee))

@bp.route('/<int:id>', methods=['DELETE'])
def delete_employee(id):
    employee = Employee.query.get_or_404(id)
    db.session.delete(employee)
    db.session.commit()
    
    return '', 204

@bp.route('/search', methods=['GET'])
def search_employees():
    """Search employees by name or employee type"""
    name = request.args.get('name', '').strip()
    employee_type_id = request.args.get('type_id', type=int)
    company_id = request.args.get('company_id', type=int)
    
    query = Employee.query.\
        join(Company).\
        join(EmployeeType)
    
    # Apply filters based on provided parameters
    if name:
        query = query.filter(
            db.or_(
                Employee.first_name.ilike(f'%{name}%'),
                Employee.last_name.ilike(f'%{name}%')
            )
        )
    
    if employee_type_id:
        query = query.filter(Employee.employee_type_id == employee_type_id)
        
    if company_id:
        query = query.filter(Employee.company_id == company_id)
    
    employees = query.\
        order_by(Employee.last_name, Employee.first_name).\
        all()
    
    return jsonify([employee_to_dict(e) for e in employees]) 
from flask import Blueprint, request, jsonify
from ..models import Employee, Company, db, EmployeeType
from datetime import datetime

bp = Blueprint('employee', __name__, url_prefix='/api/employees')

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

    employees = [{
        'id': e.id,
        'company': {
            'id': e.company.id,
            'name': e.company.name,
            'address': e.company.address,
            'phone': e.company.phone,
            'url': e.company.url
        },
        'first_name': e.first_name,
        'last_name': e.last_name,
        'type': {
            'id': e.type.id,
            'name': e.type.name
        },
        'email': e.email,
        'phone': e.phone,
        'salary': float(e.salary) if e.salary else None,
        'bio': e.bio,
        'start_date': e.start_date.isoformat(),
        'end_date': e.end_date.isoformat() if e.end_date else None
    } for e in results]
    
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
    
    return jsonify({
        'id': employee.id,
        'company_id': employee.company_id,
        'first_name': employee.first_name,
        'last_name': employee.last_name,
        'employee_type_id': employee.employee_type_id,
        'salary': float(employee.salary) if employee.salary else None,
        'bio': employee.bio,
        'start_date': employee.start_date.isoformat(),
        'end_date': employee.end_date.isoformat() if employee.end_date else None
    }), 201 
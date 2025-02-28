from flask import jsonify, Blueprint
from app import db
from app.models import EmployeeType

bp = Blueprint('employee_types', __name__)

@bp.route('/api/employee_types/', methods=['GET'])
def get_employee_types():
    try:
        employee_types = EmployeeType.query.all()
        return jsonify([{
            'id': type.id,
            'name': type.name,
            'description': type.description,
            'updated_at': type.updated_at
        } for type in employee_types])
    except Exception as e:
        print(f"Error fetching employee types: {str(e)}")  # Add logging
        return jsonify({'error': 'Failed to fetch employee types', 'details': str(e)}), 500 
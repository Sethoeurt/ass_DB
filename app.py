from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restx import Api, Resource, reqparse
from sqlalchemy import exc
from models import db, Employee, Position, Role, Salary, Attendance, Country
from config import Config
from datetime import datetime

# Initialize Flask application
app = Flask(__name__)

# Load configuration
app.config.from_object(Config())

# Initialize API
api = Api(app, version='1.0', title='Employee Management API', description='API for managing employees and related data')
api_ns = api.namespace('api', description='Employee Management Endpoints')

# Initialize database
db.init_app(app)

# Create all tables
with app.app_context():
    db.create_all()

# List of allowed genders
ALLOWED_GENDERS = ['Male', 'Female', 'Other']


# --- Parsers for Employee ---
post_employee_parser = reqparse.RequestParser()
post_employee_parser.add_argument('first_name', type=str, required=True, help="First name is required")
post_employee_parser.add_argument('last_name', type=str, required=True, help="Last name is required")
post_employee_parser.add_argument('email', type=str, required=True, help="Email is required")
post_employee_parser.add_argument('phone_number', type=str, required=True, help="Phone number is required")
post_employee_parser.add_argument('gender', type=str, required=True, choices=ALLOWED_GENDERS, help=f"Gender must be one of {', '.join(ALLOWED_GENDERS)}")
post_employee_parser.add_argument('role', type=str, required=True, help="Role name is required")  # Role name as a string
post_employee_parser.add_argument('status', type=str, choices=['Active', 'Inactive'], default='Active', help="Status must be 'Active' or 'Inactive'")

put_employee_parser = reqparse.RequestParser()
put_employee_parser.add_argument('first_name', type=str, required=True, help="First name is required")
put_employee_parser.add_argument('last_name', type=str, required=True, help="Last name is required")
put_employee_parser.add_argument('email', type=str, required=True, help="Email is required")
put_employee_parser.add_argument('phone_number', type=str, required=True, help="Phone number is required")
put_employee_parser.add_argument('gender', type=str, required=True, choices=ALLOWED_GENDERS, help=f"Gender must be one of {', '.join(ALLOWED_GENDERS)}")
put_employee_parser.add_argument('role', type=str, required=True, help="Role name is required")  # Role name as a string
put_employee_parser.add_argument('status', type=str, choices=['Active', 'Inactive'], required=True, help="Status must be 'Active' or 'Inactive'")


# --- Routes for Employee ---
@api_ns.route('/employees')
class AllEmployeeResource(Resource):
    """Resource for managing employees."""

    def get(self):
        """Get all employees."""
        employees = db.session.query(Employee).all()
        return [
            {
                'id': e.id,
                'first_name': e.first_name,
                'last_name': e.last_name,
                'email': e.email,
                'phone_number': e.phone_number,
                'gender': e.gender,
                'role': e.role,
                'status': e.status,
            } for e in employees
        ], 200

    @api.expect(post_employee_parser)
    def post(self):
        """Create a new employee."""
        args = post_employee_parser.parse_args()
        try:
            new_employee = Employee(
                first_name=args['first_name'],
                last_name=args['last_name'],
                email=args['email'],
                phone_number=args['phone_number'],
                gender=args['gender'],  # Ensure this matches your model's attribute
                role=args['role'],
                status=args['status'],
            )
            db.session.add(new_employee)
            db.session.commit()
            return {'message': 'Employee created successfully'}, 201
        except Exception as e:
            return {'message': str(e)}, 500


@api_ns.route('/employees/<int:id>')
class EmployeeResource(Resource):
    """Resource for retrieving, updating, and deleting a specific employee."""

    def get(self, id):
        """Get a specific employee by ID."""
        employee = db.session.query(Employee).filter(Employee.id == id).first()
        if employee:
            return {
                'id': employee.id,
                'first_name': employee.first_name,
                'last_name': employee.last_name,
                'email': employee.email,
                'phone_number': employee.phone_number,
                'gender': employee.gender,  # Ensure this matches your model's attribute
                'role': employee.role,
                'status': employee.status,
            }, 200
        return {'message': 'Employee not found'}, 404

    @api.expect(put_employee_parser)
    def put(self, id):
        """Update an employee by ID."""
        args = put_employee_parser.parse_args()
        employee = db.session.query(Employee).filter(Employee.id == id).first()

        if employee:
            employee.first_name = args['first_name']
            employee.last_name = args['last_name']
            employee.email = args['email']
            employee.phone_number = args['phone_number']
            employee.gender = args['gender']  # Ensure this matches your model's attribute
            employee.role = args['role']
            employee.status = args['status']
            try:
                db.session.commit()
                return {'message': 'Employee updated successfully'}, 200
            except Exception as e:
                return {'message': str(e)}, 500
        return {'message': 'Employee not found'}, 404

    def delete(self, id):
        """Delete an employee by ID."""
        employee = db.session.query(Employee).filter(Employee.id == id).first()
        if employee:
            db.session.delete(employee)
            try:
                db.session.commit()
                return {'message': 'Employee deleted successfully'}, 200
            except Exception as e:
                return {'message': str(e)}, 500
        return {'message': 'Employee not found'}, 404


# --- Routes for Position ---
post_position_parser = reqparse.RequestParser()
post_position_parser.add_argument('name', type=str, required=True, help="Position name is required")
post_position_parser.add_argument('description', type=str, required=False, help="Description is optional")

put_position_parser = reqparse.RequestParser()
put_position_parser.add_argument('name', type=str, required=True, help="Position name is required")
put_position_parser.add_argument('description', type=str, required=False, help="Description is optional")

@api_ns.route('/positions')
class AllPositionResource(Resource):
    """Resource for managing positions."""

    def get(self):
        """Get all positions."""
        positions = db.session.query(Position).all()
        return [{'id': p.id, 'name': p.name, 'description': p.description} for p in positions], 200

    @api.expect(post_position_parser)
    def post(self):
        """Create a new position."""
        args = post_position_parser.parse_args()
        new_position = Position(name=args['name'], description=args.get('description'))
        db.session.add(new_position)
        db.session.commit()
        return {'message': 'Success'}, 201


@api_ns.route('/positions/<int:id>')
class PositionResource(Resource):
    """Resource for retrieving, updating, and deleting a specific position."""

    def get(self, id):
        """Get a specific position by ID."""
        position = db.session.query(Position).filter(Position.id == id).first()
        if position:
            return {'id': position.id, 'name': position.name, 'description': position.description}, 200
        return {'message': 'Position not found'}, 404

    @api.expect(put_position_parser)
    def put(self, id):
        """Update a position by ID."""
        args = put_position_parser.parse_args()
        position = db.session.query(Position).filter(Position.id == id).first()

        if position:
            position.name = args['name']
            position.description = args.get('description', position.description)
            db.session.commit()
            return {'message': 'Success'}, 200
        return {'message': 'Position not found'}, 404

    def delete(self, id):
        """Delete a position by ID."""
        position = db.session.query(Position).filter(Position.id == id).first()
        if position:
            db.session.delete(position)
            db.session.commit()
            return {'message': 'Success'}, 200
        return {'message': 'Position not found'}, 404


# Similar updates are needed for Salary, Attendance, and Country resources to match the new database schema (based on updated fields).

# --- Run the Flask Application ---
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)

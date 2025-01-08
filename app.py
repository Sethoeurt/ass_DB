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

# Parsers for Role
post_role_parser = reqparse.RequestParser()
post_role_parser.add_argument('name', type=str, required=True, help="Role name is required")
post_role_parser.add_argument('description', type=str, required=False, help="Description is optional")

put_role_parser = reqparse.RequestParser()
put_role_parser.add_argument('name', type=str, required=True, help="Role name is required")
put_role_parser.add_argument('description', type=str, required=False, help="Description is optional")

# Parsers for Salary
post_salary_parser = reqparse.RequestParser()
post_salary_parser.add_argument('employee_id', type=int, required=True, help="Employee ID is required")
post_salary_parser.add_argument('amount', type=float, required=True, help="Salary amount is required")
post_salary_parser.add_argument('status', type=str, required=False, help="Status is optional")

put_salary_parser = reqparse.RequestParser()
put_salary_parser.add_argument('amount', type=float, required=False, help="Salary amount is optional")
put_salary_parser.add_argument('status', type=str, required=False, help="Status is optional")

# Parsers for Attendance
post_attendance_parser = reqparse.RequestParser()
post_attendance_parser.add_argument('employee_id', type=int, required=True, help="Employee ID is required")
post_attendance_parser.add_argument('date', type=str, required=True, help="Date (YYYY-MM-DD) is required")
post_attendance_parser.add_argument('status', type=str, choices=['Present', 'Absent'], required=False, default='Present', help="Status must be 'Present' or 'Absent'")

put_attendance_parser = reqparse.RequestParser()
put_attendance_parser.add_argument('status', type=str, choices=['Present', 'Absent'], required=True, help="Status must be 'Present' or 'Absent'")

# Parsers for Country
post_country_parser = reqparse.RequestParser()
post_country_parser.add_argument('country_name', type=str, required=True, help="Country name is required")

put_country_parser = reqparse.RequestParser()
put_country_parser.add_argument('country_name', type=str, required=True, help="Country name is required")


# --- Routes for Role ---
@api_ns.route('/roles')
class AllRoleResource(Resource):
    """Resource for managing roles."""

    def get(self):
        """Get all roles."""
        roles = db.session.query(Role).all()
        return [{'id': r.id, 'name': r.name, 'description': r.description} for r in roles], 200

    @api.expect(post_role_parser)
    def post(self):
        """Create a new role."""
        args = post_role_parser.parse_args()
        new_role = Role(name=args['name'], description=args.get('description'))
        db.session.add(new_role)
        db.session.commit()
        return {'message': 'Success'}, 201


@api_ns.route('/roles/<int:id>')
class RoleResource(Resource):
    """Resource for retrieving, updating, and deleting a specific role."""

    def get(self, id):
        """Get a specific role by ID."""
        role = db.session.query(Role).filter(Role.id == id).first()
        if role:
            return {'id': role.id, 'name': role.name, 'description': role.description}, 200
        return {'message': 'Role not found'}, 404

    @api.expect(put_role_parser)
    def put(self, id):
        """Update a role by ID."""
        args = put_role_parser.parse_args()
        role = db.session.query(Role).filter(Role.id == id).first()

        if role:
            role.name = args['name']
            role.description = args.get('description', role.description)
            db.session.commit()
            return {'message': 'Success'}, 200
        return {'message': 'Role not found'}, 404

    def delete(self, id):
        """Delete a role by ID."""
        role = db.session.query(Role).filter(Role.id == id).first()
        if role:
            db.session.delete(role)
            db.session.commit()
            return {'message': 'Success'}, 200
        return {'message': 'Role not found'}, 404


# --- Routes for Salary ---
@api_ns.route('/salaries')
class AllSalaryResource(Resource):
    """Resource for managing salaries."""

    def get(self):
        """Get all salaries."""
        salaries = db.session.query(Salary).all()
        return [{'id': s.id, 'employee_id': s.employee_id, 'amount': s.amount, 'status': s.status} for s in salaries], 200

    @api.expect(post_salary_parser)
    def post(self):
        """Create a new salary."""
        args = post_salary_parser.parse_args()

        # Check if the employee exists
        employee = db.session.query(Employee).filter(Employee.id == args['employee_id']).first()
        if not employee:
            return {'message': f"Employee with ID {args['employee_id']} does not exist"}, 404

        # Validate the 'status' field
        status = args.get('status', 'Active')  # Default to 'Active' if not provided
        if status not in ['Active', 'Inactive']:
            return {'message': f"Invalid status value '{status}'. Allowed values are 'Active' or 'Inactive'."}, 400

        # Create and save the salary record
        new_salary = Salary(
            employee_id=args['employee_id'],
            amount=args['amount'],
            status=status
        )

        try:
            db.session.add(new_salary)
            db.session.commit()
            return {'message': 'Success'}, 201
        except exc.SQLAlchemyError as e:
            db.session.rollback()
            return {'message': str(e)}, 500


@api_ns.route('/salaries/<int:id>')
class SalaryResource(Resource):
    """Resource for retrieving, updating, and deleting a specific salary."""

    def get(self, id):
        """Get a specific salary by ID."""
        salary = db.session.query(Salary).filter(Salary.id == id).first()
        if salary:
            return {'id': salary.id, 'employee_id': salary.employee_id, 'amount': salary.amount, 'status': salary.status}, 200
        return {'message': 'Salary not found'}, 404

    @api.expect(put_salary_parser)
    def put(self, id):
        """Update a salary by ID."""
        args = put_salary_parser.parse_args()
        salary = db.session.query(Salary).filter(Salary.id == id).first()

        if salary:
            salary.amount = args.get('amount', salary.amount)
            salary.status = args.get('status', salary.status)
            db.session.commit()
            return {'message': 'Success'}, 200
        return {'message': 'Salary not found'}, 404

    def delete(self, id):
        """Delete a salary by ID."""
        salary = db.session.query(Salary).filter(Salary.id == id).first()
        if salary:
            db.session.delete(salary)
            db.session.commit()
            return {'message': 'Success'}, 200
        return {'message': 'Salary not found'}, 404


# --- Routes for Attendance ---
@api_ns.route('/attendances')
class AllAttendanceResource(Resource):
    """Resource for managing attendances."""

    def get(self):
        """Get all attendance records."""
        attendances = db.session.query(Attendance).all()
        return [
            {
                'id': a.id,
                'employee_id': a.employee_id,
                'date': a.date.strftime('%Y-%m-%d'),
                'status': a.status,
                'created_at': a.created_at,
                'updated_at': a.updated_at,
            } for a in attendances
        ], 200

    @api.expect(post_attendance_parser)
    def post(self):
        """Create a new attendance record."""
        args = post_attendance_parser.parse_args()
        try:
            new_attendance = Attendance(
                employee_id=args['employee_id'],
                date=datetime.strptime(args['date'], '%Y-%m-%d'),
                status=args['status']
            )
            db.session.add(new_attendance)
            db.session.commit()
            return {'message': 'Success'}, 201
        except Exception as e:
            return {'message': str(e)}, 500


@api_ns.route('/attendances/<int:id>')
class AttendanceResource(Resource):
    """Resource for retrieving, updating, and deleting a specific attendance record."""

    def get(self, id):
        """Get a specific attendance record by ID."""
        attendance = db.session.query(Attendance).filter(Attendance.id == id).first()
        if attendance:
            return {
                'id': attendance.id,
                'employee_id': attendance.employee_id,
                'date': attendance.date.strftime('%Y-%m-%d'),
                'status': attendance.status,
                'created_at': attendance.created_at,
                'updated_at': attendance.updated_at,
            }, 200
        return {'message': 'Attendance record not found'}, 404

    @api.expect(put_attendance_parser)
    def put(self, id):
        """Update an attendance record by ID."""
        args = put_attendance_parser.parse_args()
        attendance = db.session.query(Attendance).filter(Attendance.id == id).first()

        if attendance:
            attendance.status = args['status']
            db.session.commit()
            return {'message': 'Success'}, 200
        return {'message': 'Attendance record not found'}, 404

    def delete(self, id):
        """Delete an attendance record by ID."""
        attendance = db.session.query(Attendance).filter(Attendance.id == id).first()
        if attendance:
            db.session.delete(attendance)
            db.session.commit()
            return {'message': 'Success'}, 200
        return {'message': 'Attendance record not found'}, 404


# --- Routes for Country ---
@api_ns.route('/countries')
class AllCountryResource(Resource):
    """Resource for managing countries."""

    def get(self):
        """Get all countries."""
        countries = db.session.query(Country).all()
        return [{'id': c.id, 'country_name': c.country_name} for c in countries], 200

    @api.expect(post_country_parser)
    def post(self):
        """Create a new country."""
        args = post_country_parser.parse_args()
        new_country = Country(country_name=args['country_name'])
        db.session.add(new_country)
        db.session.commit()
        return {'message': 'Success'}, 201


@api_ns.route('/countries/<int:id>')
class CountryResource(Resource):
    """Resource for retrieving, updating, and deleting a specific country."""

    def get(self, id):
        """Get a specific country by ID."""
        country = db.session.query(Country).filter(Country.id == id).first()
        if country:
            return {'id': country.id, 'country_name': country.country_name}, 200
        return {'message': 'Country not found'}, 404

    @api.expect(put_country_parser)
    def put(self, id):
        """Update a country by ID."""
        args = put_country_parser.parse_args()
        country = db.session.query(Country).filter(Country.id == id).first()

        if country:
            country.country_name = args['country_name']
            db.session.commit()
            return {'message': 'Success'}, 200
        return {'message': 'Country not found'}, 404

    def delete(self, id):
        """Delete a country by ID."""
        country = db.session.query(Country).filter(Country.id == id).first()
        if country:
            db.session.delete(country)
            db.session.commit()
            return {'message': 'Success'}, 200
        return {'message': 'Country not found'}, 404
    



# Similar updates are needed for Salary, Attendance, and Country resources to match the new database schema (based on updated fields)

# --- Run the Flask Application ---
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)


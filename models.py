from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Initialize the SQLAlchemy instance
db = SQLAlchemy()

# --- Models ---
class Gender(db.Model):
    """Model for Gender data."""
    __tablename__ = 'genders'
    id = db.Column('GenderID', db.Integer, primary_key=True, autoincrement=True)  # Auto-increment enabled
    name = db.Column('Name', db.String(100), nullable=False)


class Role(db.Model):
    """Model for Role data."""
    __tablename__ = 'roles'
    id = db.Column('RoleID', db.Integer, primary_key=True, autoincrement=True)  # Auto-increment enabled
    name = db.Column('Name', db.String(100), nullable=False)
    description = db.Column('Description', db.String(255), nullable=True)


class Position(db.Model):
    """Model for Position data."""
    __tablename__ = 'positions'
    id = db.Column('DepartmentID', db.Integer, primary_key=True, autoincrement=True)  # Auto-increment enabled
    name = db.Column('Name', db.String(100), nullable=False)
    description = db.Column('Description', db.String(255), nullable=True)


class Employee(db.Model):
    """Model for Employee data."""
    __tablename__ = 'employees'
    id = db.Column('EmployeeID', db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column('First_Name', db.String(100), nullable=False)
    last_name = db.Column('Last_Name', db.String(100), nullable=False)
    email = db.Column('Email', db.String(255), unique=True, nullable=True)
    phone_number = db.Column('Phone_Number', db.String(25), nullable=False)
    gender = db.Column('Gender', db.String(100), nullable=False)  # Changed to Gender string
    role = db.Column('Role', db.String(100), nullable=False)  # Kept as a string
    status = db.Column('Status', db.Enum('Active', 'Inactive'), default='Active')


class Salary(db.Model):
    """Model for Salary data."""
    __tablename__ = 'salaries'
    id = db.Column('SalaryID', db.Integer, primary_key=True, autoincrement=True)  # Auto-increment enabled
    employee_id = db.Column('EmployeeID', db.Integer, db.ForeignKey('employees.EmployeeID'), nullable=False)
    amount = db.Column('Amount', db.Float, nullable=False)
    status = db.Column('Status', db.Enum('Active', 'Inactive'), default='Active')


class Attendance(db.Model):
    """Model for Attendance data."""
    __tablename__ = 'attendances'
    id = db.Column('AttendanceID', db.Integer, primary_key=True, autoincrement=True)  # Auto-increment enabled
    employee_id = db.Column('EmployeeID', db.Integer, db.ForeignKey('employees.EmployeeID'), nullable=False)
    date = db.Column('Date', db.Date, nullable=False)
    status = db.Column('Status', db.Enum('Present', 'Absent'), default='Present')
    created_at = db.Column('CreatedAt', db.DateTime, default=datetime.utcnow)
    updated_at = db.Column('UpdatedAt', db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Country(db.Model):
    """Model for Country data."""
    __tablename__ = 'countries'
    id = db.Column('CountryID', db.Integer, primary_key=True, autoincrement=True)  # Auto-increment enabled
    name = db.Column('Name', db.String(100), nullable=False)

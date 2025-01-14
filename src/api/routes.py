"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User, Branch, AvailableSlot, Appointment, Service, Product, Employee, WorkingHours, Company
from flask_login import LoginManager
from config import Config
from api.utils import generate_sitemap, APIException
from flask_cors import CORS
from geopy.geocoders import Nominatim
from flask import render_template, redirect, url_for, flash
from flask_login import login_user
from flask_migrate import Migrate
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from datetime import datetime, timedelta

 
#app = create_app()
api = Blueprint('api', __name__)
#app = Flask(__name__)
#migrate = Migrate(app, db) 
CORS(api)

"""
app.config.from_object(Config)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///branches.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
"""

login_manager = LoginManager(api)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Allow CORS requests to this API
@api.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    users = list(map(lambda user: user.serialize(), users))
    return jsonify(users), 200

@api.route('/user/<int:id>', methods=['PUT'])
def edit_user(id):
    request_body = request.json
    user = User.query.get(id)
    if user is None:
        return jsonify({"msg": "User not found"}), 404

    if "name" in request_body:
        user.name = request_body["name"]
    if "last_name" in request_body:
        user.last_name = request_body["last_name"]
    if "phone" in request_body:
        user.phone = request_body["phone"]
    if "companies" in request_body:
        user.companies = request_body["companies"]

    db.session.commit()

    return jsonify({"msg": "User updated", "user": user.serialize()}), 200

@api.route('/user/<int:id>', methods=['DELETE'])
def delete_user():
    user = User.query.get(id)
    if user is None:
        return jsonify({"msg": "User not found"}), 404

    db.session.delete(user)
    db.session.commit()

    return jsonify({"msg": "User deleted"}), 200

@api.route('/register', methods=['POST'])
def register():
    data_user = request.json
    user = User()
    new_user = user.create_user(email=data_user["email"], password=data_user["password"])
    print(new_user)
    return jsonify({"msg": "Your registration has been successful, congratulations!"})
 
@api.route('/login', methods=['POST'])
def login(): 
    data_user = request.json
    user = User.query.filter_by(email=data_user["email"]).first()
    if user and user.check_password(password=data_user["password"]):
        access_token = create_access_token(identity=user.serialize())
        return jsonify({"token": access_token, "msg": "WELCOME!"})
    else:
        return jsonify({"msg": "Invalid email or password"}), 401
    
@api.route('/branch', methods=['GET'])
def get_branch():
    branch = Branch.query.all()
    branch = list(map(lambda branch: branch.serialize(), branch))
    return jsonify(branch), 200    

@api.route('/branch', methods=['POST'])
def add_branch():
    data = request.get_json()
    if not data:
        return jsonify({'message': 'No input data provided'}), 400

    new_branch = Branch().create_branch(
        branch_name=data['branch_name'],
        branch_address=data['branch_address'],
        branch_phone=data['branch_phone'],
        company_id=data['company_id'],
        branch_is_active=data.get('branch_is_active', True)
    )
    return jsonify({'message': 'Branch created successfully', 'branch': new_branch.serialize()}), 201

@api.route('/branch/<int:branch_id>', methods=['PUT'])
def update_branch(branch_id):
    data = request.get_json()
    branch = Branch.query.get_or_404(branch_id)
    
    if 'branch_name' in data:
        branch.branch_name = data['branch_name']
    if 'branch_address' in data:
        branch.branch_address = data['branch_address']
    if 'branch_phone' in data:
        branch.branch_phone = data['branch_phone']
    if 'branch_is_active' in data:
        branch.branch_is_active = data['branch_is_active']
    
    db.session.commit()
    return jsonify({'message': 'Branch updated successfully', 'branch': branch.serialize()}), 200

@api.route('/branch/<int:branch_id>', methods=['DELETE'])
def delete_branch(branch_id):
    branch = Branch.query.get_or_404(branch_id)
    db.session.delete(branch)
    db.session.commit()
    return jsonify({'message': 'Branch deleted successfully'}), 200

@api.route('/available_slots', methods=['GET'])
def get_available_slots():
    available_slots = AvailableSlot.query.all()
    available_slots = list(map(lambda available_slots: available_slots.serialize(), available_slots))
    return jsonify(available_slots), 200 

@api.route('/available_slots', methods=['POST'])
def add_available_slot():
    data = request.get_json()
    new_slot = AvailableSlot.create_slot(
        employee_id=data['employee_id'],
        start_time=data['start_time'],
        end_time=data['end_time'],
        available_slot_is_active=data.get('available_slot_is_active', True)
    )
    db.session.add(new_slot)
    db.session.commit()
    return jsonify(new_slot.serialize()), 201
    
@api.route('/available_slots/<int:id>', methods=['PUT'])
def update_available_slot(id):
    slot = AvailableSlot.query.get_or_404(id)
    data = request.get_json()
    try:
        if 'start_time' in data:
            slot.start_time = data['start_time']
        if 'end_time' in data:
            slot.end_time = data['end_time']
        if 'available_slot_is_active' in data:
            slot.available_slot_is_active = data['available_slot_is_active']
        db.session.commit()
        return jsonify(slot.serialize()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@api.route('/available_slots/<int:id>', methods=['DELETE'])
def delete_available_slot(id):
    slot = AvailableSlot.query.get_or_404(id)
    try:
        db.session.delete(slot)
        db.session.commit()
        return jsonify({'message': 'Available slot deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@api.route('/appointments', methods=['GET'])
def get_appointments():
    appointments = Appointment.query.all()
    appointments = list(map(lambda appointments: appointments.serialize(), appointments))
    return jsonify(appointments), 200     

@api.route('/appointments', methods=['POST'])
def add_appointment():
    data = request.get_json()
    try:
        new_appointment = Appointment.create_appointment(
            company_id=data['company_id'],
            available_slot_id=data['available_slot_id'],
            appointment_time=data['appointment_time'],
            first_name_customer=data['first_name_customer'],
            last_name_customer=data['last_name_customer'],
            phone_customer=data['phone_customer'],
            email_customer=data['email_customer'],
            observation_customer=data.get('observation_customer', '')
        )
        db.session.add(new_appointment)
        db.session.commit()
        return jsonify(new_appointment.serialize()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@api.route('/appointments/<int:id>', methods=['PUT'])
def update_appointment(id):
    appointment = Appointment.query.get_or_404(id)
    data = request.get_json()
    if 'company_id' in data:
        appointment.company_id= data['company_id']
    if 'available_slot_id' in data:
        appointment.available_slot_id = data['available_slot_id']
    if 'appointment_time' in data:
        appointment.appointment_time = data['appointment_time']
    if 'first_name_customer' in data:
        appointment.first_name_customer = data['first_name_customer']
    if 'last_name_customer' in data:
        appointment.last_name_customer = data['last_name_customer']
    if 'phone_customer' in data:
        appointment.phone_customer = data['phone_customer']
    if 'email_customer' in data:
        appointment.email_customer = data['email_customer']
    if 'observation_customer' in data:
        appointment.observation_customer = data['observation_customer']
    
    db.session.commit()
    return jsonify({'message': 'Appointment updated successfully', 'branch': appointment.serialize()}), 200

@api.route('/appointments/<int:id>', methods=['DELETE'])
def delete_appointment(id):
    appointment = Appointment.query.get_or_404(id)
    try:
        db.session.delete(appointment)
        db.session.commit()
        return jsonify({'message': 'Appointment deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@api.route('/services', methods=['GET'])
def get_services():
    services = Service.query.all()
    services = list(map(lambda services: services.serialize(), services))
    return jsonify(services), 200  

@api.route('/services', methods=['POST'])
def create_service():
    data = request.get_json()
    new_service = Service.create_service(
        service_name=data['service_name'],
        service_price=data['service_price'],
        image_url=data.get('image_url', None),
        company_id=data['company_id'],
        service_is_active=data.get('service_is_active', True)
    )
    db.session.add(new_service)
    db.session.commit()
    return jsonify(new_service.serialize()), 201


@api.route('/services/<int:service_id>', methods=['PUT'])
def update_service(service_id):
    service = Service.query.get_or_404(service_id)
    data = request.get_json()
    try:
        if 'service_name' in data:
            service.service_name = data['service_name']
        if 'service_price' in data:
            service.service_price = data['service_price']
        if 'image_url' in data:
            service.image_url = data['image_url']
        if 'service_is_active' in data:
            service.service_is_active = data['service_is_active']
        
        db.session.commit()
        return jsonify(service.serialize()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@api.route('/services/<int:service_id>', methods=['DELETE'])
def delete_service(service_id):
    service = Service.query.get_or_404(service_id)
    try:
        db.session.delete(service)
        db.session.commit()
        return jsonify({'message': 'Service successfully deleted'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400
    
@api.route('/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    products = list(map(lambda products: products.serialize(), products))
    return jsonify(products), 200  
    
@api.route('/products', methods=['POST'])
def add_product():
    data = request.get_json()
    new_product = Product(
        product_name=data['product_name'],
        product_price=data['product_price'],
        image_url=data.get('image_url', None),
        company_id=data['company_id'],
        product_is_active=data.get('product_is_active', True)
    )
    db.session.add(new_product)
    db.session.commit()
    return jsonify(new_product.serialize()), 201

@api.route('/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    product = Product.query.get_or_404(product_id)
    data = request.get_json()
    try:
        if 'product_name' in data:
            product.product_name = data['product_name']
        if 'product_price' in data:
            product.product_price = data['product_price']
        if 'image_url' in data:
            product.image_url = data['image_url']
        if 'product_is_active' in data:
            product.product_is_active = data['product_is_active']
        
        db.session.commit()
        return jsonify(product.serialize()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@api.route('/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    try:
        db.session.delete(product)
        db.session.commit()
        return jsonify({'message': 'Product successfully deleted'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400
    
@api.route('/employees', methods=['GET'])
def get_employees():
    employees = Employee.query.all()
    employees = list(map(lambda employees: employees.serialize(), employees))
    return jsonify(employees), 200  
    
@api.route('/employees', methods=['POST'])
def add_employee():
    data = request.get_json()
    new_employee = Employee(
        name=data['name'],
        last_name=data['last_name'],
        company_id=data['company_id'],
        employee_is_active=data.get('employee_is_active', True)
    )
    db.session.add(new_employee)
    db.session.commit()
    return jsonify(new_employee.serialize()), 201

@api.route('/employees/<int:employee_id>', methods=['PUT'])
def update_employee(employee_id):
    employee = Employee.query.get_or_404(employee_id)
    data = request.get_json()
    try:
        if 'name' in data:
            employee.name = data['name']
        if 'last_name' in data:
            employee.last_name = data['last_name']
        if 'employee_is_active' in data:
            employee.employee_is_active = data['employee_is_active']
        
        db.session.commit()
        return jsonify(employee.serialize()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@api.route('/employees/<int:employee_id>', methods=['DELETE'])
def delete_employee(employee_id):
    employee = Employee.query.get_or_404(employee_id)
    try:
        db.session.delete(employee)
        db.session.commit()
        return jsonify({'message': 'Employee successfully deleted'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400
    
@api.route('/workinghours', methods=['GET'])
def get_workinghours():
    workinghours = WorkingHours.query.all()
    workinghours = list(map(lambda workinghours: workinghours.serialize(), workinghours))
    return jsonify(workinghours), 200 
    
@api.route('/workinghours', methods=['POST'])
def add_working_hours():
    data = request.get_json()
    new_working_hours = WorkingHours.create_working_hours(
        employee_id=data['employee_id'],
        start_time=data['start_time'],
        end_time=data['end_time'],
        workinghours_is_active=data.get('workinghours_is_active', True)
    )
    db.session.add(new_working_hours)
    db.session.commit()
    return jsonify(new_working_hours.serialize()), 201

@api.route('/workinghours/<int:working_hours_id>', methods=['PUT'])
def update_working_hours(working_hours_id):
    working_hours = WorkingHours.query.get_or_404(working_hours_id)
    data = request.get_json()
    try:
        if 'start_time' in data:
            working_hours.start_time = datetime.fromisoformat(data['start_time'])
        if 'end_time' in data:
            working_hours.end_time = datetime.fromisoformat(data['end_time'])
        if 'workinghours_is_active' in data:
            working_hours.workinghours_is_active = data['workinghours_is_active']
        
        db.session.commit()
        return jsonify(working_hours.serialize()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@api.route('/workinghours/<int:working_hours_id>', methods=['DELETE'])
def delete_working_hours(working_hours_id):
    working_hours = WorkingHours.query.get_or_404(working_hours_id)
    try:
        db.session.delete(working_hours)
        db.session.commit()
        return jsonify({'message': 'Working hours successfully deleted'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@api.route('/company', methods=['GET'])
def get_company():
    company = Company.query.all()
    company = list(map(lambda company: company.serialize(), company))
    return jsonify(company), 200 

@api.route('/company', methods=['POST'])
def add_company():
    data = request.get_json()
    user_id = data.get('user_id')
    name = data.get('name')
    nif = data.get('nif')
    company_is_active = data.get('company_is_active', True)  # Default to True if not provided

    if not user_id or not name:
        return jsonify({"error": "user_id and name are required"}), 400

    new_company = Company().create_company(user_id=user_id, name=name, nif=nif, company_is_active=company_is_active)

    return jsonify({"message": "Company added successfully", "company": new_company.serialize()}), 201

@api.route('/company/<int:company_id>', methods=['PUT', 'DELETE'])
def manage_company(company_id):
    company = Company.query.get_or_404(company_id)

    if request.method == 'PUT':
        data = request.get_json()
        name = data.get('name')
        is_active = data.get('is_active', True)  # Default to True if not provided

        if not name:
            return jsonify({"error": "name is required"}), 400

        updated_company = company.update_company(name=name, is_active=is_active)

        return jsonify({"message": "Company updated successfully", "company": updated_company.serialize()}), 200

    elif request.method == 'DELETE':
        company.delete_company()
        return jsonify({"message": "Company deleted successfully"}), 200
    




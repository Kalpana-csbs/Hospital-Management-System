from flask import Flask, render_template, request, redirect, jsonify, session, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'hospital123'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hospital.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Add this line to suppress the warning
app.config['ENV'] = 'development'  # Set environment
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    symptoms = db.Column(db.String(200), nullable=False)
    admission_date = db.Column(db.DateTime, default=datetime.utcnow)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'))

class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    specialization = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    availability = db.Column(db.Boolean, default=True)
    patients = db.relationship('Patient', backref='doctor', lazy=True)

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=False)
    appointment_time = db.Column(db.DateTime, nullable=False)
    notes = db.Column(db.Text)
    patient = db.relationship('Patient', backref='appointments')
    doctor = db.relationship('Doctor', backref='appointments')

@app.route('/')
def login():
    if session.get('logged_in'):
        return redirect('/dashboard')
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login_post():
    username = request.form.get('username')
    password = request.form.get('password')
    
    user = User.query.filter_by(username=username).first()
    
    if user and user.password == password:
        session['logged_in'] = True
        session['username'] = username
        flash('Login successful!', 'success')
        return redirect('/dashboard')
    else:
        flash('Invalid username or password', 'error')
        return redirect('/')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/dashboard')
def dashboard():
    if not session.get('logged_in'):
        return redirect('/')
    patients = Patient.query.count()
    doctors = Doctor.query.count()
    appointments = Patient.query.filter(Patient.doctor_id.isnot(None)).count()
    return render_template('dashboard.html', 
                         patients=patients, 
                         doctors=doctors, 
                         appointments=appointments)

# Patients Page
@app.route('/patients', methods=['GET', 'POST'])
def patients():
    if request.method == 'POST':
        if 'add' in request.form:
            new_patient = Patient(
                name=request.form['name'],
                age=request.form['age'],
                gender=request.form['gender'],
                symptoms=request.form['symptoms'],
                admission_date=request.form['admission_date']
            )
            db.session.add(new_patient)
            db.session.commit()
        elif 'update' in request.form:
            patient = Patient.query.get(request.form['id'])
            patient.name = request.form['name']
            patient.age = request.form['age']
            patient.gender = request.form['gender']
            patient.symptoms = request.form['symptoms']
            patient.admission_date = request.form['admission_date']
            db.session.commit()
        elif 'delete' in request.form:
            patient = Patient.query.get(request.form['id'])
            db.session.delete(patient)
            db.session.commit()
    patients_data = Patient.query.all()
    return render_template('patients.html', patients=patients_data)

@app.route('/add_patient', methods=['POST'])
def add_patient():
    name = request.form.get('name')
    age = request.form.get('age')
    gender = request.form.get('gender')
    symptoms = request.form.get('symptoms')
    patient = Patient(name=name, age=age, gender=gender, symptoms=symptoms)
    db.session.add(patient)
    db.session.commit()
    return redirect('/patients')

@app.route('/delete_patient/<int:id>', methods=['DELETE'])
def delete_patient(id):
    patient = Patient.query.get_or_404(id)
    db.session.delete(patient)
    db.session.commit()
    return jsonify({"success": True})

@app.route('/edit_patient/<int:id>', methods=['POST'])
def edit_patient(id):
    patient = Patient.query.get_or_404(id)
    patient.name = request.form.get('name')
    patient.age = request.form.get('age')
    patient.gender = request.form.get('gender')
    patient.symptoms = request.form.get('symptoms')
    db.session.commit()
    return redirect('/patients')

# Doctors Page
@app.route('/doctors', methods=['GET', 'POST'])
def doctors():
    if request.method == 'POST':
        if 'add' in request.form:
            new_doctor = Doctor(
                name=request.form['name'],
                specialization=request.form['specialization'],
                phone=request.form['phone'],
                availability=request.form.get('availability') == 'on'
            )
            db.session.add(new_doctor)
            db.session.commit()
        elif 'update' in request.form:
            doctor = Doctor.query.get(request.form['id'])
            doctor.name = request.form['name']
            doctor.specialization = request.form['specialization']
            doctor.phone = request.form['phone']
            doctor.availability = request.form.get('availability') == 'on'
            db.session.commit()
        elif 'delete' in request.form:
            doctor = Doctor.query.get(request.form['id'])
            db.session.delete(doctor)
            db.session.commit()
    doctors_data = Doctor.query.all()
    return render_template('doctors.html', doctors=doctors_data)

@app.route('/add_doctor', methods=['POST'])
def add_doctor():
    name = request.form.get('name')
    specialization = request.form.get('specialization')
    phone = request.form.get('phone')
    doctor = Doctor(name=name, specialization=specialization, phone=phone)
    db.session.add(doctor)
    db.session.commit()
    return redirect('/doctors')

@app.route('/assign_patient', methods=['POST'])
def assign_patient():
    patient_id = request.form.get('patient_id')
    doctor_id = request.form.get('doctor_id')
    patient = Patient.query.get(patient_id)
    patient.doctor_id = doctor_id
    db.session.commit()
    return redirect('/patients')

@app.route('/appointments')
def appointments():
    if not session.get('logged_in'):
        return redirect('/')
    appointments = Appointment.query.all()
    patients = Patient.query.all()
    doctors = Doctor.query.all()
    return render_template('appointments.html', 
                         appointments=appointments,
                         patients=patients,
                         doctors=doctors)

@app.route('/add_appointment', methods=['POST'])
def add_appointment():
    if not session.get('logged_in'):
        return redirect('/')
    patient_id = request.form.get('patient_id')
    doctor_id = request.form.get('doctor_id')
    appointment_time = datetime.strptime(request.form.get('appointment_time'), '%Y-%m-%dT%H:%M')
    notes = request.form.get('notes')
    
    appointment = Appointment(
        patient_id=patient_id,
        doctor_id=doctor_id,
        appointment_time=appointment_time,
        notes=notes
    )
    db.session.add(appointment)
    db.session.commit()
    return redirect('/appointments')

@app.route('/edit_appointment/<int:id>', methods=['POST'])
def edit_appointment(id):
    if not session.get('logged_in'):
        return redirect('/')
    
    appointment = Appointment.query.get_or_404(id)
    appointment.patient_id = request.form.get('patient_id')
    appointment.doctor_id = request.form.get('doctor_id')
    appointment.appointment_date = datetime.strptime(request.form.get('date'), '%Y-%m-%d %H:%M')
    appointment.notes = request.form.get('notes')
    
    db.session.commit()
    return jsonify({'success': True})

@app.route('/delete_doctor/<int:id>', methods=['DELETE'])
def delete_doctor(id):
    doctor = Doctor.query.get_or_404(id)
    db.session.delete(doctor)
    db.session.commit()
    return jsonify({"success": True})

@app.route('/delete_appointment/<int:id>', methods=['DELETE'])
def delete_appointment(id):
    if not session.get('logged_in'):
        return redirect('/')
    
    appointment = Appointment.query.get_or_404(id)
    db.session.delete(appointment)
    db.session.commit()
    return jsonify({'success': True})

@app.route('/edit_doctor/<int:id>', methods=['POST'])
def edit_doctor(id):
    doctor = Doctor.query.get_or_404(id)
    doctor.name = request.form.get('name')
    doctor.specialization = request.form.get('specialization')
    doctor.phone = request.form.get('phone')
    doctor.availability = request.form.get('availability') == 'true'
    db.session.commit()
    return redirect('/doctors')

def create_admin_user():
    with app.app_context():
        # Check if admin user exists
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin = User(username='admin', password='admin123')
            db.session.add(admin)
            db.session.commit()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        create_admin_user()
    app.run(debug=True)

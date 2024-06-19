from flask import Flask, render_template, request, redirect, url_for, session
from models import db, User, Devis
import logging
import os
from datetime import datetime

app = Flask(__name__)
app.config.from_pyfile('config.py')
app.secret_key = os.urandom(24)  # Clé secrète pour les sessions

db.init_app(app)

# Configure logging
logging.basicConfig(level=logging.DEBUG)

@app.route('/')
def index():
    if 'user_id' in session:
        user = User.query.filter_by(id=session['user_id']).first()
        return render_template('index.html', user=user)
    elif 'employee_id' in session:
        employee = User.query.filter_by(id=session['employee_id']).first()
        return render_template('index.html', user=employee)
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        try:
            name = request.form['name']
            email = request.form['email']
            password = request.form['password']
            confirmPassword = request.form['confirmPassword']
            if password == confirmPassword:
                new_user = User(name=name, email=email, password=password)
                db.session.add(new_user)
                db.session.commit()
                app.logger.info('User created successfully')
                return redirect(url_for('login'))
            else:
                app.logger.error('Password and confirm password do not match')
        except Exception as e:
            app.logger.error('Error creating user: %s', e)
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        app.logger.debug('Attempting to log in with email: %s', email)
        user = User.query.filter_by(email=email).first()
        if user:
            app.logger.debug('User found: %s', user.email)
            if user.password == password:
                session['user_id'] = user.id
                if user.is_admin:
                    session['is_admin'] = True
                if user.is_employee:
                    session['is_employee'] = True
                    session['employee_id'] = user.id
                app.logger.info('User logged in successfully: %s', user.email)
                return redirect(url_for('index'))
            else:
                app.logger.error('Invalid password for user: %s', user.email)
        else:
            app.logger.error('No user found with email: %s', email)
        return 'Invalid credentials'
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('is_admin', None)  # Retirer l'information admin de la session
    session.pop('is_employee', None)
    session.pop('employee_id', None)
    return redirect(url_for('index'))

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user = User.query.filter_by(id=session['user_id']).first()

    if request.method == 'POST':
        user.name = request.form['name']
        user.email = request.form['email']
        if request.form['password']:
            user.password = request.form['password']
        db.session.commit()
        return redirect(url_for('profile'))

    return render_template('profile.html', user=user)

@app.route('/create_devis', methods=['GET', 'POST'])
def create_devis():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        entreprise = request.form['entreprise']
        description = request.form['description']
        service_type = request.form['service_type']
        budget = request.form['budget']
        urgence = request.form['urgence']
        contact_number = request.form['contact_number']
        contact_email = request.form['contact_email']
        additional_info = request.form['additional_info']
        user_id = session['user_id']
        date = datetime.now()

        new_devis = Devis(
            user_id=user_id,
            entreprise=entreprise,
            description=description,
            service_type=service_type,
            budget=budget,
            urgence=urgence,
            contact_number=contact_number,
            contact_email=contact_email,
            additional_info=additional_info,
            status='En attente',  # Initial status
            date=date
        )
        db.session.add(new_devis)
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('devis.html')

@app.route('/my_devis')
def my_devis():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    devis_list = Devis.query.filter_by(user_id=user_id).all()
    return render_template('devis_list.html', devis_list=devis_list)

@app.route('/my_assigned_devis')
def my_assigned_devis():
    if 'employee_id' not in session:
        return redirect(url_for('login'))

    employee_id = session['employee_id']
    devis_list = Devis.query.filter_by(employee_id=employee_id).all()
    return render_template('devis_list.html', devis_list=devis_list)

# Admin Routes
@app.route('/admin/dashboard')
def admin_dashboard():
    if 'user_id' not in session or not session.get('is_admin'):
        return redirect(url_for('login'))

    users = User.query.all()
    return render_template('admin_dashboard.html', users=users)

@app.route('/admin/user/<int:user_id>')
def admin_view_user(user_id):
    if 'user_id' not in session or not session.get('is_admin'):
        return redirect(url_for('login'))

    user = User.query.filter_by(id=user_id).first()
    return render_template('admin_view_user.html', user=user)

@app.route('/admin/user/<int:user_id>/delete')
def admin_delete_user(user_id):
    if 'user_id' not in session or not session.get('is_admin'):
        return redirect(url_for('login'))

    user = User.query.filter_by(id=user_id).first()
    if user:
        db.session.delete(user)
        db.session.commit()
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/devis/<int:devis_id>/edit', methods=['GET', 'POST'])
def admin_edit_devis(devis_id):
    if 'user_id' not in session or not session.get('is_admin'):
        return redirect(url_for('login'))

    devis = Devis.query.filter_by(id=devis_id).first()
    if request.method == 'POST':
        devis.status = request.form['status']
        devis.admin_notes = request.form['admin_notes']
        devis.employee_id = request.form['employee_id'] or None
        db.session.commit()
        return redirect(url_for('admin_view_user', user_id=devis.user_id))

    employees = User.query.filter_by(is_employee=True).all()
    return render_template('admin_edit_devis.html', devis=devis, employees=employees)

@app.route('/admin/devis/<int:devis_id>/delete')
def admin_delete_devis(devis_id):
    if 'user_id' not in session or not session.get('is_admin'):
        return redirect(url_for('login'))

    devis = Devis.query.filter_by(id=devis_id).first()
    if devis:
        db.session.delete(devis)
        db.session.commit()
    return redirect(url_for('admin_view_user', user_id=devis.user_id))

if __name__ == '__main__':
    app.run(debug=True)

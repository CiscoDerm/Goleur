from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    is_employee = db.Column(db.Boolean, default=False)

class Devis(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)  # Changement ici
    entreprise = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=False)
    service_type = db.Column(db.String(120), nullable=False)
    budget = db.Column(db.String(120), nullable=False)
    urgence = db.Column(db.String(120), nullable=False)
    contact_number = db.Column(db.String(20), nullable=False)
    contact_email = db.Column(db.String(120), nullable=False)
    additional_info = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(20), nullable=False, default='En attente')
    admin_notes = db.Column(db.Text, nullable=True)
    date = db.Column(db.DateTime, nullable=False)
    user = db.relationship('User', foreign_keys=[user_id], backref=db.backref('devis', lazy=True))
    employee = db.relationship('User', foreign_keys=[employee_id], backref=db.backref('assigned_devis', lazy=True))

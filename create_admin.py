from app import app
from models import db, User

def create_user(name, email, password, is_admin=False, is_employee=False):
    with app.app_context():
        user = User(name=name, email=email, password=password, is_admin=is_admin, is_employee=is_employee)
        db.session.add(user)
        db.session.commit()

if __name__ == "__main__":
    name = input("Enter user name: ")
    email = input("Enter user email: ")
    password = input("Enter user password: ")
    role = input("Enter role (admin/employee/user): ").lower()
    is_admin = role == 'admin'
    is_employee = role == 'employee'
    create_user(name, email, password, is_admin, is_employee)
    print("User created successfully")

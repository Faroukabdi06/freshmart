# create_admin.py

from sqlalchemy.orm import Session
from app.cores.database import SessionLocal
from app.models.users import User, UserRole
from app.utils.security import hash_password
import uuid

def create_admin():
    db: Session = SessionLocal()

    admin_email = "adminfreshmart@gmail.com"

    existing = db.query(User).filter(User.email == admin_email).first()
    if existing:
        print("Admin already exists")
        return

    admin = User(
        id=uuid.uuid4(),
        name="freshmart",
        email=admin_email,
        phone_number="0787654321",
        password_hash=hash_password("adminfreshmart001"),
        role=UserRole.ADMIN,
    )

    db.add(admin)
    db.commit()
    db.refresh(admin)

    print("Admin created successfully")
    print(f"Email: {admin_email}")
    print("Password: ChangeThisPassword123!")

    db.close()

if __name__ == "__main__":
    create_admin()

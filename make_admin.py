from app.db.database import SessionLocal
from app.db.models import User

email = input("Enter your registered email: ").strip()

db = SessionLocal()

try:
    user = db.query(User).filter(User.email == email).first()

    if user is None:
        print("User not found. Check your registered email.")
    elif user.is_admin:
        print("This user is already an admin.")
    else:
        user.is_admin = True
        db.commit()
        print(f"{user.email} is now an admin.")

except Exception:
    db.rollback()
    raise

finally:
    db.close()
import sys

from sqlalchemy import select

from app.core.security import hash_password
from app.db.session import SessionLocal
from app.models.user import User


def main() -> None:
    if len(sys.argv) != 3:
        print("Usage: python scripts/create_user.py username password")
        raise SystemExit(1)

    username = sys.argv[1]
    password = sys.argv[2]

    db = SessionLocal()

    try:
        existing_user = db.scalar(
            select(User).where(User.username == username)
        )

        if existing_user is not None:
            print("User already exists")
            raise SystemExit(1)

        user = User(
            username=username,
            hashed_password=hash_password(password),
        )

        db.add(user)
        db.commit()

        print(f"Created user: {username}")

    finally:
        db.close()


if __name__ == "__main__":
    main()
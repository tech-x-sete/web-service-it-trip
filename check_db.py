from db import SessionLocal
from models.user import User
from models.organization import Organization
from models.event import Event
from models.tag import Tag
from models.university import University

def check_db():
    db = SessionLocal()
    try:
        # Проверяем университеты
        print("\nUniversities:")
        universities = db.query(University).all()
        for u in universities:
            print(f"- {u.title}: {u.description}")

        # Проверяем организации
        print("\nOrganizations:")
        organizations = db.query(Organization).all()
        for o in organizations:
            print(f"- {o.title}: {o.description}")

        # Проверяем пользователей
        print("\nUsers:")
        users = db.query(User).all()
        for u in users:
            print(f"- {u.name} ({u.email})")

        # Проверяем события
        print("\nEvents:")
        events = db.query(Event).all()
        for e in events:
            print(f"- {e.title} at {e.place}")

        # Проверяем теги
        print("\nTags:")
        tags = db.query(Tag).all()
        for t in tags:
            print(f"- {t.title}")

    finally:
        db.close()

if __name__ == "__main__":
    check_db() 
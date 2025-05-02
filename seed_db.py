from db import SessionLocal
from models.user import User
from models.organization import Organization
from models.event import Event
from models.tag import Tag
from models.university import University
from models.user_organization import UserOrganization
from models.tag_event import TagEvent
import uuid
from datetime import date, time

def seed_db():
    db = SessionLocal()
    try:
        # Создаем университет
        university = University(
            id=uuid.uuid4(),
            title="Test University",
            description="Test University Description"
        )
        db.add(university)
        db.commit()

        # Создаем организацию
        organization = Organization(
            id=uuid.uuid4(),
            title="Test Organization",
            description="Test Organization Description",
            university_id=university.id
        )
        db.add(organization)
        db.commit()

        # Создаем пользователя
        user = User(
            id=uuid.uuid4(),
            name="Test User",
            email="test@example.com",
            password="testpassword",
            role="user"
        )
        db.add(user)
        db.commit()

        # Связываем пользователя с организацией
        user_org = UserOrganization(
            user_id=user.id,
            organization_id=organization.id
        )
        db.add(user_org)

        # Создаем тег
        tag = Tag(
            id=uuid.uuid4(),
            title="Test Tag"
        )
        db.add(tag)
        db.commit()

        # Создаем событие
        event = Event(
            id=uuid.uuid4(),
            title="Test Event",
            date_start=date(2024, 3, 1),
            date_end=date(2024, 3, 2),
            place="Test Place",
            time_start=time(10, 0),
            content="Test Content",
            priceint=100.0,
            organization_id=organization.id
        )
        db.add(event)
        db.commit()

        # Связываем событие с тегом
        tag_event = TagEvent(
            tag_id=tag.id,
            event_id=event.id
        )
        db.add(tag_event)
        db.commit()

        print("Test data added successfully!")

    except Exception as e:
        print(f"Error adding test data: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_db() 
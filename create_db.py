# create_db.py
from db import engine
from models.base import Base
from models import University, Organization, Event, Tag, User, UserOrganization, TagEvent

if __name__ == "__main__":
    # Убедитесь, что таблицы создаются в правильном порядке
    Base.metadata.drop_all(bind=engine)  # Осторожно: удалит все данные!

    Base.metadata.create_all(bind=engine, tables=[
        University.__table__,
        Organization.__table__,
        User.__table__,
        Event.__table__,
        Tag.__table__,
        UserOrganization.__table__,
        TagEvent.__table__
    ])
    print("Таблицы созданы!")
from flask import Flask, request, jsonify, render_template, json
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey, or_, create_engine
from sqlalchemy.future import engine
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['JSON_AS_ASCII'] = False

db = SQLAlchemy(app)
CORS(app)


def populate_test_data(app, db):
    with app.app_context():
        # Очищаем все таблицы (опционально)
        db.drop_all()
        db.create_all()

        # Создаем теги
        tags = [
            Tag(name='лекция'),
            Tag(name='мастер-класс'),
            Tag(name='конференция'),
            Tag(name='хакатон'),
            Tag(name='встреча')
        ]
        db.session.add_all(tags)
        db.session.commit()

        # Создаем организации
        organizations = [
            Organization(
                name='IT-клуб',
                description='Сообщество студентов, увлеченных информационными технологиями',
                logo_url='https://example.com/logos/it-club.png',
                created_at=datetime(2023, 1, 15)
            ),
            Organization(
                name='Экономический клуб',
                description='Обсуждение актуальных вопросов экономики и финансов',
                logo_url='https://example.com/logos/econ-club.png',
                created_at=datetime(2023, 2, 20)
            ),
            Organization(
                name='Клуб предпринимателей',
                description='Поддержка студенческих стартапов и бизнес-инициатив',
                logo_url='https://example.com/logos/startup-club.png',
                created_at=datetime(2023, 3, 10)
            )
        ]
        db.session.add_all(organizations)
        db.session.commit()

        # Создаем пользователей
        users = [
            User(
                username='Алексей Петров',
                login='a.petrov',
                password_hash='hash1',  # В реальном приложении используйте хеши паролей!
                role='writer',
                created_at=datetime(2023, 1, 10)
            ),
            User(
                username='Мария Иванова',
                login='m.ivanova',
                password_hash='hash2',
                role='writer',
                created_at=datetime(2023, 2, 5)
            ),
            User(
                username='Иван Сидоров',
                login='i.sidorov',
                password_hash='hash3',
                role='moderator',
                created_at=datetime(2023, 3, 1)
            ),
            User(
                username='Елена Кузнецова',
                login='e.kuznetsova',
                password_hash='hash4',
                role='guest',
                created_at=datetime(2023, 4, 15)
            )
        ]
        db.session.add_all(users)
        db.session.commit()

        # Добавляем связи пользователей с организациями
        organizations[0].users.extend([users[0], users[1]])
        organizations[1].users.extend([users[1], users[2]])
        organizations[2].users.extend([users[0], users[3]])

        # Создаем публикации
        publications = [
            Publication(
                title='Введение в Python для начинающих',
                content='Базовый курс по программированию на Python для студентов первого курса...',
                image_url='https://example.com/images/python-course.jpg',
                writer_id=users[0].id,
                organization_id=organizations[0].id,
                event_date='2023-10-15',
                location='Аудитория 310, главный корпус',
                tags=[tags[0], tags[1]],  # лекция, мастер-класс
                buttons=[
                    PublicationButton(title='Регистрация', url='https://example.com/reg/python'),
                    PublicationButton(title='Программа', url='https://example.com/program/python')
                ]
            ),
            Publication(
                title='Финансовые рынки 2023',
                content='Анализ текущей ситуации на финансовых рынках и перспективы развития...',
                image_url='https://example.com/images/finance-2023.jpg',
                writer_id=users[1].id,
                organization_id=organizations[1].id,
                event_date='2023-11-20',
                location='Аудитория 215, экономический корпус',
                tags=[tags[0], tags[2]],  # лекция, конференция
                buttons=[
                    PublicationButton(title='Записаться', url='https://example.com/reg/finance')
                ]
            ),
            Publication(
                title='Стартап-уикенд',
                content='48 часов интенсивной работы над своими бизнес-проектами...',
                image_url='https://example.com/images/startup-weekend.jpg',
                writer_id=users[2].id,
                organization_id=organizations[2].id,
                event_date='2023-12-05',
                location='Коворкинг "Точка кипения"',
                tags=[tags[3], tags[4]],  # хакатон, встреча
                buttons=[
                    PublicationButton(title='Подать заявку', url='https://example.com/reg/startup'),
                    PublicationButton(title='Правила', url='https://example.com/rules/startup'),
                    PublicationButton(title='Примеры проектов', url='https://example.com/examples/startup')
                ]
            ),
            Publication(
                title='Искусственный интеллект в бизнесе',
                content='Как современные технологии ИИ меняют подходы к ведению бизнеса...',
                image_url='https://example.com/images/ai-business.jpg',
                writer_id=users[0].id,
                organization_id=organizations[0].id,
                event_date='2024-01-15',
                location='Аудитория 410, главный корпус',
                tags=[tags[0]],  # лекция
                buttons=[
                    PublicationButton(title='Участвовать', url='https://example.com/reg/ai')
                ]
            )
        ]
        db.session.add_all(publications)
        db.session.commit()
        print("Тестовые данные успешно добавлены!")


# Association tables
user_organization = db.Table('user_organization',
                             db.Column('user_id', db.String(36), db.ForeignKey('user.id'), primary_key=True),
                             db.Column('organization_id', db.String(36), db.ForeignKey('organization.id'),
                                       primary_key=True)
                             )

publication_tag = db.Table('publication_tag',
                           db.Column('publication_id', db.String(36), db.ForeignKey('publication.id'),
                                     primary_key=True),
                           db.Column('tag_id', db.String(36), db.ForeignKey('tag.id'), primary_key=True)
                           )


# Models
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    username = db.Column(db.String(50))
    login = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(10), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    organizations = db.relationship('Organization', secondary=user_organization, back_populates='users')

    __table_args__ = (
        db.CheckConstraint("role IN ('moderator', 'writer', 'guest')", name='role_check'),
    )


class Organization(db.Model):
    __tablename__ = 'organization'
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(100))
    description = db.Column(db.Text)
    logo_url = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    users = db.relationship('User', secondary=user_organization, back_populates='organizations')
    publications = db.relationship('Publication', back_populates='organization')


class Publication(db.Model):
    __tablename__ = 'publication'
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = db.Column(db.String(200))
    content = db.Column(db.Text)
    image_url = db.Column(db.String(200))
    writer_id = db.Column(db.String(36), db.ForeignKey('user.id'), nullable=False)
    organization_id = db.Column(db.String(36), db.ForeignKey('organization.id'), nullable=False)
    event_date = db.Column(db.String(20))
    location = db.Column(db.String(100))

    writer = db.relationship('User', backref='publications')
    organization = db.relationship('Organization', back_populates='publications')
    buttons = db.relationship('PublicationButton', backref='publication', cascade='all, delete-orphan')
    tags = db.relationship('Tag', secondary=publication_tag, backref='publications')


class PublicationButton(db.Model):
    __tablename__ = 'publication_button'
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    publication_id = db.Column(db.String(36), db.ForeignKey('publication.id', ondelete='CASCADE'))
    title = db.Column(db.Text, nullable=False)
    url = db.Column(db.Text, nullable=False)


class Tag(db.Model):
    __tablename__ = 'tag'
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(50), unique=True)


with app.app_context():
    db.create_all()

populate_test_data(app, db)


# Routes
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/pub', methods=['GET'])
def get_publications():
    publications = Publication.query.all()
    result = []
    for pub in publications:
        result.append({
            'id': pub.id,
            'title': pub.title,
            'image_url': pub.image_url,
            'event_date': pub.event_date,
            'location': pub.location,
            'organization': {
                'name': pub.organization.name,
                'logo_url': pub.organization.logo_url
            },
            'tags': [tag.name for tag in pub.tags]
        })
    return jsonify(result)


@app.route('/publications/<publication_id>', methods=['GET'])
def get_publication(publication_id):
    pub = Publication.query.get_or_404(publication_id)
    return jsonify({
        'id': pub.id,
        'title': pub.title,
        'content': pub.content,
        'image_url': pub.image_url,
        'event_date': pub.event_date,
        'location': pub.location,
        'writer': {
            'id': pub.writer.id,
            'username': pub.writer.username
        },
        'organization': {
            'id': pub.organization.id,
            'name': pub.organization.name,
            'logo_url': pub.organization.logo_url
        },
        'tags': [tag.name for tag in pub.tags],
        'buttons': [{'title': b.title, 'url': b.url} for b in pub.buttons]
    })


@app.route('/organizations', methods=['GET'])
def get_organizations():
    orgs = Organization.query.all()
    return jsonify([{
        'id': org.id,
        'name': org.name,
        'description': org.description,
        'logo_url': org.logo_url,
        'created_at': org.created_at.isoformat()
    } for org in orgs])


@app.route('/organizations/<organization_id>', methods=['GET'])
def get_organization(organization_id):
    org = Organization.query.get_or_404(organization_id)
    return jsonify({
        'id': org.id,
        'name': org.name,
        'description': org.description,
        'logo_url': org.logo_url,
        'created_at': org.created_at.isoformat(),
        'members': [{'id': u.id, 'username': u.username} for u in org.users]
    })


@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([{
        'id': user.id,
        'username': user.username,
        'role': user.role,
        'created_at': user.created_at.isoformat()
    } for user in users])


@app.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify({
        'id': user.id,
        'username': user.username,
        'role': user.role,
        'organizations': [{'id': org.id, 'name': org.name} for org in user.organizations],
        'created_at': user.created_at.isoformat()
    })


@app.route('/organizations', methods=['POST'])
def add_organization():
    data = request.get_json()
    new_org = Organization(
        name=data['name'],
        description=data.get('description'),
        logo_url=data.get('logo_url'),
        created_at=datetime.utcnow()
    )
    db.session.add(new_org)
    db.session.commit()
    return jsonify({'id': new_org.id}), 201


@app.route('/users', methods=['POST'])
def add_user():
    data = request.get_json()
    if User.query.filter_by(login=data['login']).first():
        return jsonify({'error': 'Login already exists'}), 400

    new_user = User(
        username=data['username'],
        login=data['login'],
        password_hash=data['password_hash'],  # In real app, hash the password!
        role=data['role'],
        created_at=datetime.utcnow()
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'id': new_user.id}), 201


@app.route('/publications/new', methods=['POST'])
def add_publication():
    data = request.get_json()

    new_pub = Publication(
        title=data['title'],
        content=data['content'],
        image_url=data.get('image_url'),
        writer_id=data['writer_id'],
        organization_id=data['organization_id'],
        event_date=data.get('event_date'),
        location=data.get('location')
    )

    # Process tags
    for tag_name in data.get('tags', []):
        tag = Tag.query.filter_by(name=tag_name).first()
        if not tag:
            tag = Tag(name=tag_name)
            db.session.add(tag)
        new_pub.tags.append(tag)

    # Process buttons
    for button in data.get('buttons', []):
        new_pub.buttons.append(PublicationButton(
            title=button['title'],
            url=button['url']
        ))

    db.session.add(new_pub)
    db.session.commit()
    return jsonify({'id': new_pub.id}), 201


@app.route('/publications/search', methods=['GET'])
def search_publication():
    query = request.args.get('q', '')
    results = Publication.query.join(User).filter(
        or_(
            Publication.title.ilike(f'%{query}%'),
            Publication.content.ilike(f'%{query}%'),
            User.username.ilike(f'%{query}%')
        )
    ).all()

    return jsonify([{
        'id': pub.id,
        'title': pub.title,
        'image_url': pub.image_url,
        'organization': {
            'name': pub.organization.name,
            'logo_url': pub.organization.logo_url
        },
        'event_date': pub.event_date,
        'location': pub.location,
        'tags': [tag.name for tag in pub.tags]
    } for pub in results])


if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    engine = create_engine(
        'postgresql://user@localhost:5432/',
        client_encoding='utf8',
        echo=True
    )
    app.run(debug=True)


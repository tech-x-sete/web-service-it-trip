from ..init import app
from infrastructure.db.models import async_session
from ...db.repositories.organization_repository import OrganizationRepository
from ...db.repositories.user_repository import UserRepository
from core import domain


@app.route('/users/{username}', methods=['GET'])
def get_users(username: str):
    async with async_session() as session:
        repo = UserRepository(session)
        data = repo.get_user_by_username(username)

        return data


@app.route('/organization/{organization_id}', methods=['GET'])
def get_organizations(organization_id):
    async with async_session() as session:
        repo = OrganizationRepository(session)
        data = repo.get_organization_by_id(organization_id)

        return data


# @app.route('/writers', methods=['GET'])
# def get_writers():
#     async with async_session() as session:
#         ...
#
#
# @app.route('/writers', methods=['POST'])
# def post_writers():
#     async with async_session() as session:
#         ...


# @app.route('/writers/{ user_id }', methods=['DELETE'])
# def delete_writers():
#     async with async_session() as session:
#         ...


@app.route('/organizations', methods=['POST'])
def create_organization(organization: domain.Organization):
    async with async_session() as session:
        repo = OrganizationRepository(session)
        repo.create_organization(organization)


@app.route('/organizations/{ organization_id }', methods=['DELETE'])
def delete_organizations():
    async with async_session() as session:
        ...

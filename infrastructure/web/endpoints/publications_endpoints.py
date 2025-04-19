from infrastructure.db.models import async_session
from infrastructure.db.repositories.publication_repository import PublicationRepository
from flask import render_template, Blueprint

publications_bp = Blueprint('publications', __name__)


@publications_bp.route('/', methods=['GET'])
async def get_publications():
    async with async_session() as session:
        repo = PublicationRepository(session)
        data = await repo.get_all_publications()
        if data:
            return [elem.to_dict() for elem in data]
        # render_template('templates/', data=data)
        return []


@publications_bp.route('/{publication_id}', methods=['GET'])
def get_publication_by_id(id_: int):
    ...


@publications_bp.route('/', methods=['POST'])
def add_publication():
    ...


@publications_bp.route('/{publication_id}', methods=['PATCH'])
def edit_publication(id_: int):
    ...


@publications_bp.route('/{publication_id}', methods=['DELETE'])
def delete_publication(id_: int):
    ...

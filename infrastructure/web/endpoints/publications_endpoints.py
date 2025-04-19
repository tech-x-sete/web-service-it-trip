from infrastructure.db.models import async_session, Publication
from infrastructure.db.repositories.publication_repository import PublicationRepository
from flask import render_template, Blueprint
from core import domain

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
async def get_publication_by_id(id_: int):
    async with async_session() as session:
        repo = PublicationRepository(session)
        data = await repo.get_publication_by_id(id_)
        if data:
            ...


@publications_bp.route('/', methods=['POST'])
def add_publication(pub: domain.Publication):
    async with async_session() as session:
        repo = PublicationRepository(session)
        repo.create_publication(
            title=pub.title,
            content=pub.content,
            writer_id=pub.writer_id,
            organization_id=pub.organization.id,
            publish_date=pub.publish_date,
            featured_image_url=pub.featured_image_url,
            event_start_date=pub.event_start_date,
            event_end_date=pub.event_end_date,
            is_archived=pub.is_archived,
            tags=pub.tags
        )


@publications_bp.route('/{publication_id}', methods=['PATCH'])
def edit_publication(id_: int):
    ...


@publications_bp.route('/{publication_id}', methods=['DELETE'])
def delete_publication(id_: int):
    ...

from infrastructure.db.models import async_session, Publication
from infrastructure.db.repositories.publication_repository import PublicationRepository
from flask import render_template, Blueprint
from core import domain
from sqlalchemy import select, delete, update

publications_bp = Blueprint('publications', __name__)


@publications_bp.route('/', methods=['GET'])
async def get_publications():
    async with async_session() as session:
        repo = PublicationRepository(session)
        data = await repo.get_all_publications()
        if data:
            return data  # ???
            # return [elem.to_dict() for elem in data]
        # render_template('templates/', data=data)
        return []


@publications_bp.route('/{publication_id}', methods=['GET'])
async def get_publication_by_id(id_: int) -> domain.Publication:
    async with async_session() as session:
        repo = PublicationRepository(session)
        data = await repo.get_publication_by_id(id_)
        if data:
            return data


@publications_bp.route('/', methods=['POST'])
def add_publication(pub: domain.Publication) -> None:
    async with async_session() as session:  # Ну тут по хорошему проверку надо было
        repo = PublicationRepository(session)
        repo.create_publication(
            title=pub.title,
            content=pub.content,
            writer_id=pub.writer_id,
            organization_id=pub.organization.id,
            publish_date=pub.publish_date,
            location=pub.location,
            featured_image_url=pub.featured_image_url,
            event_date=pub.event_date,
            is_archived=pub.is_archived
        )


@publications_bp.route('/{publication_id}', methods=['PATCH'])
def edit_publication(id_: int):
    async with async_session() as session:
        ...


@publications_bp.route('/{publication_id}', methods=['DELETE'])
def delete_publication(publication_id: int):
    async with async_session() as session:
        result = session.execute(
            select(Publication).where(Publication.id == publication_id)
        )

        publication = result.scalars().first()
        session.execute(
            delete(Publication)
            .where(Publication.id == publication_id)
        )

        session.commit()

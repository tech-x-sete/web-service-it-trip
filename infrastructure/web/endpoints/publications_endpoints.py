from infrastructure.db.models import async_session, Publication
from infrastructure.db.repositories.publication_repository import PublicationRepository
from flask import render_template, Blueprint, request
from core import domain
from sqlalchemy import select, delete, update

publications_bp = Blueprint('publications', __name__)


@publications_bp.route('/', methods=['GET'])
async def get_publications():
    async with async_session() as session:
        repo = PublicationRepository(session)
        data = await repo.get_all_publications()
        if data:
            return data
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
async def edit_publication(publication_id: int):
    async with async_session() as session:
        data = request.get_json()
        if not data:
            return {"error": "No data provided"}, 400

        repo = PublicationRepository(session)
        publication = await repo.get_publication_by_id(publication_id)
        if not publication:
            return {"error": "Publication not found"}, 404

        update_data = {
            "title": data.get("title", publication.title),
            "content": data.get("content", publication.content),
            "featured_image_url": data.get("featured_image_url", publication.featured_image_url),
            "writer_id": data.get("writer_id", publication.writer_id),
            "organization_id": data.get("organization_id", publication.organization),
            "publish_date": data.get("publish_date", publication.publish_date),
            "event_date": data.get("event_date", publication.event_date),
            "is_archived": data.get("is_archived", publication.is_archived),
            "location": data.get("location", publication.location)
        }

        await repo.update_publication(publication_id, **update_data)

        # updated_pub = await repo.get_publication_by_id(publication_id)
        # return updated_pub


@publications_bp.route('/{publication_id}', methods=['DELETE'])
def delete_publication(publication_id: int):
    async with async_session() as session:
        result = session.execute(
            select(Publication).where(Publication.id == publication_id)
        )

        publication = result.scalars().first()
        if not publication:
            raise Exception

        session.execute(
            delete(Publication)
            .where(Publication.id == publication_id)
        )

        session.commit()

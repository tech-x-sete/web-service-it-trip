from ..init import app
from infrastructure.db.models import async_session
from infrastructure.db.repositories.publication_repository import PublicationRepository
from flask import render_template


@app.route('/v1/publications', methods=['GET'])
def get_publications():
    async with async_session() as session:
        repo = PublicationRepository(session)
        data = repo.get_all_publications()
        render_template('templates/', data=data)


@app.route('/v1/publications/{publication_id}', methods=['GET'])
def get_publication_by_id(id_: int):
    ...


@app.route('/v1/publications', methods=['POST'])
def add_publication():
    ...


@app.route('/v1/publications/{publication_id}', methods=['PATCH'])
def edit_publication(id_: int):
    ...


@app.route('/v1/publications/{publication_id}', methods=['DELETE'])
def delete_publication(id_: int):
    ...

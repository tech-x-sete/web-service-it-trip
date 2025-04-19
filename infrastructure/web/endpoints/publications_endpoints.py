from ..main import app


@app.route('/v1/publications', methods=['GET'])
def get_publications():
    ...


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

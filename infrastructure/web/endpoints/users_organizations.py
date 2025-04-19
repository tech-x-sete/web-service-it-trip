from ..init import app


@app.route('/users/{username}', methods=['GET'])
def get_users():
    ...


@app.route('/organization/{organization_id}', methods=['GET'])
def get_organizations():
    ...


@app.route('/writers', methods=['GET'])
def get_writers():
    ...


@app.route('/writers', methods=['POST'])
def post_writers():
    ...


@app.route('/writers/{ user_id }', methods=['DELETE'])
def delete_writers():
    ...


@app.route('/organizations', methods=['POST'])
def post_organizations():
    ...


@app.route('/organizations/{ organization_id }', methods=['DELETE'])
def delete_organizations():
    ...

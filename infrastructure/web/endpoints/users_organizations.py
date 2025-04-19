from ..init import app


@app.route('/v1/users/{username}', methods=['GET'])
def get_users():
    ...


@app.route('/v1/organization/{organization_id}', methods=['GET'])
def get_organizations():
    ...


@app.route('/v1/writers', methods=['GET'])
def get_writers():
    ...


@app.route('/v1/writers', methods=['POST'])
def post_writers():
    ...


@app.route('/v1/writers/{ user_id }', methods=['DELETE'])
def delete_writers():
    ...


@app.route('/v1/organizations', methods=['POST'])
def post_organizations():
    ...


@app.route('/v1/organizations/{ organization_id }', methods=['DELETE'])
def delete_organizations():
    ...

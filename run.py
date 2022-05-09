from app import create_app, db


app = create_app()
from app.blueprints.models import User
@app.shell_context_processor
def make_context():
    return {
        'db': db,
        'User': User,
    }
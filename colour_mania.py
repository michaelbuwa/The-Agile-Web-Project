from app import create_application, db
from app.config import DeploymentConfig  # or Config if you don't have DeploymentConfig
import sqlalchemy as sa
import sqlalchemy.orm as so
from app.models import User, GameResult, Friendship

app = create_application(DeploymentConfig)  # <-- Create the app instance

@app.shell_context_processor
def make_shell_context():
    return {'sa': sa, 'so': so, 'db': db, 'User': User, 'GameResult': GameResult, 'Friendship': Friendship}
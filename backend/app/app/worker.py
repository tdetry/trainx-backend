from app.db.session import SessionLocal
from app.models.user import User
from raven import Client

from app.core.celery_app import celery_app
from app.core.config import settings

client_sentry = Client(settings.SENTRY_DSN)


db = SessionLocal()


@celery_app.task(acks_late=True)
def test_celery(word: str) -> str:
    return f"test task return {word}"


@celery_app.task(acks_late=True)
def test_celery_database(id: int) -> str:
    user = db.query(User).filter(User.id == id).first()
    return f"test task return {user.full_name}"

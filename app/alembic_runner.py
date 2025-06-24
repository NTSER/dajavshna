import os
from alembic import command
from alembic.config import Config
from .config import db_settings


def run_migrations():
    alembic_cfg = Config(os.path.join(os.path.dirname(__file__), "../alembic.ini"))
    alembic_cfg.set_main_option("sqlalchemy.url", db_settings.POSTGRES_URL)
    command.upgrade(alembic_cfg, "head")

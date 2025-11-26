from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
# это загружает alembic.ini
config = context.config

# логирование
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# ИМПОРТИРУЕМ Base И МОДЕЛИ (ВАЖНО)
from models.user import User
from models.group import Group
from models.student import Student # noqa — важно для автогенерации

from db.database import Base
target_metadata = Base.metadata


def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,      # видеть изменения типов
            compare_server_default=True,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

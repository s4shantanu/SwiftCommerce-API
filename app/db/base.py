from sqlalchemy.orm import declarative_base

Base = declarative_base()

from app.models.user import User  # noqa
from app.models.product import Product  # noqa

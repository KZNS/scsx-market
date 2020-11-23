import functools

from flask_sqlalchemy import BaseQuery, SQLAlchemy
from sqlalchemy.orm import object_session
from sqlalchemy.pool import NullPool
#from sqlalchemy_searchable import make_searchable, vectorizer, SearchQueryMixin


db = SQLAlchemy()
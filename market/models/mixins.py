from .base import db


class TimestampMixin(object):
    updated_at = db.Column(db.DateTime(
        True), default=db.func.now(), nullable=False)
    created_at = db.Column(db.DateTime(
        True), default=db.func.now(), nullable=False)


class CommentMixin(object):
    comment = db.Column(db.Text, nullable=True)


class DeleteMixin(object):
    delete = db.Column(db.Boolean, default=False, nullable=False)

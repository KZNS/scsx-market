import datetime
import logging
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import column_property, validates

# from .mixins import TimestampMixin
from .base import db
# from .vote import VoteInfo,VoteVotes,VoteCandidates
# from .issues import IssuesIssues,IssueTypes
# from .postcard import db,PostcardCards,PostcardRoles,PostcardTemplates,PostcardUsers
logger = logging.getLogger(__name__)


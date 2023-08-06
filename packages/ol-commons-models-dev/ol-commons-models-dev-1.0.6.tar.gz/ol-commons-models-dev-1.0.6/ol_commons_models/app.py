import os
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Sequence
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
base = declarative_base()

db_string_connection = str(os.environ.get('STRING_CONNECTION'))
SQLALCHEMY_DATABASE_URI = db_string_connection.format(
    username=os.environ.get('DBUSERNAME'),
    password=os.environ.get('DBPASSWORD'),
    hostname=os.environ.get('DBHOSTNAME'),
    port=os.environ.get('DBPORT'),
    database=os.environ.get('DBNAME')
)

SQLALCHEMY_ECHO = False
SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_POOL_SIZE = int(os.environ.get('DBPOOL_SIZE'))
SQLALCHEMY_POOL_TIMEOUT = int(os.environ.get('DBPOOL_TIMEOUT'))
SQLALCHEMY_RECORD_QUERIES = True


class Attribute(db.Model):
    __tablename__ = 'attribute'
    sq_attribute_id = Sequence('sq_attribute_id', metadata=base.metadata)

    num_attribute_id = db.Column(db.Numeric, sq_attribute_id, server_default=sq_attribute_id.next_value(),
                                 primary_key=True)
    str_attribute_name = db.Column(db.Text)
    str_modifiedby = db.Column(db.Text)
    dte_modifieddate = db.Column(db.DateTime)
    str_createdby = db.Column(db.Text)
    dte_createddate = db.Column(db.DateTime)
    str_attribute_desc = db.Column(db.Text)


class AttributeMember(db.Model):
    __tablename__ = 'attribute_member'

    sq_attribute_member_id = Sequence('sq_attribute_member_id', metadata=base.metadata)
    num_attr_member_id = db.Column(db.Numeric, sq_attribute_member_id,
                                   server_default=sq_attribute_member_id.next_value(), primary_key=True)

    num_attribute_id = db.Column(db.Numeric)
    str_attr_member_value = db.Column(db.Text)
    str_attr_member_desc = db.Column(db.Text)
    str_modifiedby = db.Column(db.Text)
    dte_modifieddate = db.Column(db.DateTime)
    str_createdby = db.Column(db.Text)
    dte_createddate = db.Column(db.DateTime)
    num_order = db.Column(db.Numeric)
    str_attr_member_desc_2 = db.Column(db.Text)

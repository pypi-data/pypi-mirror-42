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


class PurchaseOrder(db.Model):
    __tablename__ = 'purchase_order'
    sq_pchorder_id = Sequence('sq_pchorder_id', metadata=base.metadata)

    num_pchorder_id = db.Column(db.Numeric,
                                sq_pchorder_id,
                                server_default=sq_pchorder_id.next_value(),
                                primary_key=True)

    str_pchorder_code = db.Column(db.Text)
    num_pchorder_status = db.Column(db.Numeric)
    str_modifiedby = db.Column(db.Text)
    str_createdby = db.Column(db.Text)
    dte_createddate = db.Column(db.DateTime)
    dte_modifieddate = db.Column(db.DateTime)

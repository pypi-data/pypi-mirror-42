__all__ = ['app', 'artemis', 'billing', 'logistics', 'rrhh', 'security']

import os
import string

from sqlalchemy import type_coerce, func, String
from sqlalchemy.dialects.postgresql import BYTEA

db_string_connection = os.environ.get('STRING_CONNECTION')
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


# General methods
class PGPString(BYTEA):
    def __init__(self, passphrase, length=None):
        super(PGPString, self).__init__(length)
        self.passphrase = passphrase

    def bind_expression(self, bindvalue) -> bytearray:
        bindvalue = type_coerce(bindvalue, String)
        return func.pgp_sym_encrypt(bindvalue, self.passphrase)

    def column_expression(self, col) -> string:
        return func.pgp_sym_decrypt(col, self.passphrase)

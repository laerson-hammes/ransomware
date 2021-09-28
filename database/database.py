import pymysql.cursors
from typing import Dict, Any, List
from .settings import CONN_ATTRS, START_VALUES


class Database(object):
   def __init__(self, /) -> None:
      pass
   
   
   def database_connection(self, **kwargs: Dict[str, Any]):
      """
      this function make the connection to the database
      :**kwargs param: Dict with the connection attributes / parameters
      return database connection object
      """
      try:
         connection: pymysql.connections.Connection = pymysql.connect(
            host = kwargs['host'],
            user = kwargs['user'],
            password = kwargs['password'],
            database = kwargs['database'],
            autocommit = kwargs['autocommit'],
            cursorclass = kwargs['cursorclass']
         )
         return connection
      except Exception as e:
         print(e)
            
            
   def select(self, query: str, /) -> List[Dict[str, Any]]:
      """
      this function is used to select all values from the specified database table
      :query param: query string to select values from the database
      return all results from the select statement
      """
      connection = self.database_connection(**CONN_ATTRS)
      with connection:
         with connection.cursor() as cursor:
            cursor.execute(query)
            return cursor.fetchall()
   
   
   def get_password(self, /) -> bytes:
      """
      this function get the password from the database settings table
      return encrypted password
      """
      return self.select("SELECT passwd FROM settings;")[0]['passwd'].encode()
   
   
   def get_attempts(self, /) -> int:
      """
      this function get the attempts number from the database settings table
      returns the number of attempts
      """
      return self.select("SELECT attempts FROM settings;")[0]['attempts']


   def get_bitcoins(self, /) -> int:
      """
      this function get the bitcoins number from the database settings table
      returns the amount of bitcoins
      """
      return self.select("SELECT bitcoins FROM settings;")[0]['bitcoins']
   
   
   def get_is_encrypted(self, /) -> bool:
      """
      this function get / check if the files were encrypted
      returns a boolean indicating if the files were encrypted
      """
      return self.select("SELECT is_encrypted FROM settings;")[0]['is_encrypted']

   
   def update(self, query: str, /) -> bool:
      """
      this function is used to update a specific value from the database settings table
      :query param: query string to update values from the specified table attribute
      return True if been changed, False otherwise
      """
      connection = self.database_connection(**CONN_ATTRS)
      with connection:
         with connection.cursor() as cursor:
            try:
               cursor.execute(query)
               return True
            except:
               return False
            
   
   def set_is_encrypted(self, is_encrypted: bool, /) -> bool:
      """
      this function sets the is_encrypted attribute
      :is_encrypted param: receive a boolean value for change the is_encrypted attribute
      return True if the is_encrypted attribute is been set, False otherwise
      """
      return self.update(f"UPDATE settings SET is_encrypted = {str(is_encrypted)}")
   
   
   def set_attempts(self, attempts: int, /) -> bool:
      """
      this function sets the attempts attribute
      :attempts param: receive an int value for change the attempts attribute
      return True if the attempts attribute is been set, False otherwise
      """
      return self.update(f"UPDATE settings SET attempts = {str(attempts)}")

   
   def set_bitcoins(self, bitcoins: int, /) -> bool:
      """
      this function sets the bitcoins attribute
      :bitcoins param: receive an int value for change the bitcoins attribute
      return True if the bitcoins attribute is been set, False otherwise
      """
      return self.update(f"UPDATE settings SET bitcoins = {str(bitcoins)}")

   
   def reset_settings_table_values(self, /) -> bool:
      """
      this function will reset the settings table
      returns a boolean indicating if the table has been resetted
      """
      is_encrypted: bool = self.set_is_encrypted(bool(START_VALUES['is_encrypted']))
      attempts: bool = self.set_attempts(START_VALUES['attempts'])
      bitcoins: bool = self.set_bitcoins(START_VALUES['bitcoins'])
      return is_encrypted and attempts and bitcoins
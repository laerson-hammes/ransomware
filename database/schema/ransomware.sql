CREATE DATABASE ransomware;

USE ransomware;

CREATE TABLE IF NOT EXISTS settings (
   settings_id INTEGER PRIMARY KEY AUTO_INCREMENT,
   passwd CHAR(16) NOT NULL,
   is_encrypted BOOLEAN NOT NULL,
   attempts INTEGER NOT NULL,
   bitcoins INTEGER NOT NULL
);

DROP TABLE IF EXISTS settings;

INSERT INTO settings (passwd, is_encrypted, attempts, bitcoins) VALUES ("1ab2c3e4f5g6h7i8", 0, 0, 1);

DELETE FROM settings WHERE settings_id = 1;

SELECT * FROM settings;

-- SELECT BOOLEAN(passwd) FROM settings WHERE passwd = '1ab2c3e4f5g6h7i8';

-- UPDATE settings SET is_encrypted = 0;

-- attempts = SELECT attempts FROM settings;
-- UPDATE settings SET attempts = attempts + 1;

-- bitcoins = SELECT bitcoins FROM settings;
-- UPDATE settings SET bitcoins = bitcoins + 1;
import sqlite3

conn = sqlite3.connect('streaming.db')
cursor = conn.cursor()

# criando a tabela (schema)
cursor.execute("""
CREATE TABLE video (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        resolution VARCHAR(4) CHECK (resolution IN ('240p','480p','720p')) NOT NULL,
        path VARCHAR(100) NOT NULL 
);
""")

print('Tabela criada com sucesso.')
# desconectando...


cursor.execute("""
INSERT INTO video (name, resolution, path)
VALUES ('pacman.mp4','240p','../videos/240p/pacman.mp4')
""")

cursor.execute("""
INSERT INTO video (name, resolution, path)
VALUES ('pacman.mp4','480p','../videos/480p/pacman.mp4')
""")

cursor.execute("""
INSERT INTO video (name, resolution, path)
VALUES ('pacman.mp4','720p','../videos/720p/pacman.mp4')
""")

cursor.execute("""
INSERT INTO video (name, resolution, path)
VALUES ('animacao.mp4','240p','../videos/240p/animacao.mp4')
""")

cursor.execute("""
INSERT INTO video (name, resolution, path)
VALUES ('animacao.mp4','480p','../videos/480p/animacao.mp4')
""")

cursor.execute("""
INSERT INTO video (name, resolution, path)
VALUES ('animacao.mp4','720p','../videos/720p/animacao.mp4')
""")

conn.commit()

print('Dados inseridos com sucesso.')

conn.close()

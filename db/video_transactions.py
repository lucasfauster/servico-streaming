import sqlite3


def create_video_transaction(name, resolution, path):
    conn = sqlite3.connect('../db/streaming.db')
    cursor = conn.cursor()
    cursor.execute("""INSERT INTO video (name, resolution, path) VALUES (?,?,?)""", (name, resolution, path))
    conn.commit()
    print('Vídeo inserido com sucesso.')
    conn.close()


def read_videos_transaction():
    conn = sqlite3.connect('../db/streaming.db')
    cursor = conn.cursor()
    cursor.execute("""SELECT * FROM video;""")
    videos = cursor.fetchall()
    conn.close()
    return videos


def update_videos_transaction(id_video, name, resolution, path):
    conn = sqlite3.connect('../db/streaming.db')
    cursor = conn.cursor()
    cursor.execute(""" UPDATE video SET name = ?, resolution=?, path = ? WHERE id = ?""",
                   (name, resolution, path, id_video))
    conn.commit()
    print('Vídeo atualizado com sucesso.')
    conn.close()


def delete_video_transaction(id_video):
    conn = sqlite3.connect('../db/streaming.db')
    cursor = conn.cursor()
    cursor.execute("""DELETE FROM video WHERE id = ?""", (id_video,))
    conn.commit()
    print('Vídeo removido com sucesso.')
    conn.close()



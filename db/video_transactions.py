import sqlite3


def create_video_transaction(name, resolution, path):
    conn = sqlite3.connect('../db/streaming.db')
    cursor = conn.cursor()
    cursor.execute("""INSERT INTO video (name, resolution, path) VALUES (?,?,?)""", (name, resolution, path))
    conn.commit()
    print('Vídeo inserido com sucesso.')
    conn.close()


def read_videos_transaction_to_client():
    conn = sqlite3.connect('../db/streaming.db')
    cursor = conn.cursor()
    cursor.execute("""SELECT name, resolution FROM video;""")
    videos_tuplas = cursor.fetchall()
    videos_array = []
    for video in videos_tuplas:
        videos_array.append([video[0], video[1]])
    conn.close()
    return videos_array


def read_videos_transaction_to_server():
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

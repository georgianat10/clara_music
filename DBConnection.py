import sqlite3
import sqlite3

def connection(db_name):
    sqlite_connection = None
    try:
        sqlite_connection = sqlite3.connect(db_name)

    except sqlite3.Error as error:
        print("Error while connecting to sqlite", error)

    return sqlite_connection


def close_db(sqlite_connection):
    if sqlite_connection:
        sqlite_connection.close()
        print("The SQLite connection is closed")


def create_songs_table(conn):
    sql = "CREATE TABLE songs (url varchar(255), sentiment FLOAT(2), likes INTEGER)"
    conn.execute(sql)


def delete_songs_table(conn):
    sql = "DELETE FROM songs"


def create_song(conn, song):
    sql = "INSERT INTO songs(url, sentiment, likes) VALUES (?, ?, ?)"
    cursor = conn.cursor()
    cursor.execute(sql, song)
    conn.commit()
    cursor.close()
    return cursor.lastrowid


def select_songs(conn, sentiment):
    sql = "SELECT * FROM songs WHERE sentiment = " + str(sentiment) + " AND likes = (SELECT MAX(likes) FROM songs WHERE sentiment = " + str(sentiment) + ")"
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()
    rows = cursor.fetchall()
    cursor.close()
    return rows

def change_likes(conn, song_url):
    sql = "UPDATE songs SET likes = likes + 1 WHERE url = '" + song_url +"'"
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()
    cursor.close()

def main():
    database_name = "lft.db"
    db = connection(database_name)

    songs = select_songs(db, 0.1)
    print(*songs)
    # song_index = random.randrange(songs.__len__())
    # player = play_song('https://www.youtube.com/watch?v=z86K7yk6MQg&list=PLHYZfqKGt0t0EM2hjCoyugaIJWwVeHLnW&index=20')
    # input1 = ""
    # player.play()
    # while input1 != 'stop':
    #    input1 = input()
    #    player.stop()
    # input1 = input()
    close_db(db)


if __name__ == '__main__':
    main()

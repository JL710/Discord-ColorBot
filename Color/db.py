from dataclasses import dataclass
import sqlite3


@dataclass(frozen=True)
class Color:
    id: int
    name: str
    guild_id: int
    role_id: int
    r: int
    g: int
    b: int


DB_PATH = "colors.db"


def get_cursor() -> tuple[sqlite3.Connection, sqlite3.Cursor]:
    connection: sqlite3.Connection = sqlite3.connect(DB_PATH)
    cursor: sqlite3.Cursor = connection.cursor()
    return cursor, connection


def db_check():
    """
    Checks if the database exists and will create one if not.
    """
    cursor, connection = get_cursor()
    sql_script = """
    CREATE TABLE IF NOT EXISTS colors (
        id INTEGER NOT NULL UNIQUE PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        guild_id INTEGER NOT NULL,
        role_id INTEGER NOT NULL,
        r INTEGER NOT NULL,
        g INTEGER NOT NULL,
        b INTEGER NOT NULL
    )
    """
    cursor.executescript(sql_script)

    cursor.close()
    connection.commit()
    connection.close()


def get_colors(guild_id: int) -> tuple[Color]:
    cursor, connection = get_cursor()

    cursor.execute("SELECT id, name, guild_id, role_id, r, g, b FROM colors WHERE guild_id=?", (guild_id,))

    result = cursor.fetchall()

    cursor.close()
    connection.close()

    return tuple(
        Color(
            id=row[0],
            name=row[1],
            guild_id=row[2],
            role_id=row[3],
            r=row[4],
            g=row[5],
            b=row[6]
        ) for row in result
    )


def get_color(guild_id: int, name: str) -> None | Color:
    cursor, connection = get_cursor()

    result = cursor.execute("SELECT * FROM colors WHERE guild_id=? AND name=?", (guild_id, name)).fetchone()

    cursor.close()
    connection.close()

    if not result:
        return
    return Color(
        id=result[0],
        name=result[1],
        guild_id=result[2],
        role_id=result[3],
        r=result[4],
        g=result[5],
        b=result[6]
    )


def add_color(name: str, guild_id: int, role_id: int, r: int, g: int, b: int):
    cursor, connection = get_cursor()

    cursor.execute(
        "INSERT INTO colors (name, guild_id, role_id, r, g, b) VALUES (?, ?, ?, ?, ?, ?)",
        (name, guild_id, role_id, r, g, b)
        )

    cursor.close()
    connection.commit()
    connection.close()


def delete_color(name: str, guild_id: int):
    cursor, connection = get_cursor()

    cursor.execute(
        "DELETE FROM colors WHERE name=? AND guild_id=?",
        (name, guild_id)
        )
    
    cursor.close()
    connection.commit()
    connection.close()
